# 背景虚化及虚拟背景
- - -

<Note title="说明">
- 本功能仅支持 2.15.0 及以上版本的音视频通话 UIKit。
- 本功能为付费功能，如需使用，请联系 ZEGO 商务人员。
</Note>

## 功能概述

音视频通话 UIKit 支持用户在通话时将本端画面的背景虚化或使用虚拟背景，有效保护通话隐私。

<Frame width="auto" height="auto" caption="">
  <img src="https://media-resource.spreading.io/docuo/workspace741/896bc39e2e65b82d5670b01b7c131c30/f59bd5abe2.jpeg" alt="BackgroundFeature.jpeg"/>
</Frame>

### 兼容性

背景虚化及虚拟背景功能支持的浏览器如下表：

| 浏览器 | 兼容版本 |
|  ----  | ----  |
|Google Chrome	| 90 及以上|
|Firefox | 111 及以上|
|Safari | 15 及以上 |
|移动端浏览器| 不支持 |
|微信内嵌网页| 不支持 |

### 设备和浏览器要求

请确认您的设备和浏览器满足以下要求：
- 配备 Core i5 或以上 CPU。
- 配备 8GB 或以上 RAM。
- （推荐）最新版桌面端 Google Chrome 浏览器。

## 实现流程

### 1 获取资源

安装依赖后，背景虚化和虚拟背景功能需要 `node_module/@zegocloud/zego-uikit-prebuilt/assets` 目录下的所有资源文件，请将此 `assets` 文件夹拷贝到您的项目根目录。

<Frame width="auto" height="auto" caption="">
  <img src="https://media-resource.spreading.io/docuo/workspace741/896bc39e2e65b82d5670b01b7c131c30/aa507037c3.jpeg" alt="WebAssets.jpeg"/>
</Frame>

### 2 设置配置

在创建 ZegoUIKitPrebuilt 实例时，传入 `BackgroundProcessConfig` 参数，设置背景虚化或虚拟背景的配置。

<Note title="说明">
背景虚化和虚拟背景互斥，如果您同时设置了 `blurDegree`，`objectFit` 和 `source` 参数，则仅 `blurDegree` 参数生效，只能实现背景虚化。
</Note>

<CodeGroup>
```typescript title="背景虚化"
/**
 * BackgroundProcessConfig 参数说明
 * BackgroundProcessConfig?: {
 *   blurDegree?: 1 | 2 | 3, // 虚化等级 1、2、3，等级越大，虚化程度越高
 *                           // 当设置了 blurDegree 时，source 和 objectFit 参数无效
 *   source?: HTMLImageElement, // 虚拟背景图片的 HTMLImageElement
 *   objectFit?: 'fill' | 'contain' | 'cover', // 虚拟背景填充方式
 * }
*/
// 背景虚化
const zp = ZegoUIKitPrebuilt.create(kitToken, { BackgroundProcessConfig: { blurDegree: 1 } });
```

```typescript title="虚拟背景"
/**
 * BackgroundProcessConfig 参数说明
 * BackgroundProcessConfig?: {
 *   blurDegree?: 1 | 2 | 3, // 虚化等级 1、2、3，等级越大，虚化程度越高
 *                           // 当设置了 blurDegree 时，source 和 objectFit 参数无效
 *   source?: HTMLImageElement, // 虚拟背景图片的 HTMLImageElement
 *   objectFit?: 'fill' | 'contain' | 'cover', // 虚拟背景填充方式
 * }
*/
// 虚拟背景
const img = document.createElement("img");
img.src = require("./background.jpg"); // 您的背景图片路径
const zp = ZegoUIKitPrebuilt.create(kitToken, { BackgroundProcessConfig: { source: img, objectFit: "fill" } });
```
</CodeGroup>

### 3 展示按钮

音视频通话 UIKit 默认不展示用于开关背景虚化及虚拟背景功能的按钮，若您允许用户自行开启或关闭效果，可将 `showBackgroundProcessButton` 参数设置为 `true`，即可在房间内显示此按钮。

```ts {2}
zp.joinRoom({
    showBackgroundProcessButton: true
})
```

## 自定义功能启用逻辑

如果您需要自定义本功能启用逻辑，可在通过 `onLocalStreamCreated`监听本地流创建成功后，调用 `openBackgroundProcess` 方法，启用此功能。如需关闭此功能，调用 `closeBackgroundProcess` 方法。

```ts {3,5,13}
zp.joinRoom({
    // 本地流创建成功回调
    onLocalStreamCreated: (stream) => {
        // ...
        // 开启背景虚化或虚拟背景
        zp.openBackgroundProcess();
        // 您的业务逻辑
    }
})

//...

// 关闭背景虚化或虚拟背景
zp.closeBackgroundProcess();
```