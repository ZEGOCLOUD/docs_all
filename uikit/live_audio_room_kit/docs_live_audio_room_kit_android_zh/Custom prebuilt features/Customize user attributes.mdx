# 自定义用户属性

- - -

**语聊房 UIKit（Live Audio Room Kit）** 支持自定义用户属性。用户属性（userInRoomAttributes）是键值对格式（key-value），用于设置用户等级并可被房间内其他用户获取。

## 实现流程

在您成功自定义用户属性后（或房间内的参与者完成自定义后），您（或房间内的参与者）将通过 `onUserCountOrPropertyChanged` 回调接收通知，您自定义的用户属性将在此回调中返回。

<Note title="说明">

- 对于单个用户，所有键值对的总和必须在 100 字节以内，最多可以配置 20 对。
- 每个键必须在 8 字节以内。
- 每个值必须在 64 字节以内。
</Note>

具体实现方式如下：

<CodeGroup>
```java title="Java"
ZegoUIKitPrebuiltLiveAudioRoomConfig config;
if (isHost) {
   config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
} else {
   config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
}
HashMap<String, String> userInRoomAttributes = new HashMap<>();
config.userInRoomAttributes = userInRoomAttributes;
ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config);
getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
```
```kotlin title="Kotlin"
val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
    ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
} else {
    ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
}
val userInRoomAttributes: HashMap<String, String> = HashMap()
config.userInRoomAttributes = userInRoomAttributes

val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
```
</CodeGroup>
