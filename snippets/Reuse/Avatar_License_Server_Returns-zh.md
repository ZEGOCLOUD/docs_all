<table class="collapsible-table" >
  <colgroup>
    <col width="15%">
    <col width="20%">
    <col width="35%">
    <col>
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数名</th>
<th>类型</th>
<th>说明</th>
<th>处理建议</th>
</tr>
<tr data-row-level="2">
<td>Code</td>
<td>unsigned int32</td>
<td><p><b>通过客户端发送请求</b>时，ZegoAvatar 服务端返回的错误码，取值如下：</p>
<ul>
<li>0：成功。</li>
<li>1：参数有误。</li>
<li>2：Token 有误。</li>
<li>3：证书无效。</li>
<li>4：服务内部问题。</li>
</ul></td>
<td rowspan="2"><ul><li>1：请检查您的输入参数 AppID 是否正确, AuthInfo 是否为空。</li>
<li>2：AuthInfo 获取不正确，请联系 ZEGO 技术支持处理。</li>
<li>3：AppId 没有配置可用的包名（Android）或 BundleID（iOS），请联系 ZEGO 商务人员确认。</li>
<li>4：请联系 ZEGO 技术支持处理。</li>
</ul></td>
</tr>
<tr data-row-level="3">
<td>Message</td>
<td>string</td>
<td><p>返回的提示信息，和 “Code” 的取值相对应。</p>
<ul>
<li>0：Success</li>
<li>1：Invalid argument</li>
<li>2：Invalid token</li>
<li>3：No valid license</li>
<li>4：Service unavailable</li>
</ul></td>
</tr>
<tr data-row-level="4" data-row-child="true">
<td>Data</td>
<td>object</td>
<td colspan="2">“Code” 为 0 时，返回鉴权文件的内容；“Code ”返回其他值时，表示获取鉴权失败，Data 为空。</td>
</tr>
<tr data-row-level="4-1">
<td>License</td>
<td>string</td>
<td colspan="2">鉴权文件的内容。</td>
</tr>
</tbody></table>



