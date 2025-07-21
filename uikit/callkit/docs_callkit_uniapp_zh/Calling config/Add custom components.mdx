# 添加自定义组件


## 自定义通话界面的前景

如果您想在整个通话界面的顶层添加一些自定义前景，您可以使用 `prebuiltForegroundView` 插槽，该插槽的内容将会显示在视频内容的最上面，您可以用其他内容覆盖上去，实现类似送礼动画、画框等效果。


以下是参考代码：

<CodeGroup>
```js title="基础通话" {4-6}
<template>
    <ZegoUIKitPrebuiltCall :appID="appID" :callID="callID" :appSign="appSign" :userID="userID" :userName="userName"
        :config="config">
        <template #prebuiltForegroundView>
            <image class="forground-image" :src="imgSrc" />
        </template>
    </ZegoUIKitPrebuiltCall>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import keyCenter from "@/pages/KeyCenter";
import ZegoUIKitPrebuiltCall from "@/uni_modules/zego-PrebuiltCall/components/ZegoUIKitPrebuiltCall.nvue"
import { ZegoUIKitPrebuiltCallConfig } from "@/uni_modules/zego-PrebuiltCall"
import PrairieImg from '@/static/pic.jpeg'

// 前景放个图片
const imgSrc = ref(PrairieImg)

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

</script>

<style scoped>
.forground-image {
    margin-top: 200rpx;
    width: 100rpx;
    height: 100rpx;
}
</style>

```
</CodeGroup>

## 自定义音视频视图的前景视图


如果您想要在音视频视图（AudioVideoView）的顶层添加自定义前景视图，例如在音视频视图显示时展示用户标签、彩色用户名、添加用户等级的图标等，则可以使用`audioVideoForeground`插槽。   
`audioVideoForeground` 的参数里将会传入用户信息(userInfo)，您可以根据用户信息，来确定应该显示的内容。


<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/iOS/custom_audio_videoiOS_bg.png" /></Frame>


以下是参考代码：

<CodeGroup>
```js title="基础通话" {4-8}
<template>
    <ZegoUIKitPrebuiltCall :appID="appID" :callID="callID" :appSign="appSign" :userID="userID" :userName="userName"
        :config="config">
        <template #audioVideoForeground="{ userInfo }">
            <view class="userinfo-container">
                <text :style="{ color: getColorByUser(userInfo) }">{{ userInfo.userName }}</text>
            </view>
        </template>
    </ZegoUIKitPrebuiltCall>
</template>
<script setup>
import { ref } from "vue"
import keyCenter from "@/pages/KeyCenter";
import ZegoUIKitPrebuiltCall from "@/uni_modules/zego-PrebuiltCall/components/ZegoUIKitPrebuiltCall.nvue"
import { ZegoUIKitPrebuiltCallConfig } from "@/uni_modules/zego-PrebuiltCall"

const appID = ref(keyCenter.getAppID());
const appSign = ref(keyCenter.getAppSign());
const userID = ref(keyCenter.getUserID());
const userName = ref(keyCenter.getUserID() + '_Nick');
const callID = ref(keyCenter.getCallID());
const config = {
    ...ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall(),
    onHangUp: () => {
        // 挂断后返回上一页
        uni.navigateBack()
    },
};

// 根据用户id显示不同的字体颜色
function getColorByUser(userInfo) {
    if (userInfo.userID == 'user1') {
        return 'green'
    } else {
        return 'red'
    }
}
</script>

<style scoped>
.userinfo-container {
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    background-color: #2A2A2A;

    opacity: 0.7;
    position: absolute;
    padding-left: 5rpx;
    padding-right: 5rpx;
    padding-bottom: 3rpx;
    padding-top: 3rpx;
    border-radius: 6rpx;
    top: 5rpx;
    left: 5rpx;
    
}
</style>

```
</CodeGroup>


