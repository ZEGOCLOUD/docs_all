---
name: design-example-architecture
description: This skill should be used when designing or reviewing ZEGO SDK example code architecture. Define architecture principles, platform-specific entry points, configuration standards, and quality standards to ensure examples prioritize readability over engineering best practices. Use when: creating new ZEGO SDK example projects (Android/iOS/Web/Server), reviewing existing example code architecture, ensuring code follows "single-file implementation" principle, setting up configuration management (AppID/ServerSecret from environment variables), implementing token generation and room management patterns, or checking if code follows ZEGO's example code standards.
version: 1.2.0
---

# ZEGO 示例代码架构设计

定义 ZEGO SDK 示例代码的架构原则和标准，确保示例代码"可读性优先"而非"工程化最佳实践"。

## 使用场景

当以下情况时使用本 skill：
- 创建新的 ZEGO SDK 示例项目（Android/iOS/Web/Server）
- 审查现有示例代码的架构
- 确保代码遵循"单文件实现"原则
- 设置配置管理（AppID/ServerSecret 从环境变量读取）
- 实现 Token 生成和房间管理模式
- 检查代码是否符合 ZEGO 示例代码规范

## 使用步骤

1. **确定平台** — 明确目标平台（Android/iOS/Web/Server）
2. **选择架构模板** — 从 `references/` 获取对应平台模板（principles、android、web、server）【注意：必须完整加载阅读 references/architecture-templates-principles.md 】
3. **参考示例项目** — 浏览 `examples/digital-human-quick-start/` 了解实际实现作为参考
4. **遵循核心原则** — 确保代码符合架构原则
5. **检查质量清单** — 完成后逐项验证

## 核心原则

示例代码的目的是让用户快速理解 SDK 使用方式。

| 原则 | 说明 | 反例（禁止） |
|-----|------|-------------|
| 直接调用 | View/Activity 中直接调用 SDK API | 封装成 ZegoEngineManager、ZegoRoomManager |
| 代码集中 | 相关逻辑放在单个文件中 | 分散到多个 Manager/Service 类 |
| 扁平化 | 避免层层嵌套的工具类封装 | Helper 内部再调用其他 Helper |
| 一层到底 | 如果必须有辅助类，方法也应直接调用 SDK | 抽象层、工厂模式 |

**唯一允许的封装**：权限工具（PermissionHelper）、配置常量类、UI 组件（VideoView）。

## 平台标准入口

| 平台 | 核心文件 | SDK 初始化位置 | 配置来源 |
|-----|---------|---------------|---------|
| Android Java/Kotlin | MainActivity | createEngine() 方法 | BuildConfig / local.properties |
| iOS Swift/OC | ViewController | viewDidLoad() 方法 | Config.h/m（直接编辑） |
| Web (React/Vue) | App.tsx / App.vue | useState() 初始化 | .env (VITE_ 前缀) |
| Node.js | index.js / route.js | app.listen() 之前 | .env |

## 配置规范

| 配置类型 | 存放位置 | 说明 |
|---------|---------|------|
| AppID、ServerSecret | 环境变量或配置文件 | 与代码分离，不硬编码 |
| Token | 服务端 API 获取 | 客户端不直接生成 |
| RoomID、UserID | 前端页面输入 | 用户根据需要填写 |

**Android 配置方式**：使用 `local.properties`
```properties
ZEGO_APP_ID=1234567890
ZEGO_API_BASE_URL=http://localhost:3000
```

**Web 配置方式**：使用 `.env`
```bash
VITE_APP_ID=1234567890
VITE_API_BASE_URL=http://localhost:3000
```

## 服务端默认框架

- **纯服务端 API**：默认使用 Node.js（Express）- 所有逻辑在单个 route.js 文件内
- **需要配置页面**：使用 Next.js - 业务逻辑直接在 app/api/*/route.js 中实现

**禁止**：将服务端逻辑分离到 lib/、services/、utils/ 等目录。

## 参考资源

| 文件 | 用途 |
|-----|------|
| `references/architecture-templates-principles.md` | 通用架构原则、反模式（所有平台共享）【重要，必须阅读】 |
| `references/architecture-templates-android.md` | Android 完整架构模板和代码示例 |
| `references/architecture-templates-ios.md` | iOS (Swift/OC) 完整架构模板和代码示例 |
| `references/architecture-templates-web.md` | Web (React/Vue) 完整架构模板和代码示例 |
| `references/architecture-templates-server.md` | 服务端 (Node.js/Next.js) 完整架构模板和代码示例 |
| `examples/digital-human-quick-start/` | 完整示例项目，包含多端实现 |

## 质量检查清单

### 代码结构
- [ ] 所有 SDK 调用在单个主文件内完成
- [ ] 不包含 Manager/Service/Wrapper 等封装层
- [ ] 辅助类仅限于：权限、配置、UI 组件

### 配置管理
- [ ] AppID/ServerSecret 从环境变量读取（不硬编码）
- [ ] 提供 .env.example 或 local.properties.example
- [ ] RoomID/UserID 通过页面输入

### Token 鉴权
- [ ] Token 从服务端 API 获取
- [ ] 服务端实现 Token 生成接口
- [ ] 客户端不直接生成 Token

### 文档完整性
- [ ] README 包含架构图
- [ ] README 包含时序图（Mermaid 格式）
- [ ] README 包含快速启动说明
- [ ] 多端项目有总 README 说明架构关系

## 常见错误

| 错误 | 后果 | 正确做法 |
|-----|------|---------|
| 硬编码 AppID | 用户误用配置值 | 使用 BuildConfig 或 process.env |
| 封装成 Manager 类 | 用户需跳转多个文件 | 直接在主文件调用 SDK |
| 服务端使用 lib/ 目录 | 违反代码集中原则 | 所有逻辑在 route.js 内 |
| 缺少 .env.example | 用户不知道配置什么 | 提供配置示例文件 |
| README 缺少时序图 | 难以理解调用流程 | 添加 Mermaid sequenceDiagram |
