In scenarios such as voice chatting and live streaming, gifts are an important part of interaction between hosts and participants. Exquisite gift effects can add more fun to interaction and improve the viewing experience. As the industry booms, gift effects have evolved from static to dynamic and from opaque to transparent.

A common method to realize dynamic gift effects is to play MP4 gift videos. However, MP4 does not support the Alpha channel. When played in full screen, an MP4 gift effect blocks other content in the screen and affects the viewing experience. The ZEGO Express SDK media player provides transparent rendering capabilities for playing the effects of transparent dynamic gifts.

The ZEGO Express SDK media player provides RGB and Alpha channels that can split MP4 assets, which are merged through RGB and Alpha channels, into pixel segments and play them separately. This way, the dynamic effects of transparent gifts can be played without blocking other content in the screen, which greatly improves the viewing experience.

<img src="/Pics/ZegoUIKit/Flutter/live/send_virtual_gift.gif" width="50%">

### Benefits

- **Low development costs**
  
  Without having to learn complex animation implementation solutions, developers can directly use the assets provided by designers to make and play gift special effects. This improves development efficiency and effectiveness.

- **High level of animation reproduction**
  
  Asset designers can design dynamic effects without the need to worry about whether the complex 3D effects, strokes, and particle effects can be reproduced by the technology stack used by developers.

- **Excellent compatibility**
  
  Developers do not have to resort to semi-transparent dynamic effect solutions such as Lottie and Cocos2d-X, which have disadvantages like complexity, poor performance, compatibility issues of certain models, and difficulties in maintenance.

### How it works

As shown in the figure below, the top half of the figure represents a segment of pixels from an asset split by the Alpha channel. The RGB channels on the left store information about the RGB channels of the gift asset, and the RGB channels on the right store information about the Alpha channel of the gift asset.

When the gift asset is played on a client, the R channel of the video on the right is extracted as the Alpha channel value of the corresponding pixel on the left.

During rendering, the Alpha channel value is divided by 255 and normalized to generate an Alpha value between 0 and 1. Then, the RGBA value is used to render each pixel to the screen, thus achieving a semi-transparent effect.


![https://doc-media.zego.im/sdk-doc/Pics/transparentgift.jpeg](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/transparentgift.jpeg)











