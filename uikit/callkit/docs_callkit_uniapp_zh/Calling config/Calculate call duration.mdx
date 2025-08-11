# 计算通话时长


本文档描述了如何通过配置来计算通话时长。

<Frame width="200" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/call/call_duration.jpeg" /></Frame>

## 实现流程

如需计算通话时长，请执行以下操作：

1. 将 `durationConfig` 的 `showDuration` 属性设置为 `true`（显示当前通话计时器，默认值）。

2. 开发者可以通过设置 `durationConfig` 的 `onDurationUpdate` 来监听通话时长更新事件并获取通话时长（参考以下代码）。每隔 1s 触发一次，不建议运行耗时任务。


以下是参考代码：

<CodeGroup>
```js title="基本通话"
// YourPage.nvue
<template>
    <ZegoUIKitPrebuiltCall :appID="appID" :callID="callID" :appSign="appSign" :userID="userID" :userName="userName"
        :config="config">
    </ZegoUIKitPrebuiltCall>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import keyCenter from "@/pages/KeyCenter";
import ZegoUIKitPrebuiltCall from "@/uni_modules/zego-PrebuiltCall/components/ZegoUIKitPrebuiltCall.nvue"
import { ZegoUIKitPrebuiltCallConfig } from "@/uni_modules/zego-PrebuiltCall"

const appID = ref(keyCenter.getAppID());
const appSign = ref(keyCenter.getAppSign());
const userID = ref(keyCenter.getUserID());
const userName = ref(keyCenter.getUserID() + '_Nick');
const callID = ref(keyCenter.getCallID());

const config: ZegoUIKitPrebuiltCallConfig = {
    ...ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall(), // 预设配置
    durationConfig: {
        showDuration: true,
        onDurationUpdate: (seconds)=>{
            console.log(`已经通话的时长: ${seconds} 秒`);
        }
    },
    onHangUp: () => {
        // 挂断后返回上一页
        uni.navigateBack()
    },
};

</script>

```
</CodeGroup>
