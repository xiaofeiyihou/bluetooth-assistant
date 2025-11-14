#!/usr/bin/env python3
"""
蓝牙APP - 完整演示版本
展示所有蓝牙功能，无需GUI界面
"""

import time
import threading
from typing import List, Dict, Optional

class BluetoothDemo:
    """蓝牙功能完整演示"""
    
    def __init__(self):
        self.devices = [
            {'name': 'Arduino蓝牙模块', 'address': '00:11:22:33:44:55', 'connected': False},
            {'name': 'HC-05蓝牙模块', 'address': '00:11:22:33:44:66', 'connected': False},
            {'name': 'ESP32蓝牙设备', 'address': '00:11:22:33:44:77', 'connected': False},
            {'name': '智能手表', 'address': '00:11:22:33:44:88', 'connected': False},
            {'name': '蓝牙耳机', 'address': '00:11:22:33:44:99', 'connected': False}
        ]
        self.logs = []
        self.connected_devices = []
        
    def add_log(self, message: str):
        """添加日志"""
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        
    def scan_devices(self) -> List[Dict]:
        """扫描设备"""
        self.add_log("🔍 正在扫描蓝牙设备...")
        time.sleep(2)  # 模拟扫描时间
        self.add_log(f"✅ 扫描完成，发现 {len(self.devices)} 个设备")
        return self.devices
        
    def connect_device(self, device_address: str) -> bool:
        """连接设备"""
        device = next((d for d in self.devices if d['address'] == device_address), None)
        if not device:
            self.add_log(f"❌ 设备 {device_address} 不存在")
            return False
            
        self.add_log(f"🔗 正在连接 {device['name']} ({device_address})...")
        time.sleep(1)
        
        # 模拟连接结果
        if device_address in ['00:11:22:33:44:55', '00:11:22:33:44:66']:
            device['connected'] = True
            self.connected_devices.append(device)
            self.add_log(f"✅ 成功连接到 {device['name']}")
            
            # 模拟接收消息
            threading.Timer(3, lambda: self.add_log(f"📥 {device['name']}: 'Hello from {device['name']}!'")).start()
            return True
        else:
            self.add_log(f"❌ 连接到 {device['name']} 失败")
            return False
            
    def send_message(self, message: str, device_address: str = None) -> bool:
        """发送消息"""
        if not self.connected_devices:
            self.add_log("❌ 没有连接的设备")
            return False
            
        target_device = None
        if device_address:
            target_device = next((d for d in self.connected_devices if d['address'] == device_address), None)
        elif len(self.connected_devices) == 1:
            target_device = self.connected_devices[0]
            
        if not target_device:
            self.add_log("❌ 请选择要发送的目标设备")
            return False
            
        self.add_log(f"📤 发送到 {target_device['name']}: '{message}'")
        time.sleep(0.5)
        self.add_log("✅ 消息发送成功")
        return True
        
    def get_status(self) -> str:
        """获取状态信息"""
        connected_count = len(self.connected_devices)
        total_count = len(self.devices)
        
        status = f"📊 蓝牙状态: {connected_count}/{total_count} 设备已连接\n"
        status += f"总设备: {total_count}个, 已连接: {connected_count}个\n\n"
        
        if self.connected_devices:
            status += "🔗 已连接设备:\n"
            for device in self.connected_devices:
                status += f"  • {device['name']} ({device['address']})\n"
        else:
            status += "🔴 当前没有连接的设备\n"
            
        return status
        
    def show_logs(self):
        """显示操作日志"""
        print("\n" + "="*50)
        print("📋 操作日志")
        print("="*50)
        for log in self.logs:
            print(log)
        print("="*50)

def run_complete_demo():
    """运行完整演示"""
    print("📱" + "="*58 + "📱")
    print("         手机蓝牙助手 - 完整功能演示")
    print("📱" + "="*58 + "📱")
    print()
    
    demo = BluetoothDemo()
    
    # 演示步骤1: 扫描设备
    print("🎯 演示步骤 1: 蓝牙设备扫描")
    print("-" * 30)
    devices = demo.scan_devices()
    print()
    
    print("📋 发现的设备:")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device['name']} ({device['address']})")
    print()
    
    # 演示步骤2: 连接设备
    print("🎯 演示步骤 2: 连接蓝牙设备")
    print("-" * 30)
    if devices:
        target_device = devices[0]  # 连接第一个设备
        demo.connect_device(target_device['address'])
        time.sleep(2)
        print()
    
    # 演示步骤3: 发送消息
    print("🎯 演示步骤 3: 双向通信")
    print("-" * 30)
    demo.send_message("Hello from Python Bluetooth APP!")
    time.sleep(2)
    print()
    
    # 显示状态
    print("🎯 演示步骤 4: 连接状态")
    print("-" * 30)
    print(demo.get_status())
    
    # 显示日志
    demo.show_logs()
    
    print("\n🎉 演示完成!")
    print("\n💡 功能说明:")
    print("• ✅ 蓝牙设备扫描 - 自动发现周围的BLE设备")
    print("• ✅ 设备连接管理 - 一键连接目标设备") 
    print("• ✅ 双向数据通信 - 实时消息收发")
    print("• ✅ 连接状态监控 - 实时显示连接状态")
    print("• ✅ 移动端优化 - 专为手机屏幕设计")
    print("\n🚀 实际运行:")
    print("• 在GUI版本中，可以通过触摸界面操作")
    print("• 支持真实的Arduino HC-05/HC-06、ESP32等设备")
    print("• 可以打包为Android APK在手机上运行")

if __name__ == "__main__":
    run_complete_demo()