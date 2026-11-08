// ZEGO Express Web SDK —— AI 降噪快速接入示例
//
// 主链路：创建引擎 → 登录房间 → 本地推流 → 开启/关闭 AI 降噪（enableAiDenoise）
//
// 相关官方文档：
// - AI 降噪：https://doc-zh.zego.im/real-time-video-web/audio/scenario-based-ai-noise-reduction
// - 快速开始（实现视频通话）：https://doc-zh.zego.im/real-time-video-web/quick-start/implementing-video-call
//
// 注意：AppID / Server 地址 / Token 均从页面输入，代码中不保存任何凭据。

// 第一步：引入 SDK 与 AI 降噪模块。
// AiDenoise 模块必须在 new ZegoExpressEngine 之前通过 ZegoExpressEngine.use 注册。
import { ZegoExpressEngine } from "zego-express-engine-webrtc";
import { AiDenoise } from "zego-express-engine-webrtc/aidenoise";

ZegoExpressEngine.use(AiDenoise);

// ========== 页面元素 ==========
const joinBtn = document.querySelector("#join-btn");
const leaveBtn = document.querySelector("#leave-btn");
const ansToggle = document.querySelector("#ans-toggle");
const ansState = document.querySelector("#ans-state");
const logBox = document.querySelector("#log");

// ========== 全局状态 ==========
let zg = null; // ZegoExpressEngine 实例
let localStream = null; // createZegoStream 创建的本地流
let publishStreamID = ""; // 本端推流的 streamID
let joinedRoomID = ""; // 已登录的房间 ID

function log(message) {
  const time = new Date().toLocaleTimeString();
  logBox.textContent = `[${time}] ${message}\n` + logBox.textContent;
  console.log(message);
}

function setAnsUI(enabled) {
  ansState.textContent = enabled ? "已开启" : "已关闭";
  ansState.className = "ans-state " + (enabled ? "on" : "off");
}

