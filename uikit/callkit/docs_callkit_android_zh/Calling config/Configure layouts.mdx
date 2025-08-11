# 调整布局


音视频通话 UIKit 目前支持画中画（picture-in-picture）布局和宫格式（gallery）布局，每种布局都有自己的配置。
如需选择和配置布局，请在 `ZegoUIKitPrebuiltCallConfig` 中使用 `layout` 参数。

## 画中画布局

画中画布局支持配置 `switchLargeOrSmallViewByClick`，允许用户点击小视图以实现在大视图和小视图之间切换。默认为允许。

效果如下：

| 当摄像头关闭时显示我的视图 | 当摄像头关闭时隐藏我的视图 | 切换 |
| -- | -- | -- |
| <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/layout_show_self1.gif" /></Frame> | <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/layout_show_self0.gif" /></Frame> | <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/layout_switch.gif" /></Frame> |

以下是参考代码：

:::if{props.platform=undefined}
<CodeGroup>
```java title="基本呼叫"
public class CallActivity extends AppCompatActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_call);

    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "userID";
    String userName = "userName";
    String callID = "testCallID";

    // 在这里修改自定义配置。    
    ZegoUIKitPrebuiltCallConfig config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall();
    ZegoLayoutPictureInPictureConfig pipConfig = new ZegoLayoutPictureInPictureConfig();
    pipConfig.switchLargeOrSmallViewByClick = true;
    config.layout.mode = ZegoLayoutMode.PICTURE_IN_PICTURE;
    config.layout.config = pipConfig;

    ZegoUIKitPrebuiltCallFragment fragment = ZegoUIKitPrebuiltCallFragment
            .newInstance(appID, appSign, callID, userID, userName, config);

    getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
  }
}
```
```java title="携带邀请的呼叫"
public class MainActivity extends AppCompatActivity {
    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "userID";
    String userName = "userName";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initCallInviteService();
    }

    public void initCallInviteService() {
        ZegoUIKitPrebuiltCallInvitationConfig callInvitationConfig = new ZegoUIKitPrebuiltCallInvitationConfig();
        callInvitationConfig.provider = new ZegoUIKitPrebuiltCallConfigProvider() {
                @Override
                public ZegoUIKitPrebuiltCallConfig requireConfig(ZegoCallInvitationData invitationData) {
                    ZegoUIKitPrebuiltCallConfig config;
                    boolean isVideoCall = invitationData.type == ZegoInvitationType.VIDEO_CALL.getValue();
                    boolean isGroupCall = invitationData.invitees.size() > 1;
                    if (isVideoCall && isGroupCall) {
                        config = ZegoUIKitPrebuiltCallConfig.groupVideoCall();
                    } else if (!isVideoCall && isGroupCall) {
                        config = ZegoUIKitPrebuiltCallConfig.groupVoiceCall();
                    } else if (!isVideoCall) {
                        config = ZegoUIKitPrebuiltCallConfig.oneOnOneVoiceCall();
                    } else {
                        config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall();
                    }
                    // 在这里修改您的自定义呼叫配置。                    
                    if(isGroupCall){
                        ZegoLayoutGalleryConfig galleryConfig =  new ZegoLayoutGalleryConfig();
                        galleryConfig.addBorderRadiusAndSpacingBetweenView = false;                        
                        config.layout.mode = ZegoLayoutMode.GALLERY;
                        config.layout.config = galleryConfig;
                    }else{
                        ZegoLayoutPictureInPictureConfig pipConfig = new ZegoLayoutPictureInPictureConfig();
                        pipConfig.switchLargeOrSmallViewByClick = true;
                        config.layout.mode = ZegoLayoutMode.PICTURE_IN_PICTURE;
                        config.layout.config = pipConfig
                    }
                    return config;
                }
        );
        ZegoUIKitPrebuiltCallService.init(getApplication(), appID, appSign, userID, userName,
            callInvitationConfig);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        ZegoUIKitPrebuiltCallService.logout();
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
<CodeGroup>
```swift title="基本呼叫"
class ViewController: UIViewController {
    
    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID 
    let yourAppSign: String = YourAppSign
    let callID: String = "testCallID"
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    @IBAction func makeNewCall(_ sender: Any) {
        
        // 在此处修改自定义配置。
        let config: ZegoUIKitPrebuiltCallConfig = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall()

        let layout: ZegoLayout = ZegoLayout()
        layout.mode = .pictureInPicture
        let pipConfig: ZegoLayoutPictureInPictureConfig = ZegoLayoutPictureInPictureConfig()
        pipConfig.switchLargeOrSmallViewByClick = true;
        layout.config = pipConfig
        config.layout = layout

        let callVC = ZegoUIKitPrebuiltCallVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName ?? "", callID: callID, config: config)
        callVC.modalPresentationStyle = .fullScreen
        self.present(callVC, animated: true, completion: nil)
    }
}
```
```swift title="携带邀请的呼叫"
class CallInvitationVC: UIViewController {
    let appID: UInt32 = yourAppID
    let appSign: String = "yourAppSign"
    let userID: String = "userID"
    let userName: String = "userName"
    let voiceCallButton: ZegoSendCallInvitationButton = ZegoSendCallInvitationButton(ZegoInvitationType.voiceCall.rawValue)
    let videoCallButton: ZegoSendCallInvitationButton = ZegoSendCallInvitationButton(ZegoInvitationType.videoCall.rawValue)

