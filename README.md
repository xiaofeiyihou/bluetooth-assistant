# 📱 手机蓝牙助手 - Python APP

一个基于Python和Kivy框架开发的跨平台手机蓝牙APP，支持蓝牙设备扫描、连接和双向通信功能。

## 🌟 主要功能

- **🔍 蓝牙设备扫描**: 自动扫描周围的蓝牙设备
- **🔗 设备连接**: 一键连接目标蓝牙设备  
- **💬 双向通信**: 与蓝牙设备进行实时数据交换
- **📱 移动友好**: 专为手机屏幕优化的界面设计
- **🔄 跨平台**: 支持Android、iOS和Windows平台

## 📁 项目结构

```
APP/
├── main.py                 # 原始主程序（完整版）
├── app.py                  # 基于KV文件的界面版本
├── simple_app.py           # 简化演示版（推荐）
├── bluetooth_manager.py    # 蓝牙管理模块
├── bluetooth_app.kv        # KV界面描述文件
├── requirements.txt        # Python依赖包
├── android.txt            # Android权限配置
└── README.md              # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装Python 3.7+版本。

### 2. 安装依赖

```bash
# 切换到项目目录
cd C:\Users\38778\Desktop\TEST\APP

# 安装Python依赖包
pip install -r requirements.txt
```

### 3. 运行应用

#### 简化演示版（推荐）
```bash
python simple_app.py
```

#### 完整功能版
```bash
python app.py
```

#### 原始版本
```bash
python main.py
```

## 📱 界面说明

### 主界面布局
1. **标题栏**: 显示APP名称
2. **状态栏**: 显示当前操作状态
3. **扫描按钮**: 开始/停止扫描蓝牙设备
4. **设备列表**: 显示发现的蓝牙设备
5. **通信区域**: 显示聊天记录和输入框
6. **连接状态**: 显示当前连接状态

### 操作流程
1. 点击"扫描蓝牙设备"按钮
2. 等待扫描完成，查看发现的设备列表
3. 点击目标设备进行连接
4. 连接成功后开始发送/接收消息
5. 通过底部的输入框发送消息

## 🔧 功能特性

### 蓝牙设备扫描
- 自动检测周围的BLE设备
- 显示设备名称和MAC地址
- 支持10秒扫描超时

### 设备连接
- 支持BLE (Bluetooth Low Energy) 设备
- 显示连接状态和进度
- 自动重连机制

### 双向通信
- 实时消息收发
- 支持中文消息
- 消息时间戳
- 发送/接收状态区分

## 📋 支持的蓝牙设备

### 兼容设备类型
- Arduino蓝牙模块 (HC-05, HC-06)
- ESP32开发板
- 智能手表
- 蓝牙耳机
- 其他BLE兼容设备

### 服务UUID
- 通知服务: `0000ffe0-0000-1000-8000-00805f9b34fb`
- 发送特征: `0000ffe1-0000-1000-8000-00805f9b34fb`

## 💻 开发说明

### 技术栈
- **Python 3.7+**: 主要编程语言
- **Kivy**: 跨平台UI框架
- **bleak**: BLE蓝牙通信库
- **asyncio**: 异步编程支持

### 核心模块

#### bluetooth_manager.py
- 蓝牙设备扫描
- 设备连接管理
- 数据收发处理
- 连接状态维护

#### simple_app.py
- 简化版主程序
- 模拟蓝牙功能
- 移动端界面设计
- 用户交互逻辑

### 自定义配置

#### 修改扫描时间
```python
# 在bluetooth_manager.py中
await asyncio.sleep(10)  # 修改为所需扫描时间
```

#### 添加新设备类型
```python
# 在simple_app.py中的mock_devices列表中添加
{'name': '新设备名', 'address': '设备MAC地址'}
```

#### 修改界面主题
```python
# 修改颜色配置
background_color=(0.2, 0.6, 0.8, 1)  # RGB值 (0-1范围)
```

## 📦 部署说明

### Android APK构建
1. 安装Buildozer:
   ```bash
   pip install buildozer
   ```

2. 初始化Buildozer:
   ```bash
   buildozer init
   ```

3. 构建APK:
   ```bash
   buildozer android debug
   ```

### iOS部署
1. 安装Kivy iOS:
   ```bash
   pip install kivy-ios
   ```

2. 构建iOS应用:
   ```bash
   toolchain build python3
   toolchain build kivy
   ```

### Windows部署
使用PyInstaller打包为exe文件:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed simple_app.py
```

## 🐛 常见问题

### Q1: 扫描不到蓝牙设备
**A**: 请确保：
- 蓝牙功能已开启
- 设备处于可发现状态
- 距离在有效范围内 (< 10米)
- Android设备需要位置权限

### Q2: 连接失败
**A**: 检查以下项目：
- 设备是否已配对
- 设备是否支持BLE协议
- 距离是否合适
- 设备电量是否充足

### Q3: 消息发送失败
**A**: 可能的原因：
- 设备未正确连接
- 蓝牙信号不稳定
- 设备不支持发送的数据格式

### Q4: 界面显示异常
**A**: 尝试以下解决方案：
- 更新图形驱动程序
- 检查屏幕分辨率设置
- 重启应用程序

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献指南
1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📞 支持

如果您有任何问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

## 🔮 未来规划

- [ ] 支持蓝牙classic设备
- [ ] 添加设备配对管理
- [ ] 实现文件传输功能
- [ ] 添加历史记录保存
- [ ] 支持多设备同时连接
- [ ] 添加设备图标和状态指示
- [ ] 实现语音消息支持

---

**作者**: AI Assistant  
**版本**: 1.0.0  
**更新时间**: 2024年