# 平台识别与自动化测试映射

## 平台识别

从项目目录内容识别目标平台，按以下线索判断：

| 线索 | 判断方式 |
|------|---------|
| 依赖文件 | `package.json` → Web/Node, `pubspec.yaml` → Flutter, `build.gradle` → Android, `Podfile` → iOS, `Cargo.toml` → Rust |
| 代码文件 | `.tsx`/`.jsx`/`.vue` → Web, `.kt`/`.java` → Android, `.swift`/`.m` → iOS, `.dart` → Flutter |
| 框架特征 | `next.config` → Next.js, `nuxt.config` → Nuxt, `capacitor.config` → Capacitor, `electron` dep → Electron |
| 项目结构 | `android/` + `ios/` 且无 `lib/main.dart` → React Native, `android/` + `ios/` + `lib/main.dart` → Flutter |

## 自动化测试技能映射

| 平台 | 自动化测试技能 | 构建目标 | 备注 |
|------|--------------|---------|------|
| Web (React/Vue/原生/Next.js) | `zego-browser-automation` | 浏览器应用 | 启动 dev server 后测试 |
| Android 原生 | `android-device-automation` | Android APK | 需连接设备或模拟器 |
| iOS 原生 | `ios-device-automation` | iOS 应用 | 需连接设备或模拟器 |
| Flutter | `android-device-automation` | Android APK | 跨平台框架默认构建 Android |
| React Native | `android-device-automation` | Android APK | 跨平台框架默认构建 Android |
| uni-app | `android-device-automation` | Android APK | 跨平台框架默认构建 Android |
| Electron | `desktop-computer-automation` | 桌面应用 | macOS/Windows 桌面 |
| Node.js 服务端 | 无（手动 curl/测试脚本） | 服务进程 | 用 test-cases.sh 直接验证 |

## 编译命令

| 平台 | 编译命令 | 说明 |
|------|---------|------|
| Web | `npm install && npm run build` | 构建生产包验证 |
| Android | `./gradlew assembleDebug` | 构建 Debug APK |
| iOS | `xcodebuild -workspace *.xcworkspace -scheme * build` | 构建验证 |
| Flutter | `flutter build apk` | 构建 Android APK |
| React Native | `cd android && ./gradlew assembleDebug` | 构建 Android APK |
| Node.js | `npm install && npm run build`（如有） | 服务端可能无需构建 |

## 启动命令

| 平台 | 启动命令 | 说明 |
|------|---------|------|
| Web | `npm run dev` | 通常端口 3000/5173/8080 |
| Android | `adb install app-debug.apk && adb shell am start` | 安装并启动 |
| Flutter | `flutter run` | 连接设备运行 |
| Node.js | `npm start` 或 `node index.js` | 启动服务进程 |

## 截图方式

| 平台 | 截图工具 | 方式 |
|------|---------|------|
| Web | `zego-browser-automation` 的截图功能 | Playwright 截图 |
| Android | `android-device-automation` 的截图功能 | adb screencap |
| iOS | `ios-device-automation` 的截图功能 | xcrun simctl io |
| 桌面 | `desktop-computer-automation` 的截图功能 | 系统截图 |
