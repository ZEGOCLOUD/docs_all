地理围栏指将音视频及信令数据传输限定在某一区域，用以满足地区数据隐私安全相关法规，即限定访问某一特定区域的音视频服务。例如，当指定的地理围栏区域为欧洲时，不区分 App 用户所在区域，SDK 实际访问的区域将为欧洲。


<table>
  <colgroup>
    <col>
    <col>
  </colgroup>
<tbody><tr>
<th>指定的地理围栏区域</th>
<th>App 用户所在区域</th>
<th>SDK 实际访问的区域</th>
<th>连接后的用户体验</th>
</tr>
<tr>
<td>欧洲</td>
<td>欧洲</td>
<td>欧洲</td>
<td>正常</td>
</tr>
<tr>
<td>欧洲</td>
<td>中国</td>
<td>欧洲</td>
<td>可能受到较大影响</td>
</tr>
</tbody></table>

<div class="mk-warning">

- 如果指定地理围栏区域的服务器都不可用，SDK 会直接报错。
- 由于指定地理围栏区域与 App 用户所在区域之间存在跨区域公共互联网，公共互联网网络质量较差会导致音视频体验受到影响。
</div>

![/Pics/Express/Geofencing_pic.jpeg](https://doc-media.zego.im/sdk-doc/Pics/Express/Geofencing_pic.jpeg)

当前 SDK 支持配置地区如下：

<div class="mk-hint">

如需支持更多区域，请联系 ZEGO 技术支持。
</div>


|地区|枚举| 取值 |
|-|-|-|
|中国大陆，不包含港澳台|CN| 2 |
|北美|NA| 3 |
|欧洲|EU| 4 |
|亚洲，不包括中国大陆和印度|AS| 5 |
|印度|IN| 6 |
