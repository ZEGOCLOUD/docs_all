//
//  ViewController.m
//  ZegoDigitalHumanQuickStart
//
//  单文件实现 - 对齐Android的MainActivity.kt调用流程
//  Single-file implementation - aligned with Android's MainActivity.kt call flow
//  核心流程：获取播报列表 → 获取Token → 预加载资源 → 登录房间 → 启动数字人
//  Core flow: Fetch broadcast list → Get token → Preload resources → Login room → Start digital human
//

#import "ViewController.h"
#import "Config.h"
#import <ZegoExpressEngine/ZegoExpressEngine.h>
#import <ZegoDigitalMobile/ZegoDigitalMobile.h>

// ========== 1. 内部接口扩展 ==========
// ========== 1. Internal interface extensions ==========
@interface ViewController () <ZegoDigitalMobileDelegate, ZegoDigitalHumanResourceDelegate, ZegoEventHandler, ZegoCustomVideoRenderHandler>

// 数字人视图（SDK提供的渲染视图）
// Digital human view (rendering view provided by SDK)
@property (nonatomic, strong) ZegoDigitalView *digitalHumanView;

// SDK实例
// SDK instances
@property (nonatomic, strong) ZegoExpressEngine *expressEngine;

// 房间信息
// Room information
@property (nonatomic, copy) NSString *currentRoomId;
@property (nonatomic, copy) NSString *currentStreamId;
@property (nonatomic, copy) NSString *currentUserId;
@property (nonatomic, assign) BOOL isRoomLoggedIn;

// 播报信息（从API获取）
// Broadcast information (from API)
@property (nonatomic, copy) NSString *digitalHumanId;
@property (nonatomic, copy) NSString *clientInferencePackageUrl;
@property (nonatomic, assign) BOOL isSupportSmallImageMode;

// 用于在预加载成功后启动数字人
// Used to start digital human after successful preload
@property (nonatomic, copy) NSString *pendingBase64Config;

@end

// ========== 2. 实现 ==========
// ========== 2. Implementation ==========
@implementation ViewController

#pragma mark - Lifecycle

- (void)viewDidLoad {
    [super viewDidLoad];

    // 初始化状态
    // Initialize state
    self.isRoomLoggedIn = NO;

    // 初始化UI
    // Initialize UI
    [self initViews];

    // 检查配置
    // Check configuration
    if ([Config ZEGO_APP_ID] == 0) {
        [self updateStatus:@"Please configure ZEGO_APP_ID in Config.m"];
        return;
    }

    // 初始化SDK
    // Initialize SDKs
    [self initSDKs];

    // 启动数字人播放流程
    // Start digital human playback process
    [self startDigitalHuman];
}

- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];

    // 页面消失时清理资源
    // Cleanup resources when page disappears
    [self cleanup];
}

- (void)dealloc {
    [self cleanup];
}

#pragma mark - 3. UI Setup

