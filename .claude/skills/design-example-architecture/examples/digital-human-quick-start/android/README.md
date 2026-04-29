# 数字人播报系统 - Android 播放端

本示例演示 Android 端作为播放端，拉取并播放数字人音视频流。

## 一、安装配置与运行

### 1. 环境要求
- Android Studio Hedgehog (2023.1.1) 或更高版本
- Android SDK 24+ (Android 7.0+)
- Kotlin 1.9+

### 2. 配置

编辑 `app/src/main/java/com/example/digitalhumanquickstartdemo/config/Config.kt`：

| 变量 | 说明 |
|------|------|
| `APP_ID` | ZEGO 应用 ID。从 ZEGO [控制台](https://console.zego.im/) 获取。 |
| `API_BASE_URL` | 业务后台地址。模拟器使用 `10.0.2.2` 访问宿主机，真机使用电脑的局域网 IP。 |

```kotlin
object Config {
    const val APP_ID: Long = 1234567890L  // 替换为你的 AppID
    const val API_BASE_URL = "http://localhost:3000"  // 替换为实际地址
}
```

### 3. 运行

```bash
# 打开 Android Studio，打开项目后点击运行
./gradlew installDebug
```

---

## 二、源码结构

```
android/
├── app/
│   └── src/main/
│       ├── java/com/example/digitalhumanquickstartdemo/
│       │   ├── MainActivity.kt           # 主 Activity，包含完整的播放流程
│       │   └── config/
│       │       └── Config.kt             # 配置文件
│       └── res/
│           └── layout/
│               └── activity_main.xml     # UI 布局
└── build.gradle.kts                      # 依赖配置
```

---

## 三、核心流程

```
获取播报列表 → 获取 Token → 预加载资源 → 登录房间 → 启动数字人
```

| 步骤 | 说明 |
|------|------|
| 获取播报列表 | 调用 `GET /api/broadcast`，获取 roomId、streamId 和数字人渲染信息 |
| 获取 Token | 调用 `GET /api/token?userId=xxx`，获取 RTC 登录 Token |
| 预加载资源 | 使用数字人 SDK 预加载资源文件 |
| 登录房间 | 使用 Express SDK 登录 RTC 房间 |
| 启动数字人 | 启动数字人 SDK，开启自定义视频渲染，透传视频帧和 SEI 数据 |

---

## 四、依赖说明

| 依赖 | 版本 | 说明 |
|------|------|------|
| `im.zego:digitalmobile` | 1.4.0.88 | ZEGO 数字人 SDK |
| `im.zego:express-private` | 3.22.0.46726 | ZEGO Express SDK (RTC) |
