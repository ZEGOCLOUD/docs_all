## 1 功能简介

ZEGO 依托于在音视频分发领域多年的经验，孵化出实时有序数据功能。实时有序数据具有低延迟，高频，有序，可订阅等特点。开发者可用于远程控制、音视频分发加速等场景。
 
### 1.1 功能特征

- 实时性：国内延迟可低至 25 ms。
- 高频：200 次/秒 的发送频率，每次发送 4 KB 数据量。
- 有序：发送端到接收端，有序传输数据。
- 全球覆盖：覆盖全球 200 多个国家和地区，为全球区域提供实时信令能力。
- 可订阅：一端推送，多端可订阅接收消息。

### 1.2 适用场景

开发者可以基于以上特征，将此功能应用于如下场景中：

#### 远程控制

国内时延低至 25 ms，解决远程控制时延问题，提升远程控制体验。

#### 音视频分发加速

架构在 MSDN 上的实时有序数据，可用于音视频传输，提高音视频实时性。


### 1.3 功能架构

实时有序数据功能的实现架构如下：
![/Pics/Common/ZegoExpressEngine/ZegoRealTimeSequentialData.png](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/ZegoRealTimeSequentialData.png)

1. 发送端开始推流，并在该流上附加实时有序数据；
2. 通过 ZEGO MSDN 网络，将流信息和有序数据分发到接收端；
3. 接收端开始拉流，并订阅该数据。


## 2 前提条件

在实现实时有序数据功能之前，请确保：

- 已在项目中集成 ZEGO Express SDK，详情请参考 [快速开始 - 集成](!ExpressVideoSDK-Integration/SDK_Integration)。
- 已在 [ZEGO 控制台](https://console.zego.im) 创建项目，并申请有效的 AppID 和 AppSign，详情请参考 [控制台 - 项目管理](#12107)。

















