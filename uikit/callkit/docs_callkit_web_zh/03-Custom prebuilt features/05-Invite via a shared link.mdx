# 实现分享邀请链接


## 功能概述

:::if{props.kitType=undefined}
在 ZEGO UIKit 中，用户可以通过相同的房间 ID 加入同一个通话，因此，您可以通过发送带有 roomID 参数的 URL 链接邀请其他人加入本次通话。
:::
:::if{props.kitType="LiveStreaming"}
在 ZEGO UIKit 中，用户可以通过相同的房间 ID 加入同一个直播间，因此，您可以通过发送带有 roomID 参数的 URL 链接邀请其他人加入同一个直播间。
:::

功能实现示意图如下：

<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/UIKit/invite_by_shared_link.jpeg" /></Frame>

邀请链接将会在以下两个页面显示，如下所示：

<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/Prebuilt_Web/preview_share.png" /></Frame>

<Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/Prebuilt_Web/joinRoom_share.png" /></Frame>


## 实现流程

:::if{props.kitType=undefined}
以用户 A 生成邀请链接，用户 B 加入通话为例
:::
:::if{props.kitType="LiveStreaming"}
以用户 A 生成邀请链接，用户 B 加入直播为例
:::

1. 用户 A 生成共享链接邀请用户 B 加入：

   ```javascript
   // ....
   zp.joinRoom({
       // ...,
       sharedLinks: [{
           url: window.location.protocol + '//' + window.location.host + window.location.pathname+ '?roomID=' + roomID,
       }],
       // ...
   });
   ```

2. 用户 B 解析房间 ID 并生成 Kit Token 以加入会话：

    ```javascript
    function getUrlParams(
        url = window.location.href
    ) {
        let urlStr = url.split('?')[1];
        return new URLSearchParams(urlStr);
    }
    // ...
    const roomID = getUrlParams().get('roomID') || randomID(5);
    const kitToken =  ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, roomID,  randomID(5),  randomID(5));

    // 从Kit Token创建实例对象。
    const zp = ZegoUIKitPrebuilt.create(kitToken);
    // ...
    ```
