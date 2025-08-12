# API

## ZegoUIKitPrebuiltLiveStreamingFragment

直播组件。您可以将此 Fragment 添加到项目中的任何 Activity 中，以集成直播功能。

#### newInstance

使用 AppSign 初始化直播配置。

```java
/**
 * @param appID    您可以在[ZEGO 控制台](https://console.zego.im/)中创建项目并获取appID。
 * @param appSign  您可以在[ZEGO 控制台](https://console.zego.im/)中创建项目并获取appSign。
 * @param userID   当前登录用户的ID。它可以是任何有效的字符串，通常，您可以使用您自己用户系统中的ID。
 * @param userName 当前登录用户的名称。它可以是任何有效的字符串，通常，您可以使用您自己用户系统中的名称。
 * @param liveID   直播的ID。此ID是当前直播的唯一标识符，因此您需要确保其唯一性。它可以是任何有效的字符串。提供相同liveID的用户将登录到同一个直播间。
 * @param config   用于初始化直播的配置。
 * @return
 */
public static ZegoUIKitPrebuiltLiveStreamingFragment newInstance(long appID, @NonNull String appSign, @NonNull String userID, @NonNull String userName, @NonNull String liveID, @NonNull ZegoUIKitPrebuiltLiveStreamingConfig config) 
```

#### newInstanceWithToken

使用 Token 初始化直播配置。

```java
/**
 * @param appID    您可以在 [ZEGO 控制台](https://console.zego.im/) 中创建项目并获取 AppID。
 * @param token    您可以在 [ZEGO 控制台](https://console.zego.im/) 中创建项目并获取 ServerSecret，然后通过您的服务器生成 Token，以避免泄露您的 AppSign。
 * @param userID   当前登录用户的 ID。它可以是任何有效的字符串，通常，您会使用您自己用户系统中的 ID。
 * @param userName 当前登录用户的名称。它可以是任何有效的字符串，通常，您会使用您自己用户系统中的名称。
 * @param liveID   直播的 ID。此 ID 是当前直播的唯一标识符，因此您需要确保其唯一性，它可以是任何有效的字符串，提供相同 liveID 的用户，将登录到同一个直播间。
 * @param config   用于初始化直播的配置。
 * @return
 */
public static ZegoUIKitPrebuiltLiveStreamingFragment newInstanceWithToken(long appID, @NonNull String token, @NonNull String userID, @NonNull String userName, @NonNull String liveID, @NonNull ZegoUIKitPrebuiltLiveStreamingConfig config);
```

#### addButtonToBottomMenuBar

将您的自定义按钮添加到底部菜单栏。当用户角色等于`role`时，将显示。

```java
/**
 *
 * @param viewList 准备添加的自定义的按钮列表。
 * @param role 准备把自定义按钮添加到哪个对应的角色去展示。
 */
public void addButtonToBottomMenuBar(List<View> viewList, ZegoLiveStreamingRole role);
```

## ZegoUIKitPrebuiltLiveStreamingService

### Common

连麦通用接口和事件，不包括 PK 相关接口和事件。

#### muteAllAudioVideo

静音所有音视频。如果您希望应用程序在切换到后台时停止音视频，可以使用此接口，然后在应用程序返回到前台时使用 `unMuteAllAudioVideo` 来恢复音视频。

- 函数原型：
  ```java
  public void muteAllAudioVideo();
  ```
- 示例：

  ```java
  ZegoUIKitPrebuiltLiveStreamingService.common.muteAllAudioVideo()
  ```

#### unMuteAllAudioVideo

这个函数与 `muteAllAudioVideo` 配合使用。

- 函数原型：
  ```java
  public void unMuteAllAudioVideo();
  ```
- 示例：

  ```java
  ZegoUIKitPrebuiltLiveStreamingService.common.unMuteAllAudioVideo()
  ```

#### showTopTips

用于在 `ZegoUIKitPrebuiltCallFragment` 上显示消息。