- (void)initViews {
    self.view.backgroundColor = [UIColor colorWithRed:0.4 green:0.5 blue:0.9 alpha:1.0];

    // 状态标签
    // Status label
    self.tvStatus = [[UILabel alloc] init];
    self.tvStatus.text = @"Status: Initializing...";
    self.tvStatus.textColor = [UIColor whiteColor];
    self.tvStatus.font = [UIFont systemFontOfSize:14];
    self.tvStatus.numberOfLines = 0;
    self.tvStatus.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:self.tvStatus];

    // 房间信息标签
    // Room information label
    self.tvRoomInfo = [[UILabel alloc] init];
    self.tvRoomInfo.text = @"Room: -- | Stream: --";
    self.tvRoomInfo.textColor = [UIColor whiteColor];
    self.tvRoomInfo.font = [UIFont systemFontOfSize:12];
    self.tvRoomInfo.numberOfLines = 0;
    self.tvRoomInfo.textAlignment = NSTextAlignmentCenter;
    [self.view addSubview:self.tvRoomInfo];

    // 数字人视图容器
    // Digital human view container
    self.digitalHumanContainerView = [[UIView alloc] init];
    self.digitalHumanContainerView.backgroundColor = [UIColor clearColor];
    [self.view addSubview:self.digitalHumanContainerView];

    // 布局约束
    // Layout constraints
    self.tvStatus.translatesAutoresizingMaskIntoConstraints = NO;
    self.tvRoomInfo.translatesAutoresizingMaskIntoConstraints = NO;
    self.digitalHumanContainerView.translatesAutoresizingMaskIntoConstraints = NO;

    [NSLayoutConstraint activateConstraints:@[
        [self.tvStatus.topAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.topAnchor constant:20],
        [self.tvStatus.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor constant:20],
        [self.tvStatus.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor constant:-20],

        [self.tvRoomInfo.topAnchor constraintEqualToAnchor:self.tvStatus.bottomAnchor constant:10],
        [self.tvRoomInfo.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor constant:20],
        [self.tvRoomInfo.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor constant:-20],

        [self.digitalHumanContainerView.topAnchor constraintEqualToAnchor:self.tvRoomInfo.bottomAnchor constant:20],
        [self.digitalHumanContainerView.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor],
        [self.digitalHumanContainerView.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor],
        [self.digitalHumanContainerView.bottomAnchor constraintEqualToAnchor:self.view.bottomAnchor],
    ]];
}

#pragma mark - 4. SDK Initialization

/**
 * 初始化 Express SDK 和数字人 SDK
 * Initialize Express SDK and Digital Human SDK
 */
- (void)initSDKs {
    // 初始化 Express SDK
    // Initialize Express SDK
    ZegoEngineProfile *profile = [[ZegoEngineProfile alloc] init];
    profile.appID = (unsigned int)[Config ZEGO_APP_ID];
    profile.scenario = ZegoScenarioHighQualityChatroom;

    self.expressEngine = [ZegoExpressEngine createEngineWithProfile:profile eventHandler:self];

    // 初始化数字人SDK
    // Initialize Digital Human SDK
    self.digitalMobile = [ZegoDigitalHuman create];

    // 创建数字人视图并绑定
    // Create and bind digital human view
    self.digitalHumanView = [[ZegoDigitalView alloc] initWithFrame:self.digitalHumanContainerView.bounds];
    self.digitalHumanView.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [self.digitalHumanContainerView addSubview:self.digitalHumanView];

    [self.digitalMobile attach:self.digitalHumanView];

    NSLog(@"[SDK] Express engine and digital human SDK initialized");
}

#pragma mark - 5. Main Flow

/**
 * 启动数字人播放流程 - 对齐Android的startDigitalHuman()
 * Start digital human playback process - aligned with Android's startDigitalHuman()
 */
- (void)startDigitalHuman {
    // 在后台线程执行网络请求
    // Execute network requests in background thread
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        @try {
            // 步骤1: 从业务后台获取播报列表
            // Step 1: Fetch broadcast list from backend
            [self updateStatus:@"Fetching broadcast list..."];
            NSDictionary *broadcast = [self fetchBroadcastList];
            if (!broadcast) {
                [self updateStatus:@"No available broadcast, please start broadcast task on server first"];
                return;
            }

            // 保存房间信息
            // Save room information
            self.currentRoomId = broadcast[@"roomId"];
            self.currentStreamId = broadcast[@"streamId"];
            self.digitalHumanId = broadcast[@"digitalHumanId"];
            self.clientInferencePackageUrl = broadcast[@"clientInferencePackageUrl"];
            self.isSupportSmallImageMode = [broadcast[@"isSupportSmallImageMode"] boolValue];

            dispatch_async(dispatch_get_main_queue(), ^{
                self.tvRoomInfo.text = [NSString stringWithFormat:@"Room: %@ | Stream: %@", self.currentRoomId, self.currentStreamId];
            });

            // 步骤2: 获取Token
            // Step 2: Get token
            [self updateStatus:@"Fetching token..."];
            self.currentUserId = [NSString stringWithFormat:@"user_%lld", (long long)([[NSDate date] timeIntervalSince1970] * 1000)];
            NSString *token = [self fetchToken:self.currentUserId];
            if (!token) {
                [self updateStatus:@"Failed to fetch token"];
                return;
            }

            // 步骤3: 预加载数字人资源
            // Step 3: Preload digital human resources
            [self updateStatus:@"Preloading digital human resources..."];
            [self preloadDigitalHumanResources:self.currentUserId token:token];

            // 步骤4: 登录房间（登录成功后会启动数字人）
            // Step 4: Login to room (digital human will start after successful login)
            [self updateStatus:@"Logging in to room..."];
            [self loginRoom:self.currentRoomId streamId:self.currentStreamId userId:self.currentUserId token:token broadcast:broadcast];

        } @catch (NSException *exception) {
            NSLog(@"[Error] Startup failed: %@", exception.reason);
            [self updateStatus:[NSString stringWithFormat:@"Startup failed: %@", exception.reason]];
        }
    });
}

