# ZEGO 产品和平台配置

本文件定义了 ZEGO 所有产品及其支持的平台，用于在创建示例代码时引导用户选择。

每个平台包含文档路径信息（相对于工作区目录），用于查找相关文档。客户端 API 路径是在文档路径下的一级目录，用于查找客户端 API 文档。

## 产品类别

### 互动核心产品

#### 实时音视频 (Video Call)

| 平台 | 语言 | 文档路径 | 客户端 API 路径 |
|-----|------|---------|----------------|
| iOS | Objective-C | `core_products/real-time-voice-video/zh/ios-oc` | `client-sdk/api-reference` |
| iOS | Swift | `core_products/real-time-voice-video/zh/ios-swift` | `client-sdk/api-reference` |
| Android | Java | `core_products/real-time-voice-video/zh/android-java` | `client-sdk/api-reference` |
| Android | Kotlin | `core_products/real-time-voice-video/zh/android-kotlin` | `client-sdk/api-reference` |
| macOS | Objective-C | `core_products/real-time-voice-video/zh/macos-oc` | `client-sdk/api-reference` |
| macOS | Swift | `core_products/real-time-voice-video/zh/macos-swift` | `client-sdk/api-reference` |
| macOS | C++ | `core_products/real-time-voice-video/zh/macos-cpp` | `client-sdk/api-reference` |
| Windows | C++ | `core_products/real-time-voice-video/zh/windows-cpp` | `client-sdk/api-reference` |
| Windows | C# | `core_products/real-time-voice-video/zh/windows-cs` | `client-sdk/api-reference` |
| HarmonyOS | ArkTS | `core_products/real-time-voice-video/zh/harmony-arkts` | - |
| Linux | C++ | `core_products/real-time-voice-video/zh/linux-cpp` | `client-sdk/api-reference` |
| Linux | Java | `core_products/real-time-voice-video/zh/linux-java` | `client-sdk/api-reference` |
| Web | JS | `core_products/real-time-voice-video/zh/web` | `client-sdk/api-reference` |
| 小程序 | JS | `core_products/real-time-voice-video/zh/mini-program` | `client-sdk/api-reference` |
| Flutter | Dart | `core_products/real-time-voice-video/zh/flutter-dart` | - |
| Electron | JS | `core_products/real-time-voice-video/zh/electron-js` | `client-sdk/api-reference` |
| Unreal Engine | C++ | `core_products/real-time-voice-video/zh/ue-cpp` | `client-sdk/api-reference` |
| Unity3D | C# | `core_products/real-time-voice-video/zh/u3d-cs` | `client-sdk/api-reference` |
| uni-app | JS | `core_products/real-time-voice-video/zh/uni-app` | - |
| React Native | JS | `core_products/real-time-voice-video/zh/rn-js` | - |
| Cocos Creator | TS | `core_products/real-time-voice-video/zh/cocos-creator-ts` | `client-sdk/api-reference` |
| Server | 服务端 API | `core_products/real-time-voice-video/zh/server` | - |

**说明**: 200ms低延迟，RTC通话/直播/会议，多人连麦；推拉流、混流/转码、CDN旁路；屏幕共享、水印/截图、录制；分层编码/超分/弱光/背景分割；AEC/ANS等3A与场景化AI降噪；范围音视频/空间音效；房间/消息/SEI信令、Token鉴权；QoS与网络检测、质量监控；跨平台互通。

#### 实时语音

