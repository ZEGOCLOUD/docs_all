ZEGO Express SDK 支持推流到 CDN（Content Delivery Network，内容分发网络），包括转推 CDN 和直推 CDN 两种功能。开发者基于该功能可打通 RTC 产品和 CDN 直播产品，方便用户从网页或第三方播放器直接观看和收听直播内容。为了保证安全，推流到 CDN 时默认开启 CDN 鉴权。

为防止攻击者盗取或伪造您的推流 URL 地址，您可以参考 [CDN 推流鉴权](!CDN_StreamPublishing_Authentication)，提升您推流使用的安全性。

<div class = 'mk-warning'>

在发起转推或直推 CDN 时需注意，CDN 对音视频格式有所要求，推流端音频支持 AAC 与 MP3，视频支持 H.264 与 H.265（需要 CDN 配置）。
</div>

### 转推 CDN

转推 CDN 指的是将音视频流从 ZEGO 音视频云推送到 ZEGO 自有 CDN 或第三方 CDN 的过程。

![](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/relay_cdn.png)  

转推 CDN 包括以下三种方式：
 
<table>
  <colgroup>
    <col width="25%">
    <col width="75%">
  </colgroup>
<tbody><tr>
<th>转推方式</th>
<th>说明</th>
</tr>
<tr>
<td>默认转推 CDN</td>
<td>用户使用 ZEGO Express SDK 推到 ZEGO 音视频云的直播流均会转推到 CDN，目前仅支持 ZEGO 自有 CDN。</td>
</tr>
<tr>
<td>旁路转推 CDN</td>
<td>开发者自定义指定 ZEGO 实时音视频云上的流转推至 CDN，支持 ZEGO 自有 CDN 和第三方 CDN。</td>
</tr>
<tr>
<td>混流转推 CDN</td>
<td>混流场景也可以将输出流转推至 CDN，支持 ZEGO 自有 CDN 和第三方 CDN。</td>
</tr>
</tbody></table>

### 直推 CDN

直推 CDN 指的是将音视频流直接从本地客户端推送到
CDN 的过程，用户可直接通过拉流 URL 地址从网页或第三方播放器进行观看。但由于直推 CDN 功能在网络传输过程中不经过 ZEGO 实时音视频云，因此开发者无法使用 ZEGO 的实时音视频服务。

![](https://doc-media.zego.im/sdk-doc/Pics/Android/streamByCdn/direct_to_cdn.png)

### 功能对比

两种功能的说明与使用场景如下：

<table>
  <colgroup>
    <col width="20%">
    <col width="40%">
  </colgroup>
<tbody><tr>
<th>功能</th>
<th>说明</th>
<th>使用场景</th>
</tr>
<tr>
<td>转推 CDN （推荐）</td>
<td>推流先经过 ZEGO 实时音视频云，再由 ZEGO 实时音视频云转推向 CDN。可使用 ZEGO 提供的实时音视频服务，可用于需要连麦互动的场景。</td>
<td>开发者与第三方 CDN 有业务合作，想要使用原有的第三方 CDN 流媒体网络的分发服务的同时又想使用 ZEGO Express SDK 进行实时连麦互动。适用于有连麦互动要求的业务场景，例如秀场直播、语聊房等。</td>
</tr>
<tr>
<td>直推 CDN</td>
<td>推流不经过 ZEGO 实时音视频云，直接推向 CDN。无法使用 ZEGO 提供的实时音视频服务，适用于单直播场景（无需互动）。</td>
<td>适用于开发者无需使用实时连麦互动等服务的情况，例如电商直播、游戏直播、大班课等。</td>
</tr>
</tbody></table>


