#pragma mark - 6. API Calls (Inline - 对齐Android的OkHttp调用)
// #pragma mark - 6. API Calls (Inline - aligned with Android's OkHttp calls)

/**
 * 获取播报列表 - 对齐Android的fetchBroadcastList()
 * Fetch broadcast list - aligned with Android's fetchBroadcastList()
 * GET /api/broadcast
 */
- (NSDictionary *)fetchBroadcastList {
    NSString *urlString = [NSString stringWithFormat:@"%@/api/broadcast", [Config ZEGO_API_BASE_URL]];
    NSURL *url = [NSURL URLWithString:urlString];

    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    request.HTTPMethod = @"GET";
    [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];

    NSData *data = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
    if (!data) {
        NSLog(@"[API] Failed to fetch broadcast list: No response");
        return nil;
    }

    NSError *jsonError = nil;
    id jsonResponse = [NSJSONSerialization JSONObjectWithData:data options:0 error:&jsonError];
    if (jsonError || ![jsonResponse isKindOfClass:[NSDictionary class]]) {
        NSLog(@"[API] Failed to parse broadcast list: %@", jsonError);
        return nil;
    }

    NSDictionary *json = (NSDictionary *)jsonResponse;
    NSDictionary *broadcastList = json[@"broadcastList"];
    if (![broadcastList isKindOfClass:[NSDictionary class]] || broadcastList.count == 0) {
        NSLog(@"[API] Broadcast list is empty");
        return nil;
    }

    // 获取第一个播报，仅示例
    // Get first broadcast, for demo only
    NSString *firstKey = broadcastList.allKeys.firstObject;
    NSDictionary *broadcast = broadcastList[firstKey];
    if (![broadcast isKindOfClass:[NSDictionary class]]) {
        return nil;
    }

    // 验证必需字段
    // Validate required fields
    NSString *roomId = broadcast[@"roomId"];
    NSString *streamId = broadcast[@"streamId"];
    NSString *packageUrl = broadcast[@"clientInferencePackageUrl"];
    NSString *digitalHumanId = broadcast[@"digitalHumanId"];

    if (!roomId || !streamId || !packageUrl || !digitalHumanId) {
        NSLog(@"[API] Incomplete broadcast information");
        return nil;
    }

    return @{
        @"roomId": roomId,
        @"streamId": streamId,
        @"clientInferencePackageUrl": packageUrl,
        @"digitalHumanId": digitalHumanId,
        @"isSupportSmallImageMode": broadcast[@"isSupportSmallImageMode"] ?: @NO
    };
}

/**
 * 获取Token - 对齐Android的fetchToken()
 * Fetch token - aligned with Android's fetchToken()
 * GET /api/token?userId=xxx
 */
