# 设置用户头像

互动直播 UIKit 不知道每个用户的真实个人资料图片，因此在默认情况下，会使用用户名的第一个字母来绘制用户头像。不过，互动直播 UIKit 也支持用户自行设置头像。

## 实现流程

为了配置自定义用户头像，您可以使用 `ZegoUIKitPrebuiltLiveStreamingConfig` 中的 `avatarViewProvider` 来设置自定义视图。


<Warning title="注意">
- 用户头像通常存储在服务器上。
- 您需要根据回调参数中的用户参数返回不同的头像。
- 如果您 hardcode 一个 URL，那么每个人的头像都将展示您 hardcode 后的头像。
</Warning>

以下是参考代码：

```java
long appID = yourAppID; 
String appSign = yourAppSign; 
String userID = yourUserID;
String userName = yourUserName; 
String liveID = yourLiveID; 

ZegoUIKitPrebuiltLiveStreamingConfig config = ZegoUIKitPrebuiltLiveStreamingConfig.host(true);

config.avatarViewProvider = new ZegoAvatarViewProvider() {
    @Override
    public View onUserIDUpdated(ViewGroup parent, ZegoUIKitUser uiKitUser) {
        ImageView imageView = new ImageView(parent.getContext());
        String avatarUrl = getAvatarByUserID(uiKitUser.userID); // 根据用户 ID 获取头像 URL
        if (!TextUtils.isEmpty(avatarUrl)) {
            RequestOptions requestOptions = new RequestOptions().circleCrop(); // 设置圆形裁剪
            Glide.with(parent.getContext()).load(avatarUrl).apply(requestOptions).into(imageView); // 加载图片到 ImageView
        }
        return imageView;
    }
};

ZegoUIKitPrebuiltLiveStreamingFragment fragment = ZegoUIKitPrebuiltLiveStreamingFragment.newInstance(appID, appSign, userID, userName, liveID, config);
getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, fragment).commitNow();

```

设置完成后，互动直播 UIKit 将显示您设置的自定义用户头像。
