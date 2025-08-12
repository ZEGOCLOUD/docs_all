
The ZEGO Express SDK provides the ability to
publish streams to CDN (Content Delivery Network), including forwarding streams to CDN and direct publishing streams to CDN.

This ability enables users to receive and play the stream from the CDN via a playback URL using a browser or a third-party player.

For security, CDN authentication is enabled by default when publishing streams to CDN.

#### Forward a stream to the CDN

Forwarding streams to the CDN refers to forwarding streams from ZEGO's real-time streaming cloud to the ZEGO's CDN or third-party CDNs for large-scale distribution.


![](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/forward_streams_en.png)  

There are three methods for forwarding streams to the CDN:
 
- Forwarding streams to the ZEGO's CDN (Default)

This refers to forward streams from ZEGO's real-time streaming cloud to the ZEGO's CDN. To use this, contact the ZEGO team.

- Forwarding streams to the CDN

You can specify which CDN the streams to be forwarded to, the ZEGO's CDN, or third-party CDNs.

- Forwarding mixed streams to the CDN

You can also forward the mixed output streams to the ZEGO's CDN, or third-party CDNs. 

#### Direct publishing a stream to the CDN

Direct publishing streams to the CDN refers to the process of publishing audio and video streams directly from the client application to the designated CDN. Users can then play the streams directly from the CDN via a playback URL using a browser or a third-party player. However, as the streams are not transmitted over ZEGO's real-time streaming cloud, users will not be able to get the ultra-low latency streaming experience that ZEGO can provide with its optimized real-time network.
The ZEGO's CDN or third-party CDN are supported.

![/Pics/Common/ZegoExpressEngine/direct_publishing_en.png](https://doc-media.zego.im/sdk-doc/Pics/Common/ZegoExpressEngine/direct_publishing_en.png)

####  Feature comparison 

The following are the descriptions and scenarios of the two features:

|Feature|Description|Scenario|
|-|-|-|
|Forwarding streams to the CDN (recommended)|The streams are first published to the ZEGO real-time streaming cloud, and then the ZEGO real-time streaming cloud forwards the streams to CDN. |You are working with a third-party CDN and want to use the existing third-party CDN streaming media distribution service while using the ZEGO Express SDK for real-time co-hosting interaction service. It is suitable for business scenarios requiring continuous interaction, such as private live streaming, voice chatroom, etc.|
|Direct publishing streams to the CDN |The stream is published directly to the CDN without going through the ZEGO real-time streaming cloud.|You are working with a third-party CDN for streaming media distribution service, but don't need to use real-time co-hosting interaction service. It is suitable for Livestream shopping, Livestream gaming, and large classes.|









