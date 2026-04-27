# 数字人播报系统 - Web 播放端 (Vue)

本示例演示 Web 端作为播放端，拉取并播放数字人音视频流。

## 一、安装配置与运行

### 1. 环境要求
- Node.js 18+
- 现代浏览器（Chrome、Safari、Edge 等）

### 2. 配置

编辑 `.env` 文件：

| 变量 | 说明 |
|------|------|
| `VITE_APP_ID` | ZEGO 应用 ID |
| `VITE_API_BASE_URL` | 业务后台地址 |

```bash
VITE_APP_ID=1568727687
VITE_API_BASE_URL=http://localhost:3001
```

### 3. 安装依赖并运行

```bash
npm install
npm run dev
```

访问 `http://localhost:5173`。

---

## 二、源码结构

```
web-vue/
├── src/
│   ├── App.vue                  # 主组件，包含完整的播放流程
│   ├── main.js                  # 入口文件
│   └── assets/                  # 静态资源
├── .env                         # 环境变量配置
├── package.json
└── vite.config.js
```

---

## 三、核心流程

```
获取播报列表 → 获取 Token → 登录房间 → 拉流播放
```

| 步骤 | 说明 |
|------|------|
| 获取播报列表 | 调用 `GET /api/broadcast`，获取 roomId、streamId |
| 获取 Token | 调用 `GET /api/token?userId=xxx`，获取 RTC 登录 Token |
| 登录房间 | 使用 Express SDK 登录 RTC 房间 |
| 拉流播放 | 拉取数字人音视频流并渲染到页面 |

---

## 四、依赖说明

| 依赖 | 说明 |
|------|------|
| `zego-express-engine-webrtc` | ZEGO Express Web SDK |
| `vue` | Vue 3 框架 |
| `vite` | 构建工具 |
