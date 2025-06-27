# 快速开始

这份文档将指导您如何在 uni-app 项目集成`音视频通话 UIKit`小程序 SDK 并快速开始包含呼叫邀请的音视频通话。

## 准备环境：
- 参考 [uni-app 文档](https://zh.uniapp.dcloud.io/quickstart-hx.html)创建项目。
- 使用微信小程序基础库1.7.0 或以上版本，否则不支持音视频播放。
- 通过微信小程序实时音视频播放相关类目审核（获取到对应的小程序 AppID），开通 [live-player](https://developers.weixin.qq.com/miniprogram/dev/component/live-player.html)、[live-pusher](https://developers.weixin.qq.com/miniprogram/dev/component/live-pusher.html) 组件权限。

## 前提条件
- 已在 [ZEGO 控制台](https://console.zego.im/account/login) 创建项目，并申请有效的 AppID 和 AppSign，详情请参考 [控制台 - 项目信息](https://doc-zh.zego.im/article/12107)。
- 联系 ZEGO 技术支持，开通 UIKit 相关服务。

## 安装 SDK

请在项目根目录运行以下命令将 SDK 安装到项目中。

```shell
npm i @zegocloud/zego-uikit-prebuilt-call-mini-program --save
```

## 使用步骤

<Steps>
    <Step title="在您的服务端部署好 Token 生成服务。">
    详细步骤请参考 [Token](https://doc-zh.zego.im/article/8940) 生成文档。如需快速调试，建议使用控制台生成的临时 Token，生成临时 Token 的具体操作请参考 [控制台 - 项目管理](https://doc-zh.zego.im/article/12107)。
    </Step> 
    <Step title="导入 UIKit 组件。">
    将 UIKit 组件拷贝到您的项目中。可以参考以下命令操作：
    ```shell
    mkdir -p ./ZegoUIKitPrebuiltCall && cp -r node_modules/@zegocloud/zego-uikit-prebuilt-call-mini-program/src/ ./ZegoUIKitPrebuiltCall/src/
    ```
    <Warning title="注意">
    更新 SDK 后，您需要重新执行当前步骤以刷新本地的 UIKit 组件。
    </Warning>
    </Step>
    <Step title="调用 UIKit 组件。">
        <Tabs>
            <Tab title="主包接入">
            <Steps>
                <Step title="添加跳转至 UIKit 的页面配置项。">
                复制以下代码至您项目根目录的 pages.json 文件，其中 path 需指向上一步中 UIKit 组件的存储路径。
                ```js pages.json
                {
                    "path": "ZegoUIKitPrebuiltCall/src/pages/call_invitation/InvitationCall",
                    "style": {
                        "navigationBarTitleText": "Call Invitation"
                    }
                }
                ```
                </Step>
                <Step title="初始化具备呼叫邀请功能的音视频通话 UIKit。">
                在您的首页或其他页面中，参考以下代码初始化 ZegoUIKitPrebuiltCall。

                <Warning title="注意">设置房间配置的 <code>mode</code> 参数为 <code>ZegoCallScenario.CALL_INVITATION</code> 和 <code>globalPagePath</code> 参数为 UIKit 组件的存储路径后才能发起呼叫和接受呼叫。</Warning>
                ```js YourInitPage.vue {11-12,16}
                <script setup>
                import { onMounted } from "vue";
                import { ZegoUIKitPrebuiltCall, ZegoCallScenario }  from "@zegocloud/zego-uikit-prebuilt-call-mini-program";

                const appID = 0; // 您从控制台获取的 AppID
                const server = ""; // 您从控制台获取的 Server 地址
                const userID = "user1"; // userID，需用户自己定义，保证全局唯一，建议设置为业务系统中的用户唯一标识
                const userName = "user1_name"; // userName 用户名
                const token = ""; // 您从服务端生成的 Token
                const config = {
                    mode: ZegoCallScenario.CALL_INVITATION, // 设置 mode 为 ZegoCallScenario.CALL_INVITATION 后才能发起呼叫和接受呼叫
                    globalPagePath: "/ZegoUIKitPrebuiltCall/src/pages/call_invitation/InvitationCall",  // UIKit 组件的存储路径
                }; // 房间配置

                onMounted(() => {
                    ZegoUIKitPrebuiltCall.init(appID, server, userID, userName, token, config);
                })
                </script>
                ```
                </Step>
                <Step title="添加呼叫邀请按钮。">

                在您的其他页面中，参考以下代码导入 ZegoSendCallInvitationButton 组件，当点击组件后，就会发起呼叫邀请。
                ```js YourPage.vue {3-11,15}
                <template>
                    <view class="button-container">
                        <ZegoSendCallInvitationButton
                            class="btn"
                            :invitees="invitees" 
                            :isVideoCall="true" 
                            :text="text"
                            :customData="customData"
                            :timeout="30"
                            :onPressed="sendCallback">
                        </ZegoSendCallInvitationButton>
                    </view>
                </template>
                <script setup>
                import ZegoSendCallInvitationButton from "../ZegoUIKitPrebuiltCall/src/components/ZegoSendCallInvitationButton.vue";
                import { ref } from "vue";
                // 您要呼叫的用户列表
                const invitees = ref([{
                    userID: "user_invitee",
                    userName: "user_invitee",
                }]);
                const text = ref("视频通话");
                const customData = ref("您需要传递给被叫者的其他参数");
                const sendCallback = (code, message, errorInvitees) => {
                    // 点击发起呼叫邀请的回调
                }
                </script>
                <style scoped>
                .button-container {
                    display: flex;
                    justify-content: center;
                }
                .btn {
                    text-align: center;
                    width: 570rpx;
                    height: 100rpx;
                    line-height: 100rpx;
                    font-size: 32rpx;
                    color: #fff;
                    border-radius: 20rpx;
                    background-color: #0055FF;
                }
                </style>
                ```

                #### ZegoSendCallInvitationButton 属性

                | 属性        | 类型    | 必需 | 描述                                                      |
                | :---------- | :------ | :--- | :-------------------------------------------------------- |
                | invitees    | Array of String   | 是   | 被叫用户信息。必须包括 userID 和 userName。               |
                | isVideoCall | Boolean | 是   | 如果为 true，则按下按钮时进行视频通话，否则进行语音通话。 |
                | text        | String  | 否   | 发起呼叫邀请按钮的文本。                                  |
                | customData  | String  | 否   | 您需要传递给被叫者的自定义参数。                          |
                | timeout     | Number  | 否   | 超时时长，单位为秒。默认为 60。超时后会自动取消本次呼叫。          |
                | onPressed   | Function | 否   | 点击发起呼叫邀请按钮的回调。                              |

                </Step>
            </Steps>
        </Tab>
            <Tab title="分包接入">
            <Steps>
                <Step title="配置分包">
 
                复制以下代码至您项目根目录的 manifest.json 文件。

                ```js manifest.json
                "mp-weixin" : {
                    ...
                    "optimization": {
                        "subPackages": true
                    }
                },
                ```
                </Step>
                <Step title="新建 pages/index.vue 文件">

                访问 UIKit 组件的存储路径，新建 pages/index.vue 文件，并复制以下代码至该文件。

                <Frame width="256" height="auto" caption="">
                    <img src="https://media-resource.spreading.io/docuo/workspace746/5e93b8724bfcf0da36e347272ac420f1/21853a1650.jpeg" alt="20250214-110156.jpeg"/>
                </Frame>
                ``` js index.vue
                <template>
                    <view>
                        <InvitationCall v-if="isUIKitShow"/>
                        <view class="button-container">
                            <ZegoSendCallInvitationButton
                                class="btn"
                                :isVideoCall="true"
                                :invitees="invitees"
                                :text="text"
                                :customData="customData"
                                :timeout="30"
                                :onPressed="sendCallback">
                            </ZegoSendCallInvitationButton>
                        </view>
                    </view>
                </template>
                <script setup>
                import { ref, onMounted, onUnmounted, getCurrentInstance } from 'vue';
                import { ZegoUIKitPrebuiltCall, makePrebuiltListenerID } from '@zegocloud/zego-uikit-prebuilt-call-mini-program';
                import ZegoSendCallInvitationButton from '../src/components/ZegoSendCallInvitationButton.vue';
                import InvitationCall from '../src/pages/call_invitation/invitationCall.vue';

                let isUIKitShow = ref(false);
                const LISTENER_ID = makePrebuiltListenerID(); // 生成回调ID
                // 您要呼叫的用户列表
                const invitees = ref([{
                    userID: 'user_invitee',
                    userName: 'user_invitee',
                }]);
                const text = ref("视频通话");
                const customData = ref("您需要传递给被叫者的其他参数");

                onMounted(() => {
                    const instance = getCurrentInstance()?.proxy;
                    // @ts-ignore
                    const eventChannel = instance?.getOpenerEventChannel();
                    if (eventChannel) {
                        // 监听事件获取从主包传递过来的数据
                        eventChannel.on('acceptDataFromOpenerPage', function(data) {
                            ZegoUIKitPrebuiltCall.init(data.appID, data.server, data.userID, data.userName, data.token, data.config);
                            ZegoUIKitPrebuiltCall.addPrebuiltListener(LISTENER_ID, {
                                onInitialized: () => {
                                    isUIKitShow.value = true;
                                }
                            })
                        });
                    }
                })
                
                onUnmounted(() => {
                    ZegoUIKitPrebuiltCall.removePrebuiltListener(LISTENER_ID);
                    ZegoUIKitPrebuiltCall.unInit();
                })

                const sendCallback = (code, message, errorInvitees) => {
                    // 点击发起呼叫邀请的回调
                }
                </script>
                <style scoped>
               .button-container {
                    display: flex;
                    justify-content: center;
                }
                .btn {
                    text-align: center;
                    width: 570rpx;
                    height: 100rpx;
                    line-height: 100rpx;
                    font-size: 32rpx;
                    color: #fff;
                    border-radius: 20rpx;
                    background-color: #0055FF;
                }
                </style>
                ```

                #### ZegoSendCallInvitationButton 属性

                | 属性        | 类型    | 必需 | 描述                                                      |
                | :---------- | :------ | :--- | :-------------------------------------------------------- |
                | invitees    | Array of String   | 是   | 被叫用户信息。必须包括 userID 和 userName。               |
                | isVideoCall | Boolean | 是   | 如果为 true，则按下按钮时进行视频通话，否则进行语音通话。 |
                | text        | String  | 否   | 发起呼叫邀请按钮的文本。                                  |
                | customData  | String  | 否   | 您需要传递给被叫者的自定义参数。                          |
                | timeout     | Number  | 否   | 超时时长。默认为60秒。超时后会自动取消本次呼叫。          |
                | onPressed   | Function | 否   | 点击发起呼叫邀请按钮的回调。                              |

                </Step>
                <Step title="在 pages.json 中配置分包路径">

                复制以下代码至您项目根目录的 pages.json 文件。
                ``` js pages.json
                "subPackages": [
                    {
                        "root": "ZegoUIKitPrebuiltCall",
                        "pages": [
                            {
                                "path": "pages/index",
                                "style": {
                                    "navigationBarTitleText": "ZegoUIKitPrebuiltCall"
                                }
                            },
                        ]
                    }
                ],
                ```
                </Step>
                <Step title="修改 vite 打包配置">
                由于 uniapp 的打包机制会将分包中的依赖也打入主包中，所以需要修改 vite 打包配置。请在您的项目根目录下新建一个配置文件（vite.config.js），并将以下代码复制至该文件。
                ``` js vite.config.js
                import { defineConfig } from "vite";
                import uni from "@dcloudio/vite-plugin-uni";

                export default defineConfig({
                    plugins: [uni()],
                    optimizeDeps: {
                        include: ["@zegocloud/zego-uikit-prebuilt-call-mini-program"],
                    },
                    build: {
                        rollupOptions: {
                        external: ["@zegocloud/zego-uikit-prebuilt-call-mini-program"],
                        },
                    },
                });
                ```
                </Step>
                <Step title="加载分包页面">

                参考以下代码，实现加载分包页面。

                <Note title="说明">下列代码以空项目为例（由于微信小程序的分包策略，此步骤必须实现，才能加载分包的页面），因此，请您根据实际业务需要调整代码。</Note>
                
                ```js
                <template>
                    <view>
                        <button @click="gotoSubPackage">跳转分包</button>
                    </view>
                </template>
                <script setup>
                const data = {
                    appID: 0, // 您从控制台获取的 AppID
                    server: "", // 您从控制台获取的 server 地址
                    token: "", // 您从服务端生成的 Token
                    userID: "", // userID，保证全局唯一，建议设置为业务系统中的用户唯一标识
                    userName: "", // userName 用户名
                    config: { mode: 2 }, // UIKit 的配置
                }
                const gotoSubPackage = () => {
                    // @ts-ignore
                    uni.navigateTo({
                        url: `/ZegoUIKitPrebuiltCall/pages/index`,
                        success: (res) => { 
                            // 传递数据到分包
                            res.eventChannel.emit('acceptDataFromOpenerPage', data)
                        },
                        fail: () => {
                            console.error(`navigateTo fail!`);
                        },
                        complete: () => { },
                    });
                }
                </script>
                ```
                </Step>
                <Step title="构建小程序 npm 包">
                在微信小程序工具的终端中分别运行以下 3 行命令。执行完后，在微信开发者工具中选择工具 -> 构建 npm。构建完成后， ZegoUIKitPrebuiltCall 文件夹生成 miniprogram_npm，表示构建成功。
                ```shell
                cd ZegoUIKitPrebuiltCall
                npm init -y
                npm i @zegocloud/zego-uikit-prebuilt-call-mini-program
                ```

                <Frame width="auto" height="auto" caption="新建终端">
                  <img src="https://media-resource.spreading.io/docuo/workspace746/5e93b8724bfcf0da36e347272ac420f1/36da689ece.jpeg" alt="20250214-102417.jpeg"/>
                </Frame>
                <Frame width="auto" height="auto" caption="构建npm">
                  <img src="https://media-resource.spreading.io/docuo/workspace746/5e93b8724bfcf0da36e347272ac420f1/142dce6305.jpeg" alt="20250214-103101.jpeg"/>
                </Frame>
                </Step>
            </Steps>
            </Tab>
        </Tabs>
    </Step>
</Steps>

至此，您已经完成了所有步骤！运行后的效果如下：

**主叫方**

|示例 Demo 首页|发起呼叫邀请页面|主叫等待页面|
|--|--|--|
|<Frame width="128" height="auto" caption=""><img src="https://media-resource.spreading.io/docuo/workspace564/27e54a759d23575969552654cb45bf89/c5e53f324b.png" alt="home.png"/></Frame>|<Frame width="128" height="auto" caption=""><img src="https://media-resource.spreading.io/docuo/workspace564/27e54a759d23575969552654cb45bf89/e7e43e36c2.png" alt="StartCallPage.png"/></Frame>|<Frame width="128" height="auto" caption=""><img src="https://media-resource.spreading.io/docuo/workspace564/27e54a759d23575969552654cb45bf89/8eb62111b7.png" alt="CallerWaitingPage.png"/></Frame>|

**被叫方**

|被叫收到呼叫邀请页面|接受邀请后双方通话页面|
|--|--|
|<Frame width="128" height="auto" caption=""><img src="https://media-resource.spreading.io/docuo/workspace564/27e54a759d23575969552654cb45bf89/42894b6f9b.png" alt="CalleeReceiveInvite.png"/></Frame>|<Frame width="128" height="auto" caption=""><img src="https://media-resource.spreading.io/docuo/workspace564/27e54a759d23575969552654cb45bf89/ac8b9222af.png" alt="talkingpage.png"/></Frame>|





