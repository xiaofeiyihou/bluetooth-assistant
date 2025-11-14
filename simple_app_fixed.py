#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机蓝牙APP - 简化版主程序
使用基础的Kivy界面，不依赖复杂的蓝牙库
支持UTF-8编码显示
"""

import threading
import time
import sys
import os
import locale
from typing import List, Dict, Callable

# 设置编码和本地化
if sys.version_info[0] >= 3:
    import codecs
    # 设置标准输出编码
    if hasattr(sys.stdout, 'detach'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 强制使用UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'
if hasattr(locale, 'LC_ALL'):
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except:
            pass

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

# Kivy配置 - 确保UTF-8支持
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', True)

class SimpleBluetoothManager:
    """简化的蓝牙管理器 - 模拟蓝牙功能"""
    
    def __init__(self):
        self.connected = False
        self.connected_device = None
        # 使用ASCII字符避免编码问题
        self.mock_devices = [
            {'name': 'Arduino蓝牙模块', 'address': '00:11:22:33:44:55'},
            {'name': 'HC-05蓝牙模块', 'address': '00:11:22:33:44:66'},
            {'name': 'ESP32蓝牙设备', 'address': '00:11:22:33:44:77'},
            {'name': '智能手表', 'address': '00:11:22:33:44:88'},
            {'name': '蓝牙耳机', 'address': '00:11:22:33:44:99'}
        ]
    
    def scan_devices(self, callback: Callable[[List[Dict]], None]):
        """模拟扫描蓝牙设备"""
        def scan():
            time.sleep(2)  # 模拟扫描时间
            callback(self.mock_devices)
        
        scan_thread = threading.Thread(target=scan, daemon=True)
        scan_thread.start()
    
    def connect_device(self, device_info: Dict, 
                      success_callback: Callable,
                      failed_callback: Callable,
                      data_callback: Callable):
        """模拟连接设备"""
        def connect():
            time.sleep(1)  # 模拟连接时间
            if device_info['address'] in ['00:11:22:33:44:55', '00:11:22:33:44:66']:
                self.connected = True
                self.connected_device = device_info
                success_callback(device_info)
                # 模拟接收数据
                threading.Timer(3, lambda: data_callback("Hello from " + device_info['name'])).start()
            else:
                failed_callback("设备连接失败，请检查设备是否可用")
        
        connect_thread = threading.Thread(target=connect, daemon=True)
        connect_thread.start()
    
    def send_message(self, message: str) -> bool:
        """模拟发送消息"""
        if self.connected:
            print("发送消息到 {}: {}".format(self.connected_device['name'], message))
            return True
        return False
    
    def disconnect_device(self, address: str):
        """模拟断开设备"""
        self.connected = False
        self.connected_device = None
    
    def disconnect_all(self):
        """断开所有设备"""
        self.connected = False
        self.connected_device = None

class SimpleBluetoothApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "手机蓝牙助手 (简化版)"
        Window.size = (360, 640)  # 手机屏幕尺寸
    
    def build(self):
        """构建用户界面"""
        # 主布局
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=15
        )
        
        # 设置窗口背景色
        Window.clearcolor = (0.95, 0.97, 1.0, 1.0)
        
        # 标题 - 使用简单文本避免emoji编码问题
        title_label = Label(
            text='手机蓝牙助手',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.6, 0.8, 1),
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # 状态显示
        self.status_label = Label(
            text='点击扫描开始查找蓝牙设备',
            font_size='14sp',
            size_hint_y=None,
            height=40,
            color=(0.4, 0.4, 0.4, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # 扫描按钮
        self.scan_button = Button(
            text='扫描蓝牙设备',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp',
            on_press=self.scan_devices
        )
        main_layout.add_widget(self.scan_button)
        
        # 设备列表区域
        device_list_frame = BoxLayout(
            orientation='vertical',
            size_hint_y=0.35,
            spacing=5
        )
        
        device_list_label = Label(
            text='发现的设备',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        device_list_frame.add_widget(device_list_label)
        
        scroll_view = ScrollView(size_hint_y=1)
        self.devices_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=5,
            spacing=5
        )
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        scroll_view.add_widget(self.devices_layout)
        device_list_frame.add_widget(scroll_view)
        main_layout.add_widget(device_list_frame)
        
        # 通信区域
        comm_frame = BoxLayout(
            orientation='vertical', 
            size_hint_y=0.35,
            spacing=10
        )
        
        comm_label = Label(
            text='通信记录',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        comm_frame.add_widget(comm_label)
        
        # 消息显示
        self.message_display = TextInput(
            text='欢迎使用手机蓝牙助手！\n扫描设备开始连接...\n',
            readonly=True,
            size_hint_y=0.7,
            background_color=(1, 1, 1, 1),
            font_size='12sp'
        )
        comm_frame.add_widget(self.message_display)
        
        # 发送消息布局
        send_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=10)
        
        self.message_input = TextInput(
            hint_text='输入要发送的消息...',
            multiline=False,
            size_hint_x=0.7,
            font_size='14sp',
            background_color=(1, 1, 1, 1)
        )
        send_layout.add_widget(self.message_input)
        
        self.send_button = Button(
            text='发送',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='14sp',
            on_press=self.send_message,
            disabled=True
        )
        send_layout.add_widget(self.send_button)
        comm_frame.add_widget(send_layout)
        
        main_layout.add_widget(comm_frame)
        
        # 连接状态
        self.connection_status = Label(
            text='未连接',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(1, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.connection_status)
        
        # 创建蓝牙管理器
        self.bluetooth_manager = SimpleBluetoothManager()
        self.connected_device = None
        
        return main_layout
    
    def update_status(self, message):
        """更新状态显示"""
        def update(dt):
            self.status_label.text = message
        Clock.schedule_once(update)
    
    def update_connection_status(self, connected, device_name=None):
        """更新连接状态"""
        def update(dt):
            if connected:
                self.connection_status.text = '已连接: {}'.format(device_name)
                self.connection_status.color = (0.3, 0.8, 0.3, 1)
                self.send_button.disabled = False
                self.send_button.background_color = (0.2, 0.6, 0.8, 1)
            else:
                self.connection_status.text = '未连接'
                self.connection_status.color = (1, 0.3, 0.3, 1)
                self.send_button.disabled = True
                self.send_button.background_color = (0.7, 0.7, 0.7, 1)
        Clock.schedule_once(update)
    
    def append_message(self, message, is_sent=False):
        """在消息显示区域添加消息"""
        def update(dt):
            timestamp = time.strftime('%H:%M:%S')
            prefix = "[{}] 发送: ".format(timestamp) if is_sent else "[{}] 接收: ".format(timestamp)
            
            self.message_display.text += "{}{}\n".format(prefix, message)
            # 滚动到底部
            self.message_display.cursor = (0, len(self.message_display.text))
                
        Clock.schedule_once(update)
    
    def scan_devices(self, instance):
        """扫描蓝牙设备"""
        self.update_status('正在扫描蓝牙设备...')
        self.scan_button.text = '扫描中...'
        self.scan_button.disabled = True
        
        # 清空设备列表
        self.devices_layout.clear_widgets()
        self.bluetooth_manager.scan_devices(self.on_scan_complete)
    
    def on_scan_complete(self, devices):
        """扫描完成回调"""
        def update(dt):
            self.update_status('扫描完成，找到 {} 个设备'.format(len(devices)))
            self.scan_button.text = '扫描蓝牙设备'
            self.scan_button.disabled = False
            
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
                    text="{} ({})".format(device['name'], device['address']),
                    size_hint_y=None,
                    height=60,
                    background_color=(0.9, 0.9, 0.9, 1),
                    font_size='12sp',
                    on_press=lambda x, d=device: self.connect_device(d)
                )
                self.devices_layout.add_widget(device_button)
        
        Clock.schedule_once(update)
    
    def connect_device(self, device):
        """连接蓝牙设备"""
        self.update_status('正在连接 {}...'.format(device["name"]))
        self.scan_button.text = '连接中...'
        self.scan_button.disabled = True
        
        self.bluetooth_manager.connect_device(
            device, 
            self.on_connect_success,
            self.on_connect_failed,
            self.on_data_received
        )
    
    def on_connect_success(self, device):
        """连接成功回调"""
        def update(dt):
            self.connected_device = device
            self.update_connection_status(True, device['name'])
            self.update_status('已连接设备: {}'.format(device["name"]))
            self.append_message('已成功连接到 {}'.format(device["name"]))
            self.scan_button.text = '扫描蓝牙设备'
            self.scan_button.disabled = False
        
        Clock.schedule_once(update)
    
    def on_connect_failed(self, error):
        """连接失败回调"""
        def update(dt):
            self.update_status('连接失败: {}'.format(error))
            self.append_message('连接失败: {}'.format(error))
            self.scan_button.text = '扫描蓝牙设备'
            self.scan_button.disabled = False
        
        Clock.schedule_once(update)
    
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
        elif not message:
            self.update_status('请输入要发送的消息')

if __name__ == '__main__':
    SimpleBluetoothApp().run()