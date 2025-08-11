# 自定义底部菜单栏按钮


**语聊房 UIKit（Live Audio Room Kit）** 支持自定义调整菜单栏的按钮，支持删除默认按钮或添加自定义按钮。您可以删除默认按钮或添加自定义按钮。如果需要，您可以配置bottomMenuBarConfig：

- `hostButtons`：使用此选项为房主（主持人）设置预制的按钮。
- `speakerButtons`：使用此选项为发言人设置预制的按钮。
- `audienceButtons`：使用此选项为观众设置预制的按钮。
:::if{props.platform=undefined}
- `menuBarButtonsMaxCount`：菜单栏可以显示的按钮的最大数量，支持范围设置[1, 5]，默认值是 5。
:::
:::if{props.platform="iOS"}
- `maxCount`：菜单栏可以显示的按钮的最大数量，支持范围设置[1, 5]，默认值是 5。
:::
- `showInRoomMessageButton`：是否显示消息按钮，默认显示。


:::if{props.platform=undefined}
如果内置按钮和自定义按钮的总数不超过`menuBarButtonsMaxCount`个，所有按钮都将正常显示。
:::
:::if{props.platform="iOS"}
如果内置按钮和自定义按钮的总数不超过`maxCount`个，所有按钮都将正常显示。
:::
若按钮数超过 5 个，超出的其他按钮将隐藏在（⋮）按钮中。单击此按钮将弹出底部面板以显示其他所有按钮。以下是实际效果和参考代码：

<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/bottom_bar.gif" /></Frame>


:::if{props.platform=undefined}
<CodeGroup>
```java title="Java"
  public class LiveAudioRoomActivity extends AppCompatActivity {

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_call);

          addFragment();
      }

      public void addFragment() {
          long appID = yourAppID; // 替换为您的 AppID，请从 ZEGO 控制台获取
          String appSign = yourAppSign; // 替换为您的 AppSign，请从 ZEGO 控制台获取
          String userID = yourUserID; // 替换为您的 UserID
          String userName = yourUserName; // 替换为您的 UserName

          boolean isHost = getIntent().getBooleanExtra("host", false);
          String roomID = getIntent().getStringExtra("roomID");

          ZegoUIKitPrebuiltLiveAudioRoomConfig config;
          if (isHost) {
              config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
          } else {
              config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
          }

          config.bottomMenuBarConfig.hostButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON);
          config.bottomMenuBarConfig.speakerButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON);
          config.bottomMenuBarConfig.audienceButtons = Arrays.asList(ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON);

          ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config);
          getSupportFragmentManager().beginTransaction()
              .replace(R.id.fragment_container, fragment)
              .commitNow();
      }
  }
  ```
```kotlin title="Kotlin"
  class LiveAudioRoomActivity : AppCompatActivity() {

      override fun onCreate(savedInstanceState: Bundle?) {
          super.onCreate(savedInstanceState)
          setContentView(R.layout.activity_live)
          addFragment()
      }

      private fun addFragment() {
          val appID: Long = yourAppID // 替换为您的 AppID，请从 ZEGO 控制台获取
          val appSign = yourAppSign // 替换为您的 AppSign，请从 ZEGO 控制台获取
          val userID = YourUserID // 替换为您的 UserID
          val userName = YourUserName // 替换为您的 UserName
          
          val isHost = intent.getBooleanExtra("host", false)
          val roomID = intent.getStringExtra("roomID")

          val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
              ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
          } else {
              ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
          }

          config.bottomMenuBarConfig.hostButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON)
          config.bottomMenuBarConfig.speakerButtons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON)
          config.bottomMenuBarConfig.audienceButtons = Arrays.asList(ZegoMenuBarButtonName.SHOW_MEMBER_LIST_BUTTON)

          val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
          supportFragmentManager.beginTransaction()
              .replace(R.id.fragment_container, fragment)
              .commitNow()
      }
  }
```
</CodeGroup>

此外，您也可以通过以下方法，实现相同的效果：`addButtonToMenuBar` 和 `clearBottomBarExtendButtons`。

<CodeGroup>
```java title="Java"
class ZegoUIKitPrebuiltLiveAudioRoomFragment{
    //...
    void addButtonToMenuBar(List<View> widgets, ZegoLiveAudioRoomRole role);
    void clearBottomBarExtendButtons(ZegoLiveAudioRoomRole role);
    //...
}
```
```kotlin title="Kotlin"
class ZegoUIKitPrebuiltLiveAudioRoomFragment{
    //...
    fun addButtonToMenuBar(widgets: List<View>?, role: ZegoLiveAudioRoomRole?)
    fun clearBottomBarExtendButtons(role: ZegoLiveAudioRoomRole?)
    //...
}
```
</CodeGroup>
:::

:::if{props.platform="iOS"}
<CodeGroup>
```swift title="Swift"
   class ViewController: UIViewController {

      let selfUserID: String = "userID"
      let selfUserName: String = "userName"
      let yourAppID: UInt32 = YourAppID // 替换为您的 AppID
      let yourAppSign: String = "YourAppSign" // 替换为您的 AppSign
      let roomID: String = "YourRoomID" // 替换为您的 RoomID

      @IBAction func startLiveAudio(_ sender: Any) {

          // 在此处修改您的自定义配置。
          let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
          config.bottomMenuBarConfig.hostButtons = [.showMemberListButton, .toggleMicrophoneButton]
          config.bottomMenuBarConfig.audienceButtons = [.showMemberListButton, .toggleMicrophoneButton]
          config.bottomMenuBarConfig.speakerButtons = [.showMemberListButton, .toggleMicrophoneButton]
          let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)

          liveAudioVC.modalPresentationStyle = .fullScreen
          self.present(liveAudioVC, animated: true, completion: nil)
      }
  }
  ```
```objc title="Objective-C"
@implementation ViewController

- (void)viewDidLoad {
  [super viewDidLoad];
  // Do any additional setup after loading the view.
  unsigned int appID = xxx; 
  NSString *appSign = @"xxx"; 
  NSString *userName = @"xxx";
  NSString *userID =  @"xxx";
  NSString *roomID =  @"xxx";
  
}
- (void)startLiveAudio {
  ZegoUIKitPrebuiltLiveAudioRoomConfig *config = [ZegoUIKitPrebuiltLiveAudioRoomConfig host];
  
  ZegoBottomMenuBarConfig* bottomMenuBarConfig = [[ZegoBottomMenuBarConfig alloc] initWithHostButtons:@[@(ZegoMenuBarButtonNameLeaveButton)] speakerButtons:@[@(ZegoMenuBarButtonNameToggleMicrophoneButton)] audienceButtons:@[@(ZegoMenuBarButtonNameApplyTakeSeatButton)]];
  config.bottomMenuBarConfig = bottomMenuBarConfig;

  ZegoUIKitPrebuiltLiveAudioRoomVC *vc = [[ZegoUIKitPrebuiltLiveAudioRoomVC alloc] init:appID appSign:appSign userID:userID userName:userName roomID:roomID config:config];
  vc.modalPresentationStyle = UIModalPresentationFullScreen;
[self presentViewController:vc animated:YES completion:^{
    
  }];
}
  ```
</CodeGroup>

此外，您也可以通过以下两种方法实现相同的效果：`addButtonToMenuBar` 和 `clearBottomBarExtendButtons`。

```Swift
@objc public func addButtonToMenuBar(_ button: UIButton, role: ZegoLiveAudioRoomRole)

@objc public func clearBottomBarExtendButtons(_ role: ZegoLiveAudioRoomRole) 
```
:::
