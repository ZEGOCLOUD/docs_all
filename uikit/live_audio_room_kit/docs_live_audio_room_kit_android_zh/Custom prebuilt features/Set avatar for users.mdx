# 设置用户头像

- - -

**语聊房 UIKit（Live Audio Room Kit）** 支持您通过传递图片的 URL（支持 PNG、JPG 格式）自定义用户头像，并与房间内参与者共享。

<Note title="说明">
URL 必须在 64 字节以内，如果超过 64 字节，将显示默认背景。
</Note>


## 实现流程

具体实现方式，请参考如下代码：

:::if{props.platform=undefined}
<CodeGroup>
```java title="Java"
ZegoUIKitPrebuiltLiveAudioRoomConfig config;
if (isHost) {
   config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
} else {
   config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
}
config.userAvatarUrl = YOUR IMAGE URL;
ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID,appSign, userID, userName, roomID, config);// 请从 ZEGO 控制台获取 AppID、Appsign。
getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, fragment).commitNow();
```
```kotlin title="Kotlin"
val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
     ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
} else {
     ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
}
config.userAvatarUrl = YOUR IMAGE URL

val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
```
</CodeGroup>
:::

:::if{props.platform="iOS"}
```swift
class ViewController: UIViewController {

    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID // 替换为您的 AppID，请从 ZEGO 控制台获取。
    let yourAppSign: String = "YourAppSign" // 替换为您的 AppSign，请从 ZEGO 控制台获取。
    let roomID: String = "YourRoomID" // 替换为您的 RoomID

    @IBAction func startLiveAudio(_ sender: Any) {

        // 在此处修改您的自定义配置。
        let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        config.userAvatarUrl = "https://www.zegocloud.com/_nuxt/img/discord_nav@2x.8739674.png" // 示例
        let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)
        liveAudioVC.modalPresentationStyle = .fullScreen
        self.present(liveAudioVC, animated: true, completion: nil)
    }
}
:::
