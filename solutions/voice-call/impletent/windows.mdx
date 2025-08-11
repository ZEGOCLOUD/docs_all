# 功能实现流程
- - - 

## 功能说明
实时语音场景的典型之一是，同一房间中的成员进行实时语音对话。

## 流程说明
以 2 人间的实时语音为例，主要流程如下：

<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/iOS/Applications-InstantAudio/5-InstantAudio-Implementation/flow.png" /></Frame>

> 请注意：上面流程中以 2 名房间成员间的实时语音为例，实际上 **Zego SDK 支持多人实时语音**。建议开发者按需设计。

详细步骤如下：

1. 初始化 SDK：SDK 在初始化后才可以进行登录和推拉流操作。
2. 设置回调：包括房间状态回调、推流回调、拉流回调。
3. 登录房间。
4. 推音频流：把本地的音频实时推送出去。
5. 拉音频流：播放房间内其它用户的音频。
6. 退出房间：退出房间需要停止推流、停止拉流，然后再登出房间

# 代码说明
## 初始化SDK

```c++
// 头文件包含
#include "ZegoExpressSDK.h"

ZegoEngineProfile profile;
// AppID 和 AppSign 由 ZEGO 分配给各 App；其中，为了安全考虑，建议将 AppSign 存储在 App 的业务后台，需要使用时从后台获取
profile.appID = appID;
profile.appSign = appSign;
profile.scenario = ZegoScenario::ZEGO_SCENARIO_GENERAL;
// 创建引擎实例
auto engine = ZegoExpressSDK::createEngine(profile, nullptr);
```
## 设置回调

用户可以通过设置回调接口，对关心的事件进行处理，以下是常用回调：

```c++
// 基本事件回调，需要继承自IZegoEventHandler
// SDK调用错误回调
virtual void onDebugError(int, const std::string&, const std::string&);
// 房间状态回调，登录，重连等结果信息
virtual void onRoomStateUpdate(const std::string&, ZegoRoomState, int, const std::string&);
// 房间用户更新回调，用户增加减少都会回调
virtual void onRoomUserUpdate(const std::string&, ZegoUpdateType, const std::vector<ZegoUser>&);
// 房间流变化回调，其他用户推流，停止推流都会回调
virtual void onRoomStreamUpdate(const std::string&, ZegoUpdateType, const std::vector<ZegoStream>&);
// 推流回调
virtual void onPublisherStateUpdate(const std::string&, ZegoPublisherState, int, const std::string&);
// 播放回调
virtual void onPlayerStateUpdate(const std::string&, ZegoPlayerState, int, const std::string&);
// 远端摄像头状态变化回调
virtual void onRemoteCameraStateUpdate(const std::string&, ZegoRemoteDeviceState);
// 远端麦克风状态变化回调
virtual void onRemoteMicStateUpdate(const std::string&, ZegoRemoteDeviceState);
```
以下是继承回调处理的用户类：
```
// 如果需要设置回调方法，需要继承相应的回调基类，如IZegoEventHandler
class ZegoEventHandler : public IZegoEventHandler
{
protected:
    virtual void onDebugError(int errorCode, const std::string& funcName, const std::string& info) override;
    virtual void onRoomUserUpdate(const std::string& roomID, ZegoUpdateType updateType, const std::vector<ZegoUser>& userList) override;
    virtual void onRoomStateUpdate(const std::string& roomID, ZegoRoomState state, int errorCode, const std::string& extendedData) override;
    virtual void onRoomStreamUpdate(const std::string& roomID, ZegoUpdateType updateType, const std::vector<ZegoStream>& streamList) override;
    virtual void onPublisherStateUpdate(const std::string& streamID, ZegoPublisherState state, int errorCode, const std::string& extendedData) override;
    virtual void onPublisherQualityUpdate(const std::string& streamID, const ZegoPublishStreamQuality& quality) override;
    virtual void onPlayerStateUpdate(const std::string& streamID, ZegoPlayerState state, int errorCode, const std::string& extendedData) override;
    virtual void onPlayerQualityUpdate(const std::string& streamID, const ZegoPlayStreamQuality& quality) override;    
    virtual void onRemoteCameraStateUpdate(const std::string& /*streamID*/, ZegoRemoteDeviceState /*state*/);
    virtual void onRemoteMicStateUpdate(const std::string& /*streamID*/, ZegoRemoteDeviceState /*state*/);
}；
```
以下是设置回调的代码块：
```
// 在初始化前，绑定事件
auto eventHandler = std::make_shared<ZegoEventHandler>();
auto engine = ZegoExpressSDK::getEngine();
// 设置回调
engine->setEventHandler(eventHandler);
```

## 登录房间

用户开始实时语音通话前必须加入房间。

> 注意：房间 ID 只支持最大长度为 128 字节的字符串，格式仅支持数字，英文字符 和 '~', '!', '@', '#', '$', '%', '^', '&', '\*', '(', ')', '_', '+', '=', '-', '`', ';', '’', ',', '.', '\<', '>', '/', '' 特殊字符。

```c++
// 设置用户ID及用户名，不同用户ID不得重复
ZegoUser zgUser("12333", "张三");
auto engine = ZegoExpressSDK::getEngine();
// 房间配置，最大人数设置maxMemberCount，是否接受状态通知设置isUserStatusNotify
ZegoRoomConfig roomConfig;
roomConfig.maxMemberCount = 10;
roomConfig.isUserStatusNotify = true;
// 登录房间
engine->loginRoom("room_unique_123", zgUser, roomConfig);

```

## 开始推音频流

登录房间成功后可推音视频流。开发者可调用 `startPublishingStream` 进行推流，如果不需要继续推流，请调用 `stopPublishingStream` 停止推流。

> 注意：streamID 只支持长度不超过 256 的字符串，需要在整个 AppID 内全局唯一，若出现在同一个 AppID 内，不同的用户各推了一条流且流名相同，将会导致后推流的用户推流失败。不可以包含 URL 关键字，否则推拉流失败。格式仅支持数字、英文字符和 "-"、"_"。

```c++
// 推流，如果不需要推视频流，可以使用mutePublishStreamVideo禁用视频流
auto engine = ZegoExpressSDK::getEngine();	
engine->startPublishingStream("Stream_ID_123");
engine->mutePublishStreamVideo(false);

// 停止推流
engine->stopPublishingStream();
```



## 播放音频流

登录房间成功后可播放直播音频流。开发者可调用 `startPlayingStream` 进行拉流，如果不需要继续拉流，请调用 `stopPlayingStream` 停止拉流。

> 注意：streamID 只支持长度不超过 256 的字符串。不可以包含 URL 关键字，否则推拉流失败。格式仅支持仅支持数字、英文字符和 "-"、"_"。

```c++
// 播放音频流
auto engine = ZegoExpressSDK::getEngine();
engine->startPlayingStream(streamID, &canvas);

// 停止拉流
engine->stopPlayingStream(streamID);
```



## 结束语音交流

音频通话结束后的操作主要是登出房间、停止推流、停止拉流、清理视图或数据等，视业务需求情况来判断是否需要释放 SDK。

```c++
// 结束语音交流
auto engine = ZegoExpressSDK::getEngine();
// 停止拉流
engine->stopPlayingStream(streamID);
// 停止推流
engine->stopPublishingStream();
// 退出房间
engine->logoutRoom("Room_ID_123");

// 如果不需要再使用SDK内容，可以销毁SDK
ZegoExpressSDK::destroyEngine(engine);
```
