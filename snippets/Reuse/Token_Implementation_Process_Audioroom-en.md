使用 Token 鉴权时，需要开发者先生成 Token，ZEGO 服务端对带着 Token 的用户进行校验。

以使用 Token 判断用户是否能登录房间为例介绍使用流程，如下图：

![token_uml](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/token_uml_liveroom.png)

1. 开发者客户端发起申请 Token 的请求。
2. 在开发者的服务端上生成 Token，并返回给开发者客户端。
3. 开发者客户端携带申请到的 Token 和 roomID 信息，通过 setCustomToken 接口传入 SDK。
4. ZEGO SDK 会自动将 Token 发送到 ZEGO 服务端进行校验。
5. ZEGO 服务端会将校验结果返回给 ZEGO SDK。
6. ZEGO SDK 再将校验的结果直接返回给开发者客户端，没有权限的客户端将登录失败。