- 函数原型：
  ```java
   /**
    *  在顶部显示消息提示。 
    * @param message  消息提示内容。
    * @param green  消息提示颜色，支持绿色或者红色。
    */
  public void showTopTips(String message, boolean green);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.common.showTopTips(message, green)
  ```

#### sendInRoomMessage

向房间发送广播消息，已经登录相同房间的用户能收到消息，消息可靠，此消息将会显示在直播间左下角区域。除了接口回调返回以外，还可以使用`ZegoUIKitPrebuiltLiveStreamingService.common.events.addInRoomMessageReceivedListener` 来监听房间消息的发送和接收事件。

- 函数原型：
  ```java
  /**
   * 
   * @param message 房间内发送消息的内容。
   * @param listener  房间内发送消息的结果状态监听。
   */
  public void sendInRoomMessage(String message, ZegoInRoomMessageSendStateListener listener);
  ```
- 示例：
  ```java
  // 添加 Listenser 监听来自其他人的消息
  ZegoUIKitPrebuiltLiveStreamingService.common.events.addInRoomMessageReceivedListener(inRoomMessageListener)
    // 在需要的时候发送消息给其他人
  ZegoUIKitPrebuiltLiveStreamingService.common.sendInRoomMessage(message, listener)
  ```

#### sendBarrageMessage

发送房间内弹幕消息,一般用于房间内有大量消息收发，且不需要保证消息可靠性的场景，例如直播弹幕。除了接口回调返回以外，还可以使用`ZegoUIKitPrebuiltLiveStreamingService.common.events.addBarrageMessageListener` 来监听房间消息的发送和接收事件。

- 函数原型：
  ```java
  /**
   * 
   * @param message 房间内发送弹幕消息的内容。
   * @param listener  房间内发送弹幕消息的结果状态监听。
   */
  public void sendBarrageMessage(String roomID,String message, IZegoIMSendBarrageMessageCallback listener);
  ```
- 示例：
  ```java
  // 添加 Listenser 监听来自其他人的消息
  ZegoUIKitPrebuiltLiveStreamingService.common.events.addBarrageMessageListener(barrageMessageListener)
  // 在需要的时候发送消息给其他人
  ZegoUIKitPrebuiltLiveStreamingService.common.sendBarrageMessage(roomid,message, listener)
  ```


### PK
主播 PK 相关的接口和事件。



#### sendPKBattleRequest [1/2]

向 `anotherHostUserID` 发送连麦请求并透传自定义数据，接收者可以使用 `ZegoUIKitPrebuiltLiveStreamingService.pk.events.addPKListener` 来监听 PK 连麦事件。当收到 PK 连麦请求时，将触发 `onIncomingPKBattleRequestReceived` 事件。

- 函数原型：
  ```java
  /**
   * 
   * @param anotherHostUserID 参与 PK 的另一个主持人的 UserID。
   * @param timeout  超时时间。
   * @param customData  自定义的透传数据。
   * @param callback 发送邀请的结果监听。
   */
  public void sendPKBattleRequest(String anotherHostUserID, int timeout, String customData, UserRequestCallback callback); 
  ```

- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.sendPKBattleRequest(anotherHostUserID, timeout, customData, callback)
  ```



#### sendPKBattleRequest [2/2]

向 `anotherHostUserID` 发送连麦请求，接收者可以使用 `ZegoUIKitPrebuiltLiveStreamingService.pk.events.addPKListener` 来监听 PK 连麦事件。当收到 PK 连麦请求时，将触发 `onIncomingPKBattleRequestReceived` 事件。

- 函数原型：
  ```java
  /**
   * 
   * @param anotherHostUserID 参与 PK 的另一个主持人的 UserID。
   * @param callback 发送邀请的结果监听。
   */
  public void sendPKBattleRequest(String anotherHostUserID, UserRequestCallback callback);
  ```

- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.sendPKBattleRequest(anotherHostUserID, callback)
  ```

