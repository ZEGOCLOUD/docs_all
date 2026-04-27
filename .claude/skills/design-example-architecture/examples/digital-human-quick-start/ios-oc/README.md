# 数字人播报系统 - iOS 播放端

本示例演示 iOS 端作为播放端，拉取并播放数字人音视频流。

## 一、安装配置与运行

### 1. 环境要求
- Xcode 15.0 或更高版本
- iOS 12.0+
- CocoaPods

### 2. 安装依赖

```bash
cd ZegoDigitalHumanQuickStart
pod install
```

打开 `ZegoDigitalHumanQuickStart.xcworkspace`（注意是 xcworkspace）。

### 3. 配置

编辑 `ZegoDigitalHumanQuickStart/Config.m`：

| 变量 | 说明 |
|------|------|
| `ZEGO_APP_ID` | ZEGO 应用 ID。从 ZEGO [控制台](https://console.zegocloud.com) 获取。 |
| `ZEGO_API_BASE_URL` | 业务后台地址。模拟器使用 `localhost`，真机使用电脑的局域网 IP。 |

```objc
@implementation Config

+ (NSUInteger)ZEGO_APP_ID {
    return 1568727687;  // 替换为你的 AppID
}

+ (NSString *)ZEGO_API_BASE_URL {
    return @"http://localhost:3000";  // 替换为实际地址
}

@end
```

### 4. 运行

```bash
# 在 Xcode 中选择目标设备，点击运行
# 或使用命令行
xcodebuild -workspace ZegoDigitalHumanQuickStart.xcworkspace \
           -scheme ZegoDigitalHumanQuickStart \
           -configuration Debug
```

---

## 二、源码结构

```
ios-oc/
└── ZegoDigitalHumanQuickStart/
    ├── ZegoDigitalHumanQuickStart/
    │   ├── ViewController.m           # 主视图控制器，包含完整的播放流程
    │   ├── Config.h/m                 # 配置文件
    │   └── Info.plist                 # 权限配置
    ├── Podfile                        # CocoaPods 依赖配置
    └── ZegoDigitalHumanQuickStart.xcworkspace
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
| `ZegoExpressPrivate` | 3.22.0.46788 | ZEGO Express SDK (RTC) |
| `ZegoDigitalMobile` | 1.4.0.88 | ZEGO 数字人 SDK |
