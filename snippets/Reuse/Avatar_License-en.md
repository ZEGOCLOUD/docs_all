## 概览

本文将介绍如何获取鉴权文件、以及在线鉴权的实现方案。

### 鉴权文件

鉴权文件是软件使用权的凭证，包含以下特征：

- 授权的时间
- 授权的平台
- 授权的 SDK 版本号
- 授权的功能特性


### 在线鉴权

在线鉴权，是指用户的客户端访问 ZegoAvatar 服务端，申请鉴权文件，进行网络验证的方式。从客户的角度来看可以通过在线鉴权快速，安全的通过网络验证，相比离线鉴权更可控更高效。

只有通过在线鉴权的客户端，才可以使用 ZegoAvatar SDK 的功能。

## 鉴权实现原理

在线鉴权有两种方式，开发者可以通过自己的客户端，或自己的业务服务端访问 ZegoAvatar 服务端，进行鉴权。

以下将介绍“向 ZegoAvatar 服务端请求鉴权文件”的两种方式：`通过客户端发送请求`和`通过开发者服务端发送请求`，对比如下：

<table>
  <colgroup>
    <col width="14%">
    <col width="43%">
    <col width="43%">
  </colgroup>
  <tbody><tr>
    <th>类别</th>
    <th>通过客户端发送请求</th>
    <th>通过开发者服务端发送请求</th>
  </tr>
  <tr>
    <td>实现步骤</td>
    <td><ol><li>客户端访问 ZegoAvatar SDK，获取授权信息。</li><li>ZegoAvatar SDK 返回授权信息 AuthInfo 到客户端。</li><li>客户端通过 URL 携带 AppID 和 AuthInfo，向 ZegoAvatar 服务端发送请求。</li><li>ZegoAvatar 服务端返回鉴权文件 License 到客户端。</li><li>客户端传入获取到的 License 文件，创建 ZegoAvatarService 对象。</li><li>启用 AI 功能，开始表情识别。</li>&nbsp;</ol></td>
    <td><ol>&nbsp;<li>开发者服务端通过公共网关接口 URL，直接向 ZegoAvatar 服务端发送请求。</li><li>ZegoAvatar 服务端返回鉴权文件 License 到开发者服务端。</li>
<li>开发者服务端下发 License 文件到客户端。<b>（由开发者自行实现此业务功能）</b></li><li>客户端传入获取到的 License 文件，创建 ZegoAvatarService 对象。</li><li>启用 AI 功能，开始表情识别。</li>&nbsp;</ol></td>
  </tr>
  <tr>
    <td>流程图</td>
    <td><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoAvatar/avatar_flow_1.png" width="98%"></td>
    <td><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoAvatar/avatar_flow_2.png" width="98%"></td>
  </tr>
  <tr>
    <td>优势</td>
    <td><ul><li>简单、容易接入。</li><li>开发者无需搭建自己的业务后台，也无需自行管理鉴权文件。</li></ul></td>
    <td><ul><li>开发者自行搭建的业务后台，请求网络相对稳定；且由于服务器的位置相对稳定，命中 DNS 缓存的几率也会提高。</li><li>开发者可通过自己的客户端，自行设置鉴权能力，管理鉴权文件，灵活性较高。</li></ul></td>
  </tr>
</tbody></table>



## 前提条件

实现“在线鉴权”之前：

1. 请先在 [ZEGO 控制台](https://console.zego.im/) 创建项目，并申请有效的 AppId 并申请有效的 AppId，详情请参考 [控制台 - 项目管理](#12107) 中的“项目信息”。

2. 请联系 ZEGO 商务人员，提供申请到的 AppId，获取鉴权需要使用的 AppSign，并开通相关权限。
