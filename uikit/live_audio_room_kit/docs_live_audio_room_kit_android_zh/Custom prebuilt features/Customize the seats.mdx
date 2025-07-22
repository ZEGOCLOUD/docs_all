# 自定义麦位

## 指定用户麦位

**语聊房 UIKit（Live Audio Room Kit）** 支持为语聊房中的角色设置指定麦位，主要接口如下：

1. `takeSeatIndexWhenJoining`：当加入语聊房时（对于主持人和发言人），使用此选项自动设置用户所坐的麦位。
2. `hostSeatIndexes`：仅用于设置 **主持人** 的特殊麦位（不允许发言人和观众就坐）。

## 自定义麦位布局

语聊房 UIKit 的布局方式，与行和对齐方式相关，如需自定义麦位布局，请参考以下说明：

- `ZegoLiveAudioRoomLayoutConfig`:
:::if{props.platform=undefined}
    1. `rowConfigs`(List< ZegoLiveAudioRoomLayoutRowConfig >): 有多少行，以及每行的配置方式。
:::
:::if{props.platform="iOS"}
    1. `rowConfigs`([ZegoLiveAudioRoomLayoutRowConfig]): 有多少行，以及每行的配置方式。
:::
    2. `rowSpacing`(int): 每行的间距，必须 ≥ 0。
  
- `ZegoLiveAudioRoomLayoutRowConfig`:
    1. `count`(int): 每行的麦位数，范围 [1 - 4]。
    2. `seatSpacing`(int): 每个麦位的水平间距，必须 ≥ 0（仅当对齐方式为 `FLEX_START`、`FLEX_END` 和 `CENTER` 时生效）。
    3. `alignment`(ZegoLiveAudioRoomLayoutAlignment): 为列设置的对齐方式。

:::if{props.platform=undefined}
- `ZegoLiveAudioRoomLayoutAlignment`:
    1. `FLEX_START`: 将麦位尽可能靠近起始位置。
    2. `FLEX_END`: 将麦位尽可能靠近结束位置。
    3. `CENTER`: 将麦位尽可能靠中间位置。
    4. `SPACE_BETWEEN`: 在麦位之间均匀分布剩余空间。
    5. `SPACE_AROUND`: 在麦位之间均匀分布剩余空间，并在第一个和最后一个麦位之前和之后分布一半的空间。
    6. `SPACE_EVENLY`: 在麦位之间均匀分布剩余空间，并在第一个和最后一个麦位之前和之后分布相同的空间。
:::
:::if{props.platform="iOS"}
    1. `start`: 将麦位尽可能靠近起始位置。
    2. `end`: 将麦位尽可能靠近结束位置。
    3. `center`: 将麦位尽可能靠中间位置。
    4. `spaceBetween`: 在麦位之间均匀分布剩余空间。
    5. `spaceAround`: 在麦位之间均匀分布剩余空间，并在第一个和最后一个麦位之前和之后分布一半的空间。
    6. `spaceEvenly`: 在麦位之间均匀分布剩余空间，并在第一个和最后一个麦位之前和之后分布相同的空间。
:::

    六种 `alignment` 效果如下：

<div style={{width:"100%",display:"flex",gap:"10px"}}>
    <div style={{width:"30%"}}>
        <Frame width="auto" height="auto" caption="">
            <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/alignment_2.jpeg" />
        </Frame>
    </div>
    <div style={{width:"30%"}}>
        <Frame width="auto" height="auto" caption="">
            <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/alignment_1.jpeg" />
        </Frame>
    </div>
</div>

以如下麦位设置为例，举例说明自定义设置的实现方式：

1. 第一行的唯一麦位，设置为主持人的特殊麦位。
:::if{props.platform=undefined}
2. 第二行和第三行的麦位数为 4，对齐方式为 `SPACE_AROUND`。
:::
:::if{props.platform="iOS"}
2. 第二行和第三行的麦位数为 4，对齐方式为 `spaceAround`。
:::

<div style={{width:"30%"}}>
    <Frame width="auto%" height="auto" caption="">
        <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/custom_layout.jpeg" />
    </Frame>
