场景化 AI 降噪，是指实时自动识别不同的场景，智能调整 AI 降噪策略，提供最佳的降噪及音质效果。目前支持两种常见降噪场景：
- 通话场景下，将除人声外的所有声音识别为噪音并进行消除。
在消除稳态噪声（详情请参考 [音频 3A 处理](!AudioAdvanced/Audio_3A_Processing)）的基础上，有效消除非稳态噪声且实现人声高保真，主要噪声包括鼠标、键盘、敲击、空调、厨房碗碟、嘈杂餐厅、环境风声、咳嗽、吹气等非人声的噪声，以及小房间的人声混响。
- 音乐场景下，自动调整降噪效果，还原音乐音质。
实时对 mic 输入进行音乐检测，在声卡、弹唱或近场音乐场景下，自动调整降噪等级，保证音乐的高保真音质。

<div class="mk-warning">

- 使用 AI 降噪功能前，请先联系 ZEGO 技术支持进行特殊编包。
- ZEGO Express SDK 从 3.0.0 版本开始，支持智能识别音乐场景。在音乐场景下，AI 降噪可以自动降低降噪等级，提升音质体验。如需使用该功能，请联系 ZEGO 技术支持进行特殊编包与配置。
</div>

### 功能优势

- 能消除 80% 的噪声。
- 延迟低。
- 占用内存少，和传统降噪基本一致。
- CPU 使用率低。
- 音乐场景识别准确率达 99%。


### 使用场景

本功能适用于语音房、会议、语音开黑等 1v1 或多人音视频通话场景，以及声卡、弹唱、近场音乐的直播或者在线 KTV 场景。

<div class="mk-warning">

音乐场景识别需要打开音乐检测开关，请联系 ZEGO 技术支持配置开启音乐检测功能。
</div>



### 可消除的噪声

开发者可以使用本功能，消除以下噪音：

<table>
  <colgroup>
    <col width="30%">
    <col width="70%">
  </colgroup>
  <tbody><tr>
    <th>场景</th>
    <th>一些典型噪声</th>
  </tr>
  <tr>
    <td>会议室</td>
    <td><ul><li>键盘声</li><li>桌子敲击声</li></ul></td>
  </tr>
  <tr>
    <td>办公室</td>
    <td><ul><li>键盘声</li><li>周围同事说话声</li></ul></td>
  </tr>
  <tr>
    <td>交通工具</td>
    <td><ul>
<li>汽笛声</li>
<li>汽车经过的呼啸声</li>
<li>车载音乐声</li>
<li>雨声及雨刮声</li>
</ul></td>
  </tr>
  <tr>
    <td>网吧</td>
    <td><ul>
<li>键盘声</li>
<li>周围人语音声</li>
</ul></td>
  </tr>
  <tr>
    <td>咖啡厅</td>
    <td><ul>
<li>椅子拖动声</li>
<li>周围人说话声</li>
<li>尖锐碰撞声</li>
</ul></td>
  </tr>
</tbody></table>

## 效果展示

#### 办公室

原始音频包含：鼠标点击声、键盘声、鼓掌声、摩擦声、办公室嘈杂声、空调声等。

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/office_noise_original.mp3" controls>您的浏览器不支持 audio 标签。</audio>

AI 降噪后：

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/office_noise_AIDenoise.mp3" controls>您的浏览器不支持 audio 标签。</audio>

#### 公共场所

原始音频包含：雨声、电车声、炒菜声、汽车呼啸声等。

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/public_noise_original.mp3" controls>您的浏览器不支持 audio 标签。</audio>

AI 降噪后：

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/public_noise_AIDenoise.mp3" controls>您的浏览器不支持 audio 标签。</audio>


#### 音乐场景

原始音频：

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/Original_audio.mp3" controls>您的浏览器不支持 audio 标签。</audio>

常规 AI 降噪：消除噪音，但音乐损伤大。

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/Conventional_AI_noise_reduction_effect.mp3" controls>您的浏览器不支持 audio 标签。</audio>

场景化 AI 降噪后：消除噪音，音乐品质保真。

<audio src="https://doc-media.zego.im/sdk-doc/doc/video/Express_Video_SDK/Audio/Scenario_based_AI_noise_reduction_effect.mp3" controls>您的浏览器不支持 audio 标签。</audio>





















