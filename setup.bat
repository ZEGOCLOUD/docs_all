@echo off
setlocal enabledelayedexpansion

REM Get ESC character for ANSI color support (Windows 10+ VT100)
for /f %%a in ('powershell -Command "[char]27"') do set "ESC=%%a"
set "RED=!ESC![31m"
set "GREEN=!ESC![32m"
set "YELLOW=!ESC![33m"
set "BLUE=!ESC![34m"
set "NC=!ESC![0m"

echo !BLUE!========================================!NC!
echo !BLUE!    ZEGO 文档项目环境设置脚本!NC!
echo !BLUE!========================================!NC!
echo.

REM 解析参数
set "DEV_MODE=false"
set "NO_PAUSE=false"
for %%a in (%*) do (
    if "%%a"=="--dev" set "DEV_MODE=true"
    if "%%a"=="--no-pause" set "NO_PAUSE=true"
)

REM 1. 检查 Node.js 版本
echo !YELLOW!1. 检查 Node.js 版本...!NC!
where node >nul 2>&1
if errorlevel 1 (
    echo !RED!✗ 未找到 Node.js!NC!
    echo !YELLOW!请从以下地址下载并安装 Node.js ^>= 19:!NC!
    echo !GREEN!https://nodejs.org/!NC!
    if "!NO_PAUSE!"=="false" pause
    exit /b 1
)

for /f "tokens=1" %%v in ('node -v 2^>nul') do set "NODE_VERSION=%%v"
set "NODE_VERSION=!NODE_VERSION:v=!"
for /f "tokens=1 delims=." %%m in ("!NODE_VERSION!") do set "NODE_MAJOR=%%m"

echo 当前 Node.js 版本: !GREEN!v!NODE_VERSION!!NC!

if !NODE_MAJOR! geq 19 (
    echo !GREEN!✓ Node.js 版本满足要求 (^>= 19^)!NC!
) else (
    echo !RED!✗ Node.js 版本过低，需要 ^>= 19，当前版本: !NODE_VERSION!!NC!
    echo !YELLOW!请从以下地址下载并安装最新的 LTS 版本:!NC!
    echo !GREEN!https://nodejs.org/!NC!
    if "!NO_PAUSE!"=="false" pause
    exit /b 1
)

echo.

REM 2. 安装/升级 Docuo CLI
set "NPM_REGISTRY=--registry=https://registry.npmmirror.com"
echo !YELLOW!2. 检查 Docuo CLI...!NC!
where docuo >nul 2>&1
if errorlevel 1 (
    echo !YELLOW!正在安装 Docuo CLI...!NC!
    npm install -g @spreading/docuo@latest %NPM_REGISTRY%

    where docuo >nul 2>&1
    if errorlevel 1 (
        echo !RED!✗ Docuo CLI 安装失败!NC!
        echo !YELLOW!请尝试手动安装: npm install -g @spreading/docuo!NC!
        if "!NO_PAUSE!"=="false" pause
        exit /b 1
    ) else (
        echo !GREEN!✓ Docuo CLI 安装成功!NC!
    )
) else (
    for /f "tokens=3 delims=@" %%v in ('npm list -g @spreading/docuo --depth=0 2^>nul ^| findstr "spreading/docuo"') do set "CURRENT_DOCUO_VERSION=%%v"
    for /f "tokens=*" %%v in ('npm view @spreading/docuo version %NPM_REGISTRY% 2^>nul') do set "LATEST_DOCUO_VERSION=%%v"

    echo 当前 Docuo CLI 版本: !GREEN!!CURRENT_DOCUO_VERSION!!NC!
    echo 最新 Docuo CLI 版本: !GREEN!!LATEST_DOCUO_VERSION!!NC!

    if "!CURRENT_DOCUO_VERSION!"=="!LATEST_DOCUO_VERSION!" (
        echo !GREEN!✓ Docuo CLI 已是最新版本，无需升级!NC!
    ) else (
        echo !YELLOW!正在清理旧缓存内容...!NC!
        docuo clear
        echo !GREEN!✓ 旧缓存已清理!NC!
        echo !YELLOW!正在升级 Docuo CLI: !CURRENT_DOCUO_VERSION! -^> !LATEST_DOCUO_VERSION!...!NC!
        npm install -g @spreading/docuo@latest %NPM_REGISTRY%
        echo !GREEN!✓ Docuo CLI 已升级到 !LATEST_DOCUO_VERSION!!NC!
    )
)

echo.

REM 以下步骤仅在 --dev 模式下执行
if "!DEV_MODE!"=="true" (
    REM 3. 复制 Git Hooks
    echo !YELLOW!3. 复制 Git Hooks...!NC!
    xcopy /y /q ".hooks\*" ".git\hooks\" >nul 2>&1
    if errorlevel 1 (
        echo !RED!✗ Git Hooks 复制失败，请检查 .hooks 目录是否存在!NC!
    ) else (
        echo !GREEN!✓ Git Hooks 复制成功!NC!
    )
    echo.

    REM 4. 提醒安装 VS Code 插件
    echo !YELLOW!4. 推荐的 VS Code 插件:!NC!
    echo !BLUE!请安装以下插件以获得更好的开发体验:!NC!
    echo.
    echo !GREEN!• Docuo:!NC! https://marketplace.visualstudio.com/items?itemName=spreading-docuo.docuo
    echo !GREEN!• Markdown Table:!NC! https://marketplace.visualstudio.com/items?itemName=TakumiI.markdowntable
    echo !GREEN!• GitLens:!NC! https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
    echo !GREEN!• MDX:!NC! https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx
    echo !GREEN!• GitHub Pull Request:!NC! https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github
    echo.

    REM 5. 提醒查看详细使用说明
    echo !YELLOW!5. 详细使用说明:!NC!
    echo !BLUE!请查看详细的使用指南:!NC!
    echo !GREEN!https://zegocloud.feishu.cn/wiki/G3stwqUPYinrVEkkWkFctzdTnwb!NC!
    echo.
)

echo !BLUE!========================================!NC!
echo !BLUE!    环境设置完成！!NC!
echo !BLUE!========================================!NC!
if "!NO_PAUSE!"=="false" pause
endlocal
