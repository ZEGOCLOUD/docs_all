# 设置退出确认框


**语聊房 UIKit（Live Audio Room Kit）** 默认在用户点击离开房间按钮或 Android 的返回按钮时，立即结束发言或观看，并退出语聊房。

## 实现流程

如果您想添加一个确认对话框，来再次确认用户是否想要离开语聊房，您可以使用 `confirmDialogInfo` 配置。

`confirmDialogInfo`：配置此参数后，将在结束语聊房之前，弹出一个您自定义的默认样式的确认对话框。

- 显示效果如下：
    
<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/leave_confirmation.gif" /></Frame> 

- 具体参考代码如下：

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

          ZegoDialogInfo confirmDialogInfo = new ZegoDialogInfo();
          confirmDialogInfo.title= "Leave the room";
          confirmDialogInfo.message= "Are you sure to leave the room?";
          confirmDialogInfo.cancelButtonName= "Cancel";
          confirmDialogInfo.confirmButtonName= "OK";
          config.confirmDialogInfo = confirmDialogInfo;

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

          val confirmDialogInfo = ZegoDialogInfo()
          confirmDialogInfo.title = "Leave the room"
          confirmDialogInfo.message = "Are you sure to leave the room?"
          confirmDialogInfo.cancelButtonName = "Cancel"
          confirmDialogInfo.confirmButtonName = "OK"
          config.confirmDialogInfo = confirmDialogInfo

          val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
          supportFragmentManager.beginTransaction()
              .replace(R.id.fragment_container, fragment)
              .commitNow()
      }
  }
```
</CodeGroup>