| 平台 | 语言 | 文档路径 | 客户端 API 路径 |
|-----|------|---------|----------------|
| iOS | Objective-C | `core_products/real-time-voice/zh/ios-oc` | `client-sdk/api-reference` |
| iOS | Swift | `core_products/real-time-voice/zh/ios-swift` | `client-sdk/api-reference` |
| Android | Java | `core_products/real-time-voice/zh/android-java` | `client-sdk/api-reference` |
| Android | Kotlin | `core_products/real-time-voice/zh/android-kotlin` | `client-sdk/api-reference` |
| macOS | Objective-C | `core_products/real-time-voice/zh/macos-oc` | `client-sdk/api-reference` |
| macOS | Swift | `core_products/real-time-voice/zh/macos-swift` | `client-sdk/api-reference` |
| macOS | C++ | `core_products/real-time-voice/zh/macos-cpp` | `client-sdk/api-reference` |
| Windows | C++ | `core_products/real-time-voice/zh/windows-cpp` | `client-sdk/api-reference` |
| HarmonyOS | ArkTS | `core_products/real-time-voice/zh/harmony-arkts` | `client-sdk/api-reference` |
| Linux | C++ | `core_products/real-time-voice/zh/linux-cpp` | `client-sdk/api-reference` |
| Web | JS | `core_products/real-time-voice/zh/web` | `client-sdk/api-reference` |
| 小程序 | JS | `core_products/real-time-voice/zh/mini-program` | `client-sdk/api-reference` |
| Flutter | Dart | `core_products/real-time-voice/zh/flutter-dart` | `client-sdk/api-reference` |
| Electron | JS | `core_products/real-time-voice/zh/electron-js` | `client-sdk/api-reference` |
| Unreal Engine | C++ | `core_products/real-time-voice/zh/ue-cpp` | `client-sdk/api-reference` |
| Unity3D | C# | `core_products/real-time-voice/zh/u3d-cs` | `client-sdk/api-reference` |
| uni-app | JS | `core_products/real-time-voice/zh/uni-app` | `client-sdk/api-reference` |
| React Native | JS | `core_products/real-time-voice/zh/rn-js` | `client-sdk/api-reference` |
| Cocos Creator | TS | `core_products/real-time-voice/zh/cocos-creator-ts` | `client-sdk/api-reference` |
| Server | 服务端 API | `core_products/real-time-voice-video/zh/server` | - |

**说明**: 200ms低延迟，语音通话/语聊房/会议；AEC/ANS/AGC等3A，场景化AI降噪，变声/美声/混响，耳返；空间/范围音效；BGM/混音/本地播放；弱网抗丢包；设备/网络检测、质量洞察；旁路推CDN/混流；房间/消息信令；多端SDK

#### 超低延迟直播 (Live Streaming)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| iOS | Objective-C | `core_products/low-latency-live-streaming/zh/ios-oc` |
| iOS | Swift | `core_products/low-latency-live-streaming/zh/ios-swift` |
| Android | Java | `core_products/low-latency-live-streaming/zh/android-java` |
| Android | Kotlin | `core_products/low-latency-live-streaming/zh/android-kotlin` |
| macOS | Objective-C | `core_products/low-latency-live-streaming/zh/macos-oc` |
| macOS | Swift | `core_products/low-latency-live-streaming/zh/macos-swift` |
| macOS | C++ | `core_products/low-latency-live-streaming/zh/macos-cpp` |
| Windows | C++ | `core_products/low-latency-live-streaming/zh/windows-cpp` |
| Linux | C++ | `core_products/low-latency-live-streaming/zh/linux-cpp` |
| Web | JS | `core_products/low-latency-live-streaming/zh/web` |
| Flutter | Dart | `core_products/low-latency-live-streaming/zh/flutter-dart` |
| Electron | JS | `core_products/low-latency-live-streaming/zh/electron-js` |
| Unity3D | C# | `core_products/low-latency-live-streaming/zh/u3d-cs` |
| uni-app | JS | `core_products/low-latency-live-streaming/zh/uniapp` |
| React Native | JS | `core_products/low-latency-live-streaming/zh/rn-js` |
| All | 客户端 API | `core_products/low-latency-live-streaming/zh/client-api` |
| Server | 服务端 API | `core_products/real-time-voice-video/zh/server` |

**说明**: 超低延迟直播600–1000ms，毫秒级同步<400ms；抗弱网低卡顿，首帧秒开；4K60fps；OBS/RTMP推流、CDN分发，转码/混流/截帧/录制；千万并发，MSDN全球节点覆盖；调度与运维监控；安全合规与鉴权；多端播放与互通

