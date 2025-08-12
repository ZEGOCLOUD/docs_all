```xml
<!-- SDK 必须使用的权限 -->
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

如图所示：

![](https://doc-media.zego.im/sdk-doc/Pics/Android/WhiteBoard/new_project_4.png)

权限说明如下：

|     权限     |     必要性               | 权限说明             | 需要理由                                                     |
| :------- | ---------------------- | -------------------- | ------------------------------------------------------------ |
| INTERNET |       必要权限         | 访问网络权限         | SDK 基本功能都需在联网的情况下才可以使用。                      |
| ACCESS_WIFI_STATE |   必要权限    | 获取当前 WIFI 状态权限 | SDK 会根据网络状态的改变执行不同的操作。如当网络重连的时候，SDK 内部会将网络断开时的状态都恢复，用户不需做额外的操作。 |
| ACCESS_NETWORK_STATE |  必要权限  | 获取当前网络状态权限 | SDK 会根据网络状态的改变执行不同的操作。如当网络重连的时候，SDK 内部会将网络断开时的状态都恢复，用户不需做额外的操作。 |
| WRITE_EXTERNAL_STORAGE | 必要权限 | 内置 SD 卡写权限        | 若需要使用媒体播放器或音效播放器加载 Android 外部存储内的媒体资源文件，则需要申请此权限，否则 SDK 无法加载资源。                   |
| READ_EXTERNAL_STORAGE |  必要权限 | 内置 SD 卡读权限        | SDK 会将日志和相关配置文件保存在内置 SD 卡内。                   |





