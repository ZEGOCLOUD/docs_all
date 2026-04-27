import { NextResponse } from "next/server";
import crypto from "crypto";
import { createCipheriv } from "crypto";

export const runtime = "nodejs";

// CORS 头配置（测试环境，不做跨域限制）
// Configure CORS headers for testing (no cross-origin restrictions)
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

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

// 创建数字人视频流任务
// Create digital human video stream task
const createStreamTask = async (params) => {
  const data = await post(
    "CreateDigitalHumanStreamTask",
    {
      DigitalHumanConfig: { DigitalHumanId: params.digitalHumanId },
      RTCConfig: { RoomId: params.roomId, StreamId: params.streamId },
      ExtraConfig: { OutputMode: params.outputMode ?? 1 },
    }
  );
  return data.TaskId;
};

// 通过文本驱动数字人播报
// Drive digital human broadcast by text
const driveByText = async (params) => {
  await post(
    "DriveByText",
    {
      TaskId: params.taskId,
      Text: params.text,
      InterruptMode: 1,
      TTSConfig: {
        TimbreId: params.timbreId,
        SpeechRate: 0,
        PitchRate: 0,
        Volume: 50,
      },
    }
  );
};

// 停止数字人视频流任务
// Stop digital human video stream task
const stopStreamTask = async (params) => {
  await post(
    "StopDigitalHumanStreamTask",
    { TaskId: params.taskId }
  );
};

// 获取数字人渲染信息（Android/iOS 需要使用素材包下载地址）
// Get digital human render info (Android/iOS need the asset package download URL)
const getDigitalHumanRenderInfo = async (params) => {
  const data = await post(
    "GetDigitalHumanRenderInfo",
    { DigitalHumanId: params.digitalHumanId }
  );
  return {
    clientInferencePackageUrl: data.ClientInferencePackageUrl,
    isSupportSmallImageMode: data.IsSupportSmallImageMode,
  };
};

// ========== Broadcast 管理逻辑 ==========

const globalState = globalThis;

const toNumber = (value, fallback) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

// 获取服务器配置信息
// Get server configuration
const getServerConfig = () => {
  const appId = toNumber(process.env.APP_ID, 0);
  const serverSecret = process.env.SERVER_SECRET || "";
  const tokenExpireSeconds = toNumber(process.env.TOKEN_EXPIRE_SECONDS, 3600);

  if (!appId) {
    throw new Error("APP_ID not configured");
  }
  if (!serverSecret) {
    throw new Error("SERVER_SECRET not configured");
  }

  return { appId, serverSecret, tokenExpireSeconds };
};

export const getBroadcastList = () => globalState.__DH_BROADCASTS__;

// 开始播报任务
// Start broadcast task
const startBroadcast = async (options) => {
  // 初始化全局状态
  // Initialize global state
  if (!globalState.__DH_BROADCASTS__) {
    globalState.__DH_BROADCASTS__ = {};
  }

  const config = getServerConfig();

  const broadcastIndex = options?.broadcastIndex ?? 0;
  const digitalHumanId = options?.digitalHumanId;
  const timbreId = options?.timbreId;
  const roomId = options?.roomId;
  const streamId = options?.streamId;
  const outputMode = options?.outputMode ?? 1;  // 1=Web模式, 2=Mobile模式
  const textPool = options?.textPool && options.textPool.length > 0
    ? options.textPool
    : [];

  // 验证必需参数
  // Validate required parameters
  if (!digitalHumanId) {
    throw new Error("Digital human ID not configured, please pass via parameter");
  }
  if (!timbreId) {
    throw new Error("Timbre ID not configured, please pass via parameter");
  }
  if (!roomId) {
    throw new Error("Room ID not configured, please pass via parameter");
  }
  if (!streamId) {
    throw new Error("Stream ID not configured, please pass via parameter");
  }

  // 如果已存在该索引的播报任务，先停止旧任务
  // If a broadcast task with this index exists, stop the old task first
  if (globalState.__DH_BROADCASTS__ && globalState.__DH_BROADCASTS__[broadcastIndex]) {
    await stopBroadcast(broadcastIndex);
  }

  // 调用 ZEGO 数字人 API 创建新的播报任务
  // Call ZEGO Digital Human API to create a new broadcast task
  const taskId = await createStreamTask({
    appId: config.appId,
    serverSecret: config.serverSecret,
    digitalHumanId,
    roomId,
    streamId,
    outputMode,
  });

  // 获取数字人渲染信息（Android/iOS 端需要）
  // Get digital human render info (required by Android/iOS)
  const renderInfo = await getDigitalHumanRenderInfo({ digitalHumanId });

  // 单次驱动播报的异步函数
  // Async function to drive broadcast once
  const driveOnce = async () => {
    try {
      const text = textPool[Math.floor(Math.random() * textPool.length)];
      await driveByText({
        appId: config.appId,
        serverSecret: config.serverSecret,
        taskId,
        text,
        timbreId,
      });
    } catch (error) {
      console.log(`Broadcast drive failed (task may have stopped):`, error.message);
    }
  };

  // 启动定时器，每隔 8 秒调用一次 driveOnce
  // Start a timer to call driveOnce every 8 seconds
  // 注意！！！这仅仅是演示，实际请根据业务需求自行实现
  // NOTE!!! This is just a demo, implement according to your business requirements
  const timer = setInterval(
    () => driveOnce().catch(() => {}),
    8000
  );

  // 延迟后首次驱动，给 ZEGO API 时间处理新创建的任务
  // Delay initial drive to give ZEGO API time to process the newly created task
  setTimeout(() => driveOnce(), 500);

  // 更新全局状态（生产环境建议使用数据库）
  // Update global state (recommend using database in production)
  globalState.__DH_BROADCASTS__[broadcastIndex] = {
    taskId,
    roomId,
    streamId,
    digitalHumanId,
    clientInferencePackageUrl: renderInfo.clientInferencePackageUrl,
    isSupportSmallImageMode: renderInfo.isSupportSmallImageMode,
    timer,
  };
};

