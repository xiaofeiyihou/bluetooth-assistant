"""
蓝牙管理模块
实现蓝牙设备扫描、连接和数据通信功能
"""

import asyncio
import threading
import time
from typing import List, Dict, Callable, Optional
from bleak import BleakScanner, BleakClient, BleakError
from kivy.logger import Logger

class BluetoothManager:
    def __init__(self):
        self.clients = {}
        self.scanner = None
        self.is_scanning = False
        self.discovered_devices = []
        
    async def scan_devices_async(self, callback: Callable[[List[Dict]], None]):
        """异步扫描蓝牙设备"""
        try:
            self.is_scanning = True
            devices = []
            
            def device_detected(device, advertisement_data):
                """设备检测回调"""
                device_info = {
                    'name': device.name or '未知设备',
                    'address': device.address,
                    'rssi': advertisement_data.rssi,
                    'device': device
                }
                # 避免重复添加同一设备
                if not any(d['address'] == device.address for d in devices):
                    devices.append(device_info)
                    Logger.info(f"发现设备: {device.name} ({device.address})")
            
            # 启动扫描器
            self.scanner = BleakScanner(device_detected)
            await self.scanner.start()
            
            # 扫描10秒
            await asyncio.sleep(10)
            
            # 停止扫描
            await self.scanner.stop()
            self.is_scanning = False
            self.discovered_devices = devices
            
            Logger.info(f"扫描完成，发现 {len(devices)} 个设备")
            callback(devices)
            
        except Exception as e:
            Logger.error(f"扫描蓝牙设备时出错: {e}")
            self.is_scanning = False
            callback([])
    
    def scan_devices(self, callback: Callable[[List[Dict]], None]):
        """在单独线程中执行异步扫描"""
        def run_scan():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.scan_devices_async(callback))
            finally:
                loop.close()
        
        scan_thread = threading.Thread(target=run_scan, daemon=True)
        scan_thread.start()
    
    async def connect_device_async(self, device_info: Dict, 
                                 success_callback: Callable,
                                 failed_callback: Callable,
                                 data_callback: Callable):
        """异步连接设备"""
        try:
            device = device_info['device']
            address = device.address
            name = device_info['name']
            
            Logger.info(f"正在连接设备: {name} ({address})")
            
            # 创建客户端
            client = BleakClient(device)
            
            # 设置数据接收回调
            def data_received(data):
                """数据接收回调"""
                try:
                    message = data.decode('utf-8')
                    Logger.info(f"收到数据: {message}")
                    data_callback(message)
                except Exception as e:
                    Logger.error(f"解析接收数据时出错: {e}")
            
            client.register_for_notify(0xFFE0, data_received)  # 通用串口服务UUID
            
            # 连接设备
            await client.connect()
            Logger.info(f"设备连接成功: {name}")
            
            # 启动通知
            await client.start_notify(0xFFE0, data_received)
            
            # 保存客户端
            self.clients[address] = {
                'client': client,
                'device_info': device_info,
                'name': name
            }
            
            success_callback(device_info)
            
        except BleakError as e:
            Logger.error(f"连接设备失败: {e}")
            failed_callback(str(e))
        except Exception as e:
            Logger.error(f"连接设备时发生未知错误: {e}")
            failed_callback(f"未知错误: {e}")
    
    def connect_device(self, device_info: Dict,
                      success_callback: Callable,
                      failed_callback: Callable,
                      data_callback: Callable):
        """在单独线程中执行异步连接"""
        def run_connect():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    self.connect_device_async(device_info, success_callback, failed_callback, data_callback)
                )
            finally:
                loop.close()
        
        connect_thread = threading.Thread(target=run_connect, daemon=True)
        connect_thread.start()
    
    def send_message(self, message: str, address: Optional[str] = None) -> bool:
        """发送消息到指定的蓝牙设备"""
        try:
            if not address and len(self.clients) == 1:
                # 如果只有一个设备，发送给它
                address = list(self.clients.keys())[0]
            elif not address and len(self.clients) > 1:
                Logger.error("有多个连接设备，请指定目标地址")
                return False
            
            if address not in self.clients:
                Logger.error(f"未找到设备地址: {address}")
                return False
            
            async def send_async():
                try:
                    client = self.clients[address]['client']
                    # 发送消息（使用通用串口UUID）
                    await client.write_gatt_char(0xFFE1, message.encode('utf-8'))
                    Logger.info(f"消息发送成功: {message}")
                    return True
                except Exception as e:
                    Logger.error(f"发送消息时出错: {e}")
                    return False
            
            # 在新线程中发送
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(send_async())
            finally:
                loop.close()
                
        except Exception as e:
            Logger.error(f"发送消息时发生错误: {e}")
            return False
    
    def disconnect_device(self, address: str):
        """断开指定设备连接"""
        if address in self.clients:
            async def disconnect_async():
                try:
                    client = self.clients[address]['client']
                    await client.disconnect()
                    Logger.info(f"设备已断开连接: {address}")
                except Exception as e:
                    Logger.error(f"断开设备连接时出错: {e}")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(disconnect_async())
            finally:
                loop.close()
            
            del self.clients[address]
    
    def disconnect_all(self):
        """断开所有设备连接"""
        addresses = list(self.clients.keys())
        for address in addresses:
            self.disconnect_device(address)
    
    def get_connected_devices(self) -> List[Dict]:
        """获取已连接的设备列表"""
        return [info['device_info'] for info in self.clients.values()]
    
    def is_device_connected(self, address: str) -> bool:
        """检查设备是否已连接"""
        return address in self.clients
    
    def get_device_info(self, address: str) -> Optional[Dict]:
        """获取设备信息"""
        if address in self.clients:
            return self.clients[address]['device_info']
        return None