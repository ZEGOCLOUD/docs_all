# 使用 Token 鉴权

---

## 1 功能简介

鉴权是指验证用户是否拥有访问系统的权限，ZEGO 通过 Token 对用户进行鉴权，来避免因权限控制缺失或操作不当引发的风险问题。

用户在登录房间时带上 Token 参数，ZEGO 服务端会根据 Token 来判断用户的权限，目前仅支持校验用户登录房间和用户在房间内推流这两个权限。

<div class="mk-warning">

使用 Token 鉴权功能前，请联系 ZEGO 技术支持开通。

</div>

为提高业务安全性，ZEGO 建议开发者使用 Token 鉴权，来做一些业务上“进房限制”或“上麦限制”，特别是以下场景：

- 房间有普通房间和会员房间的区别，需要控制非会员用户登录会员房间。
- 语聊房中，需要控制推流用户和麦上用户的一致，防止“幽灵麦”现象，即在房间里听到了非麦上用户声音的情况。
- 狼人杀等发言游戏，需要防止应用被黑客破解之后，黑客可以使用其他用户 ID 登录同一房间，获取到游戏进行的信息进行作弊，影响正常用户的游戏体验。

## 2 前提条件

- 根据实际业务情况，联系 ZEGO 技术支持开通 Token 鉴权功能。
- 已在项目中集成 ZEGO Express SDK（2.8.0 版本及以上），实现基本的实时音视频功能，请参考 [快速开始 - 集成](!ExpressVideoSDK-Integration/SDK_Integration) 和 [快速开始 - 实现视频通话](!ExpressVideoSDK-Integration/Solution_Implementation)。


## 3 实现流程

开通 Token 鉴权功能后，由开发者的服务端生成 Token，用户携带 Token 登录房间，ZEGO 服务端对带着 Token 的用户进行校验，来判断用户是否能登录房间或在房间内推流。

使用 Token 判断用户是否能登录房间的使用流程如下图：

![token_uml](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/token_uml.png)

1. 客户端发起申请 Token 的请求。
2. 在开发者的服务端上生成 Token，并返回给客户端。
3. 客户端携带申请到的 Token 和 userID、roomID 信息，登录对应的房间。
4. ZEGO SDK 会自动将 Token 发送到 ZEGO 服务端进行校验。
5. ZEGO 服务端会将校验的结果返回给 ZEGO SDK。
6. ZEGO SDK 再将校验的结果直接返回给客户端，没有权限客户端登录将失败。


## 4 使用步骤

本节将详细介绍如何在开发者的服务端上生成 Token、如何使用 Token 和 Token 过期时的处理方式。

### 4.1 生成 Token

开发者获得项目的 AppID 和 ServerSecret 信息后，根据实际业务需求，即可在自己的服务端生成带有校验规则的 Token，校验规则如下：

- 只校验登录权限：登录时校验权限，推流时不校验权限。
- 只校验推流权限：推流时校验权限，登录时不校验权限。
- 同时校验登录和推流权限：登录和推流时均校验权限。


<div class="mk-warning">

为保证安全性，开发者一定要在自己的服务端生成 Token。

</div>


#### 4.1.1 获取 AppId 和 ServerSecret

生成 Token 需要开发者项目的唯一标识 AppId 和密钥 ServerSecret，获取方式如下：

