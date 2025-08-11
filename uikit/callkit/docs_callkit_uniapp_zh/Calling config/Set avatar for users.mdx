# 设置用户头像

- - -

用户头像通常存储在服务器中。音视频通话 UIKit 不知道每个用户的真实头像，因此默认使用用户名的首字母来绘制用户头像，如下所示：

| 用户静音时 | 用户发言时 |
| -- | -- |
| <Frame width="128" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/_default_avatar_nowave.jpg" /></Frame> | <Frame width="128" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/_default_avatar.jpg" /></Frame> |

要配置自定义用户头像，可以在使用 `ZegoUIKitPrebuiltCall.nvue` 时，通过插槽 `avatarView` 来自定义用户头像视图。

<Note title="说明">
- 您需要根据回调参数中的用户参数为不同的用户返回不同的头像。如果硬编码一个 URL，那么每个人的头像都将是您硬编码的那个 URL。
- 用户头像可以通过 HTTPS 或 HTTP 协议的 URL 地址或 base64 编码字符串来提供。
</Note>

以下是参考代码：

<CodeGroup>
```js title="基本通话" {33}
// YourPage.nvue
<template>
    <ZegoUIKitPrebuiltCall :appID="appID" :callID="callID" :appSign="appSign" :userID="userID" :userName="userName"
        :config="config">
        <template #avatarView="{ userInfo }">
            <image mode="aspectFit" :style="{ width: 130, height: 130, borderRadius: 65 }"
                :src="getAvatar(userInfo)" />
        </template>
    </ZegoUIKitPrebuiltCall>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import keyCenter from "@/pages/KeyCenter";
import ZegoUIKitPrebuiltCall from "@/uni_modules/zego-PrebuiltCall/components/ZegoUIKitPrebuiltCall.nvue"
import { ZegoUIKitPrebuiltCallConfig } from "@/uni_modules/zego-PrebuiltCall"
import AvatarImg from '@/static/avatar/avatar-01.jpeg'

const appID = ref(keyCenter.getAppID());
const appSign = ref(keyCenter.getAppSign());
const userID = ref(keyCenter.getUserID());
const userName = ref(keyCenter.getUserID() + '_Nick');
const callID = ref(keyCenter.getCallID());
const config: ZegoUIKitPrebuiltCallConfig = {
    ...ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall(),
    onHangUp: () => {
        // 挂断后返回上一页
        uni.navigateBack()
    },
};

// 根据 userInfo.userID 判断应该返回的头像地址, 这里简单处理
function getAvatar(userInfo) {
    return AvatarImg
}
</script>
```
</CodeGroup>

完成后，音视频通话 UIKit 将显示您设置的自定义用户头像。
