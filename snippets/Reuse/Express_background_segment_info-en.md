主体分割与传输即在推流端将矩形视频内的主体（多数情况下是人）通过 AI 算法分离出来并在 RTC 网络中传输、在拉流端渲染的技术。

<div class="mk-warning">

主体分割与传输功能目前为内测功能，如需接入，请联系 ZEGO 商务人员或 ZEGO 技术支持。
</div>

- **用户实际视频画面**

    用户可能身处环境比较复杂的室内或室外，也有可能身处有绿幕背景的直播间。

    |复杂场景|绿幕背景|
    |-|-|
    |<img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_with_realenvironment.jpg" width="90%">    | <img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_with_greenscreen.png" width="90%">


- **ZEGO 主体分割与传输的视频画面**

    ZEGO 通过自研 AI 主体分割算法，准确识别并分离画面中的主体，将分割出的主体信息编码后在 RTC 网络中传输。无论是复杂的实景，还是简单的绿幕背景，都能获得清晰的边缘效果。

    <img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_after_segmentation.png" width="50%">

- **在业务场景中的应用**

    根据不同的业务需求，将拉取到的主体在对应的场景中渲染出来。让身处不同空间的用户，在同一个“空间”中互动。

    <img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/stage.png" width="80%">


### 应用场景

**场景 1**：MR（Mixed Reality，混合现实）多人异地同台
    通过ZEGO主体传输能力，将3D虚拟空间与真实世界的人像融为一体。为企业发布会、年会、在线研讨会等，提供异地同台互动的沉浸式体验。
- 极致沉浸
打造虚实相生的极致沉浸感，还原真实现场体验，提升活动的参与度和效果。
- 极致灵活
主体传输兼容ZEGO RTC网络和CDN网络，无论是嘉宾还是观众，都能根据业务需求选择成本和效果均衡的传输方式。

**场景 2**：同场互动
    ZEGO 提供的主体传输服务，给业务侧处理带来极高的灵活性和可拓展性。通过在拉流端将多个用户的主体渲染到一张统一的背景图上，可以实现：
- 多人在线健身
- 多人在线自习
- 多人在线广场舞
- 多人在线一起看电影


**场景 3**：秀场直播同台 PK
    传统直播主播连麦 PK 时，两个或者多个主播间，始终会被矩形的视频框分隔开，难以实现真正的同台 PK。
    ZEGO 主体分割和传输能力，消除主播间的矩形分割，让主播同处一个场景，提升用户体验感。


### 功能详情


ZEGO 自研实景抠图和绿幕抠图算法，

<table>
  <colgroup>
    <col>
    <col>
    <col>
  </colgroup>
<tbody><tr>
<th>能力类别</th>
<th>实景分割</th>
<th>绿幕分割</th>
</tr>
<tr>
<td>能力描述</td>
<td>将主体从实际场景中分割出来。</td>
<td>将主体从绿幕场景中分割出来。</td>
</tr>
<tr>
<td>优点</td>
<td>对主体所处环境没有过多要求，用户可以随时随地使用。</td>
<td><ul><li>分割的主体不限于人体，可以是商品、人和手里的物体比如杯子、乐器等。</li> <li>边缘处理比实景分割更精细。</li> <li>性能消耗相较于实景分割较少。</li></ul></td>
</tr>
<tr>
<td>缺点</td>
<td><ul><li>边缘处理精细程度略差于绿幕分割。</li> <li>只能分离人像，如果有其他主体，如用户手中的杯子、乐器等，可能会出现异常。</li></ul></td>
<td>用户需要先部署一套绿幕，使用门槛较高。</td>
</tr>
<tr>
<td>分割前</td>
<td>
<img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_with_realenvironment.jpg" width="80%"></td>
<td><img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_with_greenscreen.png" width="80%"></td>
</tr>
<tr>
<td>分割后</td>
<td><img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_after_segmentation.png" width="80%"></td>
<td>
<img src="https://doc-media.zego.im/sdk-doc/Pics/subject_segmentation/people_after_segmentation.png" width="80%"></td>
</tr>
</tbody></table>
