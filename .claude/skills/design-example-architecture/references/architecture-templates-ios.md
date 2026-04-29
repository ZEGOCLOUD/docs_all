# iOS 示例代码架构模板

基于"单文件实现"原则的 iOS 示例代码架构模板。

## 项目结构

```
VideoCall-Example/
├── VideoCall-Example/
│   ├── ViewController.m           # 主视图控制器（所有逻辑在此文件）
│   ├── Config.h/m                 # 配置文件（直接编辑）
│   ├── Info.plist                 # 权限配置
│   └── AppDelegate.h/m            # 应用入口
├── Podfile                        # CocoaPods 依赖
└── README.md
```

## 配置管理

### Config.h / Config.m（直接编辑）

iOS 示例代码使用 Config.h/m 直接存储配置值，用户直接编辑 .m 文件中的值。

**Config.h**:

```objc
#import <Foundation/Foundation.h>

/**
 * 客户端配置 / Client configuration
 */
@interface Config : NSObject

// 从即构控制台获取: https://console.zegocloud.com
// Get from ZEGO console: https://console.zegocloud.com
@property (class, nonatomic, readonly) NSUInteger ZEGO_APP_ID;

// 业务后台地址 / Backend API address
@property (class, nonatomic, readonly) NSString *ZEGO_API_BASE_URL;

@end
```

**Config.m**:

```objc
#import "Config.h"

@implementation Config

+ (NSUInteger)ZEGO_APP_ID {
    // 从即构控制台获取: https://console.zegocloud.com
    // Get from ZEGO console: https://console.zegocloud.com
    return 1234567890;
}

+ (NSString *)ZEGO_API_BASE_URL {
    return @"http://localhost:3000";
}

@end
```

### ViewController.m（配置检查）

```objc
#import "Config.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    // 检查配置 / Check configuration
    if ([Config ZEGO_APP_ID] == 0) {
        [self updateStatus:@"Please configure ZEGO_APP_ID in Config.m"];
        return;
    }

    // 创建引擎 / Create engine
    ZegoEngineProfile *profile = [[ZegoEngineProfile alloc] init];
    profile.appID = [Config ZEGO_APP_ID];
    // ...
}

@end
```

## ViewController.m（完整示例）

```objc
#import "ViewController.h"
#import "Config.h"
#import <ZegoExpressEngine/ZegoExpressEngine.h>

@interface ViewController () <ZegoEventHandler>

@property (nonatomic, strong) ZegoExpressEngine *engine;
@property (nonatomic, strong) ZegoDigitalView *digitalHumanView;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    // 检查配置 / Check configuration
    if ([Config ZEGO_APP_ID] == 0) {
        NSLog(@"Please configure ZEGO_APP_ID in Config.m");
        return;
    }

    // 初始化SDK / Initialize SDK
    [self initSDK];

    // 开始业务流程 / Start business flow
    [self startCall];
}

// ========== 创建引擎（直接调用 SDK）/ Create engine (direct SDK call) ==========
- (void)initSDK {
    ZegoEngineProfile *profile = [[ZegoEngineProfile alloc] init];
    profile.appID = [Config ZEGO_APP_ID];
    profile.scenario = ZegoScenarioDefault;
    profile.application = [UIApplication sharedApplication];

    self.engine = [ZegoExpressEngine createEngineWithProfile:profile eventHandler:self];
}

// ========== 从服务端获取 Token 并登录房间 / Get token from server and login room ==========
- (void)loginRoomWithToken:(NSString *)roomID userID:(NSString *)userID {
    NSString *urlString = [NSString stringWithFormat:@"%@/api/token", [Config ZEGO_API_BASE_URL]];
    NSURL *url = [NSURL URLWithString:urlString];

    // 构建请求 / Build request
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    request.HTTPMethod = @"POST";

    NSDictionary *params = @{@"roomId": roomID, @"userId": userID};
    NSError *error;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:params options:0 error:&error];
    request.HTTPBody = jsonData;

    // 发送请求 / Send request
    NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithRequest:request
        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error) {
            NSLog(@"获取 Token 失败 / Failed to get token: %@", error);
            return;
        }

        NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
        NSString *token = json[@"token"];

        if (token) {
            [self doLoginRoom:roomID userID:userID userName:userID token:token];
        }
    }];
    [task resume];
}

// ========== 执行登录房间操作 / Execute login room ==========
- (void)doLoginRoom:(NSString *)roomID userID:(NSString *)userID userName:(NSString *)userName token:(NSString *)token {
    ZegoUser *user = [[ZegoUser alloc] initWithUserID:userID userName:userName];

    ZegoRoomConfig *roomConfig = [[ZegoRoomConfig alloc] init];
    roomConfig.token = token;
    roomConfig.isUserStatusNotify = YES;

    [self.engine loginRoom:roomID user:user config:roomConfig callback:^(int errorCode) {
        if (errorCode == 0) {
            NSLog(@"登录成功 / Login success");
            [self startPublish];
        } else {
            NSLog(@"登录失败 / Login failed: %d", errorCode);
        }
    }];
}

// ========== 预览并推流（直接调用 SDK）/ Preview and publish (direct SDK call) ==========
- (void)startPublish {
    ZegoCanvas *previewCanvas = [[ZegoCanvas alloc] initWithView:self.previewView];
    [self.engine startPreview:previewCanvas];

    NSString *streamID = self.currentUserId;
    [self.engine startPublishingStream:streamID];
}

// ========== 设置事件回调（直接在 ViewController 内实现）/ Set event handler ==========
#pragma mark - ZegoEventHandler

- (void)onRoomStreamUpdate:(NSString *)roomID
                updateType:(ZegoUpdateType)updateType
                 streamList:(NSArray<ZegoStream *> *)streamList
              extendedData:(NSDictionary *)extendedData {
    if (updateType == ZegoUpdateTypeAdd) {
        for (ZegoStream *stream in streamList) {
            ZegoCanvas *playCanvas = [[ZegoCanvas alloc] initWithView:self.remoteView];
            [self.engine startPlayingStream:stream.streamID canvas:playCanvas];
        }
    } else if (updateType == ZegoUpdateTypeDelete) {
        for (ZegoStream *stream in streamList) {
            [self.engine stopPlayingStream:stream.streamID];
        }
    }
}

- (void)onRoomStateChanged:(NSString *)roomID
                    reason:(ZegoRoomStateChangedReason)reason
                 errorCode:(int)errorCode
                   message:(NSString *)message {
    if (reason == ZegoRoomStateChangedReasonLogined) {
        // 登录房间成功 / Login room success
    } else if (reason == ZegoRoomStateChangedReasonLoginFailed) {
        NSLog(@"登录失败 / Login failed: %d", errorCode);
    }
}

- (void)dealloc {
    [self.engine logoutRoom];
    [ZegoExpressEngine destroyEngine:nil];
}

@end
```

## 关键点说明

1. **所有 SDK 调用都在 ViewController 内完成**
2. **回调通过 protocol 直接在 ViewController 内实现**
3. **AppID 从 Config 类读取，用户直接编辑 Config.m**
4. **RoomID、UserID 通过页面输入或 API 获取**
5. **Token 从服务端 API 获取**