    override func viewDidLoad() {
        super.viewDidLoad()
        let config = ZegoUIKitPrebuiltCallInvitationConfig([ZegoUIKitSignalingPlugin()], notifyWhenAppRunningInBackgroundOrQuit: false, isSandboxEnvironment: false)
        ZegoUIKitPrebuiltCallInvitationService.shared.initWithAppID(self.appID, appSign: self.appSign, userID: self.userID, userName: self.userName, config: config)
        ZegoUIKitPrebuiltCallInvitationService.shared.delegate = self
    }
}

extension CallInvitationVC: ZegoUIKitPrebuiltCallInvitationServiceDelegate {
    // MARK: -ZegoUIKitPrebuiltCallInvitationServiceDelegate
    func requireConfig(_ data: ZegoCallInvitationData) -> ZegoUIKitPrebuiltCallConfig {
        var config = ZegoUIKitPrebuiltCallConfig.groupVoiceCall()
        if data.type == .voiceCall {
            if data.invitees?.count ?? 0 > 1 {
                config = ZegoUIKitPrebuiltCallConfig.groupVoiceCall()
            } else {
                config = ZegoUIKitPrebuiltCallConfig.oneOnOneVoiceCall()
            }
        } else {
            if data.invitees?.count ?? 0 > 1 {
                config = ZegoUIKitPrebuiltCallConfig.groupVideoCall()
            } else {
                config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall()
            }
        }
        // 在此处修改自定义配置。
        let layout: ZegoLayout = ZegoLayout()
        if data.invitees?.count ?? 0 > 1 {
            layout.mode = .gallery
            let layoutConfig: ZegoLayoutGalleryConfig = ZegoLayoutGalleryConfig()
            layoutConfig.addBorderRadiusAndSpacingBetweenView = false;
            layout.config = layoutConfig
        } else {
            layout.mode = .pictureInPicture
            let pipConfig: ZegoLayoutPictureInPictureConfig = ZegoLayoutPictureInPictureConfig()
            pipConfig.switchLargeOrSmallViewByClick = true;
            layout.config = pipConfig
        }
        config.layout = layout
        return config
    }
}
```
</CodeGroup>
:::


## 宫格式布局

宫格式布局支持的配置是：

- `addBorderRadiusAndSpacingBetweenView`：在宫格式布局中，可以使用此选项添加边框圆角半径和视图之间的间距。true：启用（默认）。false：禁用。

效果如下：

|添加边框圆角半径和间距 | 不添加边框圆角半径和间距|
|----|----|
|<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/conference/6.png" /></Frame> |<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/conference/6_false.png" /></Frame>|

:::if{props.platform=undefined}
<CodeGroup>
```java title="基本呼叫"
public class CallActivity extends AppCompatActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_call);

    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "userID";
    String userName = "userName";
    String callID = "testCallID";

    // 在这里修改自定义配置。    
    ZegoUIKitPrebuiltCallConfig config = ZegoUIKitPrebuiltCallConfig.groupVideoCall();
    ZegoLayoutGalleryConfig galleryConfig =  new ZegoLayoutGalleryConfig();
    galleryConfig.addBorderRadiusAndSpacingBetweenView = false;
    config.layout.config = galleryConfig;

    ZegoUIKitPrebuiltCallFragment fragment = ZegoUIKitPrebuiltCallFragment
            .newInstance(appID, appSign, callID, userID, userName, config);

    getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
  }
}
```
```java title="携带邀请的呼叫"
public class MainActivity extends AppCompatActivity {
    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "userID";
    String userName = "userName";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initCallInviteService();
    }

    public void initCallInviteService() {
        ZegoUIKitPrebuiltCallInvitationConfig callInvitationConfig = new ZegoUIKitPrebuiltCallInvitationConfig();
        callInvitationConfig.provider = new ZegoUIKitPrebuiltCallConfigProvider() {
                @Override
                public ZegoUIKitPrebuiltCallConfig requireConfig(ZegoCallInvitationData invitationData) {
                    ZegoUIKitPrebuiltCallConfig config;
                    boolean isVideoCall = invitationData.type == ZegoInvitationType.VIDEO_CALL.getValue();
                    boolean isGroupCall = invitationData.invitees.size() > 1;
                    if (isVideoCall && isGroupCall) {
                        config = ZegoUIKitPrebuiltCallConfig.groupVideoCall();
                    } else if (!isVideoCall && isGroupCall) {
                        config = ZegoUIKitPrebuiltCallConfig.groupVoiceCall();
                    } else if (!isVideoCall) {
                        config = ZegoUIKitPrebuiltCallConfig.oneOnOneVoiceCall();
                    } else {
                        config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall();
                    }
                    // 在这里修改自定义呼叫配置。                    
                    if(isGroupCall){
                        ZegoLayoutGalleryConfig galleryConfig =  new ZegoLayoutGalleryConfig();
                        galleryConfig.addBorderRadiusAndSpacingBetweenView = false;
                        config.layout.config = galleryConfig;
                    }else{
                        ZegoLayoutPictureInPictureConfig pipConfig = new ZegoLayoutPictureInPictureConfig();
                        pipConfig.switchLargeOrSmallViewByClick = true;
                        config.layout.config = pipConfig;
                    }
                    return config;
                }
        );
        ZegoUIKitPrebuiltCallService.init(getApplication(), appID, appSign, userID, userName,
            callInvitationConfig);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        ZegoUIKitPrebuiltCallService.logout();
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
<CodeGroup>
```swift title="基本呼叫"
class ViewController: UIViewController {
    
    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID
    let yourAppSign: String = YourAppSign
    let callID: String = "testCallID"
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    @IBAction func makeNewCall(_ sender: Any) {
        
        // 在此处修改自定义配置。
        let config: ZegoUIKitPrebuiltCallConfig = ZegoUIKitPrebuiltCallConfig.groupVideoCall()

        let layout: ZegoLayout = ZegoLayout()
        layout.mode = .gallery
        let layoutConfig: ZegoLayoutGalleryConfig = ZegoLayoutGalleryConfig()
        layoutConfig.addBorderRadiusAndSpacingBetweenView = false;
        layout.config = layoutConfig
        config.layout = layout

        let callVC = ZegoUIKitPrebuiltCallVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName ?? "", callID: callID, config: config)
        callVC.modalPresentationStyle = .fullScreen
        self.present(callVC, animated: true, completion: nil)
    }
}
```
```swift title="携带邀请的呼叫"
class CallInvitationVC: UIViewController {
    let appID: UInt32 = yourAppID
    let appSign: String = "yourAppSign"
    let userID: String = "userID"
    let userName: String = "userName"
    let voiceCallButton: ZegoSendCallInvitationButton = ZegoSendCallInvitationButton(ZegoInvitationType.voiceCall.rawValue)
    let videoCallButton: ZegoSendCallInvitationButton = ZegoSendCallInvitationButton(ZegoInvitationType.videoCall.rawValue)

    override func viewDidLoad() {
        super.viewDidLoad()
        let config = ZegoUIKitPrebuiltCallInvitationConfig([ZegoUIKitSignalingPlugin()], notifyWhenAppRunningInBackgroundOrQuit: false, isSandboxEnvironment: false)
        ZegoUIKitPrebuiltCallInvitationService.shared.initWithAppID(self.appID, appSign: self.appSign, userID: self.userID, userName: self.userName, config: config)
        ZegoUIKitPrebuiltCallInvitationService.shared.delegate = self
    }
}

extension CallInvitationVC: ZegoUIKitPrebuiltCallInvitationServiceDelegate {
    //MARK: -ZegoUIKitPrebuiltCallInvitationServiceDelegate
    func requireConfig(_ data: ZegoCallInvitationData) -> ZegoUIKitPrebuiltCallConfig {
        var config = ZegoUIKitPrebuiltCallConfig(.groupVoiceCall)
        if data.type == .voiceCall {
            if data.invitees?.count ?? 0 > 1 {
                config = ZegoUIKitPrebuiltCallConfig.groupVoiceCall()
            } else {
                config = ZegoUIKitPrebuiltCallConfig.oneOnOneVoiceCall()
            }
        } else {
            if data.invitees?.count ?? 0 > 1 {
                config = ZegoUIKitPrebuiltCallConfig.groupVideoCall()
            } else {
                config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall()
            }
        }
        // 在此处修改自定义配置。
        let layout: ZegoLayout = ZegoLayout()
        if data.invitees?.count ?? 0 > 1 {
            layout.mode = .gallery
            let layoutConfig: ZegoLayoutGalleryConfig = ZegoLayoutGalleryConfig()
            layoutConfig.addBorderRadiusAndSpacingBetweenView = false;
            layout.config = layoutConfig
        } else {
            layout.mode = .pictureInPicture
            let pipConfig: ZegoLayoutPictureInPictureConfig = ZegoLayoutPictureInPictureConfig()
            pipConfig.switchLargeOrSmallViewByClick = true;
            layout.config = pipConfig
        }
        config.layout = layout
        return config
    }
}
```
</CodeGroup>
:::
