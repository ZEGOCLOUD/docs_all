# 设置退出确认框


互动直播 UIKit（Live Streaming Kit）默认在用户点击“结束直播”按钮后就立即结束直播。但也支持添加一个直播结束确认的对话框，以二次确认用户是否要离开直播。

## 实现流程

您可以使用 `confirmDialogInfo` 配置。在配置 `confirmDialogInfo` 参数之后，互动直播 UIKit 将在结束直播之前弹出一个默认样式的二次确认对话框，显示预设的直播确认信息。

效果将如下所示：

<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/live/live_confirm.gif" /></Frame>

参考代码如下：

:::if{props.platform=undefined}
<CodeGroup>
```java title="Java"
public class LiveActivity extends AppCompatActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_live);

    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "userID";
    String userName = "userName";
    String liveID = "testLiveID";

    // 在此处修改您的自定义配置。
    ZegoUIKitPrebuiltLiveStreamingConfig config;
    if (isHost) {
        config = ZegoUIKitPrebuiltLiveStreamingConfig.host();
    } else {
        config = ZegoUIKitPrebuiltLiveStreamingConfig.audience();
    }
    ZegoDialogInfo confirmDialogInfo = new ZegoDialogInfo();
    confirmDialogInfo.title= "Leave confirm";
    confirmDialogInfo.message= "Do you want to leave?";
    confirmDialogInfo.cancelButtonName= "Cancel";
    confirmDialogInfo.confirmButtonName= "Confirm";
    config.confirmDialogInfo = confirmDialogInfo;

    ZegoUIKitPrebuiltLiveStreamingFragment fragment = ZegoUIKitPrebuiltLiveStreamingFragment
            .newInstance(appID, appSign, userID, userName, liveID, config);

    getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
  }
}
```
```kotlin title="Kotlin"
class LiveActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_live)
        val appID: Long = YourAppID
        val appSign: String = YourAppSign
        val userID = "userID"
        val userName = "userName"
        val liveID = "testLiveID"

        // 在此处修改您的自定义配置。
        val config: ZegoUIKitPrebuiltLiveStreamingConfig = if (isHost) {
            ZegoUIKitPrebuiltLiveStreamingConfig.host()
        } else {
            ZegoUIKitPrebuiltLiveStreamingConfig.audience()
        }
        val confirmDialogInfo = ZegoDialogInfo()
        confirmDialogInfo.title = "Leave confirm"
        confirmDialogInfo.message = "Do you want to leave?"
        confirmDialogInfo.cancelButtonName = "Cancel"
        confirmDialogInfo.confirmButtonName = "Confirm"
        config.confirmDialogInfo = confirmDialogInfo
        val fragment = ZegoUIKitPrebuiltLiveStreamingFragment
            .newInstance(appID, appSign, userID, userName, liveID, config)
        supportFragmentManager
            .beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
```swift
class ViewController: UIViewController {
    
    let selfUserID: String = "userID" 
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID
    let yourAppSign: String = YourAppSign
    let liveID: String = "testLiveID"
    
    @IBAction func makeNewLive(_ sender: Any) {
        
        // 在这里修改您的自定义配置。
        let config: ZegoUIKitPrebuiltLiveStreamingConfig = ZegoUIKitPrebuiltLiveStreamingConfig.host()

        let confirmDialogInfo = ZegoConfirmDialogInfo()
        confirmDialogInfo.title= "Leave confirm";
        confirmDialogInfo.message= "Do you want to leave?";
        confirmDialogInfo.cancelButtonName= "Cancel";
        confirmDialogInfo.confirmButtonName= "Confirm";
        config.confirmDialogInfo = confirmDialogInfo
        
        let liveVC = ZegoUIKitPrebuiltLiveStreamingVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: self.selfUserName ?? "", liveID: liveID, config: config)
        
        liveVC.modalPresentationStyle = .fullScreen
        self.present(liveVC, animated: true, completion: nil)
    }
}
```
:::


如果您想要监听离开事件，互动直播 UIKit 提供了一个 `onLeaveLiveStreaming`回调 ，当直播结束时将自动触发 `onLeaveLiveStreaming`。当然，您也可以在 `onLeaveLiveStreaming` 中实现自定义的业务逻辑。
