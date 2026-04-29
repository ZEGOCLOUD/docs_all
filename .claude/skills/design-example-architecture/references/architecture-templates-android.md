# Android 示例代码架构模板

基于"单文件实现"原则的 Android 示例代码架构模板。

## 项目结构

```
VideoCall-Example/
├── app/
│   └── src/
│       └── main/
│           ├── java/com/zego/express/demo/helloworld/
│           │   └── MainActivity.java           # 主界面（所有逻辑在此文件）
│           ├── res/layout/
│           │   └── activity_main.xml           # 界面布局（含输入框）
│           └── AndroidManifest.xml
├── local.properties.example                   # 环境变量示例
├── build.gradle.kts
└── README.md
```

## 配置管理

### build.gradle.kts（读取 local.properties）

```kotlin
android {
    defaultConfig {
        // 从 local.properties 读取配置 / Read config from local.properties
        val appId = project.findProperty("ZEGO_APP_ID")?.toString() ?: "0"
        val apiBaseUrl = project.findProperty("ZEGO_API_BASE_URL")?.toString() ?: "http://localhost:3000"

        buildConfigField("long", "ZEGO_APP_ID", appId)
        buildConfigField("String", "ZEGO_API_BASE_URL", "\"$apiBaseUrl\"")
    }
}

buildFeatures {
    buildConfig = true
}
```

### local.properties.example

```properties
# ZEGO 配置 / ZEGO Configuration
# 从即构控制台获取: https://console.zego.im
# Get from ZEGO console: https://console.zegocloud.com
ZEGO_APP_ID=1234567890

# 业务后台地址 / Backend API address
ZEGO_API_BASE_URL=http://localhost:3000
```

### MainActivity.java（配置检查）

```java
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 检查配置 / Check configuration
        if (BuildConfig.ZEGO_APP_ID == 0L) {
            Toast.makeText(this, "Please configure ZEGO_APP_ID in local.properties", Toast.LENGTH_LONG).show();
            return;
        }

        // 创建引擎 / Create engine
        ZegoEngineProfile profile = new ZegoEngineProfile();
        profile.appID = BuildConfig.ZEGO_APP_ID;
        // ...
    }
}
```

## MainActivity.java（完整示例）

