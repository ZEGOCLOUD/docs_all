@echo off
setlocal enabledelayedexpansion

REM Get ESC character for ANSI color support (Windows 10+ VT100)
for /f %%a in ('powershell -Command "[char]27"') do set "ESC=%%a"
set "RED=!ESC![31m"
set "GREEN=!ESC![32m"
set "YELLOW=!ESC![33m"
set "BLUE=!ESC![34m"
set "NC=!ESC![0m"

REM 检查 docuo 是否存在
set "NPM_REGISTRY=--registry=https://registry.npmmirror.com"
where docuo >nul 2>&1
if errorlevel 1 (
    echo !YELLOW!未检测到 docuo!NC!
    goto :do_setup
)

REM docuo 存在，检查是否为最新版本
for /f "tokens=3 delims=@" %%v in ('npm list -g @spreading/docuo --depth=0 2^>nul ^| findstr "spreading/docuo"') do set "CURRENT_DOCUO_VERSION=%%v"
for /f "tokens=*" %%v in ('npm view @spreading/docuo version %NPM_REGISTRY% 2^>nul') do set "LATEST_DOCUO_VERSION=%%v"

if not defined CURRENT_DOCUO_VERSION goto :lang_select
if not defined LATEST_DOCUO_VERSION goto :lang_select
if "!CURRENT_DOCUO_VERSION!"=="!LATEST_DOCUO_VERSION!" goto :lang_select

echo !YELLOW!Docuo CLI 版本不是最新 (当前: !CURRENT_DOCUO_VERSION!, 最新: !LATEST_DOCUO_VERSION!^)!NC!

:do_setup
echo !YELLOW!正在执行 setup.bat...!NC!
call "%~dp0setup.bat" --no-pause
if errorlevel 1 (
    echo !RED!✗ 安装失败，请手动执行 setup.bat!NC!
    pause
    exit /b 1
)

:lang_select
REM 交互选择语言
echo !BLUE!请选择文档语言:!NC!
echo   !GREEN!1^) 中文!NC! (默认^)
echo   !GREEN!2^) 英文!NC!
set /p "LANG_CHOICE=请输入选择 [1/2]: "

if "!LANG_CHOICE!"=="2" (
    echo !GREEN!启动英文文档...!NC!
    docuo dev --en
) else (
    echo !GREEN!启动中文文档...!NC!
    docuo dev --zh
)

pause
endlocal