- (NSString *)fetchToken:(NSString *)userId {
    NSString *urlString = [NSString stringWithFormat:@"%@/api/token?userId=%@", [Config ZEGO_API_BASE_URL], userId];
    NSURL *url = [NSURL URLWithString:urlString];

    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    request.HTTPMethod = @"GET";
    [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];

    NSData *data = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
    if (!data) {
        NSLog(@"[API] Failed to fetch token: No response");
        return nil;
    }

    NSError *jsonError = nil;
    id jsonResponse = [NSJSONSerialization JSONObjectWithData:data options:0 error:&jsonError];
    if (jsonError || ![jsonResponse isKindOfClass:[NSDictionary class]]) {
        NSLog(@"[API] Failed to parse token: %@", jsonError);
        return nil;
    }

    NSDictionary *json = (NSDictionary *)jsonResponse;
    NSString *token = json[@"token"];
    return token;
}

#pragma mark - 7. RTC Operations

/**
 * 登录房间 - 对齐Android的loginRoom()
 * Login to room - aligned with Android's loginRoom()
 */
- (void)loginRoom:(NSString *)roomId
          streamId:(NSString *)streamId
            userId:(NSString *)userId
             token:(NSString *)token
         broadcast:(NSDictionary *)broadcast {

    ZegoEngineConfig *engineConfig = [[ZegoEngineConfig alloc] init];
    engineConfig.advancedConfig = @{
        @"set_audio_volume_ducking_mode": @"1",
        @"enable_rnd_volume_adaptive": @"true",
        @"sideinfo_callback_version": @"3",
        @"sideinfo_bound_to_video_decoder": @"true"
    };
    [ZegoExpressEngine setEngineConfig:engineConfig];

    [self.expressEngine setRoomScenario:ZegoScenarioHighQualityChatroom];

    ZegoRoomConfig *roomConfig = [[ZegoRoomConfig alloc] init];
    roomConfig.isUserStatusNotify = YES;
    roomConfig.token = token;

    ZegoUser *user = [[ZegoUser alloc] init];
    user.userID = userId;
    user.userName = userId;

    __weak typeof(self) weakSelf = self;
    [self.expressEngine loginRoom:roomId user:user config:roomConfig callback:^(int errorCode, NSDictionary *extendedData) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;

        if (errorCode == 0) {
            strongSelf.isRoomLoggedIn = YES;
            NSLog(@"[RTC] Room login successful");

            // 登录成功后：开启自定义渲染
            // After successful login: enable custom video rendering
            [strongSelf enableCustomVideoRender];

            // 生成配置
            // Generate configuration
            NSString *base64Config = [strongSelf generateBase64Config:strongSelf.digitalHumanId
                                                               roomId:strongSelf.currentRoomId
                                                            streamId:strongSelf.currentStreamId
                                                          packageUrl:strongSelf.clientInferencePackageUrl
                                           isSupportSmallImageMode:strongSelf.isSupportSmallImageMode];
            strongSelf.pendingBase64Config = base64Config;

            [strongSelf startDigitalHumanSDK:base64Config];
        } else {
            NSLog(@"[RTC] Room login failed: %d", errorCode);
            [strongSelf updateStatus:[NSString stringWithFormat:@"Room login failed: %d", errorCode]];
        }
    }];
}

/**
 * 开启自定义视频渲染 - 对齐Android的enableCustomVideoRender()
 * Enable custom video rendering - aligned with Android's enableCustomVideoRender()
 */
- (void)enableCustomVideoRender {
    ZegoCustomVideoRenderConfig *renderConfig = [[ZegoCustomVideoRenderConfig alloc] init];
    renderConfig.bufferType = ZegoVideoBufferTypeRawData;
    renderConfig.frameFormatSeries = ZegoVideoFrameFormatSeriesRGB;
    renderConfig.enableEngineRender = NO;
    [self.expressEngine enableCustomVideoRender:YES config:renderConfig];

    // 设置视频帧回调
    // Set video frame callback
    [self.expressEngine setCustomVideoRenderHandler:self];

    NSLog(@"[RTC] Custom video rendering enabled");
}

/**
 * 开始拉流 - 对齐Android的startPlayingStream()
 * Start playing stream - aligned with Android's startPlayingStream()
 */
