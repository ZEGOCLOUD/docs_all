## 功能简介

低照度增强，指在环境光较暗，摄像头采集到的画面亮度不满足看清通话方人脸、进行人脸识别等业务需求的时候，对画面亮度进行增强的功能。
ZEGO 提供两种低照度增强的方式：

1. 通过开启自适应帧率，在设定的帧率范围内动态降低采集帧率，以延长每一帧的画面曝光时间，达到增强采集到的画面亮度的效果
例如：开发者开启并设置自适应帧率范围为[10,25]。环境光照充足的时候，采集帧率依然是25帧，环境光照度较低的时候，采集帧率会在[10,25]之间动态调整，以延长每一帧的曝光时间增强采集画面的亮度。
2. 通过算法对采集到的画面亮度进行增强：
  （1）手动增强模式：根据接收到的参数确定是否开启算法增强
  （2）自动增强模式：根据用户所处环境的环境光照度，SDK自动决定是否开启算法增强和增强的程度

两种处理方式可以独立使用，也可以同时使用，均兼容美颜功能。

### 功能优势

1. 全机型覆盖
2. 支持多种模式，根据业务需求灵活选择
3. 系统资源占用小

### 效果展示
- 增强前
![/Pics/lowlightenhancement/lowlightenhancement_before.jpg](https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_before.jpg)
- 增强后
![/Pics/lowlightenhancement/lowlightenhancement_after.jpg](https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_after.jpg)

## 前提条件

在使用低照度增强功能之前，请确保：

- 已在项目中集成 ZEGO Express SDK，实现基本的实时音视频功能，详情请参考 [快速开始](#195)。
- 已在 [ZEGO 控制台](https://console.zego.im) 创建项目，并申请有效的 AppID 和 AppSign，详情请参考 [控制台 - 项目管理](#1265)。