</div>

:::if{props.platform=undefined}
<CodeGroup>
```java Java
public class LiveAudioRoomActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_call);

        addFragment();
    }

    public void addFragment() {
        long appID = yourAppID;
        String appSign = yourAppSign;
        String userID = yourUserID;
        String userName = yourUserName;

        boolean isHost = getIntent().getBooleanExtra("host", false);
        String roomID = getIntent().getStringExtra("roomID");

        ZegoUIKitPrebuiltLiveAudioRoomConfig config;
        if (isHost) {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
            config.takeSeatIndexWhenJoining = 0;
        } else {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
        }

        config.hostSeatIndexes = Collections.singletonList(0);
        config.layoutConfig.rowConfigs = Arrays.asList(
                new ZegoLiveAudioRoomLayoutRowConfig(1, ZegoLiveAudioRoomLayoutAlignment.CENTER),
                new ZegoLiveAudioRoomLayoutRowConfig(4, ZegoLiveAudioRoomLayoutAlignment.SPACE_AROUND),
                new ZegoLiveAudioRoomLayoutRowConfig(4, ZegoLiveAudioRoomLayoutAlignment.SPACE_AROUND));

        ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
            appID, appSign, userID, userName,roomID,config);
        getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
    }
}
```

```kotlin Kotlin
class LiveAudioRoomActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_live)
        addFragment()
    }

    private fun addFragment() {
        val appID: Long = yourAppID
        val appSign = yourAppSign
        val userID = YourUserID
        val userName = YourUserName
        
        val isHost = intent.getBooleanExtra("host", false)
        val roomID = intent.getStringExtra("roomID")

        val config: ZegoUIKitPrebuiltLiveAudioRoomConfig
        if (isHost) {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
            config.takeSeatIndexWhenJoining = 0
        } else {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
        }
        config.hostSeatIndexes = listOf(0)
        config.layoutConfig.rowConfigs = Arrays.asList<Any>(
            ZegoLiveAudioRoomLayoutRowConfig(1, ZegoLiveAudioRoomLayoutAlignment.CENTER),
            ZegoLiveAudioRoomLayoutRowConfig(4, ZegoLiveAudioRoomLayoutAlignment.SPACE_AROUND),
            ZegoLiveAudioRoomLayoutRowConfig(4, ZegoLiveAudioRoomLayoutAlignment.SPACE_AROUND)
        )

        val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
            appID, appSign, userID, userName, roomID, config
        )
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
```Swift
class ViewController: UIViewController {

    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID
    let yourAppSign: String = "YourAppSign"
    let roomID: String = "YourRoomID"

    @IBAction func startLiveAudio(_ sender: Any) {

        // Modify your custom configurations here.
        let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        let layoutConfig: ZegoLiveAudioRoomLayoutConfig = ZegoLiveAudioRoomLayoutConfig()
        layoutConfig.rowSpecing = 5
        
        let rowConfig0: ZegoLiveAudioRoomLayoutRowConfig = ZegoLiveAudioRoomLayoutRowConfig()
        rowConfig0.count = 1
        rowConfig0.alignment = .center
        
        let rowConfig1: ZegoLiveAudioRoomLayoutRowConfig = ZegoLiveAudioRoomLayoutRowConfig()
        rowConfig1.count = 4
        rowConfig1.alignment = .spaceAround
        
        let rowConfig2: ZegoLiveAudioRoomLayoutRowConfig = ZegoLiveAudioRoomLayoutRowConfig()
        rowConfig2.count = 4
        rowConfig2.alignment = .spaceAround
        
        layoutConfig.rowConfigs = [rowConfig0,rowConfig1, rowConfig2]
        layoutConfig.rowSpecing = 0
        config.layoutConfig = layoutConfig
  
        let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)

