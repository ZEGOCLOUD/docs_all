<div class="mk-hint">

- 主持人端调用 [pause](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~java_android~class~ZegoAccurateSyncMediaPlayer#pause) 接口暂停播放时，房间内的所有观众端会同步暂停；调用 [resume](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~java_android~class~ZegoAccurateSyncMediaPlayer#resume) 接口恢复播放时，房间内的所有观众端会同步恢复。（如果观众主动点击了暂停按钮，则观众端不会恢复。）
- 观众端也可以调用 [pause](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~java_android~class~ZegoAccurateSyncMediaPlayer#pause) 接口暂停播放，但只暂停自己的播放进度，并且不受主持人的影响；观众端调用 [resume](https://doc-zh.zego.im/article/api?doc=ZegoAccurateSyncMediaPlayerSDK_API~java_android~class~ZegoAccurateSyncMediaPlayer#resume) 接口恢复播放时，会继续播放视频（如果此时主持人已暂停播放，则观众端的影片仍为暂停状态），但不会同步主持人的视频进度，而是从原来暂停的地方继续播放。

</div>







