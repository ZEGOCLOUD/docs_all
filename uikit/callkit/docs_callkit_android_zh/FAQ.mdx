# FAQ

<Accordion title="1. 如何解决同时集成 Firebase Cloud Message 时的冲突？" defaultOpen="false">
当 Call Kit 接收到来自 FCM 的消息时，如果该消息不是来自 Zego SDK，它会向当前应用发送一个广播，广播的 action 是 `com.zegocloud.zegouikit.call.fcm`，类似以下代码：

```java
Intent intent = new Intent("com.zegocloud.zegouikit.call.fcm");
intent.putExtra("remoteMessage", remoteMessage);
context.sendBroadcast(intent);
```
因此，如果您已经集成了Firebase Messaging，只需按照以下步骤完成迁移：

1. 在您的应用程序中创建并静态注册一个BroadcastReceiver：
   - 创建一个BroadcastReceiver，例如`YourCustomBroadcastReceiver.java`。
   - 将其注册到应用程序的`Manifest.xml`文件的`application`节点，并将 action 设置为`"com.zegocloud.zegouikit.call.fcm"`，例如：
   ```xml
   <receiver
        android:name="com.zegocloud.uikit.demo.calloffline.YourCustomBroadcastReceiver"
        android:enabled="true"
        android:exported="false">
        <intent-filter>
          <action android:name="com.zegocloud.zegouikit.call.fcm"/>
        </intent-filter>
    </receiver>
   ```
2. 在`Manifest.xml`中删除原始的FCM服务，它看起来像这样：
    ```xml
    <service
        android:name=".java.MyFirebaseMessagingService"
        android:exported="false">
        <intent-filter>
            <action android:name="com.google.firebase.MESSAGING_EVENT" />
        </intent-filter>
    </service>
    ```
   请删除它以避免与Zego SDK冲突。

3. 监听和处理相关事件：
   您需要将逻辑从`MyFirebaseMessagingService`迁移到`YourCustomBroadcastReceiver`，如下所示。

   原始代码：
   ```java
   public class YourFirebaseMsgService extends FirebaseMessagingService {
        @Override
        public void onMessageReceived(RemoteMessage remoteMessage) {
            // 您的自定义逻辑
        }
    }
   ```
   请按照以下方式进行迁移，并删除YourFirebaseMsgService.java：

   ```java
   public class YourCustomBroadcastReceiver extends BroadcastReceiver {

        private static final String TAG = "CustomReceiver";

        public void onReceive(Context context, Intent intent) {
            com.google.firebase.messaging.RemoteMessage remoteMessage = intent.getParcelableExtra("remoteMessage");
            // 您的自定义逻辑
            Log.d(TAG, "onReceive.remoteMessage.getData: " + remoteMessage.getData());
        }
    }
   ```
通过这些步骤，您应该能够接收和处理自己的FCM消息。
</Accordion>


<Accordion title="2. 如何禁用 callInviteButton 的弹出显示？" defaultOpen="false">

ZegoSendCallInvitationButton 默认会显示一些错误提示，你可以通过以下方式禁用提示：

```java
ZegoSendCallInvitationButton callInviteButton;

// ...

callInviteButton.showErrorToast(false);
callInviteButton.setOnClickListener(new ClickListener() {
    @Override
    public void onClick(int errorCode, String errorMessage, List<ZegoCallUser> errorInvitees) {
        // add you custom logic for request resoult. 0 means send request success,else means failed.When errorCode is 0 , there may still have some error invitess.please check if all invitess receive successed.
    }
});

```

</Accordion>

<Accordion title="3. 在通话时如何自定义返回按钮事件？" defaultOpen="false">
默认情况下，在通话中，如果点击了安卓手机的返回按钮，用户将直接离开通话。

如果你想添加一个确认对话框，你可以像这样更改 `callInvitationConfig` ：

```java
ZegoUIKitPrebuiltCallInvitationConfig callInvitationConfig = new ZegoUIKitPrebuiltCallInvitationConfig();

callInvitationConfig.provider = new ZegoUIKitPrebuiltCallConfigProvider() {
    @Override
    public ZegoUIKitPrebuiltCallConfig requireConfig(ZegoCallInvitationData invitationData) {
        ZegoUIKitPrebuiltCallConfig config = null;
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
        config.hangUpConfirmDialogInfo = new ZegoHangUpConfirmDialogInfo();
        return config;
    }
};
```
你可以调整成员变量 `config.hangUpConfirmDialogInfo` 的值来更改对话框的文本。

你可以重写 `BackPressEvent` 来自定义返回按钮事件，像这样：

```java
ZegoUIKitPrebuiltCallService.events.setBackPressEvent(new BackPressEvent() {
    @Override
    public boolean onBackPressed() {
    //返回 true 表示你需要自定义返回按钮事件，返回 false 表示你不需要自定义返回按钮事件，它将按默认行为执行。
        return true;
    }
});
``` 

例如，如果你想在已经配置了 `ZegoMenuBarButtonName.MINIMIZING_BUTTON` 的情况下通过点击返回按钮最小化通话，你可以在回调中调用 `ZegoUIKitPrebuiltCallService.minimizeCall()` ：

```java
ZegoUIKitPrebuiltCallService.events.setBackPressEvent(new BackPressEvent() {
    @Override
    public boolean onBackPressed() {
        ZegoUIKitPrebuiltCallService.minimizeCall();
        return true;
    }
});
```
</Accordion>

<Accordion title="4. 如何获取日志文件？" defaultOpen="false">
我们包含三个不同的日志目录：

<Frame width="256" height="auto" caption="">
  <img src="https://doc-media.zego.im/sdk-doc/Pics/zegocloud/call/logs.png" />
</Frame>

* Express SDK 日志：

    默认情况下，Express SDK 会生成两种类型的日志文件：

    * 以 "zegoavlog" 开头的 TXT 日志文件，默认每个日志文件的最大大小为 5MB（5 * 1024 * 1024 字节）。
    * 压缩文件名为 "zegoavlog\{序列号\}-\{时间戳\}" 的 ZIP 压缩文件。解压缩该文件后，您会得到一个名为 "zegoavlog\{序列号\}-\{时间戳\}" 的 TXT 日志文件。"\{序列号\}" 可能会有所不同，但"\{时间戳\}" 是相同的。
    例如，解压缩 zegoavlog3-16901111.zip 将得到 zegoavlog2-16901111.txt 日志文件。

    默认的存储路径为：
    Android："/storage/Android/data/[应用程序包名]/files"


* ZIM SDK 日志：
    默认的存储路径为：
    "/storage/Android/data/[应用程序包名]/files/ZIMLogs" 


* UIKit 日志：
    默认的存储路径为：
    "/storage/Android/data/[应用程序包名]/files/uikit_log"

请将所有这些文件发送给我们，以帮助您解决问题。
</Accordion>