```java
public class MainActivity extends AppCompatActivity {

    // ========== 成员变量 / Member variables ==========
    ZegoExpressEngine engine;
    RequestQueue requestQueue;

    private EditText etRoomId;
    private EditText etUserId;
    private EditText etUserName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 初始化视图 / Initialize views
        etRoomId = findViewById(R.id.etRoomId);
        etUserId = findViewById(R.id.etUserId);
        etUserName = findViewById(R.id.etUserName);

        requestQueue = Volley.newRequestQueue(this);

        // 开始通话按钮 - 直接调用 SDK / Start call button - direct SDK calls
        findViewById(R.id.startButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String roomID = etRoomId.getText().toString();
                String userID = etUserId.getText().toString();
                String userName = etUserName.getText().toString();

                if (TextUtils.isEmpty(roomID) || TextUtils.isEmpty(userID)) {
                    Toast.makeText(MainActivity.this, "请填写房间ID和用户ID / Please enter Room ID and User ID", Toast.LENGTH_LONG).show();
                    return;
                }

                createEngine();           // 创建引擎 / Create engine
                setEventHandler();       // 设置回调 / Set event handler
                loginRoomWithToken(roomID, userID, userName);  // 使用 Token 登录房间 / Login room with token
            }
        });

        // 停止通话按钮 / Stop call button
        findViewById(R.id.stopButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (engine != null) {
                    engine.logoutRoom();
                    ZegoExpressEngine.destroyEngine(new IZegoDestroyCompletionCallback() {
                        @Override
                        public void onDestroyCompletion() {
                            // 销毁成功 / Destroy completed
                        }
                    });
                    engine = null;
                }
            }
        });
    }

    // ========== 创建引擎（直接调用 SDK）/ Create engine (direct SDK call) ==========
    void createEngine() {
        ZegoEngineProfile profile = new ZegoEngineProfile();
        profile.appID = BuildConfig.ZEGO_APP_ID;
        profile.scenario = ZegoScenario.DEFAULT;
        profile.application = getApplication();
        engine = ZegoExpressEngine.createEngine(profile, null);
    }

    // ========== 从服务端获取 Token 并登录房间 / Get token from server and login room ==========
    void loginRoomWithToken(String roomID, String userID, String userName) {
        String url = AppConfig.TOKEN_SERVER_URL + "/api/token";

        Map<String, String> params = new HashMap<>();
        params.put("roomId", roomID);
        params.put("userId", userID);

        JSONObject jsonObject = new JSONObject(params);

        JsonObjectRequest request = new JsonObjectRequest(
            Request.Method.POST,
            url,
            jsonObject,
            response -> {
                String token = response.optString("token");
                if (!TextUtils.isEmpty(token)) {
                    doLoginRoom(roomID, userID, userName, token);
                }
            },
            error -> {
                Toast.makeText(this, "获取 Token 失败 / Failed to get token: " + error.getMessage(), Toast.LENGTH_LONG).show();
            }
        );

        requestQueue.add(request);
    }

    // ========== 执行登录房间操作 / Execute login room ==========
    void doLoginRoom(String roomID, String userID, String userName, String token) {
        ZegoUser user = new ZegoUser(userID, userName);

        ZegoRoomConfig roomConfig = new ZegoRoomConfig();
        roomConfig.token = token;
        roomConfig.isUserStatusNotify = true;

        engine.loginRoom(roomID, user, roomConfig, (int error, JSONObject extendedData) -> {
            if (error == 0) {
                Toast.makeText(this, "登录成功 / Login success", Toast.LENGTH_LONG).show();
                startPublish();
            } else {
                Toast.makeText(this, "登录失败 / Login failed: " + error, Toast.LENGTH_LONG).show();
            }
        });
    }

    // ========== 预览并推流（直接调用 SDK）/ Preview and publish (direct SDK call) ==========
    void startPublish() {
        ZegoCanvas previewCanvas = new ZegoCanvas(findViewById(R.id.previewView));
        engine.startPreview(previewCanvas);

        String streamID = etUserId.getText().toString();
        engine.startPublishingStream(streamID);
    }

    // ========== 设置事件回调（直接在 Activity 内实现）/ Set event handler ==========
    void setEventHandler() {
        engine.setEventHandler(new IZegoEventHandler() {

            @Override
            public void onRoomStreamUpdate(String roomID, ZegoUpdateType updateType,
                    ArrayList<ZegoStream> streamList, JSONObject extendedData) {
                super.onRoomStreamUpdate(roomID, updateType, streamList, extendedData);
                if (updateType == ZegoUpdateType.ADD) {
                    for (ZegoStream stream : streamList) {
                        ZegoCanvas playCanvas = new ZegoCanvas(findViewById(R.id.remoteView));
                        engine.startPlayingStream(stream.streamID, playCanvas);
                    }
                } else if (updateType == ZegoUpdateType.DELETE) {
                    for (ZegoStream stream : streamList) {
                        engine.stopPlayingStream(stream.streamID);
                    }
                }
            }

            @Override
            public void onRoomStateChanged(String roomID, ZegoRoomStateChangedReason reason,
                    int errorCode, JSONObject jsonObject) {
                super.onRoomStateChanged(roomID, reason, errorCode, jsonObject);
                if (reason == ZegoRoomStateChangedReason.LOGINED) {
                    // 登录房间成功 / Login room success
                } else if (reason == ZegoRoomStateChangedReason.LOGIN_FAILED) {
                    Toast.makeText(MainActivity.this,
                        "登录失败 / Login failed: " + errorCode, Toast.LENGTH_LONG).show();
                }
            }
        });
    }
}
```

## 关键点说明

1. **所有 SDK 调用都在 MainActivity 内完成**
2. **回调通过匿名内部类直接实现**
3. **AppID 从 BuildConfig 读取，不硬编码**
4. **RoomID、UserID 通过页面输入获取**
5. **Token 从服务端 API 获取**