// ========== 登录房间并推流 ==========
joinBtn.addEventListener("click", async () => {
  // 1. 读取页面配置：AppID、Server 地址、RoomID、UserID、Token
  const appID = Number(document.querySelector("#app-id").value);
  const server = document.querySelector("#server").value.trim();
  const roomID = document.querySelector("#room-id").value.trim();
  const userID = document.querySelector("#user-id").value.trim();
  const token = document.querySelector("#token").value.trim();

  if (!appID || !roomID || !userID || !token) {
    log("请先填写 AppID、RoomID、UserID 和 Token（AppID/Token 从 ZEGO 控制台获取）。");
    return;
  }

  joinBtn.disabled = true;
  try {
    // 2. 创建引擎（AppID 为 Number 类型；SDK 3.7.0 及以上版本 Server 地址可传空字符串）
    zg = new ZegoExpressEngine(appID, server);

    // 3. 注册回调：房间状态、远端流变化
    zg.on("roomStateChanged", (roomID, reason, errorCode) => {
      log(`房间状态变更：${roomID} ${reason} ${errorCode}`);
      if (reason === "LOGINED") {
        log("登录房间成功，只有房间状态为连接成功时才能推流、拉流。");
      } else if (reason === "LOGIN_FAILED") {
        log(`登录房间失败，错误码：${errorCode}（请检查 AppID / Token 是否有效）。`);
      }
    });

    zg.on("roomStreamUpdate", async (roomID, updateType, streamList) => {
      if (updateType === "ADD") {
        // 远端流新增：拉流播放（收听端在另一个标签页/设备上听 AI 降噪开/关的差异）
        for (const stream of streamList) {
          log(`远端流新增：${stream.streamID}，开始拉流。`);
          const remoteStream = await zg.startPlayingStream(stream.streamID);
          const remoteView = zg.createRemoteStreamView(remoteStream);
          remoteView.play("remote-video", { enableAutoplayDialog: true });
        }
      } else if (updateType === "DELETE") {
        for (const stream of streamList) {
          log(`远端流删除：${stream.streamID}，停止拉流。`);
          zg.stopPlayingStream(stream.streamID);
        }
      }
    });

    // 4. 通话前检测浏览器兼容性
    const capability = await zg.checkSystemRequirements();
    log(`浏览器兼容性检测结果：${JSON.stringify(capability)}`);
    if (!capability.webRTC) {
      log("当前浏览器不支持 WebRTC，请更换最新版 Chrome 浏览器后重试。");
      await cleanup();
      joinBtn.disabled = false;
      return;
    }

    // 5. 登录房间（userUpdate 为 true 才能收到 roomUserUpdate 回调）
    const loginResult = await zg.loginRoom(
      roomID,
      token,
      { userID, userName: userID },
      { userUpdate: true }
    );
    if (loginResult !== true) {
      log("登录房间失败：loginRoom 未返回成功，请检查 Token 是否过期。");
      await cleanup();
      joinBtn.disabled = false;
      return;
    }
    joinedRoomID = roomID;

    // 6. 创建本地流（默认采集摄像头与麦克风），并预览画面
    localStream = await zg.createZegoStream();
    localStream.playVideo(document.querySelector("#local-video"), { enableAutoplayDialog: true });

    // 7. 开始推流（streamID 需保证同一 AppID 下全局唯一）
    publishStreamID = `stream-${userID}-${Date.now()}`;
    zg.startPublishingStream(publishStreamID, localStream);
    log(`推流中：${publishStreamID}。现在可以切换「AI 降噪」开关进行对照测试。`);

    // 推流成功后允许切换 AI 降噪
    ansToggle.disabled = false;
    leaveBtn.disabled = false;
    setAnsUI(false);
  } catch (error) {
    // SDK 异常可能是 Error 或 ZegoServerResponse 对象，分别格式化
    const detail = error instanceof Error ? error.message : JSON.stringify(error);
    log(`出错：${detail}`);
    // 失败后恢复初始状态
    await cleanup();
    joinBtn.disabled = false;
  }
});

// ========== AI 降噪开关 ==========
// enableAiDenoise(localStream, enable)：推流前或推流中均可调用，对本端流实时生效。
ansToggle.addEventListener("change", async () => {
  if (!zg || !localStream) {
    ansToggle.checked = false;
    return;
  }
  const enable = ansToggle.checked;
  ansToggle.disabled = true;
  try {
    await zg.enableAiDenoise(localStream, enable);
    setAnsUI(enable);
    log(`AI 降噪已${enable ? "开启" : "关闭"}：enableAiDenoise(localStream, ${enable})。`);
  } catch (error) {
    // 常见错误码：1103081 当前浏览器不支持 AI 降噪；1103080 AI 降噪运行错误
    ansToggle.checked = !enable;
    const detail = error instanceof Error ? error.message : JSON.stringify(error);
    log(`AI 降噪切换失败：${detail}。建议使用最新版 Chrome/Edge 浏览器。`);
  } finally {
    ansToggle.disabled = false;
  }
});

// ========== 退出房间 ==========
async function cleanup() {
  ansToggle.disabled = true;
  ansToggle.checked = false;
  setAnsUI(false);
  leaveBtn.disabled = true;

  if (zg) {
    if (publishStreamID) {
      zg.stopPublishingStream(publishStreamID);
      publishStreamID = "";
    }
    if (localStream) {
      zg.destroyStream(localStream);
      localStream = null;
    }
    if (joinedRoomID) {
      zg.logoutRoom(joinedRoomID);
      joinedRoomID = "";
    }
    zg.destroyEngine();
    zg = null;
  }
  document.querySelector("#local-video").innerHTML = "";
  document.querySelector("#remote-video").innerHTML = "";
  log("已退出房间并销毁引擎。");
}

leaveBtn.addEventListener("click", async () => {
  await cleanup();
  joinBtn.disabled = false;
});
