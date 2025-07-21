## 功能简介

超分辨率（简称超分）功能可以在拉流端对拉取到的视频流画面的宽和高进行倍增。例如：拉流端拉取到的原始画面分辨率为 640p x 360p，对画面进行超分处理后分辨率将提升为 1280p x 720p。

<div class = "mk-warning">

- 超分功能为限免功能，限免日期截止 2023 年 2 月 28 日。
- 限免期外的收费标准，请咨询 ZEGO 商务人员。

</div>

### 效果展示

- 人像

|超分前|超分后|
|-|-|
|<img src="https://doc-media.zego.im/sdk-doc/Pics/VideoSuperResolution/portrait_720.jpg" width="50%">| ![https://doc-media.zego.im/sdk-doc/Pics/VideoSuperResolution/portrait_360.jpg](https://doc-media.zego.im/sdk-doc/Pics/VideoSuperResolution/portrait_360.jpg)|




- **文字**

|超分前|超分后|
|-|-|
|<img src="https://doc-media.zego.im/sdk-doc/Pics/VideoSuperResolution/text_720.jpg" width=50% >| ![/Pics/VideoSuperResolution/text_360.jpg](https://doc-media.zego.im/sdk-doc/Pics/VideoSuperResolution/text_360.jpg)|



### 应用场景


<div class="mk-warning">

由于同一台设备同时只能对 1 条流开启超分功能，因此超分功能仅适用于在只有单流或者有 1 路焦点流的场景。  
</div>


- 1V1 视频通话场景
- 直播场景：直播场景大多数情况下，只拉取 1 条流，可对拉取的单流直播画面开启超分。当拉取多条流时，可对重点关注的主播开启超分功能。
- 在线教育：在线教育场景可能存在多流，但是会有 1 路焦点流（如教师），可以选择对教师的板书画面或正在发言的学生画面开启超分功能，实现增强效果。

### 功能优势

- **低功耗**：开启 360p 超分后，以 OPPO R11 为例，电流增量小于 60mA，额外耗电极小。
- **低发热**：开启 360p 超分半小时后，以 OPPO R11（骁龙 660）为例，温度上升小于 1.5°C。
- **高性能**：能开启超分功能的设备，超过 95% 的 CPU 增量小于 2%，内存增量小于 100MB。