- (void)startPlayingStream:(NSString *)streamID {
    // 设置拉流缓冲区
    // Set stream buffer interval range
    [self.expressEngine setPlayStreamBufferIntervalRange:streamID min:100 max:2000];

    // 开始拉流
    // Start playing stream
    [self.expressEngine startPlayingStream:streamID];

    [self updateStatus:@"Playing..."];
    NSLog(@"[RTC] Started playing stream: %@", streamID];
}

#pragma mark - 8. Digital Human

/**
 * 预加载数字人资源 - 对齐Android的preloadDigitalHumanResources()
 * Preload digital human resources - aligned with Android's preloadDigitalHumanResources()
 */
- (void)preloadDigitalHumanResources:(NSString *)userId
                               token:(NSString *)token {
    ZegoDigitalHumanAuth *auth = [[ZegoDigitalHumanAuth alloc] initWithAppID:(unsigned int)[Config ZEGO_APP_ID]
                                                                        userID:userId
                                                                         token:token];

    [[ZegoDigitalHumanResource sharedInstance] preloadWithAuth:auth
                                               digitalHumanId:self.digitalHumanId
                                                     delegate:self];
    NSLog(@"[DigitalHuman] Starting resource preload: %@", self.digitalHumanId);
}

/**
 * 启动数字人SDK - 对齐Android的startDigitalHumanSDK()
 * Start digital human SDK - aligned with Android's startDigitalHumanSDK()
 */
- (void)startDigitalHumanSDK:(NSString *)base64Config {
    if (!self.digitalMobile) {
        [self updateStatus:@"Digital human SDK not initialized"];
        return;
    }

    @try {
        [self.digitalMobile start:base64Config delegate:self];
        NSLog(@"[DigitalHuman] Starting digital human");
    } @catch (NSException *exception) {
        NSLog(@"[DigitalHuman] Startup failed: %@", exception.reason);
        [self updateStatus:[NSString stringWithFormat:@"Failed to start digital human SDK: %@", exception.reason]];
    }
}

/**
 * 停止数字人
 * Stop digital human
 */
- (void)stopDigitalHuman {
    if (self.digitalMobile) {
        [self.digitalMobile stop];
        self.digitalMobile = nil;
    }
    NSLog(@"[DigitalHuman] Digital human stopped");
}

#pragma mark - 9. Helper Methods

/**
 * 生成 Base64Config - 对齐Android的generateBase64Config()
 * Generate Base64Config - aligned with Android's generateBase64Config()
 */
- (NSString *)generateBase64Config:(NSString *)digitalHumanId
                           roomId:(NSString *)roomId
                        streamId:(NSString *)streamId
                      packageUrl:(NSString *)packageUrl
       isSupportSmallImageMode:(BOOL)isSupportSmallImageMode {

    // 构建Streams配置
    // Build Streams configuration
    NSDictionary *stream = @{
        @"RoomId": roomId ?: @"",
        @"StreamId": streamId ?: @"",
        @"EncodeCode": @"H264",
        @"PackageUrl": packageUrl ?: @"",
        @"ConfigId": @"mobile",
        @"IsSupportSmallImageMode": isSupportSmallImageMode ? @YES : @NO
    };

    NSDictionary *config = @{
        @"DigitalHumanId": digitalHumanId ?: @"",
        @"Streams": @[stream]
    };

    NSError *jsonError = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:config options:0 error:&jsonError];
    if (jsonError) {
        NSLog(@"[Config] JSON serialization failed: %@", jsonError);
        return @"";
    }

    NSString *base64String = [jsonData base64EncodedStringWithOptions:0];
    return base64String;
}

/**
 * 更新状态显示
 * Update status display
 */
- (void)updateStatus:(NSString *)msg {
    dispatch_async(dispatch_get_main_queue(), ^{
        self.tvStatus.text = [NSString stringWithFormat:@"Status: %@", msg];
        NSLog(@"[Status] %@", msg);
    });
}

/**
 * 清理资源
 * Cleanup resources
 */
