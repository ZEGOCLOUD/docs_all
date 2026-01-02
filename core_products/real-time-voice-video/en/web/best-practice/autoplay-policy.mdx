# 浏览器自动播放策略（Web）

---

## 应用场景


为了避免网页自动播放音视频对用户造成干扰，浏览器加强了对自动播放策略（Autoplay）的限制：**浏览器在没有交互操作之前不允许有声音的媒体文件自动播放**。

各个浏览器关于自动播放策略有不同的实现，详情请参考以下文章：

- Chrome：[Autoplay Policy Changes](https://developers.google.com/web/updates/2017/09/autoplay-policy-changes)。
- Safari：[Auto-Play Policy Changes for macOS](https://webkit.org/blog/7734/auto-play-policy-changes-for-macos/)。
- Firefox：[Allow or block media autoplay in Firefox](https://support.mozilla.org/en-US/kb/block-autoplay)。
- 旧版本 Safari 同时播放多视频限制：[Safari 同时播放多视频限制](https://doc-zh.zego.im/article/9327)。

在使用 ZEGO Web SDK 拉流时，媒体流中包含音频且未静音会受到浏览器自动播放策略的限制，导致音频不能正常播放。本文主要介绍如何解决 SDK 因自动播放策略限制，导致播放失败的问题。

## 解决方案

为了解决上述播放失败的问题，本文介绍的以下两种解决方案：

- 方案一：使用 SDK 提供的自动播放弹窗。
- 方案二：业务应用层自行进行恢复播放处理。

### 使用 SDK 提供的自动播放弹窗

使用 SDK 提供的媒体流播放组件 [ZegoStreamView](/article/api?doc=Express_Video_SDK_API~javascript_web~class~ZegoStreamView) 来播放媒体流，当自动播放失败时，SDK 会在界面上弹窗引导用户点击页面。产生交互后 SDK 主动恢复播放媒体流的音视频。

- 优点：业务应用层无需再做任何处理，简单高效。

- 缺点：SDK 提供的弹窗不一定符合业务产品设计要求，此时可考虑使用方案二。

### 业务应用层实现恢复播放

1. 在 [ZegoStreamView.play](/article/api?doc=Express_Video_SDK_API~javascript_web~class~ZegoStreamView#play) 接口中将第二个参数 [options.enableAutoplayDialog](/article/api?doc=Express_Video_SDK_API~javascript_web~interface~ZegoStreamViewOptions#mirror) 参数设置为 false，关闭 SDK 的自动弹窗。

2. 监听自动播放失败错误事件，当自动播放失败时，显示弹窗或按钮引导用户与页面产生交互后，再调用 [ZegoStreamView.resume](/article/api?doc=Express_Video_SDK_API~javascript_web~class~ZegoStreamView#resume) 接口恢复播放。

  <Warning title="注意">

  在大多数浏览器进行如上操作可以避免出现自动播放失败。但是由于各浏览器厂商对于自动播放策略的实现存在差异，即使提前引导用户与页面产生交互或者设置静音，也不能确保不会出现自动播放失败错误，例如 iOS 的 Safari 浏览器、微信浏览器及其小程序的 Webview 中，自动播放限制较为严格，**因此第二步的处理作为保底策略必须保留**。
  </Warning>

3. （可选）在进入页面时提前引导用户与页面产生交互（例如点击、触摸等），后面再调用 [ZegoStreamView.play](/article/api?doc=Express_Video_SDK_API~javascript_web~class~ZegoStreamView#play) 播放音视频。

```js
// remoteStreamView 为远端媒体流播放组件实例对象。
remoteStreamView.play('remote-video', {
  enableAutoplayDialog: false
});
remoteStreamView.on("autoplayFailed",()=>{
    // 自动播放受限导致播放失败，在界面上显示自定义的按钮，引导用户点击按钮。
    // 在按钮的点击事件的回调函数中，执行 remoteStreamView.resume();
});
```
