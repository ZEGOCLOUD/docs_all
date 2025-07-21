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
<td>主播</td>
<td>推一路 RTC 单流，拉取其他麦上听众的 RTC 单流</td>
</tr>
<tr>
<td>麦上听众</td>
<td>推一路 RTC 单流，拉取其他麦上听众和主播的 RTC 单流。</td>
</tr>
<tr>
<td>麦下听众</td>
<td>不推流，仅从 RTC 服务器拉取麦上听众和主播的 RTC 单流。</td>
</tr>
</tbody></table>

![/Pics/GoEnjoy/MetaChat/metachat_stream_management.png](https://doc-media.zego.im/sdk-doc/Pics/GoEnjoy/MetaChat/metachat_stream_management.png)