- (void)cleanup {
    // 停止数字人
    // Stop digital human
    [self stopDigitalHuman];

    // 停止拉流
    // Stop playing stream
    if (self.currentStreamId) {
        [self.expressEngine stopPlayingStream:self.currentStreamId];
    }

    // 退出房间
    // Logout room
    if (self.isRoomLoggedIn && self.currentRoomId) {
        [self.expressEngine logoutRoom:self.currentRoomId];
        self.isRoomLoggedIn = NO;
    }

    // 销毁引擎
    // Destroy engine
    if (self.expressEngine) {
        [ZegoExpressEngine destroyEngine:nil];
        self.expressEngine = nil;
    }
}

#pragma mark - 10. Delegates

// ========== ZegoDigitalMobileDelegate ==========

- (void)onDigitalMobileStartSuccess {
    [self updateStatus:@"Digital human started successfully"];
}

- (void)onError:(int)errorCode errorMsg:(NSString *)errorMsg {
    NSLog(@"[DigitalHuman] Error: %d, %@", errorCode, errorMsg);
    [self updateStatus:[NSString stringWithFormat:@"Digital human error: %@", errorMsg ?: @"Unknown error"]];
}

- (void)onSurfaceFirstFrameDraw {
    [self updateStatus:@"Digital human playing"];
}

// ========== ZegoDigitalHumanResourceDelegate ==========

- (void)onPreloadSuccess:(NSString *)digitalHumanId {
    NSLog(@"[DigitalHuman] Preload success: %@", digitalHumanId);
}

- (void)onPreloadFailed:(NSString *)digitalHumanId
              errorCode:(NSInteger)errorCode
           errorMessage:(NSString *)errorMessage {
    NSLog(@"[DigitalHuman] Preload failed: %@ - code: %ld, msg: %@", digitalHumanId, (long)errorCode, errorMessage);
}

- (void)onPreloadProgress:(NSString *)digitalHumanId
                 progress:(float)progress {
    // 预加载进度（可选显示）
    // Preload progress (optional display)
}

// ========== ZegoEventHandler ==========

- (void)onRoomStreamUpdate:(ZegoUpdateType)updateType
                streamList:(NSArray<ZegoStream *> *)streamList
              extendedData:(NSDictionary *)extendedData
                    roomID:(NSString *)roomID {

    if (updateType == ZegoUpdateTypeAdd) {
        for (ZegoStream *stream in streamList) {
            if ([stream.streamID isEqualToString:self.currentStreamId]) {
                [self startPlayingStream:stream.streamID];
                break;
            }
        }
    }
}

- (void)onPlayerSyncRecvSEI:(NSData *)data streamID:(NSString *)streamID {
    if ([streamID isEqualToString:self.currentStreamId] && self.digitalMobile) {
        // 重要：将 SEI 信息设置到数字人 SDK
        // IMPORTANT: Set SEI data to digital human SDK
        [self.digitalMobile onPlayerSyncRecvSEI:streamID data:data];
    }
}

// ========== ZegoCustomVideoRenderHandler ==========

- (void)onRemoteVideoFrameRawData:(unsigned char **)data
                       dataLength:(unsigned int *)dataLength
                            param:(ZegoVideoFrameParam *)param
                         streamID:(NSString *)streamID {

    if (!data || !dataLength || !param || !streamID || ![streamID isEqualToString:self.currentStreamId]) {
        return;
    }

    if (!self.digitalMobile) {
        return;
    }

    // 创建ZDMVideoFrameParam
    // Create ZDMVideoFrameParam
    ZDMVideoFrameParam *dmParam = [[ZDMVideoFrameParam alloc] init];
    dmParam.format = (ZDMVideoFrameFormat)param.format;
    dmParam.width = param.size.width;
    dmParam.height = param.size.height;
    dmParam.rotation = param.rotation;

    // 设置步长
    // Set strides
    for (int i = 0; i < 4; i++) {
        [dmParam setStride:param.strides[i] atIndex:i];
    }

    // 重要：将视频帧数据设置到数字人 SDK
    // IMPORTANT: Set video frame data to digital human SDK
    [self.digitalMobile onRemoteVideoFrameRawData:data
                                            dataLength:dataLength
                                                 param:dmParam
                                              streamID:streamID];
}

@end
