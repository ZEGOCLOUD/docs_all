# 自定义菜单栏


互动直播 UIKit（Live Streaming Kit）支持自定义调整菜单栏的按钮，支持删除默认按钮或添加自定义按钮。

## 实现流程

通过配置 `bottomMenuBarConfig` 的以下参数实现自定义菜单栏：

- `hostButtons`：用于设置主播使用的按钮。
- `coHostButtons`：用于设置其他管理员（副主持人）使用的按钮。
- `audienceButtons`：用于设置观众使用的按钮。
- `menuBarButtonsMaxCount`：菜单栏可显示的最大按钮数。取值范围 [1-5]，默认值为 5。
- `showInRoomMessageButton`：是否显示消息按钮，默认显示。
:::if{props.platform=undefined}
- `showMemberButton`: 是否显示成员列表按钮，默认情况下显示。

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

    // 在此处修改您的自定义配置
    ZegoUIKitPrebuiltLiveStreamingConfig config;
    if (isHost) {
        config = ZegoUIKitPrebuiltLiveStreamingConfig.host();
    } else {
        config = ZegoUIKitPrebuiltLiveStreamingConfig.audience();
    }
    config.bottomMenuBarConfig.hostButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON);
    config.bottomMenuBarConfig.coHostButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON,ZegoMenuBarButtonName.COHOST_CONTROL_BUTTON);
    config.bottomMenuBarConfig.audienceButtons = Arrays.asList(ZegoMenuBarButtonName.COHOST_CONTROL_BUTTON);

    ZegoUIKitPrebuiltLiveStreamingFragment fragment = ZegoUIKitPrebuiltLiveStreamingFragment.newInstance(appID, appSign, userID, userName, liveID, config);

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

        // 在此处修改您的自定义配置
        val config: ZegoUIKitPrebuiltLiveStreamingConfig = if (isHost) {
            ZegoUIKitPrebuiltLiveStreamingConfig.host()
        } else {
            ZegoUIKitPrebuiltLiveStreamingConfig.audience()
        }
        config.bottomMenuBarConfig.hostButtons = Arrays.asList<Any>(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON)
        config.bottomMenuBarConfig.coHostButtons = Arrays.asList<Any>(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON, ZegoMenuBarButtonName.COHOST_CONTROL_BUTTON)
        config.bottomMenuBarConfig.audienceButtons =
            Arrays.asList<Any>(ZegoMenuBarButtonName.COHOST_CONTROL_BUTTON)

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
        let config: ZegoUIKitPrebuiltLiveStreamingConfig = ZegoUIKitPrebuiltLiveStreamingConfig.host([ZegoUIKitSignalingPlugin()])
        config.turnOnCameraWhenJoining = false
        config.turnOnMicrophoneWhenJoining = false
        config.bottomMenuBarConfig.hostButtons = [.switchCameraButton,.toggleMicrophoneButton,.toggleCameraButton]
        config.bottomMenuBarConfig.coHostButtons = [.coHostControlButton,.switchCameraButton,.toggleMicrophoneButton,.toggleCameraButton]
        config.bottomMenuBarConfig.audienceButtons = [.coHostControlButton]

        let liveVC = ZegoUIKitPrebuiltLiveStreamingVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: self.selfUserName ?? "", liveID: liveID, config: config)
        
        liveVC.modalPresentationStyle = .fullScreen
        liveVC.delegate = self
        self.present(liveVC, animated: true, completion: nil)
    }
}
```
:::


此外，还可以使用 `addButtonToBottomMenuBar` 和 `clearBottomMenuBarExtendButtons` 方法向菜单栏添加或清除自定义按钮。

:::if{props.platform="iOS"}
添加按钮时可通过`position`指定按钮添加的位置，默认添加在左边。

<CodeGroup>
```swift title="方法原型"
func addButtonToBottomMenuBar(_ button: UIButton, role: ZegoLiveStreamingRole, position:ZegoBottomMenuBarPosition = .left)
```
```swift title="示例代码"
 liveVC.addButtonToBottomMenuBar(button, role: .host, position: .left)
 liveVC.addButtonToBottomMenuBar(button, role: .host, position: .right)
```
</CodeGroup>
:::




## 显示效果
- 如果内置按钮和自定义按钮的总数不超过 5 个，所有按钮都将显示。
- 若按钮数量超过 5 个，超出的其他按钮将隐藏在（⋮）按钮中，单击此按钮，将弹出底部面板以显示其他所有按钮。效果如下图所示：

<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/live/live_buttom_menu_bar.gif" /></Frame>
