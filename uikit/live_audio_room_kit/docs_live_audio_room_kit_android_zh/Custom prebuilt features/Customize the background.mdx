# 自定义背景

**语聊房 UIKit (Live Audio Room Kit)** 允许您自定义语聊房的背景视图。

## 实现流程

以实现如下自定义设置为例，将为您举例说明具体实现方式。
1. 在左上角显示语聊房的标题和房间 ID。
2. 显示自定义背景图片。

<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/background.jpeg" /></Frame> 

具体实现方式如下：

:::if{props.platform=undefined}
1. 创建 `AudioRoomBackgroundView` 类。
<CodeGroup>
```java title="Java"
  import android.content.Context;
  import android.graphics.Color;
  import android.text.TextUtils.TruncateAt;
  import android.util.AttributeSet;
  import android.util.TypedValue;
  import android.widget.FrameLayout;
  import android.widget.LinearLayout;
  import android.widget.TextView;
  import androidx.annotation.NonNull;
  import androidx.annotation.Nullable;
  import com.zegocloud.uikit.utils.Utils;

  public class AudioRoomBackgroundView extends FrameLayout {

      private TextView roomName;
      private TextView roomID;

      public AudioRoomBackgroundView(@NonNull Context context) {
          super(context);
          initView();
      }

      public AudioRoomBackgroundView(@NonNull Context context, @Nullable AttributeSet attrs) {
          super(context, attrs);
          initView();
      }

      public AudioRoomBackgroundView(@NonNull Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
          super(context, attrs, defStyleAttr);
          initView();
      }

      private void initView() {
          LinearLayout linearLayout = new LinearLayout(getContext());
          linearLayout.setOrientation(LinearLayout.VERTICAL);

          LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-2, -2);
          int marginEnd = Utils.dp2px(12, getResources().getDisplayMetrics());
          params.setMargins(0, 0, marginEnd, 0);

          roomName = new TextView(getContext());
          roomName.setMaxLines(1);
          roomName.setEllipsize(TruncateAt.END);
          roomName.setSingleLine(true);
          roomName.getPaint().setFakeBoldText(true);
          roomName.setTextColor(Color.parseColor("#ff1b1b1b"));
          roomName.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16);
          roomName.setMaxWidth(Utils.dp2px(200, getResources().getDisplayMetrics()));
          linearLayout.addView(roomName, params);

          roomID = new TextView(getContext());
          roomID.setMaxLines(1);
          roomID.setEllipsize(TruncateAt.END);
          roomID.setSingleLine(true);
          roomID.setTextColor(Color.parseColor("#ff606060"));
          roomID.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16);
          roomID.setMaxWidth(Utils.dp2px(120, getResources().getDisplayMetrics()));
          linearLayout.addView(roomID, params);

          FrameLayout.LayoutParams layoutParams = new FrameLayout.LayoutParams(-2, -2);
          int marginStart = Utils.dp2px(16, getResources().getDisplayMetrics());
          int marginTop = Utils.dp2px(10, getResources().getDisplayMetrics());
          layoutParams.setMargins(marginStart, marginTop, 0, 0);
          addView(linearLayout, layoutParams);
      }

      public void setRoomName(String roomName) {
          this.roomName.setText(roomName);
      }

      public void setRoomID(String roomID) {
          this.roomID.setText("ID: " + roomID);
      }
  }
```

```kotlin title="Kotlin"
  import android.content.Context
  import android.graphics.Color
  import android.text.TextUtils.TruncateAt
  import android.util.AttributeSet
  import android.util.TypedValue
  import android.widget.FrameLayout
  import android.widget.LinearLayout
  import android.widget.TextView
  import com.zegocloud.uikit.utils.Utils

  class AudioRoomBackgroundView : FrameLayout {
      private lateinit var roomName: TextView
      private lateinit var roomID: TextView

      constructor(context: Context) : super(context) {
          initView()
      }

      constructor(context: Context, attrs: AttributeSet?) : super(context, attrs) {
          initView()
      }

      constructor(context: Context, attrs: AttributeSet?, defStyleAttr: Int) : super(
          context, attrs, defStyleAttr
      ) {
          initView()
      }

      private fun initView() {
          val linearLayout = LinearLayout(context)
          linearLayout.orientation = LinearLayout.VERTICAL
          val params = LinearLayout.LayoutParams(-2, -2)
          val marginEnd: Int = Utils.dp2px(12, resources.displayMetrics)
          params.setMargins(0, 0, marginEnd, 0)
          roomName = TextView(context)
          roomName.maxLines = 1
          roomName.ellipsize = TruncateAt.END
          roomName.isSingleLine = true
          roomName.paint.isFakeBoldText = true
          roomName.setTextColor(Color.parseColor("#ff1b1b1b"))
          roomName.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
          roomName.maxWidth = Utils.dp2px(200, resources.displayMetrics)
          linearLayout.addView(roomName, params)
          roomID = TextView(context)
          roomID.maxLines = 1
          roomID.ellipsize = TruncateAt.END
          roomID.isSingleLine = true
          roomID.setTextColor(Color.parseColor("#ff606060"))
          roomID.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f)
          roomID.maxWidth = Utils.dp2px(120, resources.displayMetrics)
          linearLayout.addView(roomID, params)
          val layoutParams = LayoutParams(-2, -2)
          val marginStart: Int = Utils.dp2px(16, resources.displayMetrics)
          val marginTop: Int = Utils.dp2px(10, resources.displayMetrics)
          layoutParams.setMargins(marginStart, marginTop, 0, 0)
          addView(linearLayout, layoutParams)
      }

      fun setRoomName(roomName: String?) {
          this.roomName.text = roomName
      }

      fun setRoomID(roomID: String) {
          this.roomID.text = "ID: $roomID"
      }
  }
  ```