        liveAudioVC.modalPresentationStyle = .fullScreen
        self.present(liveAudioVC, animated: true, completion: nil)
    }
}
```
:::

## 自定义麦位的 UI

默认情况下，麦位的用户界面会显示围绕用户头像的声浪。

如果您对声浪样式不满意，或者想自定义前景和背景视图，请相应地使用`seatConfig`中的配置。

### 隐藏声浪

默认情况下，声浪会显示出来，如果要隐藏它，请使用`showSoundWaveInAudioMode`配置。

`showSoundWaveInAudioMode`: 使用此选项来决定是否显示用户头像周围的声浪。默认情况下显示。

以下是参考代码：

:::if{props.platform=undefined}
<CodeGroup>
```java Java
public class LiveAudioRoomActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_call);

        addFragment();
    }

    public void addFragment() {
        long appID = yourAppID;
        String appSign = yourAppSign;
        String userID = yourUserID;
        String userName = yourUserName;

        boolean isHost = getIntent().getBooleanExtra("host", false);
        String roomID = getIntent().getStringExtra("roomID");

        ZegoUIKitPrebuiltLiveAudioRoomConfig config;
        if (isHost) {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
        } else {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
        }

        config.seatConfig.showSoundWaveInAudioMode = false;

        ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
            appID, appSign, userID, userName,roomID,config);
        getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
    }
}
```

```kotlin Kotlin
class LiveAudioRoomActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_live)
        addFragment()
    }

    private fun addFragment() {
        val appID: Long = yourAppID
        val appSign = yourAppSign
        val userID = YourUserID
        val userName = YourUserName
        
        val isHost = intent.getBooleanExtra("host", false)
        val roomID = intent.getStringExtra("roomID")

        val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        } else {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
        }

        config.seatConfig.showSoundWaveInAudioMode = false

        val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(
            appID, appSign, userID, userName, roomID, config
        )
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
```Swift
class ViewController: UIViewController {

    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID
    let yourAppSign: String = "YourAppSign"
    let roomID: String = "YourRoomID"

    @IBAction func startLiveAudio(_ sender: Any) {

        // Modify your custom configurations here.
        let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        config.seatConfig.showSoundWaveInAudioMode = false
        let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)

        liveAudioVC.modalPresentationStyle = .fullScreen
        self.present(liveAudioVC, animated: true, completion: nil)
    }
}
```
:::

### 自定义麦位的前景或背景视图

:::if{props.platform=undefined}
要自定义用户麦位的视图，请根据需要在`seatConfig`中设置以下属性。

- `foregroundViewProvider`：使用此属性自定义组件或者在视图的顶层添加一些自定义组件，例如显示用户级别的图标。
- `backgroundColor`：使用此属性自定义背景颜色。
- `backgroundImage`：使用此属性自定义背景图像。
:::
:::if{props.platform="iOS"}
要自定义麦位的背景视图，请使用以下属性：

1. `backgroundColor`：使用此属性自定义背景颜色。
2. `backgroundImage`：使用此属性自定义背景图片。

要自定义用户麦位的前景视图，您需要声明 delegate 并实现 `getSeatForegroundView` 方法。
:::

以下是效果和参考代码的示例：

<div style={{width:"30%"}}>
    <Frame width="auto" height="auto" caption="">
        <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/custom_bg_fg.gif" />
    </Frame>
</div>

:::if{props.platform=undefined}
<CodeGroup>
```java Java
public class LiveAudioRoomActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_call);

        addFragment();
    }

    public void addFragment() {
        long appID = yourAppID;
        String appSign = yourAppSign;
        String userID = yourUserID;
        String userName = yourUserName;

        boolean isHost = getIntent().getBooleanExtra("host", false);
        String roomID = getIntent().getStringExtra("roomID");

        ZegoUIKitPrebuiltLiveAudioRoomConfig config;
        if (isHost) {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
        } else {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
        }
        config.seatConfig.backgroundColor = 0xffcccccc;
        config.seatConfig.foregroundViewProvider = new ZegoLiveAudioRoomSeatForegroundViewProvider() {
            @Override
            public ZegoBaseAudioVideoForegroundView getForegroundView(ViewGroup parent, ZegoUIKitUser uiKitUser, int seatIndex) {
                return new YourCustomAudioForegroundView(parent.getContext(), uiKitUser,seatIndex);
            }
        };

        ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName,roomID,config);
        getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
    }
}
```

