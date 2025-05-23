# 视频截图

---

## 功能描述

云端录制支持两种截图功能，分别为 [仅自动截图不录制](#仅自动截图不录制) 和 [同时手动截图并录制](#同时手动截图并录制)。

本文介绍如何通过使用云端录制 API 进行视频截图。

## 仅自动截图不录制

仅自动截图不录制，是指以固定频率在**单流录制模式** 和 **混流录制模式** 下对视频流进行截图，截图文件为 JPG 格式。

<Warning title="注意">
- 在单流录制时仅自动截图不录制操作，会按照截图分辨率对应的单流录制档位收费。
- 在混流录制时仅截图操作不录制操作，只会按照截图分辨率对应的单流录制档位收费，不会收取两次录制费用。
</Warning>

在调用 [StartRecord](/cloud-recording-server/start) 方法时，将 `OutputFileFormat` 设置为 “jpg” 即可进行视频截图。您可以通过设置 `SnapshotInterval` 参数控制截图的周期，默认为每 10 秒对房间内的所有流截一次图。

<Warning title="注意">
* `StreamType` 设置为 1（仅录制音频）时**不支持**输出截图文件，需要有视频流才能截图。
* 通过 [查询录制状态接口](/cloud-recording-server/query) 查询视频截图任务状态时，返回参数不会包含文件列表。
</Warning>

录制过程中产生截图文件后会上传至第三方云存储，每次完成截图时会回调通知文件信息，每个回调通知对应一个截图文件。

### 请求示例

以下是一个在单流录制模式下启动自动截图的示例。

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
        "OutputFileFormat": "jpg",
        "OutputFolder": "record/",
        "SnapshotInterval": 10
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

## 同时手动截图并录制

同时手动截图并录制，是指开始 **混流录制** 任务后，在需要截图时，您自行调用服务端接口 [TakeSnapshot](/cloud-recording-server/take-snapshot) 截图。

<Note title="说明">
在混流录制时进行手动截图，只会按照截图分辨率对应的单流录制档位收费，不会收取两次录制费用。
</Note>