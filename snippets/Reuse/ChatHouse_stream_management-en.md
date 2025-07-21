## 推拉流管理

为了实现成本与体验效果的平衡，本方案各角色的推拉流策略如下表所示：

<table>
  <colgroup>
    <col>
    <col>
  </colgroup>
<tbody><tr>
<th>角色</th>
<th>推拉流</th>
</tr>
<tr>
<td>房主</td>
<td>推一路 RTC 单流，拉取其他麦上观众的 RTC 单流，并负责发起混流任务。</td>
</tr>
<tr>
<td>麦上观众</td>
<td>推一路 RTC 单流，拉取其他麦上观众和房主的 RTC 单流。</td>
</tr>
<tr>
<td>麦下观众</td>
<td>不推流，不从 RTC 服务器拉单流，仅拉取 ZEGO CDN 混流。</td>
</tr>
</tbody></table>


![CDN拉流](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/mixed_flow.png)

有关混流相关接口的使用及注意事项，请参考 [实时音视频 - 基础功能 - 混流](!ExpressVideoSDK-Other_Functions/Mixer)。    

如需转推至 ZEGO 外的第三方 CDN，请参考 [实时音视频 - 基础功能 - 使用CDN直播](!ExpressVideoSDK-Publisher_Player_Advanced/RelayToCDN)。

<div class='mk-warning'>

混流如需使用 ZEGO CDN 服务，需要在控制台开通混流时，选择混流转推方式为 **转推到 ZEGO CDN**，详情请参考 [控制台 - 项目管理 - 服务配置 - CDN](#14214)。
</div>
