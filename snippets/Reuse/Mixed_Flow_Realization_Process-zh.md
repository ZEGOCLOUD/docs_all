![](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/Mixed_flow.png)

主要流程如下：
1. 房间内的用户推流到 ZEGO 实时音视频云服务器上。
2. ZEGO 实时音视频云服务器可以根据需要配置推混流或者推单独的 A 流和 B 流到 CDN 服务器。（采用 RTMP 协议）
3. 拉流端根据需要从 CDN 服务器上拉混流，也可以拉单独的 A 流和 B 流（支持RTMP、FLV、HLS等协议）。