```kotlin Kotlin
class LiveAudioRoomActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_live)
        addFragment()
    }

    private fun addFragment() {
        val appID: Long = yourAppID
        val appSign = yourAppSign
        val userID = YourUserID
        val userName = YourUserName
        
        val isHost = intent.getBooleanExtra("host", false)
        val roomID = intent.getStringExtra("roomID")

        val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        } else {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
        }

      config.seatConfig.backgroundColor = 0xffcccccc
      config.seatConfig.foregroundViewProvider = object : ZegoLiveAudioRoomSeatForegroundViewProvider() {
            fun getForegroundView(parent:ViewGroup,uiKitUser: ZegoUIKitUser?,seatIndex: int): ZegoBaseAudioVideoForegroundView {
                return YourCustomAudioForegroundView(parent.context, uiKitUser, seatIndex)
            }
        }

        val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>
:::
:::if{props.platform="iOS"}
```Swift
class ViewController: UIViewController {

    let selfUserID: String = "userID"
    let selfUserName: String = "userName"
    let yourAppID: UInt32 = YourAppID
    let yourAppSign: String = "YourAppSign"
    let roomID: String = "YourRoomID"

    @IBAction func startLiveAudio(_ sender: Any) {

        // Modify your custom configurations here.
        let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        config.seatConfig.backgroudColor = <#Your backgroudColor#>
        config.seatConfig.backgroundImage = <#Your image#>
        let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)
        liveAudioVC.delegate = self
        liveAudioVC.modalPresentationStyle = .fullScreen
        self.present(liveAudioVC, animated: true, completion: nil)
    }
}

extension ViewController : ZegoUIKitPrebuiltLiveAudioRoomVCDelegate {
    func getSeatForegroundView(_ userInfo: ZegoUIKitUser?, seatIndex: Int) -> UIView? {
        return YourCustomVideoForegroundView
    }
}
```
:::

:::if{props.platform=undefined}
### 自定义麦位打开/关闭状态对应的图标

要自定义麦位打开/关闭状态对应的图标，请根据需要在`seatConfig`中中设置以下属性。

- `openIcon`：使用此属性自定义麦位的打开图标，通常显示为麦位的默认图标。
- `closeIcon`：使用此属性自定义麦位的关闭图标，当主持人关闭麦位时显示。

以下是参考代码：

<CodeGroup>
```java Java
public class LiveAudioRoomActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_call);

        addFragment();
    }

    public void addFragment() {
        long appID = yourAppID;
        String appSign = yourAppSign;
        String userID = yourUserID;
        String userName = yourUserName;

        boolean isHost = getIntent().getBooleanExtra("host", false);
        String roomID = getIntent().getStringExtra("roomID");

        ZegoUIKitPrebuiltLiveAudioRoomConfig config;
        if (isHost) {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.host();
        } else {
            config = ZegoUIKitPrebuiltLiveAudioRoomConfig.audience();
        }
        config.seatConfig.openIcon = yourOpenDrawable;
        config.seatConfig.closeIcon = yourCloseDrawable;       
     

        ZegoUIKitPrebuiltLiveAudioRoomFragment fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName,roomID,config);
        getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow();
    }
}
```

```kotlin Kotlin
class LiveAudioRoomActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_live)
        addFragment()
    }

    private fun addFragment() {
        val appID: Long = yourAppID
        val appSign = yourAppSign
        val userID = YourUserID
        val userName = YourUserName
        
        val isHost = intent.getBooleanExtra("host", false)
        val roomID = intent.getStringExtra("roomID")

        val config: ZegoUIKitPrebuiltLiveAudioRoomConfig = if (isHost) {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
        } else {
            ZegoUIKitPrebuiltLiveAudioRoomConfig.audience()
        }

      config.seatConfig.openIcon = yourOpenDrawable;
      config.seatConfig.closeIcon = yourCloseDrawable;       
     

        val fragment = ZegoUIKitPrebuiltLiveAudioRoomFragment.newInstance(appID, appSign, userID, userName, roomID, config)
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commitNow()
    }
}
```
</CodeGroup>
:::
