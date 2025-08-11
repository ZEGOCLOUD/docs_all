## 部署 Firebase Cloud Functions

ZEGO Call 默认使用  Firebase Cloud Functions 作为业务后台，因此我们建议您在集成 Call SDK 前先开通并部署 Firebase Cloud Functions。 

<div class="mk-hint">

若您想要开发自己的业务后台替代Firebase，请参考 [Using ZEGOCall with your business server](!users).

</div>


1. 参考 [Firebase 官方文档](https://firebase.google.com/docs/functions/get-started) 前三节创建并初始化一个云函数项目.    
    
    **Note**: 我们使用 Realtime Database 作为数据库，您还需要在 Firebase 控制台中创建一个新的 Realtime Database。
2. 下载 [云函数示例源码](https://github.com/ZEGOCLOUD/call_firebase_funcitons). 
3. 复制源码中的 "firebase.json" 和 "functions\index.js" 复制到你的云函数项目目录，覆盖同名文件。
4. 复制 "functions\token04" 到你的云函数项目目录下 “index.js” 的所在文件夹内。
5. 修改 "index.js" 文件，将 appID 和 secret 的取值修改为您在 [ZEGOCLOUD Admin Console](https://console.zegocloud.com) 获取的 AppID 和 ServerSecret.

    ![https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/index_appid.png](https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/index_appid.png)

6. 在 Firebase CLI 中运行 `firebase deploy --only functions` 命令部署云函数。




