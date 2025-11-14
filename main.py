#!/usr/bin/env python3
"""
手机蓝牙APP - 主程序
使用Kivy创建跨平台移动界面
"""

import asyncio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from bluetooth_manager import BluetoothManager
from kivy.logger import Logger

class BluetoothApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "蓝牙助手"
        self.bluetooth_manager = BluetoothManager()
        self.devices_list = []
        self.connected_device = None
        
    def build(self):
        """构建用户界面"""
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title_label = Label(
            text='手机蓝牙助手',
            font_size='24sp',
            size_hint=(1, 0.1),
            color=(0.2, 0.6, 0.8, 1)
        )
        main_layout.add_widget(title_label)
        
        # 状态显示
        self.status_label = Label(
            text='点击扫描开始查找蓝牙设备',
            font_size='14sp',
            size_hint=(1, 0.1),
            text_size=(None, None),
            halign='center'
        )
        main_layout.add_widget(self.status_label)
        
        # 扫描按钮
        scan_button = Button(
            text='扫描蓝牙设备',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1),
            on_press=self.scan_devices
        )
        main_layout.add_widget(scan_button)
        
        # 设备列表区域
        scroll_view = ScrollView(size_hint=(1, 0.4))
        self.devices_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=10,
            spacing=5
        )
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        scroll_view.add_widget(self.devices_layout)
        main_layout.add_widget(scroll_view)
        
        # 通信区域
        comm_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=5)
        
        # 消息显示
        self.message_display = TextInput(
            text='',
            readonly=True,
            size_hint_y=0.7,
            background_color=(0.9, 0.9, 0.9, 1)
        )
        comm_layout.add_widget(self.message_display)
        
        # 发送消息布局
        send_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        
        self.message_input = TextInput(
            hint_text='输入要发送的消息',
            size_hint_x=0.7,
            multiline=False
        )
        send_layout.add_widget(self.message_input)
        
        self.send_button = Button(
            text='发送',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1),
            on_press=self.send_message,
            disabled=True
        )
        send_layout.add_widget(self.send_button)
        comm_layout.add_widget(send_layout)
        
        main_layout.add_widget(comm_layout)
        
        return main_layout
    
    def update_status(self, message):
        """更新状态显示"""
        def update(dt):
            self.status_label.text = message
        Clock.schedule_once(update)
    
    def update_devices_list(self, devices):
        """更新设备列表显示"""
        def update(dt):
            self.devices_layout.clear_widgets()
            if not devices:
                no_device_label = Label(
                    text='未找到蓝牙设备',
                    font_size='16sp',
                    size_hint_y=None,
                    height=40
                )
                self.devices_layout.add_widget(no_device_label)
                return
                
            for device in devices:
                device_button = Button(
                    text=f"{device['name']} ({device['address']})",
                    size_hint_y=None,
                    height=50,
                    background_color=(0.7, 0.7, 0.7, 1),
                    on_press=lambda x, d=device: self.connect_device(d)
                )
                self.devices_layout.add_widget(device_button)
                
        Clock.schedule_once(update)
    
    def append_message(self, message, is_sent=False):
        """在消息显示区域添加消息"""
        def update(dt):
            prefix = "发送: " if is_sent else "接收: "
            self.message_display.text += f"{prefix}{message}\n"
            # 滚动到底部
            self.message_display.cursor = (0, len(self.message_display.text))
                
        Clock.schedule_once(update)
    
    def scan_devices(self, instance):
        """扫描蓝牙设备"""
        self.update_status('正在扫描蓝牙设备...')
        self.bluetooth_manager.scan_devices(self.on_scan_complete)
    
    def on_scan_complete(self, devices):
        """扫描完成回调"""
        self.update_status(f'扫描完成，找到 {len(devices)} 个设备')
        self.update_devices_list(devices)
    
    def connect_device(self, device):
        """连接蓝牙设备"""
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
        self.update_status(f'已连接设备: {device["name"]}')
        self.send_button.disabled = False
        self.append_message(f'已成功连接到 {device["name"]}')
    
    def on_connect_failed(self, error):
        """连接失败回调"""
        self.update_status(f'连接失败: {error}')
        self.append_message(f'连接失败: {error}')
    
    def on_data_received(self, data):
        """数据接收回调"""
        self.append_message(data, is_sent=False)
    
    def send_message(self, instance):
        """发送消息"""
        message = self.message_input.text.strip()
        if message and self.connected_device:
            # 发送消息
            success = self.bluetooth_manager.send_message(message)
            if success:
                self.append_message(message, is_sent=True)
                self.message_input.text = ''
            else:
                self.update_status('发送失败')
        elif not self.connected_device:
            self.update_status('请先连接设备')
    
    def on_start(self):
        """应用启动时的初始化"""
        self.update_status('应用启动，请开始扫描蓝牙设备')
    
    def on_stop(self):
        """应用关闭时清理资源"""
        if self.bluetooth_manager:
            self.bluetooth_manager.disconnect_all()

if __name__ == '__main__':
    BluetoothApp().run()