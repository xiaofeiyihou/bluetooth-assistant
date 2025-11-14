#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bluetooth APP - English Version
Fixed encoding issues by using only English text
"""

import threading
import time
import sys
import os
from typing import List, Dict, Callable

# Force UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info[0] >= 3:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Kivy configuration
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', True)

class SimpleBluetoothManager:
    """Simplified Bluetooth Manager - Mock Bluetooth functionality"""
    
    def __init__(self):
        self.connected = False
        self.connected_device = None
        self.mock_devices = [
            {'name': 'Arduino BT Module', 'address': '00:11:22:33:44:55'},
            {'name': 'HC-05 Module', 'address': '00:11:22:33:44:66'},
            {'name': 'ESP32 Device', 'address': '00:11:22:33:44:77'},
            {'name': 'Smart Watch', 'address': '00:11:22:33:44:88'},
            {'name': 'Bluetooth Headset', 'address': '00:11:22:33:44:99'}
        ]
    
    def scan_devices(self, callback: Callable[[List[Dict]], None]):
        """Mock scan for Bluetooth devices"""
        def scan():
            time.sleep(2)  # Mock scan time
            callback(self.mock_devices)
        
        scan_thread = threading.Thread(target=scan, daemon=True)
        scan_thread.start()
    
    def connect_device(self, device_info: Dict, 
                      success_callback: Callable,
                      failed_callback: Callable,
                      data_callback: Callable):
        """Mock connect to device"""
        def connect():
            time.sleep(1)  # Mock connect time
            if device_info['address'] in ['00:11:22:33:44:55', '00:11:22:33:44:66']:
                self.connected = True
                self.connected_device = device_info
                success_callback(device_info)
                # Mock receive data
                threading.Timer(3, lambda: data_callback("Hello from " + device_info['name'])).start()
            else:
                failed_callback("Connection failed - check device availability")
        
        connect_thread = threading.Thread(target=connect, daemon=True)
        connect_thread.start()
    
    def send_message(self, message: str) -> bool:
        """Mock send message"""
        if self.connected:
            print("Sending to {}: {}".format(self.connected_device['name'], message))
            return True
        return False
    
    def disconnect_device(self, address: str):
        """Mock disconnect device"""
        self.connected = False
        self.connected_device = None
    
    def disconnect_all(self):
        """Disconnect all devices"""
        self.connected = False
        self.connected_device = None

class SimpleBluetoothApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Bluetooth Assistant"
        Window.size = (360, 640)  # Mobile screen size
    
    def build(self):
        """Build user interface"""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=15
        )
        
        # Set window background color
        Window.clearcolor = (0.95, 0.97, 1.0, 1.0)
        
        # Title
        title_label = Label(
            text='Bluetooth Assistant',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.6, 0.8, 1),
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # Status display
        self.status_label = Label(
            text='Click Scan to find Bluetooth devices',
            font_size='14sp',
            size_hint_y=None,
            height=40,
            color=(0.4, 0.4, 0.4, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Scan button
        self.scan_button = Button(
            text='Scan Bluetooth Devices',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp',
            on_press=self.scan_devices
        )
        main_layout.add_widget(self.scan_button)
        
        # Device list area
        device_list_frame = BoxLayout(
            orientation='vertical',
            size_hint_y=0.35,
            spacing=5
        )
        
        device_list_label = Label(
            text='Discovered Devices',
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
        
        # Communication area
        comm_frame = BoxLayout(
            orientation='vertical', 
            size_hint_y=0.35,
            spacing=10
        )
        
        comm_label = Label(
            text='Communication Log',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        comm_frame.add_widget(comm_label)
        
        # Message display
        self.message_display = TextInput(
            text='Welcome to Bluetooth Assistant!\nScan devices to start connecting...\n',
            readonly=True,
            size_hint_y=0.7,
            background_color=(1, 1, 1, 1),
            font_size='12sp'
        )
        comm_frame.add_widget(self.message_display)
        
        # Send message layout
        send_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=10)
        
        self.message_input = TextInput(
            hint_text='Enter message to send...',
            multiline=False,
            size_hint_x=0.7,
            font_size='14sp',
            background_color=(1, 1, 1, 1)
        )
        send_layout.add_widget(self.message_input)
        
        self.send_button = Button(
            text='Send',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='14sp',
            on_press=self.send_message,
            disabled=True
        )
        send_layout.add_widget(self.send_button)
        comm_frame.add_widget(send_layout)
        
        main_layout.add_widget(comm_frame)
        
        # Connection status
        self.connection_status = Label(
            text='Not Connected',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=(1, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.connection_status)
        
        # Create Bluetooth manager
        self.bluetooth_manager = SimpleBluetoothManager()
        self.connected_device = None
        
        return main_layout
    
    def update_status(self, message):
        """Update status display"""
        def update(dt):
            self.status_label.text = message
        Clock.schedule_once(update)
    
    def update_connection_status(self, connected, device_name=None):
        """Update connection status"""
        def update(dt):
            if connected:
                self.connection_status.text = 'Connected: {}'.format(device_name)
                self.connection_status.color = (0.3, 0.8, 0.3, 1)
                self.send_button.disabled = False
                self.send_button.background_color = (0.2, 0.6, 0.8, 1)
            else:
                self.connection_status.text = 'Not Connected'
                self.connection_status.color = (1, 0.3, 0.3, 1)
                self.send_button.disabled = True
                self.send_button.background_color = (0.7, 0.7, 0.7, 1)
        Clock.schedule_once(update)
    
    def append_message(self, message, is_sent=False):
        """Add message to display area"""
        def update(dt):
            timestamp = time.strftime('%H:%M:%S')
            prefix = "[{}] Sent: ".format(timestamp) if is_sent else "[{}] Received: ".format(timestamp)
            
            self.message_display.text += "{}{}\n".format(prefix, message)
            # Scroll to bottom
            self.message_display.cursor = (0, len(self.message_display.text))
                
        Clock.schedule_once(update)
    
    def scan_devices(self, instance):
        """Scan for Bluetooth devices"""
        self.update_status('Scanning for Bluetooth devices...')
        self.scan_button.text = 'Scanning...'
        self.scan_button.disabled = True
        
        # Clear device list
        self.devices_layout.clear_widgets()
        self.bluetooth_manager.scan_devices(self.on_scan_complete)
    
    def on_scan_complete(self, devices):
        """Scan complete callback"""
        def update(dt):
            self.update_status('Scan complete, found {} devices'.format(len(devices)))
            self.scan_button.text = 'Scan Bluetooth Devices'
            self.scan_button.disabled = False
            
            self.devices_layout.clear_widgets()
            if not devices:
                no_device_label = Label(
                    text='No Bluetooth devices found',
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
        """Connect to Bluetooth device"""
        self.update_status('Connecting to {}...'.format(device["name"]))
        self.scan_button.text = 'Connecting...'
        self.scan_button.disabled = True
        
        self.bluetooth_manager.connect_device(
            device, 
            self.on_connect_success,
            self.on_connect_failed,
            self.on_data_received
        )
    
    def on_connect_success(self, device):
        """Connection success callback"""
        def update(dt):
            self.connected_device = device
            self.update_connection_status(True, device['name'])
            self.update_status('Connected to: {}'.format(device["name"]))
            self.append_message('Successfully connected to {}'.format(device["name"]))
            self.scan_button.text = 'Scan Bluetooth Devices'
            self.scan_button.disabled = False
        
        Clock.schedule_once(update)
    
    def on_connect_failed(self, error):
        """Connection failed callback"""
        def update(dt):
            self.update_status('Connection failed: {}'.format(error))
            self.append_message('Connection failed: {}'.format(error))
            self.scan_button.text = 'Scan Bluetooth Devices'
            self.scan_button.disabled = False
        
        Clock.schedule_once(update)
    
    def on_data_received(self, data):
        """Data received callback"""
        self.append_message(data, is_sent=False)
    
    def send_message(self, instance):
        """Send message"""
        message = self.message_input.text.strip()
        if message and self.connected_device:
            # Send message
            success = self.bluetooth_manager.send_message(message)
            if success:
                self.append_message(message, is_sent=True)
                self.message_input.text = ''
            else:
                self.update_status('Send failed')
        elif not self.connected_device:
            self.update_status('Please connect device first')
        elif not message:
            self.update_status('Please enter a message')

if __name__ == '__main__':
    SimpleBluetoothApp().run()