1. 在 [ZEGO 控制台](https://console.zego.im/) 中，在“概览 > 我的项目”中，即可查看 AppID。


2. 在 [ZEGO 控制台](https://console.zego.im/) 中，在“概览 > 我的项目”中，单击项目的“查看”信息，进入项目的“基本信息”页。单击“服务端API密钥”下的“查看”，弹窗中的 “ServerSecret” 即生成 Token 需要使用的密钥。


<div class = 'mk-hint'>

可按如下方式查看控制台界面：
- **2021-11-16** 之后在 [ZEGO 控制台](https://console.zego.im) 创建项目的用户，请参考 [控制台 - 项目管理](12107#3)  中的 “查看项目基本信息”。
- **2021-11-16** 及之前在 [ZEGO 控制台](https://console.zego.im) 创建项目的用户，请参考  [控制台（旧版） - 项目管理](1265#3)  中的 “查看项目基本信息”。
</div>



#### 4.1.2 生成 Token

客户端向开发者服务端发送请求申请 Token，由开发者服务端生成 Token 后返回给到对应客户端。

ZEGO 在 GitHub/Gitee 提供了一个开源的 zego_server_assistant 插件，支持使用 Go、C++、Java、Python、PHP、.NET、Node.js 语言，在开发者的服务端部署生成 Token。


<div class = 'mk-warning'>

zego_server_assistant 中包含 “token03” 和 “token04” 两个版本的插件：

- token03：适用于 ZEGO 实时音视频产品。
- token04：适用于 ZEGO 即时通讯产品。

请使用 “token03” 版本的插件来生成 Token。

</div>

各语言的参考信息如下：

<table>
  <colgroup>
    <col width="20%">
    <col width="30%">
    <col width="20%">
    <col width="30%">
  </colgroup>
  <tbody><tr>
    <th>语言</th>
    <th>支持版本</th>
    <th>关键函数</th>
    <th>具体地址</th>
  </tr>
  <tr>
    <td>Go</td>
    <td>Go 1.14.15 或以上版本</td>
    <td>GenerateToken03</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/go/src/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/blob/release/github/token/go/src/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>C++</td>
    <td>C++ 11 或以上版本</td>
    <td>GenerateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/c%2B%2B/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/c++/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Java</td>
    <td>Java 1.8 或以上版本</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/java/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/java/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Python</td>
    <td>Python 3.6.8 或以上版本</td>
    <td>generate_token</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/python/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/python/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>PHP</td>
    <td>PHP 7.0 或以上版本</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/php/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/php/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>.NET</td>
    <td>.NET Framework 3.5 或以上版本</td>
    <td>GenerateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/.net/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/.net/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Node.js</td>
    <td>Node.js 8 或以上版本</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/nodejs/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/nodejs/token03">Gitee</a></li></ul></td>
  </tr>
</tbody></table>


以 Go 语言为例，开发者可参考以下步骤使用 zego_server_assistant 生成 Token：

1. 将 “go/zegoserverassistant” 目录拷贝到开发者的服务端项目中。
2. 使用命令 `import zsa "your-project-go-mod-path/zegoserverassistant"` 引入插件，需要将 “your-project-go-mod-path” 替换为开发者自己的项目名称。
3. 调用插件提供的 GenerateToken 方法生成 Token。


以下示例代码生成一个允许登录房间、不允许推流的 Token：

```go
const (
	PrivilegeKeyLogin   = 1 // 表示登录房间的权限
	PrivilegeKeyPublish = 2 // 表示允许在房间内推流的权限
  
	PrivilegeEnable     = 1 // 表示有权限
	PrivilegeDisable    = 0 // 表示无权限
)

var appId uint32 = 1   // 唯一标识 AppId
roomId := "demo"  // 房间 ID
userId := "demo"  // 用户 ID
secret := "22222222222222222222222222222222"  // 密钥 ServerSecret
var effectiveTimeInSeconds int64 = 3600 // 有效时间，单位：秒
privilege := make(map[int]int)
privilege[zsa.PrivilegeKeyLogin] = zsa.PrivilegeEnable      // 有登录房间权限
privilege[zsa.PrivilegeKeyPublish] = zsa.PrivilegeDisable   // 无在房间内推流权限

token, err := zsa.GenerateToken(appId, roomId, userId, privilege, secret, effectiveTimeInSeconds)
if err != nil {
    fmt.Println(err)
    return
}
fmt.Println(token)
```



<div class="mk-warning">


运行生成 Token 的 Java 源码时，如果出现 “java.security.InvalidKeyException:illegal Key Size” 异常提示，请参考 [相关常见问题文档](/faq/java_illegal_key_size_solution?product=ExpressVideo&platform=all) 解决。
</div>



为方便开发者体验使用 Token 鉴权，[ZEGO 控制台](https://console.zego.im/) 提供生成临时 Token 的功能，开发者可直接获取 Token 使用，详情请参考 [控制台 - 开发辅助](#16309)。但是在开发者自己的线上环境中，一定要通过自己的服务端生成 Token。














