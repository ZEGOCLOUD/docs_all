# 屏幕共享


## 什么是屏幕共享

屏幕共享，是指在视频通话或互动直播过程中，将屏幕内容以视频的方式分享给其他的观众，以增强互动体验，提高沟通效率。屏幕共享在如下场景中应用广泛：
- 视频会议场景中，屏幕共享可以将发言者本地的文件、数据、网页、PPT 等画面分享给其他参会人。
- 在线课堂场景中，屏幕共享可以将老师的课件、笔记、讲课内容等画面展示给学生观看。


| 开始屏幕共享                                                                                                     | 移动应用共享的屏幕                                                                                                 | Web 应用共享的屏幕                                                                                                         | 横屏模式                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| <Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/UIkit_ScreenShare/conference_watch_screen_share.png" /></Frame> | <Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/UIkit_ScreenShare/conference_watch_screen_share.png" /></Frame> | <Frame width="230" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/UIkit_ScreenShare/conference_watch_web_screenshare.png" /></Frame> | <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/UIkit_ScreenShare/fullScreenShare.png" /></Frame> |

## 实现流程

### 添加权限
为了实现屏幕共享功能，请进入 “app/src/main” 目录，打开 “AndroidManifest.xml” 文件，添加以下权限：

```xml app/src/main/AndroidManifest.xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" />
```
<Warning title="警告">如果你的应用需要上传到 Google Play Store，由于 [Google Play 的政策](https://support.google.com/googleplay/android-developer/answer/13392821?hl=zh)限制，你可能需要针对这两个权限作出相应的声明才可以避免被拒绝。</Warning>

### 共享屏幕

屏幕共享仅支持在宫格布局中使用，如需共享您的屏幕，您需要先将 `ZegoUIKitPrebuiltCallConfig` 内的 `layout` 设置为 `Gallery`。

如需在屏幕共享期间设置是否默认使用全屏模式，您需要在 `ZegoLayoutGalleryConfig` 内配置 `showNewScreenSharingViewInFullscreenMode`，将其设置为 `true`，即当开始屏幕共享时，共享的屏幕将自动全屏显示。

同时，全屏模式按钮是可自定义的，您可以通过配置 `ZegoLayoutGalleryConfig` 内的 `showScreenSharingFullscreenModeToggleButtonRules`，决定它的显示方式：
- `SHOW_WHEN_SCREEN_PRESSED`：点击共享屏幕时，将显示全屏模式按钮。
- `ALWAYS_SHOW`：始终显示全屏模式按钮。
- `ALWAYS_HIDE`：始终隐藏全屏模式按钮。

如需开始屏幕共享，将 `ZegoMenuBarButtonName.SCREEN_SHARING_TOGGLE_BUTTON` 配置添加到 `bottomMenuBarConfig` 或 `topMenuBarConfig` 中，以便显示屏幕共享按钮。

以下是参考代码：

<CodeGroup>
```java title="Java"
public class CallActivity extends AppCompatActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_call);

    long appID = YourAppID;
    String appSign = YourAppSign;
    String userID = "用户 ID";
    String userName = "用户名";
    String callID = "通话 ID";

    ZegoUIKitPrebuiltCallConfig config = ZegoUIKitPrebuiltCallConfig.groupVideoCall();

    config.bottomMenuBarConfig.buttons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON,
            ZegoMenuBarButtonName.SWITCH_CAMERA_BUTTON, ZegoMenuBarButtonName.HANG_UP_BUTTON,
            ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SCREEN_SHARING_TOGGLE_BUTTON);

    ZegoLayoutGalleryConfig galleryConfig = new ZegoLayoutGalleryConfig();
    galleryConfig.removeViewWhenAudioVideoUnavailable = true;
    galleryConfig.showNewScreenSharingViewInFullscreenMode = true;
    galleryConfig.showScreenSharingFullscreenModeToggleButtonRules  = ZegoShowFullscreenModeToggleButtonRules.SHOW_WHEN_SCREEN_PRESSED;
    config.zegoLayout = new ZegoLayout(ZegoLayoutMode.GALLERY, galleryConfig);

    ZegoUIKitPrebuiltCallFragment fragment = ZegoUIKitPrebuiltCallFragment.newInstance(appID,appSign, userID, userName, callID, config);
    getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, fragment).commitNow();
```
```kotlin title="Kotlin"
class CallActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_call)
        val appID: Long = YourAppID
        val appSign: String = YourAppSign
        val userID = "用户 ID"
        val userName = "用户名"
        val callID = "通话 ID"

        config.bottomMenuBarConfig.buttons = Arrays.asList<ZegoMenuBarButtonName>(
            ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON,
            ZegoMenuBarButtonName.SWITCH_CAMERA_BUTTON,
            ZegoMenuBarButtonName.HANG_UP_BUTTON,
            ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON,
            ZegoMenuBarButtonName.SCREEN_SHARING_TOGGLE_BUTTON
        )
        val galleryConfig = ZegoLayoutGalleryConfig()
        galleryConfig.removeViewWhenAudioVideoUnavailable = true
        galleryConfig.showNewScreenSharingViewInFullscreenMode = true
        galleryConfig.showScreenSharingFullscreenModeToggleButtonRules =
            ZegoShowFullscreenModeToggleButtonRules.SHOW_WHEN_SCREEN_PRESSED
        config.zegoLayout = ZegoLayout(ZegoLayoutMode.GALLERY, galleryConfig)

        val fragment: ZegoUIKitPrebuiltCallFragment =
            ZegoUIKitPrebuiltCallFragment.newInstance(
                appID,appSign, userID, userName, callID, config
            )
        supportFragmentManager.beginTransaction().replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>

如果您使用通话邀请功能，则可以在 `ZegoUIKitPrebuiltCallInvitationConfig` 中设置 `galleryLayout`。

```java
ZegoUIKitPrebuiltCallInvitationConfig callInvitationConfig = new ZegoUIKitPrebuiltCallInvitationConfig();
callInvitationConfig.notifyWhenAppRunningInBackgroundOrQuit = false;
callInvitationConfig.provider = new ZegoUIKitPrebuiltCallConfigProvider() {
    @Override
    public ZegoUIKitPrebuiltCallConfig requireConfig(ZegoCallInvitationData invitationData) {
        ZegoUIKitPrebuiltCallConfig config = ZegoUIKitPrebuiltCallConfig.groupVideoCall();
        config.bottomMenuBarConfig.buttons = Arrays.asList(ZegoMenuBarButtonName.TOGGLE_CAMERA_BUTTON,ZegoMenuBarButtonName.SWITCH_CAMERA_BUTTON, ZegoMenuBarButtonName.HANG_UP_BUTTON,ZegoMenuBarButtonName.TOGGLE_MICROPHONE_BUTTON, ZegoMenuBarButtonName.SCREEN_SHARING_TOGGLE_BUTTON);
        ZegoLayoutGalleryConfig galleryConfig = new ZegoLayoutGalleryConfig();
        galleryConfig.removeViewWhenAudioVideoUnavailable = true;
        galleryConfig.showNewScreenSharingViewInFullscreenMode = true;
        galleryConfig.showScreenSharingFullscreenModeToggleButtonRules = ZegoShowFullscreenModeToggleButtonRules.SHOW_WHEN_SCREEN_PRESSED;
        config.layout = new ZegoLayout(ZegoLayoutMode.GALLERY, galleryConfig);
        return config;
    }
};
ZegoUIKitPrebuiltCallService.init(getApplication(), appID, appSign, userID, userName, callInvitationConfig);
```

### 屏幕旋转

您可以参考以下流程，实现屏幕旋转：

1. 在手机设置中，关闭旋转锁定功能。
2. 将 `android:configChanges="locale|keyboardHidden|fontScale|orientation|screenSize|screenLayout|layoutDirection|density|uiMode"` 属性添加到 `Activity` 的 `manifest` 文件配置中。以 `CallActivity` 为例：

```xml
<activity
   android:name=".CallActivity"
   android:configChanges="locale|keyboardHidden|fontScale|orientation|screenSize|screenLayout|layoutDirection|density|uiMode"
   android:exported="false" />
```
