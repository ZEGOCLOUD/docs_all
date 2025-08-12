## 功能简介

ZEGO Express SDK 提供了 AI 降噪功能，开发者可以在使用麦克风采集声音时，对声音进行降噪处理；并在传统降噪（详情请参考 [噪声抑制](!Audio_3A_Processing#4_3)）消除稳态噪声的基础上，同步处理非稳态噪声（包括鼠标点击声、键盘声、敲击声、空调声、厨房碗碟碰撞声、餐厅嘈杂声、环境风声、咳嗽声、吹气声等非人声噪声），保留纯净语音，提升用户的通话体验。

<div class="mk-warning">

使用 AI 降噪功能前，请先联系 ZEGO 技术支持进行特殊编包。
</div>

### 功能优势

- 能消除 80% 的噪声。
- 延迟低。
- 占用内存少，和传统降噪基本一致。
- CPU 使用率低。


### 使用场景

本功能可应用于通话、会议等没有背景音乐等场景。

<div class="mk-warning">

使用本功能时，会对麦克风采集的音乐（包括人通过麦克风唱歌的声音）有一定的损伤，但是对音效播放器、媒体播放器推送的数据不会有影响。
</div>

- 普通音质语聊房场景。
- 会议场景。
- 音视频通话场景（如语音开黑、1v1 视频通话等）。


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









