# 数字人播报系统编排端

本示例演示数字人播报系统的编排端，用于配置播报内容并启动播报任务。

## 一、安装配置与启动

### 1. 环境要求
- Node.js 18+

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入 ZEGO 控制台获取的配置：

| 变量 | 说明 |
|------|------|
| `APP_ID` | ZEGO 应用 ID。从 ZEGO [控制台](https://console.zego.im/) 获取。 |
| `SERVER_SECRET` | 服务端密钥（32位，用于生成 Token，服务端 API 签名验证）。从 ZEGO [控制台](https://console.zego.im/) 获取。 |
| `TOKEN_EXPIRE_SECONDS` | ZEGO 客户端 SDK 用的 Token 有效期（秒，默认 3600） |

### 3. 安装依赖并启动

```bash
npm install
npm run dev
```

访问 `http://localhost:3000` 打开配置页面。

---

## 二、源码结构

```
server/
├── app/
│   ├── api/                    # API 路由
│   │   ├── broadcast/          # 播报任务管理
│   │   ├── token/              # Token 生成
│   │   ├── digital-humans/     # 数字人列表
│   │   └── timbres/            # 音色列表
│   ├── page.jsx                # 编排面板（Web UI）
├── lib/                        # 核心逻辑
│   ├── digitalHuman.js         # ZEGO 数字人 API 封装
│   ├── token.js                # Token04 算法实现。用于生成 ZEGO 客户端 SDK 用的 Token
│   └── broadcast.js            # 播报任务管理逻辑。请根据业务需求自行实现。
├── instrumentation.js          # 服务器启动钩子。用于清理遗留的数字人任务。
└── package.json
```

---



## 三、API 接口说明

业务后台提供两类接口，分别供编排端和播放端调用：

### 1. 编排端调用接口

编排端（编排面板）调用以下接口配置和管理播报任务：

| 端点 | 方法 | 请求参数 | 说明 |
|------|------|---------|------|
| `/api/digital-humans` | GET | - | 获取数字人列表 |
| `/api/broadcast` | POST | `digitalHumanId`, `timbreId`, `roomId`, `streamId`, `textPool`, `outputMode` | 启动播报任务 |
| `/api/broadcast?index=N` | DELETE | `index`（查询参数） | 停止指定播报任务 |
| `/api/timbres` | GET | `digitalHumanId`（可选） | 获取音色列表 |