# 用户权限控制

---

## 1 功能简介

用户权限控制指的是用户登录房间，或是在房间内进行推流等操作时，ZEGO 服务端根据用户登录时携带的 Token 参数，判断用户是否有对应的权限，避免因权限控制缺失或操作不当引发的风险问题。
目前仅支持用户登录房间和用户房间内推流两个权限的校验。

<div class="mk-warning">


开发者可联系 ZEGO 技术支持开通用户权限控制功能。ZEGO 服务端的校验逻辑如下：

默认不校验用户的权限，通过 AppId 和 AppSign 即可使用 ZEGO 产品。

</div>

### 1.1 应用场景

开启用户权限控制功能后，ZEGO 服务端会对用户的权限进行校验。如果开发者的业务上希望给房间加上进房限制或者上麦限制，即仅允许指定的用户登录房间或者在房间内推流，就可以开启用户权限控制功能。

为提高业务安全性，ZEGO 建议每个业务场景都应该开启用户登录房间的权限控制，特别是以下场景：

- 房间有普通房间和会员房间的区别，需要控制非会员用户登录会员房间 。
- 语聊房中，需要控制推流用户和麦上用户的一致，防止“幽灵麦”现象，即在房间里听到了非麦上用户声音的情况。
- 狼人杀等发言游戏，需要防止应用被黑客破解之后，黑客可以使用其他用户 ID 登录同一房间，获取到游戏进行的信息进行作弊，影响正常用户的游戏体验。


## 2 前提条件

- 根据实际业务情况，联系 ZEGO 技术支持配置开启用户权限控制功能，约定 ZEGO 服务端的校验逻辑。

    <div class="mk-hint">
    
    目前支持约定的校验逻辑如下：
    - 只校验登录：登录时校验权限，推流时不校验权限。
    - 只校验推流：推流时校验权限，登录时不校验权限。
    - 同时校验登录和推流：登录和推流时均校验权限。

    </div>

- 已在项目中集成 ZEGO LiveRoom SDK（2021年6月18日以后），实现基本的实时音视频功能。


## 3 实现原理

开启用户权限控制功能后，开发者服务端生成 Token，ZEGO 服务端会对带着 Token 的用户进行校验，根据 Token 参数判断用户是否能登录特定房间和在房间内推流。


用户权限控制功能的登录校验使用流程如下图：

![token_uml](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/token_uml.png)

1. 客户端发起申请 Token 的请求。
2. 在开发者的服务端上生成 Token，并返回给客户端。
3. 客户端携带申请到的 Token 和 userID、roomID 信息，登录对应的房间。
4. ZEGO SDK 会自动将 Token 发送到 ZEGO 服务端进行校验。
5. ZEGO 服务端会将校验的结果返回给 ZEGO SDK。
6. ZEGO SDK 再将校验的结果直接返回给客户端，没有权限客户端登录将失败。



## 4 使用步骤

以下将介绍开发者的服务端如何生成 Token、如何使用 SDK 设置 Token 以及 Token 过期时的处理方式。

### 4.1 生成 Token

<div class="mk-warning">


为保证安全性，开发者一定要在自己的服务端生成 Token。 
</div>



#### 4.1.1 获取 AppId 和 ServerSecret

生成 Token 需要开发者项目的唯一标识 AppId 和密钥 ServerSecret，获取方式如下：

1. 在 [ZEGO 控制台](https://console.zego.im/) 中，在“概览 > 我的项目”中，即可查看 AppId。

![get_AppID.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/get_AppID.png)

2. 在 [ZEGO 控制台](https://console.zego.im/) 中，在“概览 > 我的项目”中，单击项目的“配置”信息，进入项目的“基本信息”页，单击项目的“后台相关密钥”，弹窗中的 “ServerSecret” 即生成 Token 需要使用的密钥。

![get_ServerSecret.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/get_ServerSecret.png)


#### 4.1.2 开发者服务端生成 Token

<div class="mk-hint">


客户端向开发者服务端发送请求申请 Token，由开发者服务端计算 Token 并返回给对应客户端。
</div>


为方便开发者使用，ZEGO 在 GitHub/Gitee 提供了一个开源的 zego_server_assistant 插件，支持使用 Go、C++、Java、Python、PHP、.NET、Node.js 等语言，在开发者的服务端部署生成 Token。

<table>
  <colgroup>
    <col>
    <col>
    <col>
  </colgroup>
  <tbody><tr>
    <th>语言</th>
    <th>关键函数</th>
    <th>具体地址</th>
  </tr>
  <tr>
    <td>Go</td>
    <td>GenerateToken03</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/go/src/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/blob/release/github/token/go/src/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>C++</td>
    <td>GenerateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/c%2B%2B/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/c++/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Java</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/java/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/java/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Python</td>
    <td>generate_token</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/python/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/python/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>PHP</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/php/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/php/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>.NET</td>
    <td>GenerateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/.net/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/.net/token03">Gitee</a></li></ul></td>
  </tr>
  <tr>
    <td>Node.js</td>
    <td>generateToken</td>
    <td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/nodejs/token03">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/nodejs/token03">Gitee</a></li></ul></td>
  </tr>
</tbody></table>


以 Go 语言为例，开发者可参考以下步骤使用 zego_server_assistant 生成 Token：


1. 将 “go/zegoserverassistant” 目录拷贝到开发者的服务端项目中。
2. 使用命令 `import zsa "your-project-go-mod-path/zegoserverassistant"` 引入插件，需要将 “your-project-go-mod-path” 替换为开发者自己的项目名称。
3. 调用插件提供的 GenerateToken 方法生成 Token。




```go
const (
	PrivilegeKeyLogin   = 1 // 登录
	PrivilegeKeyPublish = 2 // 推流
	PrivilegeEnable     = 1 // 有权限：允许登陆或推流
	PrivilegeDisable    = 0 // 无权限：不允许登陆或推流
)

var appId uint32 = <Your AppId>   // type: uint32
roomId := <Your roomID>  // type: string
userId := <Your userID>  // type: string
secret := <ServerSecret>  // type: 32 byte length string
var effectiveTimeInSeconds int64 = <Your token effectiveTime> //type: int64; unit: s
privilege := make(map[int]int)
privilege[zsa.PrivilegeKeyLogin] = zsa.PrivilegeEnable      // 有登录权限
privilege[zsa.PrivilegeKeyPublish] = zsa.PrivilegeDisable   // 无推流权限

token, err := zsa.GenerateToken(appId, roomId, userId, privilege, secret, effectiveTimeInSeconds)
if err != nil {
    fmt.Println(err)
    return
}
fmt.Println(token)
```




#### 4.1.3 使用控制台临时 Token 功能

<div class="mk-hint">


为方便开发者体验和测试用户权限控制功能，[ZEGO 控制台](https://console.zego.im/) 提供生成临时 Token 的功能，开发者可直接获取 Token 使用。但是在开发者自己的线上环境中，一定要通过自己的服务端生成 Token。
</div>


1. 在 [ZEGO 控制台](https://console.zego.im/) 中，在“概览 > 我的项目”中，单击项目的“配置”信息，进入项目的“基本信息”页，单击项目的“音视频临时 Token”，在弹窗中填写测试的 “RoomId” 和 “UserId” 信息。

![console_Token.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/console_Token.png)

2. 填写完信息，单击“生成”按钮即可查看生成的 “临时Token” 信息，该 Token 的有效期为 24 小时。

![console_Token_Result.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/console_Token_Result.png)













