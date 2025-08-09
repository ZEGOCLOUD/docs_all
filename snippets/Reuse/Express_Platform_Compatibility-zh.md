极速视频支持 iOS、Android、Windows、macOS、HarmonyOS、Web、小程序并支持平台间互通，具体的兼容性要求见下表。
<table>
  <colgroup>
    <col width="20%">
    <col width="57%">
    <col width="23%">
  </colgroup>
<tbody><tr>
<th>平台</th>
<th>支持版本</th>
<th>支持架构</th>
</tr>
<tr>
<td>iOS</td>
<td>12.0 或以上版本</td>
<td><ul><li>arm64</li><li>x86_64（模拟器）</li><li>arm64（模拟器）</li><li>x86_64（Mac Catalyst）</li><li>arm64（Mac Catalyst）</li></ul></td>
</tr>
<tr>
<td>Android</td>
<td>4.4 或以上版本</td>
<td><ul><li>arm64-v8a</li><li>armeabi-v7a</li><li>x86</li><li>x86_64</li></ul></td>
</tr>
<tr>
<td>Windows</td>
<td>Windows 7 或以上版本</td>
<td><ul><li>x86</li><li>x64</li></ul></td>
</tr>
<tr>
<td>Linux</td>
<td>任意具有 GLIBC 2.16 或以上版本的 Linux 发行版系统</td>
<td><ul><li>amd64 (x86_64-linux-gnu)</li><li>arm64 (aarch64-linux-gnu)</li><li> armhf (arm-linux-gnueabihf)</li><li>armel (arm-linux-gnueabi)</li></ul></td>
</tr>
<tr>
<td>HarmonyOS</td>
<td><ul><li>DevEco Studio 4.1.3.600 Release 或以上版本</li><li>配套 <a href="https://developer.harmonyos.com/cn/docs/documentation/doc-references-V2/syscap-0000001580345394-V2?catalogVersion=V2" target="blank">API Version 11</a> 的 HarmonyOS NEXT SDK 或以上版本</li><li>配套 <a href="https://developer.harmonyos.com/cn/docs/documentation/doc-references-V2/syscap-0000001580345394-V2?catalogVersion=V2" target="blank">API Version 11</a> 的 HarmonyOS NEXT 2.0.0.59 操作系统或以上版本</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>macOS</td>
<td>10.13 或以上版本</td>
<td><ul><li>x86_64</li><li>arm64</li></ul></td>
</tr>
<tr>
<td>Web</td>
<td><ul><li>Chrome 58 或以上版本</li><li>Firefox 56 或以上版本</li><li>Safari 11 或以上版本</li><li>Opera 45 或以上版本</li><li>QQ 浏览器 Windows 10.1 或以上版本、macOS 4.4 或以上版本</li><li>360 安全浏览器极速模式</li></ul><p>更多兼容性要求，请参考 <a target="_blank" href="/real-time-video-web/introduction/browser-restrictions">限制说明 - 浏览器兼容性和已知问题</a></p></td>
<td>-</td>
</tr>
<tr>
<td>小程序</td>
<td><ul><li>微信小程序基础库 1.7.0 或以上版本</li><li>支付宝小程序基础库 1.23.0 或以上版本，低版本需要做 <a target="_blank" href="https://opendocs.alipay.com/mini/framework/compatibility">兼容处理</a></li></ul></td>
<td>-</td>
</tr>
<tr>
<td>Flutter</td>
<td><ul>
<li>Flutter 2.0 或以上版本</li>
<li>iOS 12.0 或以上版本</li>
<li>Android 4.4 或以上版本
</li><li>Windows 8 或以上版本</li>
<li>Web： Chrome 58 或以上版本、Firefox 56 或以上版本、Safari 11 或以上版本、Opera 45 或以上版本、QQ 浏览器 Windows 10.1 或以上版本/macOS 4.4 或以上版本、360 安全浏览器极速模式</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>Electron</td>
<td><ul><li>Electron 7.0.0 或以上版本</li><li>Windows 7 及以上 / macOS 10.13 及以上操作系统</li><li>Linux 支持 x86_64、aarch64、armhf 架构的 Linux 操作系统，如需使用 Linux 平台，请联系 ZEGO 技术支持。</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>uni-app</td>
<td><ul><li>HBuilderX 3.0.0 或以上版本</li><li>iOS 12.0 或以上版本</li><li>Android 4.4 或以上版本</li><li>Web： Chrome 58 或以上版本、Firefox 56 或以上版本、Safari 11 或以上版本、Opera 45 或以上版本、QQ 浏览器 Windows 10.1 或以上版本/macOS 4.4 或以上版本、360 安全浏览器极速模式</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>Unity3D</td>
<td><ul><li>Unity 2018.4.21f1 或以上版本</li><li>Android：Android 4.4 或以上版本</li><li>iOS：Xcode 15.0 或以上版本，iOS 12.0 或以上版本</li><li>macOS：macOS 10.13 或以上版本</li><li>Windows：Windows 7 或以上版本</li><li>Linux：任意具有 GLIBC 2.16 或以上版本的 Linux 发行版系统（目前仅支持 x86_64 架构），libasound（ALSA），libv4l2（v4l utils），CMake 3.7 或以上版本</li><li>WebGL：浏览器需要支持 WebGL 以及 WebAssembly（推荐使用 WebGL 2.0），Chrome 57 或以上版本、Firefox 56 或以上版本、Safari 11 或以上版本，不支持移动端</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>React Native</td>
<td><ul><li>React Native 0.60.0 或以上版本</li><li>iOS 12.0 或以上版本</li><li>Android 4.4 或以上版本</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>Unreal Engine</td>
<td><ul><li>Unreal Engine 4.25 或以上版本</li><li>iOS 12.0 或以上版本</li><li>Android 5.0 或以上版本</li><li>macOS 11 或以上版本</li><li>Windows 7 或以上版本</li></ul></td>
<td>-</td>
</tr>
<tr>
<td>Cocos Creator</td>
<td><ul><li>Cocos Creator 3.6.0 或以上版本</li><li>iOS 12.0 或以上版本</li><li>Android 5.0 或以上版本</li><li>macOS 10.13 或以上版本</li><li>Windows 7 或以上版本</li></ul></td>
<td>-</td>
</tr>
</tbody></table>


<div class="mk-hint">

如果您有更多关于平台或版本支持的相关需求，请联系 ZEGO 技术支持处理。
</div>


























































































