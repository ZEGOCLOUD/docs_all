# 单流录制
---
## 功能描述

云端录制支持如下两种录制模式：

* 单流录制：分别录制房间内每条音视频流、白板，每条音视频流都会生成对应的音视频文件，所有白板会生成一个视频文件。
* 混流录制：房间内所有音视频流、白板混合录制成一个音视频文件。

本文介绍如何通过使用云端录制 API 进行单流录制。

## 实现方法

在开启云端录制服务和开通第三方存储服务后，可以参考以下流程实现**单流音视频**的录制。

在调用 [StartRecord](/cloud-recording-server/start) 方法时，将 `RecordMode` 参数设为 “1” 即可启用单流录制模式。

通过将 `OutputFileFormat` 参数设为 “mp4”、“flv” 或 “hls” 可以生成对应格式的视频文件。假设 `OutputFileFormat` 设为 “mp4” ，根据录制内容的不同，生成的文件如下：

|录制内容|参数设置|录制生成文件|
|:----|:----|:----|
|仅录制音频| StreamType 设为 “1”|每个 streamID 生成一个 mp4 文件，mp4 文件内仅存储该 streamID 的音频数据。|
|仅录制视频| StreamType 设为 “2”|每个 streamID 生成一个 mp4 文件，mp4 文件内仅存储该 streamID 的视频数据。|
|录制音视频（合并）| StreamType 设为 “3”|每个 streamID 生成一个 mp4 文件，mp4 文件内存储该 streamID 的音视频数据。|
|录制音视频（分离）| StreamType 设为 “4”|每个 streamID 生成一个 mp4 文件和一个 aac 文件，mp4 文件内仅存储该 streamID 的视频数据，aac 文件内仅存储该 streamID 的音频数据。|

<Warning title="注意">

`StreamType` 仅适用于音视频流，所有白板会录制生成另一个 mp4 文件，该 mp4 文件内仅存储白板的视频数据。

</Warning>


## 请求示例

`Content-type` 为 `application/json;charset=utf-8`，StartRecord 请求包体内容如下：

```json
{
	"RoomId": "xxxx",
	"RecordInputParams": {
		"RecordMode": 1,
		"StreamType": 3,
		"MaxIdleTime": 60
	},
	"RecordOutputParams": {
		"OutputFileFormat": "mp4",
		"OutputFolder": "record/"
	},
	"StorageParams": {
		"Vendor": 2,
		"Region": "oss-xxxx",
		"Bucket": "xxxx",
		"AccessKeyId": "xxxx",
		"AccessKeySecret": "xxxx"
	}
}
```

## 常见问题

- [单流和混流的录制分辨率分别在哪里设置？](https://doc-zh.zego.im/faq/record_solution)
- [在单流录制过程中，为什么白板文件设置的 StreamType 不生效？](https://doc-zh.zego.im/faq/stream_type_invalid)
- [开始录制后，如果房间内新增了流，这个新增的流会被录制吗？](https://doc-zh.zego.im/faq/new_stream)
- [在录制过程中，如果音视频流退出房间再重进，会是什么表现？](https://doc-zh.zego.im/faq/Enter_after_exit)
