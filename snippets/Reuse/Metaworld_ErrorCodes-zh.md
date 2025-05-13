<table>
  <colgroup>
    <col width="10%">
    <col width="40%">
    <col width="50%">
  </colgroup>
<tbody><tr>
<th>错误码</th>
<th>描述</th>
<th>处理意见</th>
</tr>
<tr>
<td>0</td>
<td>成功。</td>
<td>-</td>
</tr>
<tr>
<td>1000001</td>
<td>未知错误。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>5000001</td>
<td>License 格式无效。</td>
<td><p>请检查 License 是否正确。</p><p>请注意：License 必须是通过请求 ZEGO 服务器获取到的字符串（具体请参考 <a href="!metaworld_license" target="_blank">设置 License 鉴权</a>），而不是通过 ZegoMetaWorldService 的 <code>getAuthInfo</code> 接口获取到的签名字符串。</p><p></p></td>
</tr>
<tr>
<td>5000002</td>
<td>License 已过期。</td>
<td>请联系 ZEGO 技术支持，确认套餐是否正常；或确认手机、设备时间是否为标准时间。</td>
</tr>
<tr>
<td>5000004</td>
<td>License 不包含当前平台（Android、iOS）的授权。</td>
<td>请联系 ZEGO 技术支持，将当前平台添加到 License 中。</td>
</tr>
<tr>
<td>5000005</td>
<td>当前应用不支持该 License，License 不包含该应用的 ApplicationID（Android 平台）或 BundleID（iOS 平台）。</td>
<td>请联系 ZEGO 技术支持添加对应的 ApplicationID 或 BundleID。</td>
</tr>
<tr>
<td>5000006</td>
<td>初始化 ZegoMetaWorldService 时，没有进行鉴权。</td>
<td>请在初始化 ZegoMetaWorldService 时，传入 License，鉴权通过后才能进行其他操作。</td>
</tr>
<tr>
<td>5000200</td>
<td>License 包含 SDK 不支持的特性。</td>
<td>请联系 ZEGO 技术支持确认 SDK 版本是否正确。</td>
</tr>
<tr>
<td>5000201</td>
<td>License 不包含 AI 捏脸功能的授权。</td>
<td>请联系 ZEGO 技术支持确认授权配置是否正确。</td>
</tr>
<tr>
<td>5000202</td>
<td>License 不包含手动捏脸、妆容换转等功能的授权。</td>
<td>请联系 ZEGO 技术支持确认授权配置是否正确。</td>
</tr>
<tr>
<td>5000203</td>
<td>License 不包含表情随动功能的授权。</td>
<td>请联系 ZEGO 技术支持确认授权配置是否正确。</td>
</tr>
<tr>
<td>5000204</td>
<td>缺少可用的 License。</td>
<td>请确认鉴权是否成功。</td>
</tr>
<tr>
<td>5000206</td>
<td>License 不包括声音随动功能的授权。</td>
<td>请联系 ZEGO 技术支持确认授权配置是否正确。</td>
</tr>
<tr>
<td>5000207</td>
<td>License 不包括肢体随动功能的授权。</td>
<td>请联系 ZEGO 技术支持确认授权配置是否正确。</td>
</tr>
<tr>
<td>6000100</td>
<td>打开摄像头失败。</td>
<td>
请先确认设备是否有可用的摄像头。如果摄像头可用，请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>6000101</td>
<td>调用表情随动、肢体随动等功能的相关接口时，缺少摄像头权限。</td>
<td>请确认摄像头权限是否成功获取。</td>
</tr>
<tr>
<td>6000102</td>
<td>调用声音驱动、录制音频等功能的相关接口时，缺少麦克风权限。</td>
<td>请确认麦克风权限是否成功获取。</td>
</tr>
<tr>
<td>6000103</td>
<td>
当前设备的摄像头驱动异常或硬件异常，导致配置或启动摄像头失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>6000104</td>
<td>当前设备的摄像头驱动异常或硬件异常，导致配置摄像头参数失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>6000105</td>
<td>设备的摄像头被其他应用占用，启动摄像头预览失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>6000200</td>
<td>AI 模型的路径参数未设置或者值为空字符串。</td>
<td>请确保初始化时传入的 AIPath 的值是正确的文件路径。</td>
</tr>
<tr>
<td>6000201</td>
<td>AI 模型的路径参数对应的文件不存在。</td>
<td>请确保初始化时传入的 AIPath 对应的文件真实存在。</td>
</tr>
<tr>
<td>8010000</td>
<td>房间资源下载失败，可能是本地网络连接失败，或者房间资源已失效。</td>
<td>请确认本地网络连接是否正常，以及服务器资源是否有效。</td>
</tr>
<tr>
<td>8010001</td>
<td>房间资源加载失败，可能是房间资源制作异常。</td>
<td>请联系 ZEGO 技术支持确认。</td>
</tr>
<tr>
<td>8010001</td>
<td>角色资源下载失败，可能是本地网络连接失败，或者角色资源已失效。</td>
<td>请确认本地网络连接是否正常，以及服务器资源是否有效。</td>
</tr>
<tr>
<td>8010002</td>
<td>角色资源加载失败，可能是角色资源制作异常。</td>
<td>请联系 ZEGO 技术支持确认。</td>
</tr>
<tr>
<td>8010003</td>
<td>角色出生点位置为空，可能是房间资源没有配置默认出生点。</td>
<td>请联系 ZEGO 技术支持确认。</td>
</tr>
<tr>
<td>8020000</td>
<td>角色控制器播放动画失败，对应 ID 的角色动画未编排、或编排时未赋予动画资源列表。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8020001</td>
<td>角色控制器播放动画失败，编排时对应 ID 的资源列表未赋予动画片段。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8020002</td>
<td>角色控制器播放动画失败，动画组件不存在。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8030000</td>
<td>镜头特效列表为空，对应的特效 ID 未编排。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8030001</td>
<td>找不到与镜头特效 ID 匹配的镜头特效。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8030002</td>
<td>镜头跟踪目标为空。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8030003</td>
<td>镜头注视目标为空。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040000</td>
<td>特效配置文件 URL 路径为空。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040001</td>
<td>特效组件初始化失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040002</td>
<td>特效配置文件解析失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040003</td>
<td>传入的特效 ID 为空。</td>
<td>请检查 <code>playEffect</code> 方法传入的特效 ID 是否为空。</td>
</tr>
<tr>
<td>8040004</td>
<td>特效配置文件配置节点有误。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040005</td>
<td>特效资源加载失败。</td>
<td>请先检查特效资源服务器路径是否有效。如果确认有效，请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040006</td>
<td>特效轨迹配置异常，最多支持 1 条轨迹。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8040007</td>
<td>没有可执行的特效任务。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8070002</td>
<td>资源加载异常，不存在 catalog 文件。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8070003</td>
<td>资源加载异常，本地索引文件失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8070004</td>
<td>资源加载异常，出现未知错误。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8070005</td>
<td>资源加载异常，文件索引 key 不匹配。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8080000</td>
<td>加载 Avatar 房间失败，Avatar 房间对应的资源不存在或者下载失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<tr>
<td>8080001</td>
<td>创建 Avatar 失败，Avatar 对应的资源不存在或者下载失败。</td>
<td>请先 <a href="/faq/MetaWorld_log?product=Metaworld" target="_blank">获取日志</a>，并联系 ZEGO 技术支持处理。</td>
</tr>
<td>8090001</td>
<td>使用范围语音推流失败，userID 或 roomID 是空。</td>
<td>请检查 userID、roomID 是否正确。</td>
</tr>
</tbody></table>













