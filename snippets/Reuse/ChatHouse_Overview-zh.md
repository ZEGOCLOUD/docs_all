## 概述

语聊房是指在线语音连麦虚拟房间。在本方案中，每个房间设有若干个麦位，主播在麦上聊天，同时向房间内其他用户推流，其他听众可以进入房间收听。主播也可邀请听众上麦互动，但是听众之间不能互相邀请上麦进行互动。

ZEGO 语聊房解决方案预设 5 个麦位（包括主播麦位），听众人数在客户端侧没有做限制（但会受限于 ZEGO Express SDK 和 ZIM SDK）。

## 方案架构

本方案房间内业务的整体架构如下图所示。由于业务后台仅管理房间列表，不涉及房间内业务，因此没有在下图中体现。房间内通过 ZIM SDK 进行消息的可靠传输，实现麦位管理，通过 ZEGO Express SDK 实现推拉流管理。   

![/Pics/GoEnjoy/chathouse/Android/chat_house_internal_buiness_architec.png](https://doc-media.zego.im/sdk-doc/Pics/GoEnjoy/chathouse/Android/chat_house_internal_buiness_architec.png)

<div class="mk-warning">

在实现本方案过程中，如果您无需使用 `视频` 相关服务（`纯音频` 场景），请及时调用 Express SDK 的 [enableCamera](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~java_android~class~ZegoExpressEngine#enable-camera) 接口关闭摄像头（默认是开启的），以免产生视频使用时长，造成额外费用，给您带来不便。
</div>

## 体验 App 源码

ZEGO 针对语聊房场景提供了 [体验 App 源码](!ChatHouse-DownloadDemo)，以供开发者进一步了解 ZEGO 语聊房方案。

## 前提条件

- 已在 [ZEGO 控制台](https://console.zego.im) 创建项目，并申请有效的 AppID 和 AppSign，详情请参考 [控制台 - 项目管理 - 项目信息](#12107)。
- 已在项目中集成 ZEGO Express SDK，实现基本的实时音视频功能，详情请参考 [实时音视频 - 快速开始 - 集成](!ExpressVideoSDK-Integration/SDK_Integration)。
- 已在项目中集成 ZIM SDK，实现基本的消息收发功能，详情请参考 [即时通讯 - 快速开始 - 实现基本消息收发](!IM-Quick_Starts/Implementation_of_sending_and_receiving)。
- 已在 [ZEGO 控制台](https://console.zego.im) 开通即时通讯服务，详情请参考 [控制台 - 服务配置 - 即时通讯](#14994)。

















