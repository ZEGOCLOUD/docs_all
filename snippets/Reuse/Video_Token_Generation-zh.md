## 1 功能简介

使用 ZegoAccurateSyncMediaPlayer SDK 获取播放`ZEGO 影视资源`时，需要携带一个 ZEGO 影视资源 Token 用于鉴权。ZEGO 服务端会根据传入的 ZEGO 影视资源 Token 判断用户是否有权限获取播放`ZEGO 影视资源`，避免因权限控制缺失或操作不当引发的资源外泄。

<div class="mk-warning">

1. 本文档所指 ZEGO 影视资源 Token 与 ZegoAccurateSyncMediaPlayer SDK 相关，其目的是获取 ZEGO 影视资源，与 Express Video SDK 所用的音视频 Token 不同。
</div>

## 2 实现原理

用户获取播放`ZEGO 影视资源`之前，需要先请求开发者服务端获得授权，由开发者服务端派发 ZEGO 影视资源 Token，随后客户端在获取播放`ZEGO 影视资源`时设置 ZEGO 影视资源 Token。ZEGO 服务端在收到对应的请求后会对 ZEGO 影视资源 Token 进行校验，判断用户是否有权限获取播放`ZEGO 影视资源`。

获取播放`ZEGO 影视资源`时，ZEGO 影视资源 Token 校验的流程如下图：

![/Pics/copyrightedvideo/Video_Token.png](https://doc-media.zego.im/sdk-doc/Pics/copyrightedvideo/Video_Token.png)

1. 开发者客户端发起申请 ZEGO 影视资源 Token 的请求。
2. 在开发者的服务端上生成 ZEGO 影视资源 Token ，并返回给开发者客户端。
3. 开发者客户端携带申请到的 ZEGO 影视资源 Token 和 VideoId 信息，通过 `loadCopyrightedVideo` 接口传入 SDK。
4. ZEGO SDK 会自动将 ZEGO 影视资源 Token 发送到 ZEGO 服务端进行校验。
5. ZEGO 服务端会将校验结果返回给 ZEGO SDK。
6. ZEGO SDK 再将校验的结果直接返回给开发者客户端，没有权限的客户端将加载视频失败。

## 3 使用步骤

以下将介绍开发者的服务端如何生成 ZEGO 影视资源 Token、如何使用 SDK 设置 ZEGO 影视资源 Token、以及 ZEGO 影视资源 Token 过期时的处理方式。

### 3.1 生成 ZEGO 影视资源 Token

<div class="mk-warning">

为保证安全性，ZEGO 强烈建议开发者在自己的服务端生成 ZEGO 影视资源 Token。 
</div>

#### 3.1.1 获取 AppID 和 ServerSecret

生成 ZEGO 影视资源 Token 需要开发者项目的唯一标识 AppId 和密钥 ServerSecret，请参考 [控制台 - 项目管理](#12107) 中的 “项目信息”获取。

<div class="mk-warning">

获取 AppID 后，请联系 ZEGO 商务人员开通服务，否则无法生成着 ZEGO 影视资源 Token。

</div>

#### 3.1.2 开发者服务端生成 ZEGO 影视资源 Token

<div class="mk-hint">

客户端向开发者服务端发送请求申请 ZEGO 影视资源 Token，由开发者服务端生成 ZEGO 影视资源 Token 并返回给对应客户端。
</div>

为方便开发者使用，ZEGO 在 GitHub/Gitee 提供了一个开源的 zego_server_assistant 插件，支持使用 Go、C++、Java、Python、PHP、.NET、Node.js 等语言，在开发者的服务端部署生成 ZEGO 影视资源 Token。

<div class="mk-warning">

在下载完代码后，请参考下文的示例代码做**相应修改**，添加 **VideoPayload** 相关内容，才能够生成 ZEGO 影视资源 Token。
</div>

<table>
  <colgroup>
    <col>
    <col>
    <col>
    <col>
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
<td>GenerateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/go/src/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/blob/release/github/token/go/src/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>C++</td>
<td>C++ 11 或以上版本</td>
<td>GenerateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/c%2B%2B/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/c++/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>Java</td>
<td>Java 1.8 或以上版本</td>
<td>generateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/java/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/java/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>Python</td>
<td>Python 3.6.8 或以上版本</td>
<td>generate_token04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/python/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/python/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>PHP</td>
<td>PHP 7.0 或以上版本</td>
<td>generateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/php/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/php/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>.NET</td>
<td>.NET Framework 3.5 或以上版本</td>
<td>GenerateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/.net/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/.net/token04">Gitee</a></li></ul></td>
</tr>
<tr>
<td>Node.js</td>
<td>Node.js 8 或以上版本</td>
<td>generateToken04</td>
<td><ul><li><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/tree/release/github/token/nodejs/token04">GitHub</a></li><li><a target="_blank" href="https://gitee.com/zegodev_admin/zego_server_assistant/tree/release/github/token/nodejs/token04">Gitee</a></li></ul></td>
</tr>
</tbody></table>

以 Go 语言为例，开发者可参考以下步骤使用 zego_server_assistant 生成 ZEGO 影视资源 Token：


1. 首先将 “go/zegoserverassistant” 目录，拷贝到开发者的服务端项目中。
2. 使用命令 `import zsa "your-project-go-mod-path/zegoserverassistant"` 引入插件，需要将 “your-project-go-mod-path” 替换为开发者自己的项目名称。
3. 调用插件提供的 `GenerateToken04` 方法生成 ZEGO 影视资源 Token。

生成 ZEGO 影视资源 Token 的示例代码如下：

```go
package main

import (
    "encoding/json"
    "fmt"
    "github.com/zegoim/zego_server_assistant/token/go/src/token04"
)

/*
获取播放 ZEGO 影视资源 Token 生成示例代码
 */


//token 拓展属性，需要开发者基于下载的代码自行添加
type VideoPayLoad struct {
    RoomId       string      `json:"room_id"`           //房间id；
    VideoId      string      `json:"video_id"`          //视频id；
}

func main() {
    var appId uint32 = 1                                  //需开发者替换，Zego派发的应用id, 可从Zego控制台获取，开发者的唯一标识
    roomId := "room_123"                                  //需开发者替换，房间id
    userId := "User_123"                                  //需开发者替换，用户id
    videoId := "249850980283048"                          //需开发者替换，视频id
    serverSecret := "abcdefghijklmnopqrstuvwxyzabcdef"    //需开发者替换，每个应用都有一个密钥，可从Zego控制台获取，开发者需妥善保管
    var effectiveTimeInSeconds int64 = 3600               //需开发者替换，token有效时长，单位秒

    //需要开发者基于下载的代码自行添加
    payloadData := &VideoPayLoad{
        RoomId:       roomId,
        VideoId:      videoId,
    }
    
    payload, err := json.Marshal(payloadData)
    if err != nil {
        fmt.Println(err)
        return
    }

    token, err := token04.GenerateToken04(appId, userId, serverSecret, effectiveTimeInSeconds, string(payload))
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(token)
}
```









