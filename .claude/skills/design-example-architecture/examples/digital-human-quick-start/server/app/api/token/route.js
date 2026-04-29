import { createCipheriv } from "crypto";
import { NextResponse } from "next/server";

// 指定运行时环境为 Node.js
// Specify the runtime environment as Node.js
export const runtime = "nodejs";

// CORS 头配置，允许跨域访问
// Configure CORS headers to allow cross-origin access
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

// ========== Token 生成工具函数 ==========

// 生成随机 Nonce 值
// Generate a random Nonce value
const makeNonce = () => {
  const min = -2147483648;
  const max = 2147483647;
  return Math.ceil(min + (max - min) * Math.random());
};

// 生成随机初始化向量（IV）
// Generate a random initialization vector (IV)
const makeRandomIv = () => {
  const chars = "0123456789abcdefghijklmnopqrstuvwxyz";
  const out = [];
  for (let i = 0; i < 16; i += 1) {
    out.push(chars.charAt(Math.floor(Math.random() * chars.length)));
  }
  return out.join("");
};

// 根据密钥长度获取对应的 AES 加密算法
// Get the corresponding AES encryption algorithm based on key length
const getAlgorithm = (key) => {
  const length = Buffer.from(key).length;
  if (length === 16) return "aes-128-cbc";
  if (length === 24) return "aes-192-cbc";
  if (length === 32) return "aes-256-cbc";
  throw new Error(`Invalid ServerSecret length: ${length}`);
};

// 使用 AES 算法加密明文
// Encrypt plain text using AES algorithm
const aesEncrypt = (plainText, key, iv) => {
  const cipher = createCipheriv(getAlgorithm(key), key, iv);
  cipher.setAutoPadding(true);
  const encrypted = Buffer.concat([cipher.update(plainText), cipher.final()]);
  return Uint8Array.from(encrypted).buffer;
};

// 生成 ZEGO Token（版本 04）
// Generate ZEGO Token (version 04)
const generateToken04 = (
  appId,
  userId,
  secret,
  effectiveTimeInSeconds,
  payload = ""
) => {
  if (!appId || typeof appId !== "number") {
    throw new Error("Invalid appId");
  }
  if (!userId) {
    throw new Error("Invalid userId");
  }
  if (!secret || secret.length !== 32) {
    throw new Error("ServerSecret must be a 32-character string");
  }
  if (!effectiveTimeInSeconds) {
    throw new Error("Invalid effectiveTimeInSeconds");
  }

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

  // 构建二进制缓冲区，存储过期时间、IV 长度、加密内容长度等信息
  // Build binary buffer to store expiration time, IV length, encrypted content length, etc.
  const b1 = new Uint8Array(8);
  const b2 = new Uint8Array(2);
  const b3 = new Uint8Array(2);
  new DataView(b1.buffer).setBigInt64(0, BigInt(tokenInfo.expire), false);
  new DataView(b2.buffer).setUint16(0, iv.length, false);
  new DataView(b3.buffer).setUint16(0, encryptBuf.byteLength, false);

  // 拼接所有二进制数据并返回 Base64 编码的 Token
  // Concatenate all binary data and return Base64 encoded token
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

// 处理 OPTIONS 预检请求
// Handle OPTIONS preflight request
export const OPTIONS = async () => {
  return new NextResponse(null, {
    status: 200,
    headers: corsHeaders,
  });
};

// GET 请求处理器：生成并返回 ZEGO Token
// Generate and return ZEGO Token
export const GET = async (request) => {
  const appId = Number(process.env.APP_ID, 0);
  const serverSecret = process.env.SERVER_SECRET;
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get("userId");
  // 生成有效期 3600 秒的 Token
  // Generate a token with 3600 seconds validity
  const token = generateToken04(appId, userId, serverSecret, 3600, "");
  return NextResponse.json({ token }, {
    headers: corsHeaders,
  });
};
