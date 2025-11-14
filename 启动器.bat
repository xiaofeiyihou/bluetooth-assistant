@echo off
echo ========================================
echo          手机蓝牙助手启动器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请先安装Python 3.7+并添加到系统PATH
    echo.
    pause
    exit /b 1
)

echo [信息] 检测到Python已安装
python --version

:: 检查是否存在虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo [信息] 未检测到虚拟环境，创建中...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成
)

:: 激活虚拟环境
echo [信息] 激活虚拟环境...
call venv\Scripts\activate.bat

:: 检查依赖文件
if not exist "requirements.txt" (
    echo [错误] 找不到requirements.txt文件
    pause
    exit /b 1
)

:: 检查依赖是否已安装
echo [信息] 检查依赖包...
pip show kivy >nul 2>&1
if errorlevel 1 (
    echo [信息] 安装依赖包中...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
    echo [成功] 依赖包安装完成
) else (
    echo [成功] 依赖包已安装
)

:: 选择运行模式
echo.
echo 请选择运行模式:
echo 1. 简化演示版 (推荐)
echo 2. 完整功能版
echo 3. 原始版本
echo 4. 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo [信息] 启动简化演示版...
    python simple_app.py
) else if "%choice%"=="2" (
    echo [信息] 启动完整功能版...
    python app.py
) else if "%choice%"=="3" (
    echo [信息] 启动原始版本...
    python main.py
) else if "%choice%"=="4" (
    echo [信息] 退出启动器
    exit /b 0
) else (
    echo [错误] 无效选择，退出
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo [错误] 应用运行出错
    echo 请检查错误信息并重试
    pause
) else (
    echo.
    echo [信息] 应用正常退出
)

pause