</CodeGroup>

2. 将 `AudioRoomBackgroundView` 设置到 `ZegoUIKitPrebuiltLiveAudioRoomFragment`。

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

          ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
              appID, appSign, userID, userName,roomID,config);
          getSupportFragmentManager().beginTransaction()
              .replace(R.id.fragment_container, fragment)
              .commitNow();
          AudioRoomBackgroundView roomBackgroundView = new AudioRoomBackgroundView(this);
          roomBackgroundView.setRoomID(roomID);
          roomBackgroundView.setRoomName("Live Audio Room");
          roomBackgroundView.setBackgroundResource(R.drawable.background);
          fragment.setBackgroundView(roomBackgroundView);
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

          val config: ZegoUIKitPrebuiltLiveAudioRoomConfig
          if (isHost) {
              config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
          } else {
              config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
          }
          val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
              appID, appSign, userID, userName, roomID, config
          )
          supportFragmentManager.beginTransaction()
              .replace(R.id.fragment_container, fragment)
              .commitNow()
          val roomBackgroundView = AudioRoomBackgroundView(this)
          roomBackgroundView.setRoomID(roomID)
          roomBackgroundView.setRoomName("Live Audio Room")
          roomBackgroundView.setBackgroundResource(R.drawable.background)
          fragment.setBackgroundView(roomBackgroundView)
      }
  }
  ```
</CodeGroup>
:::

:::if{props.platform="iOS"}
1. 创建 `AudioRoomBackgroundView` 类。

  ```swift
  class AudioRoomBackgroundView: UIView {
      
      lazy var roomNameLabel: UILabel = {
          let label = UILabel()
          label.font = UIFont.systemFont(ofSize: 24, weight: .semibold)
          label.textAlignment = .left
          label.numberOfLines = 1
          label.textColor = UIColor.black

          return label
      }()
      
      lazy var roomIDLabel: UILabel = {
          let label = UILabel()
          label.textAlignment = .left
          label.font = UIFont.systemFont(ofSize: 12, weight: .regular)
          label.textColor = UIColor.black
          return label
      }()
      
      lazy var backgroundImageView: UIImageView = {
          let view = UIImageView()
          return view
      }()

      override init(frame: CGRect) {
          super.init(frame: frame)
          self.addSubview(backgroundImageView)
          self.addSubview(roomNameLabel)
          self.addSubview(roomIDLabel)
      }
      
      required init?(coder: NSCoder) {
          fatalError("init(coder:) has not been implemented")
      }
      
      override func layoutSubviews() {
          super.layoutSubviews()
          self.setupLayout()
      }
      
      func setupLayout() {
          self.backgroundImageView.frame = CGRect(x: 0, y: 0, width: self.frame.width, height: self.frame.height)
          self.roomNameLabel.frame = CGRect(x: 27, y: 57, width: self.frame.width - 27, height: 33)
          self.roomIDLabel.frame = CGRect(x:27, y: self.roomNameLabel.frame.maxY + 2, width: self.frame.width - 27, height: 21)
      }
      
      public func setBackgroundViewContent(_ roomName: String, roomID: String, image: UIImage) {
          self.roomNameLabel.text = roomName
          self.roomIDLabel.text = roomID
          self.backgroundImageView.image = image
      }

  }
  ```
2. 将 `AudioRoomBackgroundView` 设置到 `ZegoUIKitPrebuiltLiveAudioRoomVC` 中。
  ```swift
  class ViewController: UIViewController {

      let selfUserID: String = "userID"
      let selfUserName: String = "userName"
      let yourAppID: UInt32 = YourAppID // 替换为您的 AppID，请从 ZEGO 控制台获取
      let yourAppSign: String = "YourAppSign" // 替换为您的 AppSign，请从 ZEGO 控制台获取
      let roomID: String = "YourRoomID" // 替换为您的 RoomID

      @IBAction func startLiveAudio(_ sender: Any) {

          // 在此处修改您的自定义配置。
          let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
          let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)
          liveAudioVC.modalPresentationStyle = .fullScreen
          let backgroundView: AudioRoomBackgroundView = AudioRoomBackgroundView(frame: CGRect(x: 0, y: 0, width: liveAudioVC.view.frame.width, height: liveAudioVC.view.frame.height))
          backgroundView.setBackgroundViewContent("语聊房", roomID: roomID, image: UIImage(named: "your_background_image_name")) // 替换为实际的图片名称
          liveAudioVC.setBackgroundView(backgroundView)
          self.present(liveAudioVC, animated: true, completion: nil)
      }
  }
  ```
:::