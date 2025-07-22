## 概述

ZEGO 为一起看场景提供了两种解决方案，分别为` ZEGO 影视资源方案` 和 `自定义影视资源方案`。` ZEGO 影视资源方案`是由 ZEGO 提供一站式的影视资源播放能力。`自定义影视资源方案`是指使用您的影视资源，ZEGO 提供播放与进度同步能力。
 
不论是哪种方案，您都可以基于 ZegoAccurateSyncMediaPlayer SDK 和 Zego Express SDK ，分别从客户端和服务端实现主持人播放影片，观众在客户端同步影片进度。

## 架构图

### 客户端为主持人

当房间内的一名用户（客户端）作为主持人，其余房间内用户作为观众时，主持人可同步自己的播放状态给观众端，并主动让所有观众向自己的进度同步，或观众可以主动让自己的视频进度向主持人对齐，以达到同步观看的效果，方案架构图如下：

![/Pics/iOS/ZegoCopyrightedVideo/Client_Architecture.png](https://doc-media.zego.im/sdk-doc/Pics/iOS/ZegoCopyrightedVideo/Client_Architecture.png)

### 服务端为主持人

当业务服务端作为房间内主持人，房内用户均为观众时，服务端播放视频，观众端可以向服务器端同步进度。开发者通过服务器端 API 统一同步当前播放视频的状态与进度。

![/Pics/iOS/ZegoCopyrightedVideo/Sever_Architecture.png](https://doc-media.zego.im/sdk-doc/Pics/iOS/ZegoCopyrightedVideo/Sever_Architecture.png)