// 停止播报任务
// Stop broadcast task
const stopBroadcast = async (broadcastIndex) => {
  const broadcastInfo = globalState.__DH_BROADCASTS__[broadcastIndex];
  if (!broadcastInfo) {
    console.log(`Broadcast task ${broadcastIndex} does not exist`);
    return;
  }

  // 立即清除定时器，防止后续调用
  // Immediately clear the timer to prevent future calls
  if (broadcastInfo.timer) {
    clearInterval(broadcastInfo.timer);
  }

  // 保存 taskId 后删除状态，防止重复调用
  // Save taskId then delete state to prevent duplicate calls
  const taskId = broadcastInfo.taskId;
  delete globalState.__DH_BROADCASTS__[broadcastIndex];

  // 调用 ZEGO 数字人 API 停止播报任务
  // Call ZEGO Digital Human API to stop the broadcast task
  try {
    await stopStreamTask({ taskId });
    console.log(`Stopped broadcast task ${taskId} successfully`);
  } catch (error) {
    console.log(`Error stopping broadcast task ${taskId} (may have already stopped):`, error.message);
  }
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

// GET /api/broadcast - 获取当前播报任务列表
// Get current broadcast task list
export const GET = async () => {
  const broadcastList = getBroadcastList() || {};

  // 过滤掉不可序列化的 timer 对象
  // Filter out non-serializable timer objects
  const sanitizedList = {};
  for (const [index, info] of Object.entries(broadcastList)) {
    sanitizedList[index] = {
      taskId: info.taskId,
      roomId: info.roomId,
      streamId: info.streamId,
      digitalHumanId: info.digitalHumanId,
      clientInferencePackageUrl: info.clientInferencePackageUrl,
      isSupportSmallImageMode: info.isSupportSmallImageMode,
      // timer 不可序列化，不返回
      // timer is not serializable, exclude from response
    };
  }

  return NextResponse.json({
    broadcastList: sanitizedList,
  }, {
    headers: corsHeaders,
  });
};

// POST /api/broadcast - 开始新的播报任务
// Start a new broadcast task
export const POST = async (request) => {
  try {
    const body = await request.json();
    console.log("[POST /api/broadcast] Starting broadcast with params:", {
      broadcastIndex: body.broadcastIndex,
      digitalHumanId: body.digitalHumanId,
      timbreId: body.timbreId,
      roomId: body.roomId,
      streamId: body.streamId,
      textPoolLength: body.textPool?.length,
    });
    await startBroadcast(body);
    return NextResponse.json({
      success: true,
      message: "Broadcast task started"
    }, {
      headers: corsHeaders,
    });
  } catch (error) {
    console.error("[POST /api/broadcast] Error:", error);
    return NextResponse.json({
      success: false,
      error: error.message
    }, {
      status: 400,
      headers: corsHeaders,
    });
  }
};

// DELETE /api/broadcast/:index - 停止指定的播报任务
// Stop the specified broadcast task
export const DELETE = async (request) => {
  try {
    const { searchParams } = new URL(request.url);
    const index = searchParams.get("index");

    if (index === null) {
      return NextResponse.json({
        success: false,
        error: "Missing index parameter"
      }, {
        status: 400,
        headers: corsHeaders,
      });
    }

    await stopBroadcast(Number(index));
    return NextResponse.json({
      success: true,
      message: `Broadcast task ${index} stopped`
    }, {
      headers: corsHeaders,
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, {
      status: 400,
      headers: corsHeaders,
    });
  }
};
