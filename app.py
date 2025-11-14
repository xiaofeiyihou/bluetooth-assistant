#!/usr/bin/env python3
"""
手机蓝牙APP - 主程序 (使用Kivy语言界面)
实现蓝牙设备扫描、连接和双向通信
"""

import asyncio
import threading
from typing import List, Dict, Callable, Optional
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.logger import Logger
from bluetooth_manager import BluetoothManager

class BluetoothAppUI(BoxLayout):
    """蓝牙APP的主界面类"""
    
    # 绑定属性
    is_connected = BooleanProperty(False)
    is_scanning = BooleanProperty(False)
    
    status_label = ObjectProperty()
    scan_button = ObjectProperty()
    devices_layout = ObjectProperty()
    message_display = ObjectProperty()
    message_input = ObjectProperty()
    send_button = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "蓝牙助手"
        self.bluetooth_manager = BluetoothManager()
        self.devices_list = []
        self.connected_device = None
    
    def on_kv_post(self, base_widget):
        """KV文件加载完成后的回调"""
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI组件引用"""
        # 获取KV文件中的组件
        self.status_label = self.ids.status_label
        self.scan_button = self.ids.scan_button
        self.devices_layout = self.ids.devices_layout
        self.message_display = self.ids.message_display
        self.message_input = self.ids.message_input
        self.send_button = self.ids.send_button
        
        # 初始状态设置
        self.is_connected = False
        self.is_scanning = False
    
    def update_status(self, message):
        """更新状态显示"""
        def update(dt):
            if self.status_label:
                self.status_label.text = message
        Clock.schedule_once(update)
    
    def update_devices_list(self, devices):
        """更新设备列表显示"""
        def update(dt):
            if not self.devices_layout:
                return
                
            self.devices_layout.clear_widgets()
            if not devices:
                no_device_label = Label(
                    text='未找到蓝牙设备',
                    font_size='16sp',
                    size_hint_y=None,
                    height=40,
                    color=(0.5, 0.5, 0.5, 1)
                )
                self.devices_layout.add_widget(no_device_label)
                return
                
            for device in devices:
                device_button = Button(
                    text=f"{device['name']} ({device['address']})",
                    size_hint_y=None,
                    height=50,
                    background_color=(0.2, 0.6, 0.8, 1),
                    on_press=lambda x, d=device: self.connect_device(d)
                )
                self.devices_layout.add_widget(device_button)
                
        Clock.schedule_once(update)
    
    def append_message(self, message, is_sent=False):
        """在消息显示区域添加消息"""
        def update(dt):
            if not self.message_display:
                return
            prefix = "发送: " if is_sent else "接收: "
            color_prefix = "[color=00FF00]" if is_sent else "[color=0066CC]"
            end_color = "[/color]"
            formatted_message = f"{color_prefix}{prefix}{message}{end_color}\n"
            
            self.message_display.text += formatted_message
            # 滚动到底部
            self.message_display.cursor = (0, len(self.message_display.text))
                
        Clock.schedule_once(update)
    
    def set_scanning_state(self, scanning):
        """设置扫描状态"""
        def update(dt):
            self.is_scanning = scanning
            if self.scan_button:
                self.scan_button.text = '正在扫描...' if scanning else '扫描蓝牙设备'
                self.scan_button.disabled = scanning
        Clock.schedule_once(update)
    
    def set_connected_state(self, connected):
        """设置连接状态"""
        def update(dt):
            self.is_connected = connected
            if self.send_button:
                self.send_button.disabled = not connected
                self.send_button.background_color = (0.2, 0.6, 0.8, 1) if connected else (0.7, 0.7, 0.7, 1)
        Clock.schedule_once(update)
    
    def scan_devices(self):
        """扫描蓝牙设备"""
        if self.is_scanning:
            return
            
        self.set_scanning_state(True)
        self.update_status('正在扫描蓝牙设备...')
        self.devices_list = []
        self.bluetooth_manager.scan_devices(self.on_scan_complete)
    
    def on_scan_complete(self, devices):
        """扫描完成回调"""
        self.devices_list = devices
        self.set_scanning_state(False)
        self.update_status(f'扫描完成，找到 {len(devices)} 个设备')
        self.update_devices_list(devices)
    
    def connect_device(self, device):
        """连接蓝牙设备"""
        if self.is_scanning:
            return
            
        self.update_status(f'正在连接 {device["name"]}...')
        self.bluetooth_manager.connect_device(
            device, 
            self.on_connect_success,
            self.on_connect_failed,
            self.on_data_received
        )
    
    def on_connect_success(self, device):
        """连接成功回调"""
        self.connected_device = device
        self.set_connected_state(True)
        self.update_status(f'已连接设备: {device["name"]}')
        self.append_message(f'已成功连接到 {device["name"]}')
    
    def on_connect_failed(self, error):
        """连接失败回调"""
        self.update_status(f'连接失败: {error}')
        self.append_message(f'连接失败: {error}')
        self.set_connected_state(False)
    
    def on_data_received(self, data):
        """数据接收回调"""
        self.append_message(data, is_sent=False)
    
    def send_message(self):
        """发送消息"""
        message = self.message_input.text.strip()
        if message and self.is_connected:
            # 发送消息
            success = self.bluetooth_manager.send_message(message)
            if success:
                self.append_message(message, is_sent=True)
                self.message_input.text = ''
            else:
                self.update_status('发送失败')
        elif not self.is_connected:
            self.update_status('请先连接设备')
        elif not message:
            self.update_status('请输入要发送的消息')
    
    def disconnect_device(self):
        """断开当前设备连接"""
        if self.connected_device:
            self.bluetooth_manager.disconnect_device(self.connected_device['address'])
            self.connected_device = None
            self.set_connected_state(False)
            self.update_status('设备已断开连接')
            self.append_message('设备已断开连接')

class BluetoothApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = '手机蓝牙助手'
        self.use_kivy_settings = False
        
    def build(self):
        """构建应用程序"""
        Logger.info("蓝牙APP启动")
        return BluetoothAppUI()
    
    def on_start(self):
        """应用启动时的初始化"""
        Logger.info("蓝牙APP开始运行")
    
    def on_stop(self):
        """应用关闭时清理资源"""
        Logger.info("蓝牙APP正在关闭")
        # 这里会调用BluetoothAppUI实例的disconnect_device
        # 但我们需要先获取根组件
        if hasattr(self, 'root') and self.root:
            if hasattr(self.root, 'bluetooth_manager') and self.root.bluetooth_manager:
                self.root.bluetooth_manager.disconnect_all()

if __name__ == '__main__':
    BluetoothApp().run()