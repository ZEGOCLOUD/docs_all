## 前提条件

在实现同步播放视频之前，请确保：

- 已在 [ZEGO 控制台](https://console.zego.im) 创建项目，并申请有效的 AppID 和 AppSign，详情请参考 [控制台 - 项目管理 - 项目信息](#12107)。
- 已在项目中集成 ZegoAccurateSyncMediaPlayer SDK，详情请参考 [精准同步播放器 - 快速开始 - 集成 SDK](!ZegoAccurateSyncMediaPlayerSDK-Integrated_CopyrightedVideo_SDK)。
- 已在项目中集成 ZEGO Express SDK，实现基本的实时音视频功能，详情请参考 [精准同步播放器 - 快速开始 - 集成 SDK](!ZegoAccurateSyncMediaPlayerSDK-Integrated_CopyrightedVideo_SDK)。


## 示例 Demo

ZEGO 提供了[示例 Demo](!DownloadDemo/DownloadDemo)，以供开发者进一步了解。

## 实现流程

![/Pics/iOS/ZegoCopyrightedVideo/Third_Party_Video_Resource_Implementation_Host.png](https://storage.zego.im/sdk-doc/Pics/iOS/ZegoCopyrightedVideo/Third_Party_Video_Resource_Implementation_Host.png)

### 1 开通服务

在实现影视资源同步播放之前，请联系 ZEGO 商务人员开通服务。

### 2 初始化 Express SDK

<div class="mk-warning">

实现影视资源同步播放时，ZegoAccurateSyncMediaPlayer SDK 的信令传输，是基于 ZEGO Express SDK 的房间信令通道实现的，所以首先，开发者需要初始化 ZEGO Express SDK。
</div>

1. 创建界面。根据场景需要，为你的项目播放视频的用户界面。我们推荐你在项目中添加如下元素：

    - 播放视频窗口
    - 操作按钮（包含播放，暂停，进度条等功能）

2. 在项目中引入 ZEGO Express 头文件。   
```objc
// 引入 ZegoExpressEngine.h 头文件
#import <ZegoExpressEngine/ZegoExpressEngine.h>
```

3. 创建引擎。   
调用 ZEGO Express SDK 的 [createEngineWithProfile](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~class~ZegoExpressEngine#create-engine-with-profile-event-handler) 接口，将申请到的 AppID 和 AppSign 分别传入参数“appID”和“appSign”，创建引擎单例对象。   
注册回调，可将实现了 [ZegoEventHandler](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~protocol~ZegoEventHandler) 的对象（例如 “self”）传入参数 “eventHandler”。   
```objc
ZegoEngineProfile *profile = [[ZegoEngineProfile alloc] init];
// 请通过 ZEGO 控制台获取，格式为：1234567890
profile.appID = <#appID#>;
// 请通过 ZEGO 控制台获取，格式为：@"0123456789012345678901234567890123456789012345678901234567890123"（共64个字符）
profile.appSign = <#appSign#>; 
// 实时通讯场景接入
profile.scenario = ZegoScenarioCommunication; 
// 创建引擎，并注册 self 为 eventHandler 回调。不需要注册回调的话，eventHandler 参数可以传 nil，后续可调用 "-setEventHandler:" 方法设置回调
[ZegoExpressEngine createEngineWithProfile:profile eventHandler:self];
```

### 3 初始化 ZegoAccurateSyncMediaPlayer SDK

1. 在项目中引入 ZegoAccurateSyncMediaPlayer 头文件。

    ```objc
    // 引入 ZegoAccurateSyncMediaPlayer.h 头文件
    #import <ZegoAccurateSyncMediaPlayer/ZegoAccurateSyncMediaPlayer.h>
    ```

2. 调用 ZegoAccurateSyncMediaPlayer SDK 的 [init](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSync#init-config-callback) 接口，传入 userID，设置用户角色为 “ZegoAccurateSyncUserRoleHost”，初始化 ZegoAccurateSyncMediaPlayer SDK。

    <div class="mk-hint">

    同一个 AppID 内，需保证 “userID” 全局唯一，建议开发者将 “userID” 与自己业务的账号系统进行关联。

    </div>

    ```objc
    ZegoAccurateSyncConfig * confg = [ZegoAccurateSyncConfig new];
    // 请通过官网注册获取，格式为：1234567890
    confg.appID = [ZegoEnvManager shareManager].appID; 
    //设置用户为ZegoAccurateSyncUserRoleHost 主持人角色（ZegoAccurateSyncUserRoleAudience为观众角色，所有观众会同步主持人的进度一个房间内最好只设置一个主持人角色）
    confg.role = ZegoAccurateSyncUserRoleHost; 
    //设置用户ID，根据自己业务需求设置对应用户ID，用于统计
    confg.userID =  @"";
    
    // 初始化，并注册 self 为 eventHandler 回调。不需要注册回调的话，eventHandler 参数可以传 nil，后续可调用 "-setEventHandler:" 方法设置回调
    [[ZegoAccurateSync sharedManager] init:confg callback:^(enum ZegoAccurateSyncError errorCode, NSDictionary * _Nonnull response) {}];
    [[ZegoAccurateSync sharedManager] setEventHandler:self];
    ```

### 4 登录房间

调用 ZEGO Express SDK 的 [loginRoom](https://doc-zh.zego.im/article/api?doc=express-video-sdk_API~objectivec_ios~class~ZegoExpressEngine#login-room-user) 接口登录房间。roomID 和 userID 的参数由开发者的本地业务生成，但是需要满足以下条件：
- 同一个 AppID 内，需保证 “roomID” 全局唯一。  
- 需要和 <a href="#4_3">3 初始化 ZegoAccurateSyncMediaPlayer SDK</a> 中的 userID 一致。

```objc
// roomID 由您本地生成,需保证 “roomID” 全局唯一。不同用户要登陆同一个房间才能进行通话
NSString *roomID = @"room1";

// 创建用户对象，ZegoUser 的构造方法 userWithUserID 会将 “userName” 设为与传的参数 “userID” 一样。“userID” 与 “userName” 不能为 “nil”，否则会导致登录房间失败。
ZegoUser *user = [ZegoUser userWithUserID:@"user1"];

ZegoRoomConfig *roomConfig = [[ZegoRoomConfig alloc] init];

//如果您使用 appSign 的方式鉴权，token 参数不需填写；如果需要使用更加安全的 鉴权方式： token 鉴权，请参考[如何从 AppSign 鉴权升级为 Token 鉴权](https://doc-zh.zego.im/faq/token_upgrade?product=ExpressVideo&platform=all)
// roomConfig.token = @"<#token#>";

// 登录房间
[[ZegoExpressEngine sharedEngine] loginRoom:roomID user:user config:roomConfig callback:^(int errorCode, NSDictionary * _Nullable extendedData) {
    // (可选回调) 登录房间结果，如果仅关注登录结果，关注此回调即可
}];
```

<div class="mk-warning">

必须收到 [onRoomStateChanged](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~protocol~ZegoEventHandler#on-room-state-changed-error-code-extended-data-room-id) 指示登录房间成功，后续才能成功 <a href="#4_6">加载视频</a>。
</div>

### 5 透传房间附加消息

在 ZEGO Express SDK 的 [ZegoEventHandler](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~protocol~ZegoEventHandler) 回调中，注册 [onRoomExtraInfoUpdate](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~protocol~ZegoEventHandler#on-room-extra-info-update-room-id) 监听，将房间内的附加消息，透传给 ZegoAccurateSyncMediaPlayer SDK。再调用 ZegoAccurateSyncMediaPlayer SDK 的 [roomExtraInfoUpdated](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSync#room-extra-info-updated-room-id-room-extra-info-list) 接口，同步“主持人端”和“观众端”的视频播放进度。

```objc
- (void)onRoomExtraInfoUpdate:(NSArray<ZegoRoomExtraInfo *> *)roomExtraInfoList roomID:(NSString *)roomID
{
   [[ZegoAccurateSync sharedManager] roomExtraInfoUpdated:roomID roomExtraInfoList:roomExtraInfoList];
}
```

### 6 创建播放器，加载视频资源。

1. 定义播放器。

    ```objc
    @interface ZegoPlayerViewController ()<ZegoAccurateSyncMediaPlayerEventHandler>

    @property (nonatomic, strong) ZegoAccurateSyncMediaPlayer * player;

    @end
    ```

2. 调用 ZegoAccurateSyncMediaPlayer SDK 的 [createMediaPlayer](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSync#create-media-player) 创建播放器，设置播放界面视图。传入视频资源 URL，调用 ZegoAccurateSyncMediaPlayer SDK 的 [loadVideo](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#load-video-play-url-start-position-callback) 接口加载视频。

    <div class="mk-warning">

    - 加载视频前，请确认是否收到 [onRoomStateChanged](https://doc-zh.zego.im/article/api?doc=Express_Video_SDK_API~objective-c_ios~protocol~ZegoEventHandler#on-room-state-changed-error-code-extended-data-room-id) 指示 <a href="#4_4">登录房间</a> 成功，否则可能会导致加载视频失败。
    - 播放器支持的格式有：MP3、MP4、FLV、WAV、AAC、M3U8 和 MKV，如需支持其他格式，请联系 ZEGO 技术支持。
    </div>

    ```objc
    ZegoAccurateSyncMediaPlayer * player = [[ZegoAccurateSync sharedManager] createMediaPlayer];
    //初始化播放视图，self.view可以换成自己想要呈现的播放视图
    ZegoAccurateSyncMediaPlayerCanvas *canvas = [[ZegoAccurateSyncMediaPlayerCanvas alloc] initWithView:self.view];
    //设置播放视图
    [player setPlayerCanvas:canvas];
    //监听player事件，播放状态，进度等
    [player setEventHandler:self];

    //加载视频，URL 为需要播放的视频资源地址。例如：http://trackermv.kugou.com/interface/index?cmd=104&hash=402E2EFD5F0362EFB17B9DED3DED4E08
    //startPosition 一般填0，即从头开始播，但实际情况会根据该影片在房间里的进度来跳转，如果房间里没有播放该视频，则从头开始播放。
    [player loadVideo:URL startPosition:position callback:^(enum ZegoAccurateSyncError errorCode) {}];  

    self.player = player;
    ```

### 7 开始播放

主持人登录房间，并且播放器设置完成后，可以调用 ZegoAccurateSyncMediaPlayer SDK 的 [start](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#start) 接口，开始播放选择的视频资源了。

<div class=mk-warning>

- 只有 [loadVideo](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#load-video-play-url-start-position-callback) 成功后，才能调用 [start](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#start) 开始播放视频。
- 如果在播放视频资源过程中需要切换视频，不能直接调用 [loadVideo](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#load-video-play-url-start-position-callback)，需要先调用 [stop](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#stop) 接口停止播放当前视频，具体做法请参看 <a href="4_10">停止播放</a>。

</div>

```objc
[self.player start];//开始播放
```

### 8 暂停/恢复播放

播放过程中，主持人可以调用 ZegoAccurateSyncMediaPlayer SDK 的 [pause](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#pause) 接口暂停播放，然后调用 [resume](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#resume) 接口恢复播放。

```objc
[self.player pause];//暂停播放

[self.player resume];//恢复播放
```

<div class="mk-hint">

- 主持人端调用 [pause](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#pause) 接口暂停播放时，房间内的所有观众端会同步暂停；调用 [resume](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#resume) 接口恢复播放时，房间内的所有观众端会同步恢复。（如果观众主动点击了暂停按钮，则观众端不会恢复。）
- 观众端也可以调用 [pause](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#pause) 接口暂停播放，但只暂停自己的播放进度，并且不受主持人的影响；观众端调用 [resume](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#resume) 接口恢复播放时，会继续播放视频（如果此时主持人已暂停播放，则观众端的影片仍为暂停状态），但不会同步主持人的视频进度，而是从原来暂停的地方继续播放。

</div>

### 9 跳转到指定时间播放

播放过程中，主持人如果想要改变播放进度，跳转到指定时间的位置播放，可以调用 ZegoAccurateSyncMediaPlayer SDK 的 [seekTo](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#seek-to-millisecond-callback) 接口，传入时间（单位为 ms），进行跳转。

```objc
// your_start_position 为你传入的时间（单位为 ms）
[self.player seekTo:your_start_position callback:^(enum ZegoAccurateSyncError errorCode) {}];
```

### 10 停止播放

播放过程中，主持人可以调用 ZegoAccurateSyncMediaPlayer SDK 的 [stop](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#stop) 接口，直接停止播放。

```objc
[self.player stop];//停止播放
```


## 常用功能

### 播放器播放状态变化回调通知

播放过程中，播放器的状态发生变化时，开发者可以通过以下回调接口，获取相关的状态通知，并在回调中根据不同状态处理业务逻辑。

```objc
// 播放器状态回调，可以在这里更改播放按钮状态
//
// 支持版本 ：v1.0.0。
//
// 详情描述：播放器状态改变或者错误时调用
// @param mediaPlayer 播放器对象
// @param state 播放器状态
// @param errorCode 错误码
- (void)onStateUpdate:(ZegoAccurateSyncMediaPlayer*)mediaPlayer state:(ZegoAccurateSyncMediaPlayerState)state errorCode:(enum ZegoAccurateSyncError)errorCode
{
}

// 播放器网络状况
//
// 支持版本：v1.0.0。
//
// 详情描述：播放器网络状态改变时调用
// @param mediaPlayer 播放器对象
// @param event 网络状况
- (void)onNetworkEvent:(ZegoAccurateSyncMediaPlayer *)mediaPlayer event:(ZegoAccurateSyncMediaPlayerNetworkEvent)event
{
   
}

// 播放器进度回调，可以用来刷新改变当前播放进度
//
// 支持版本：v1.0.0。
//
// 详情描述：播放器进度改变时调用，1000毫秒调用一次
// @param mediaPlayer 播放器对象
// @param millisecond 播放进度
- (void)onPlayingProgress:(ZegoAccurateSyncMediaPlayer *)mediaPlayer progress:(unsigned long long)millisecond
{  
}

// 播放器进度延迟回调，可以用于提示或者调试用
//
// 支持版本：v1.0.0。
//
// 详情描述：播放器进度延迟回调
// @param mediaPlayer 播放器对象
// @param progressGap 与服务端进度误差。正数说明比服务端记录值慢，负数是说明比服务端记录值快，单位为毫秒
- (void)onVideoProgressGapWithServer:(ZegoAccurateSyncMediaPlayer *)mediaPlayer progressGap:(long long)progressGap
{    
    NSString * tip = @"";
    if (progressGap > 0) {
        tip = @"进度比服务器慢";
    }else if (progressGap < 0){
        tip = @"进度比服务器快";
    }
    //当前进度与服务器进度比较
    NSString * gap = [NSString stringWithFormat:@"%@%@ ms",tip,@(llabs(progressGap)).stringValue];
}

// 播放器速度改变通知
//
// 支持版本：v1.1.0。
//
// 详情描述：播放器速度改变通知
// @param mediaPlayer 播放器对象
// @param playSpeed 播放倍速
- (void)onPlayerSpeedChanged:(ZegoAccurateSyncMediaPlayer *)mediaPlayer playSpeed:(float)playSpeed
{

}
```

### 进度同步

主持人注册了 ZegoAccurateSyncMediaPlayer SDK 的 [onVideoProgressGapWithServer](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayerEventHandler#on-video-progress-gap-with-server-media-player-progress-gap) 后，如果在播放过程中，主持人的进度与服务器的进度不同步，主持人会收到相关通知。此时如果主持人调用 ZegoAccurateSyncMediaPlayer SDK 的 [syncServerProgress](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSync#sync-server-progress-video-id) 接口，房间内所有人会向服务器同步进度。

```objc
// videoID 为房间内正在播放的视频的 ID
[[ZegoAccurateSync sharedManager] syncServerProgress:self.player.videoID];
```

<div class="mk-hint">

自定义影视资源的 videoID，需要调用 [loadVideo](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#load-video-play-url-start-position-callback) 接口加载成功后，才能从 ZegoAccurateSyncMediaPlayer 的 属性 [videoID](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSyncMediaPlayer#current-state) 获得。
</div>

### 资源回收

1. 退出房间  
主持人调用 ZEGO Express SDK 的 [logoutRoom](https://doc-zh.zego.im/article/api?doc=express-video-sdk_API~objectivec_ios~class~ZegoExpressEngine#logout-room) 接口，退出房间。

    ```objc
    // 退出房间
    [[ZegoExpressEngine sharedEngine] logoutRoom];
    ```

    <div class="mk-hint">

    主持人退出房间后，如果没有暂停或停止视频播放，房间内的观众可以继续观看当前视频。
    </div>

2. 销毁播放的视频资源  
播放视频结束后，主持人如需销毁本地的视频播放资源，可以调用 ZegoAccurateSyncMediaPlayer SDK 的  [unInit](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~objective-c_ios~class~ZegoAccurateSync#un-init) 接口，销毁本地资源，并反初始化 SDK。

    ```objc
    [[ZegoAccurateSync sharedManager] unInit];
    ```

3. 销毁引擎   
如果退出房间，不需要使用到引擎资源，可以调用 ZEGO Express SDK 的 [destroyEngine](https://doc-zh.zego.im/article/api?doc=express-video-sdk_API~objectivec_ios~class~ZegoExpressEngine#destroy-engine) 接口，销毁引擎。

    ```objc
    [ZegoExpressEngine destroyEngine:nil];
    ```
















