## 概述

语聊房是指在线语音连麦虚拟房间。在本方案中，每个房间设有若干个麦位，主播在麦上聊天，同时把整个房间直播出去，其他观众可以进入房间收听。主播也可邀请观众上麦互动，但是观众之间不能互相邀请上麦进行互动。

ZEGO 语聊房解决方案预设 5 个麦位（包括主播麦位），观众人数在客户端侧没有做限制（但会受限于 ZEGO Express SDK 和 ZIM SDK）。

## 方案架构

本方案房间内业务的整体架构如下图所示。由于业务后台仅管理房间列表，不涉及房间内业务，因此没有在下图中体现。房间内通过 ZIM SDK 进行消息的可靠传输，实现麦位管理等，通过 ZEGO Express SDK 实现推拉流管理。   

![/Pics/GoEnjoy/GoChatHouse/iOS/internal_buiness_architect.png](https://doc-media.zego.im/sdk-doc/Pics/GoEnjoy/GoChatHouse/iOS/internal_buiness_architect.png)

## 体验 App 源码

ZEGO 针对语聊房场景提供了 [体验 App 源码](!ChatHouse-DownloadDemo)，以供开发者进一步了解 ZEGO 语聊房方案。