#### startPKBattleWith

向另一个主播发送 PK 连麦请求后，如果监听到对方同意 PK，则可以调用此接口开始 PK。

- 函数原型：
  ```java
  /**
   * @param anotherHostLiveID  参与 PK 的另一个主播的 LiveID。
   * @param anotherHostUserID   参与 PK 的另一个主播的 UserID。
   * @param anotherHostName  参与 PK 的另一个主播的名字。
   */
  public void startPKBattleWith(String anotherHostLiveID, String anotherHostUserID, String anotherHostName);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.startPKBattleWith(anotherHostLiveID, anotherHostUserID, anotherHostName)
  ```

#### stopPKBattle

停止 PK。

- 函数原型：
  ```java
  public void stopPKBattle();
  ```

- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.stopPKBattle()
  ```



#### cancelPKBattleRequest [1/2]

在您调用 `sendPKBattleRequest` 后，您可以使用此方法来取消 PK 连麦请求。

- 函数原型：
  ```java
  /**
   * @param callback 取消邀请的结果监听。
   */
  public void cancelPKBattleRequest(UserRequestCallback callback);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.cancelPKBattleRequest(callback)
  ```



#### cancelPKBattleRequest [2/2]

在您调用 `sendPKBattleRequest` 后，您可以使用此方法来取消 PK 连麦请求，并透传自定义数据。

- 函数原型：
  ```java
  /**
   * @param customData 自定义的透传数据。
   * @param callback 取消邀请的结果监听。
   */
  public void cancelPKBattleRequest(String customData, UserRequestCallback callback);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.cancelPKBattleRequest(customData, callback)
  ```

#### acceptIncomingPKBattleRequest

当收到一个 PK 连麦请求时，您可以使用此方法进行接受。

- 函数原型：
  ```java
  /**
   * @param requestID PK 邀请的 ID，表示同意哪一个 PK 邀请。
   * @param anotherHostLiveID  参与 PK 的另一个主播的 Live ID。
   * @param anotherHostUser  参与 PK 的另一个主播的信息。
   */
  public void acceptIncomingPKBattleRequest(String requestID, String anotherHostLiveID, ZegoUIKitUser anotherHostUser);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.acceptIncomingPKBattleRequest(requestID, anotherHostLiveID, anotherHostUser)
  ```

#### rejectPKBattleStartRequest

当收到一个 PK 连麦请求时，您可以使用此方法拒绝接受连麦请求。

- 函数原型：

  ```java
  /**
   * @param requestID PK 邀请的 ID，表示拒绝哪一个 PK 邀请。
   */
  void rejectPKBattleStartRequest(String requestID);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.rejectPKBattleStartRequest(requestID)
  ```

#### getPKInfo

获取当前的 PK 信息。如果您不在 PK 中，将返回 null。

- 函数原型：
  ```java
  public PKInfo getPKInfo();
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.getPKInfo()
  ```

#### getSendPKStartRequest

在您调用 `sendPKBattleRequest` 后，您可以使用此方法来获取请求信息。

- 函数原型：

  ```java
  public PKRequest getSendPKStartRequest();
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.getSendPKStartRequest()
  ```

#### muteAnotherHostAudio

在 PK 中，让对方主播静音。

- 函数原型：

  ```java
  /**
   * @param mute 是否把另外一个人的混流声音关掉。
   * @param callback 操作结果。
   */
  public void muteAnotherHostAudio(boolean mute, ZegoUIKitCallback callback);
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.muteAnotherHostAudio(mute, callback)
  ```

#### isAnotherHostMuted

在 PK 中，对方主播是否被静音。

- 函数原型：

  ```java
  public boolean isAnotherHostMuted();
  ```
- 示例：
  ```java
  ZegoUIKitPrebuiltLiveStreamingService.pk.isAnotherHostMuted()
  ```
