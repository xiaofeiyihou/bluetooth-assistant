# 蓝牙助手APP - GitHub Actions 自动构建指南

## 概述

您的蓝牙助手APP已经准备好进行APK构建了！通过GitHub Actions，您可以轻松地在云端构建Android APK，无需复杂的本地环境配置。

## 🚀 快速开始

### 1. 创建GitHub仓库

```bash
# 在GitHub上创建新仓库，命名为 bluetooth-assistant
# 上传所有项目文件到仓库
```

### 2. 启用Actions

1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 系统会自动检测 `.github/workflows/build.yml` 文件
4. 点击 "Enable Actions"

### 3. 触发构建

构建会自动在以下情况触发：
- 推送到 `main` 或 `master` 分支
- 创建Pull Request到 `main` 或 `master` 分支

手动触发：
1. 进入 Actions 页面
2. 选择 "Build Android APK" workflow
3. 点击 "Run workflow"

### 4. 下载APK

构建完成后：
1. 进入 Actions 页面
2. 查看最新的构建记录
3. 点击构建记录查看详情
4. 在底部 "Artifacts" 部分下载APK文件

## 📱 构建结果

GitHub Actions会生成两个构建产物：

1. **Debug APK** (`bluetooth-assistant-debug`)
   - 用于测试和开发
   - 包含调试信息
   - 文件较大但开发友好

2. **Release AAB** (`bluetooth-assistant-release`)
   - 用于发布到Google Play
   - 优化过的大小
   - 签名版本

## 📋 构建配置

### 当前配置：
- **包名**: `com.bluetooth.assistant`
- **应用名称**: `Bluetooth Assistant`
- **最低Android版本**: API 21 (Android 5.0)
- **目标Android版本**: API 31 (Android 12)
- **入口文件**: `simple_app_english.py`

### 权限配置：
```xml
BLUETOOTH
BLUETOOTH_ADMIN
ACCESS_FINE_LOCATION
VIBRATE
INTERNET
ACCESS_COARSE_LOCATION
```

## 🔧 自定义构建

### 修改应用信息
编辑 `buildozer.spec` 文件：
- 应用标题: `title = 您的应用名称`
- 包名: `package.name = 您的包名`
- 版本: `version = 1.0`

### 修改权限
在 `buildozer.spec` 中：
```
android.permissions = 权限1,权限2,权限3
```

### 添加依赖
在 `buildozer.spec` 中：
```
requirements = python3,kivy,其他依赖
```

## 🛠️ 项目文件结构

```
bluetooth-assistant/
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions配置文件
├── buildozer.spec             # Buildozer构建配置
├── android.txt                # Android权限配置
├── simple_app_english.py      # 主应用文件（英文界面）
├── requirements.txt           # Python依赖
└── README.md                  # 项目说明
```

## 📊 构建日志

每次构建都会生成详细的日志，包含：
- 环境设置过程
- 依赖安装过程
- 构建过程
- 错误信息（如有）

## 🎯 立即可用的功能

您的应用已经包含：

✅ **完整的蓝牙管理功能**
- 设备扫描
- 蓝牙连接
- 消息发送/接收

✅ **现代化UI界面**
- 英文界面（避免乱码）
- Kivy跨平台UI
- 响应式设计

✅ **Android权限完整配置**
- 所有必需权限
- Android 12+ 兼容
- Google Play 政策合规

✅ **跨平台兼容性**
- Windows/MacOS/Linux开发
- Android/iOS构建支持
- 云端构建无障碍

## 🚨 常见问题

### Q: 构建失败怎么办？
A: 检查Actions页面的构建日志，常见问题包括：
- 语法错误
- 依赖缺失
- 权限问题

### Q: 能否自定义构建时间？
A: 可以在workflow中修改触发条件或使用手动触发

### Q: 如何上传到Google Play？
A: 下载生成的AAB文件，上传到Google Play Console

## 📞 技术支持

如果遇到问题：
1. 检查构建日志
2. 确认所有文件已上传
3. 验证`buildozer.spec`配置正确
4. 确认GitHub仓库设置为public（如使用免费计划）

## 🎉 下一步

1. **创建GitHub仓库**
2. **上传项目文件**
3. **启用GitHub Actions**
4. **触发第一次构建**
5. **下载并测试APK**
6. **发布到Google Play或分发**

您的蓝牙助手APP已经完全可以构建和部署了！🎊