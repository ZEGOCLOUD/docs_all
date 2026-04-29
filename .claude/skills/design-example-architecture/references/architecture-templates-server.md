# 服务端示例代码架构模板

基于"单文件实现"原则的服务端示例代码架构模板。

## Node.js + Express

### 项目结构

```
Server-Example/
├── index.js                        # 所有逻辑在此文件
├── .env.example                    # 环境变量示例
├── package.json
└── README.md
```

### .env.example

```bash
# AppID / AppID
APP_ID=1234567890

# ServerSecret / ServerSecret（请妥善保管 / Keep it secret）
SERVER_SECRET=your_server_secret_here

# 端口 / Port
PORT=3000
```

### index.js（完整示例）

```javascript
const express = require('express');
const cors = require('cors');
const { ZegoServerAssistant } = require('zego-server-assistant');

const app = express();
app.use(cors());
app.use(express.json());

// ========== Token 生成接口（直接在路由中实现）/ Token endpoint ==========
app.post('/api/token', (req, res) => {
  const { roomId, userId } = req.body;

  if (!userId) {
    return res.status(400).json({
      error: '缺少参数 / Missing parameter: userId is required'
    });
  }

  // 使用 zego_server_assistant 生成 Token
  // Use zego_server_assistant to generate token
  const token = ZegoServerAssistant.generateToken04(
    Number(process.env.APP_ID),
    userId,
    process.env.SERVER_SECRET,
    3600,                    // Token 有效期 / Token validity period (seconds)
    ''                       // payload：基础鉴权传空字符串
  );

  res.json({ token });
});

// ========== 获取房间用户数接口（直接在路由中实现）/ Get room user count ==========
app.get('/api/room/:roomId/users', (req, res) => {
  const { roomId } = req.params;

  // 生成签名参数 / Generate signature parameters
  const crypto = require('crypto');
  const signatureNonce = crypto.randomBytes(8).toString('hex');
  const timestamp = Math.round(Date.now() / 1000);
  const hash = crypto.createHash('md5');
  hash.update(process.env.APP_ID + signatureNonce + process.env.SERVER_SECRET + timestamp);
  const signature = hash.digest('hex');

  // 构建请求 URL / Build request URL
  const params = new URLSearchParams({
    Action: 'DescribeUserNum',
    AppId: process.env.APP_ID,
    SignatureNonce: signatureNonce,
    Timestamp: timestamp,
    Signature: signature,
    SignatureVersion: '2.0',
    'RoomId[]': roomId
  });

  const url = `https://rtc-api.zego.im/?${params.toString()}`;

  // 发送请求 / Send request
  fetch(url)
    .then(response => response.json())
    .then(data => res.json(data))
    .catch(error => res.status(500).json({ error: error.message }));
});

// ========== 启动服务 / Start server ==========
app.listen(process.env.PORT || 3000, () => {
  console.log(`服务运行在端口 / Server running on port ${process.env.PORT || 3000}`);
});
```

## Next.js

### 项目结构

```
Server-Example/
├── app/
│   ├── api/
│   │   ├── token/
│   │   │   └── route.js           # Token 生成（所有逻辑在此文件）
│   │   └── broadcast/
│   │       └── route.js           # 广播管理（所有逻辑在此文件）
│   ├── page.jsx                    # 配置页面
│   └── layout.jsx
├── .env.example                    # 环境变量示例
├── package.json
└── README.md
```

### app/api/token/route.js（完整示例）

```javascript
import { createCipheriv } from 'crypto';
import { NextResponse } from 'next/server';

export const runtime = "nodejs";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

// 生成随机 Nonce / Generate random Nonce
const makeNonce = () => {
  const min = -2147483648;
  const max = 2147483647;
  return Math.ceil(min + (max - min) * Math.random());
};

// 生成随机 IV / Generate random IV
const makeRandomIv = () => {
  const chars = "0123456789abcdefghijklmnopqrstuvwxyz";
  const out = [];
  for (let i = 0; i < 16; i += 1) {
    out.push(chars.charAt(Math.floor(Math.random() * chars.length)));
  }
  return out.join("");
};

// 获取 AES 算法 / Get AES algorithm
const getAlgorithm = (key) => {
  const length = Buffer.from(key).length;
  if (length === 16) return "aes-128-cbc";
  if (length === 24) return "aes-192-cbc";
  if (length === 32) return "aes-256-cbc";
  throw new Error(`Invalid ServerSecret length: ${length}`);
};

// AES 加密 / AES encryption
const aesEncrypt = (plainText, key, iv) => {
  const cipher = createCipheriv(getAlgorithm(key), key, iv);
  cipher.setAutoPadding(true);
  const encrypted = Buffer.concat([cipher.update(plainText), cipher.final()]);
  return Uint8Array.from(encrypted).buffer;
};

// 生成 Token04 / Generate Token04
const generateToken04 = (appId, userId, secret, effectiveTimeInSeconds, payload = "") => {
  const createTime = Math.floor(Date.now() / 1000);
  const tokenInfo = {
    app_id: appId,
    user_id: userId,
    nonce: makeNonce(),
    ctime: createTime,
    expire: createTime + effectiveTimeInSeconds,
    payload,
  };

  const plainText = JSON.stringify(tokenInfo);
  const iv = makeRandomIv();
  const encryptBuf = aesEncrypt(plainText, secret, iv);

  const b1 = new Uint8Array(8);
  const b2 = new Uint8Array(2);
  const b3 = new Uint8Array(2);
  new DataView(b1.buffer).setBigInt64(0, BigInt(tokenInfo.expire), false);
  new DataView(b2.buffer).setUint16(0, iv.length, false);
  new DataView(b3.buffer).setUint16(0, encryptBuf.byteLength, false);

  const buf = Buffer.concat([
    Buffer.from(b1),
    Buffer.from(b2),
    Buffer.from(iv),
    Buffer.from(b3),
    Buffer.from(encryptBuf),
  ]);

  return `04${Buffer.from(buf).toString("base64")}`;
};

// ========== HTTP 路由处理 ==========

export const OPTIONS = async () => {
  return new NextResponse(null, {
    status: 200,
    headers: corsHeaders,
  });
};

export const GET = async (request) => {
  const appId = Number(process.env.APP_ID, 0);
  const serverSecret = process.env.SERVER_SECRET;
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get("userId");

  const token = generateToken04(appId, userId, serverSecret, 3600, "");

  return NextResponse.json({ token }, {
    headers: corsHeaders,
  });
};
```

## 关键点说明

### Node.js + Express
1. **所有逻辑在 index.js 单文件内**
2. **AppID、ServerSecret 从环境变量读取**
3. **业务逻辑直接在路由处理函数中实现**

### Next.js
1. **所有逻辑在 route.js 单文件内**
2. **禁止使用 lib/、services/ 目录**
3. **API 签名、加密等工具函数直接写在 route.js 底部**
