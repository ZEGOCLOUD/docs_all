以在 AE 软件中输出素材为例。

1. 在 AE 中正常制作带透明效果的视频，并分别输出 RGB 及 Alpha 通道视频。
    - 输出 RGB 通道的视频。
        <img src="https://doc-media.zego.im/sdk-doc/Pics/Express/output_RGB.jpeg" width="60%">
    - 输出 Alpha 通道的视频。
        <img src="https://doc-media.zego.im/sdk-doc/Pics/Express/output_Alpha.jpeg" width="60%">


2. 在 AE 中，将输出的 RGB 及 Alpha 通道视频拼接为一个视频。
    ZEGO 媒体播放器支持以下三种拼接方式，拼接出的视频越接近正方形，性能越好。开发者可以根据源素材的比例，选择合适的拼接方式：
    - Alpha 通道在下方。
        <img src="https://doc-media.zego.im/sdk-doc/Pics/Express/RGB_up_Alpha.jpeg" width="30%">
    - Alpha 通道在左侧。
        <img src="https://doc-media.zego.im/sdk-doc/Pics/Express/Alpha_RGB.jpeg" width="60%">
    - Alpha 通道在右侧。
        <img src="https://doc-media.zego.im/sdk-doc/Pics/Express/RGB_Alpha.jpeg" width="60%">