#### 即时通讯 (ZIM)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Android | Java | `core_products/zim/zh/docs_zim_android_zh` |
| HarmonyOS | ArkTS | `core_products/zim/zh/docs_zim_harmonyos_zh` |
| Flutter | Dart | `core_products/zim/zh/docs_zim_flutter_zh` |
| iOS | Objective-C | `core_products/zim/zh/docs_zim_ios_zh` |
| macOS | Objective-C | `core_products/zim/zh/docs_zim_macos_zh` |
| React Native | TS | `core_products/zim/zh/docs_zim_rn_zh` |
| Unity3D | C# | `core_products/zim/zh/docs_zim_u3d_zh` |
| Web | TS | `core_products/zim/zh/docs_zim_web_zh` |
| Windows | C++ | `core_products/zim/zh/docs_zim_windows_zh` |
| 小程序 | TS | `core_products/zim/zh/docs_zim_miniprogram_zh` |
| uni-app x | UTS | `core_products/zim/zh/docs_zim_uniapp_x_zh` |
| uni-app | TS | `core_products/zim/zh/docs_zim_uniapp_zh` |
| All | 客户端 API | `core_products/zim/zh/client-api` |
| Server | 服务端 API | `core_products/zim/zh/docs_zim_server_zh` |

**说明**: 单聊/群聊/房间消息，会话/群组/用户管理；消息收发/撤回/已读回执/离线推送；信令与呼叫邀请；消息搜索/本地存储；内容审核与敏感词；服务端API与回调；多端SDK（Android/iOS/Web/Flutter/Unity/Windows/macOS）

### UIKits

#### 音视频通话 UIKit (Call Kit)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Android | Java | `uikit/callkit/docs_callkit_android_zh` |
| iOS | Swift | `uikit/callkit/docs_callkit_ios_zh` |
| Web | JS | `uikit/callkit/docs_callkit_web_zh` |
| 小程序 | JS | `uikit/callkit/docs_callkit_miniprogram_zh` |
| uni-app | JS | `uikit/callkit/docs_callkit_uniapp_zh` |

**说明**: 极速集成音视频通话/会议，预置呼叫UI与业务逻辑；1v1/多人、视频/语音、屏幕共享；呼叫邀请/超时/忙线/离线推送；设备/网络检测、弱网抗丢包；美颜与音效；记录与回放；多端SDK与示例，可自定义主题与组件

#### 互动直播 UIKit (Live Streaming Kit)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Android | Java | `uikit/live_streaming_kit/docs_live_streaming_kit_android_zh` |
| iOS | Swift | `uikit/live_streaming_kit/docs_live_streaming_kit_ios_zh` |
| Web | JS | `uikit/live_streaming_kit/docs_live_streaming_kit_web_zh` |

**说明**: 一站式开播/看播预置UI：推流、连麦互动、聊天/礼物/点赞、混流/转码、封面与标题、开播配置；低延迟与弱网优化；主播工具条、观众互动控件；录制/截帧；美颜/滤镜；权限鉴权；多端SDK与可定制扩展

#### 语聊房 UIKit (Live Audio Room Kit)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Android | Java | `uikit/live_audio_room_kit/docs_live_audio_room_kit_android_zh` |
| iOS | Swift | `uikit/live_audio_room_kit/docs_live_audio_room_kit_ios_zh` |

**说明**: 语聊房快速搭建：麦位管理（上/下麦、锁麦、禁言）、主持与管理员、邀请与连麦、文本聊天/礼物/表情、背景音乐/变声/混响、耳返/空间音效；弱网优化；房间管理与鉴权；多端SDK、可主题定制

#### IMKit

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Android | Java | `uikit/imkit/docs_in_app_chat_kit_android_zh` |
| iOS | Swift | `uikit/imkit/docs_in_app_chat_kit_ios_zh` |

**说明**: 即时通讯UI组件：会话列表、聊天窗口、消息输入框；文本/图片/语音/文件/表情/自定义消息；已读回执、撤回、引用、@、草稿；群聊/好友与用户资料；离线推送；本地缓存与搜索；多端SDK与可定制主题

### 互动扩展服务

#### 超级白板 (Super Board)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| iOS | Objective-C | `extended_services/super_board/zh/ios` |
| Android | Java | `extended_services/super_board/zh/android` |
| Web | JS | `extended_services/super_board/zh/web` |
| Flutter | Dart | `extended_services/super_board/zh/flutter` |
| Electron | JS | `extended_services/super_board/zh/electron` |
| React Native | JS | `extended_services/super_board/zh/rn` |
| 客户端 API | - | `extended_services/super_board/zh/client-api` |
| Server | 服务端 API | `extended_services/super_board/zh/server` |

