# 实现挂断确认对话框


在默认情况下，当用户点击“结束通话”按钮或 Android 的返回按钮时，Call Kit 会直接结束通话。但是您也可以设置**确认对话框**来双重确认用户是否要挂断通话。

<Frame width="256" height="auto" caption="">
  <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/hangup_confirm.gif" />
</Frame>

## 实现流程

使用 `hangUpConfirmInfo` 配置：在配置了 `hangUpConfirmInfo` 参数之后，Call Kit 将在结束通话之前弹出一个带有默认样式的确认对话框，显示您设置的确认信息。

示例代码如下：

<CodeGroup>
```java title="基本通话"
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

    // 在此修改您的自定义配置。
    ZegoUIKitPrebuiltCallConfig config = ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall();
    config.hangUpConfirmDialogInfo = new ZegoHangUpConfirmDialogInfo();
    config.hangUpConfirmDialogInfo.title= "Hangup confirm";
    config.hangUpConfirmDialogInfo.message= "Do you want to hangup?";
    config.hangUpConfirmDialogInfo.cancelButtonName= "Cancel";
    config.hangUpConfirmDialogInfo.confirmButtonName= "Confirm";

    ZegoUIKitPrebuiltCallFragment fragment = ZegoUIKitPrebuiltCallFragment
            .newInstance(appID, appSign, callID, userID, userName, config);

    getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
  }
}
```
```java title="携带邀请的通话"
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
        ZegoUIKitPrebuiltCallInvitationConfig callInvitationConfig = new ZegoUIKitPrebuiltCallInvitationConfig(),
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
                    // Modify your custom calling configurations here.
                    config.hangUpConfirmDialogInfo = new ZegoHangUpConfirmDialogInfo();
                    config.hangUpConfirmDialogInfo.title= "Hangup confirm";
                    config.hangUpConfirmDialogInfo.message= "Do you want to hangup?";
                    config.hangUpConfirmDialogInfo.cancelButtonName= "Cancel";
                    config.hangUpConfirmDialogInfo.confirmButtonName= "Confirm";
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

## 监听挂断事件

如果您想要监听挂断事件，例如在结束通话时保存通话录音，Call Kit 提供了一个 `leaveCallListener` 方法，当然，您也可以在 `leaveCallListener` 中实现自定义业务逻辑。
