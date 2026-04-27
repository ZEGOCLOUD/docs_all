# 示例代码架构原则

本文件定义 ZEGO 示例代码的通用架构原则，所有平台共享。

## 核心设计原则：可读性优先

示例代码的目的是让用户快速理解 SDK 使用方式，而非展示工程化最佳实践。

| 原则 | 说明 | 反例（禁止） |
|-----|------|-------------|
| 直接调用 | View/Activity 中直接调用 SDK API | 封装成 ZegoEngineManager、ZegoRoomManager |
| 代码集中 | 相关逻辑放在单个文件中 | 分散到多个 Manager/Service 类 |
| 扁平化 | 避免层层嵌套的工具类封装 | Helper 内部再调用其他 Helper |
| 一层到底 | 如果必须有辅助类，方法也应直接调用 SDK | 抽象层、工厂模式等过度设计 |

**唯一允许的封装**：
- 权限相关工具（如 PermissionHelper）
- 配置常量类（从环境变量/配置文件读取）
- UI 组件（如自定义 VideoView）

## 配置规范

| 配置类型 | 存放位置 | 说明 |
|---------|---------|------|
| AppID、ServerSecret | 环境变量或配置文件 | 与代码分离，不硬编码，也不要让用户在前端页面输入。示例代码必须有fallback读取环境变量中 ZEGO_APPID 和 ZEGO_SERVER_SECRET 的值的行为 |
| Token | 服务端 API 获取 | 客户端不直接生成 |
| RoomID、UserID | 前端页面输入 | 用户根据需要填写 |

## UI 规范
**对于移动端（Android、iOS、Flutter、uni-app、HarmonyOS、react-native）**：
- 要设置安全区，避免UI元素被状态栏遮挡
- 核心的元素组件要靠顶部，避免被虚拟键盘弹出后遮挡

## 技术约束

1. **服务端默认框架**:
   - 纯服务端 API：默认使用 Node.js（Express）- 所有逻辑在单个 route.js 文件内
   - 需要配置页面：使用 Next.js - 业务逻辑直接在 app/api/*/route.js 中实现
2. **禁止**：将服务端逻辑分离到 lib/、services/、utils/ 等目录

## 各平台标准入口

| 平台 | 核心文件 | SDK 初始化位置 | 配置来源 |
|-----|---------|---------------|---------|
| Android Java/Kotlin | MainActivity | createEngine() 方法 | BuildConfig / local.properties |
| iOS Swift/OC | ViewController | viewDidLoad() 方法 | Config.xcconfig |
| Web (React/Vue) | App.tsx / App.vue | useState() 初始化 | .env (VITE_ 前缀) |
| Node.js | index.js / route.js | app.listen() 之前 | .env |

## 反模式：不要这样写

### ❌ 错误示例：层层封装

```
MainActivity
    └── ZegoEngineManager
            └── ZegoRoomManager
                    └── ZegoStreamManager
                            └── ZegoEventHandler
```

用户需要打开 5 个文件才能理解登录房间的逻辑。

### ❌ 错误示例：硬编码配置

```java
long appId = 1234567890;  // 硬编码 / Hardcoded
```

### ✅ 正确示例：单文件 + 配置分离

```
MainActivity
    ├── createEngine(): 直接 ZegoExpressEngine.createEngine(profile)
    │   └── profile.appID = BuildConfig.APP_ID  // 从配置读取
    ├── loginRoom(): 直接 engine.loginRoom()
    │   └── roomID = etRoomId.getText()  // 用户输入
    ├── setEventHandler(): 直接实现 IZegoEventHandler
    └── getToken(): 从服务端获取 Token
```

用户阅读一个文件就能理解完整流程。