**说明**: 多人实时白板：笔迹/橡皮/图形/文本/激光笔，图片/文档呈现（PPT/PDF），画布缩放/翻页/无限画布；对象选择/权限/多页；录制/回放；与RTC同步；房间与鉴权；跨平台SDK

#### 云端播放器 (Cloud Player)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| 文档 | - | `extended_services/cloud_player/zh/all` |
| Server | 服务端 API | `extended_services/cloud_player/zh/server` |

**说明**: 云端播放器：低延迟播放，弱网优化，自适应码率（ABR）；支持多协议/多格式输入（RTC/HLS/FLV等）；快进/拖动；水印/截图；权限鉴权与统计；多端接入

#### AI 美颜 (AI Effects)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| iOS | Objective-C | `extended_services/ai-effects/zh/ios-objc` |
| Android | Java | `extended_services/ai-effects/zh/android-java` |
| macOS | Objective-C | `extended_services/ai-effects/zh/macos-objc` |
| macOS | C | `extended_services/ai-effects/zh/macos-c` |
| Windows | C | `extended_services/ai-effects/zh/windows-c` |
| Flutter | Dart | `extended_services/ai-effects/zh/flutter-dart` |
| React Native | JS | `extended_services/ai-effects/zh/react-native-javascript` |

**说明**: AI 美颜/美型/滤镜，背景分割/抠像，贴纸/特效，手势/人像关键点；GPU加速，低功耗；素材管理与动态加载；无缝联动RTC渲染，多端SDK

#### 云端录制 (Cloud Recording)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| 文档 | - | `extended_services/cloud_recording/zh/all` |
| Server | 服务端 API | `extended_services/cloud_recording/zh/server` |

**说明**: 单流/混流录制，转码/合成，截帧/截图，存储与下载，任务管理/回调，媒体合并；结合CDN/旁路；稳定可靠，高并发

#### 本地服务端录制

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Linux | C++ | `extended_services/local_recording/zh/docs_local_recording_linux_cpp_zh` |
| Linux | Java | `extended_services/local_recording/zh/docs_local_recording_linux_java_zh` |

**说明**: 在自有服务器侧拉流录制，单流/混流、容器格式可选，断点续录、文件切片与上传；性能控制与监控；与调度/鉴权配合

#### 星图 (Analytics Dashboard)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| 文档 | - | `extended_services/analytics_dashboard/zh/all` |
| Server | 服务端 API | `extended_services/analytics_dashboard/zh/server` |

**说明**: 全链路质量监控/可视化与告警；通话KPI、设备/网络检测、呼叫详单；实时/历史报表，地域节点与并发容量洞察；QoS分析与问题定位

#### 云端实时语音识别 (Cloud Realtime ASR)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Server | - | `extended_services/cloud-realtime-asr/zh/server` |

**说明**: 云端实时语音识别：流式低延迟转写，中文与多语种，标点/时间戳，热词/词库与领域自定义；SDK/HTTP接入，回调与任务管理，可靠稳定

### AIGC

#### 实时互动 AI Agent (Conversation AI)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Server | - | `core_products/aiagent/zh/server` |
| Android | Java | `core_products/aiagent/zh/android` |
| iOS | Objective-C | `core_products/aiagent/zh/ios` |
| Web | JS | `core_products/aiagent/zh/web` |
| Flutter | Dart | `core_products/aiagent/zh/flutter` |

**说明**: 语音/视频多模态，ASR/TTS/LLM，对话管理与工具调用；场景模板；接入RTC/IM/白板；低延迟交互，Server API/SDK

#### 数字人 API (Digital Human AI)

| 平台 | 语言 | 文档路径 |
|-----|------|---------|
| Server | 服务端 | `core_products/digital-human/zh/server` |
| Android | Java | `core_products/digital-human/zh/android` |
| iOS | Objective-C | `core_products/digital-human/zh/ios` |
| Web | JS | `core_products/digital-human/zh/web` |

**说明**: 实时TTS驱动语音与唇形联动，表情/动作控制，剧本播报；流式渲染输出与背景合成；高拟真、低延迟；服务端API/SDK

---

**注意**: 文档搜索策略详见 `references/doc-path-guide.md`
