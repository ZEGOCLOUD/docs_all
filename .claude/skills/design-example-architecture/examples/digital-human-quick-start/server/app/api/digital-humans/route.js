import { NextResponse } from "next/server";
import crypto from "crypto";

export const runtime = "nodejs";

// ========== ZEGO Digital Human API 工具函数 ==========

// 构建通用 API 请求参数（包含签名）
// Build common API request parameters (including signature)
const buildCommonParams = (action) => {
  const appId = process.env.APP_ID;
  const serverSecret = process.env.SERVER_SECRET || "";
  const signatureNonce = crypto.randomBytes(8).toString("hex");
  const timestamp = Math.floor(Date.now() / 1000);
  // 计算 MD5 签名
  // Calculate MD5 signature
  const signature = crypto
    .createHash("md5")
    .update(`${appId}${signatureNonce}${serverSecret}${timestamp}`)
    .digest("hex");

  return new URLSearchParams({
    Action: action,
    AppId: appId.toString(),
    SignatureNonce: signatureNonce,
    Timestamp: timestamp.toString(),
    Signature: signature,
    SignatureVersion: "2.0",
  });
};

// 发送 POST 请求到 ZEGO 数字人 API
// Send POST request to ZEGO Digital Human API
const post = async (action, body) => {
  const params = buildCommonParams(action);
  const url = `https://aigc-digitalhuman-api.zegotech.cn/?${params.toString()}`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (data.Code !== 0) {
    throw new Error(`Digital Human API failed: ${data.Code} ${data.Message}`);
  }
  return data.Data;
};

// 获取数字人列表
// Get digital human list
const getDigitalHumanList = async (params) => {
  const body = {};
  if (params.inferenceMode !== undefined) {
    body.InferenceMode = params.inferenceMode;
  }
  if (params.fetchMode !== undefined) {
    body.FetchMode = params.fetchMode;
  }
  if (params.offset !== undefined) {
    body.Offset = params.offset;
  }
  if (params.limit !== undefined) {
    body.Limit = params.limit;
  }

  const data = await post("GetDigitalHumanList", body);
  return data;
};

// ========== HTTP 路由处理 ==========

// GET 请求处理器：获取数字人列表
// Get digital human list
export const GET = async (request) => {
  try {
    const searchParams = request.nextUrl.searchParams;
    const inferenceMode = searchParams.get("inferenceMode")
      ? parseInt(searchParams.get("inferenceMode"), 10)
      : undefined;
    const fetchMode = searchParams.get("fetchMode")
      ? parseInt(searchParams.get("fetchMode"), 10)
      : undefined;
    const offset = searchParams.get("offset")
      ? parseInt(searchParams.get("offset"), 10)
      : 0;
    const limit = searchParams.get("limit")
      ? parseInt(searchParams.get("limit"), 10)
      : 20;

    const result = await getDigitalHumanList({
      inferenceMode,
      fetchMode,
      offset,
      limit,
    });

    return NextResponse.json(result);
  } catch (error) {
    console.error("Failed to get digital human list:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 }
    );
  }
};
