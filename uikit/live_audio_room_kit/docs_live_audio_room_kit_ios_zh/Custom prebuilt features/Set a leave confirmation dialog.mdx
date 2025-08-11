# 设置退出确认框


**语聊房 UIKit（Live Audio Room Kit）** 默认在用户点击离开房间按钮时，立即结束发言或观看，并退出语聊房。


## 实现流程

如果您想添加一个确认对话框来再次确认用户是否想要离开语聊房，您可以使用 `confirmDialogInfo` 配置。

`confirmDialogInfo`：配置此参数后，将在离开语聊房之前，弹出一个带有确认信息的默认样式的确认对话框。

- 显示效果如下：
    
<Frame width="256" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/audio_room/leave_confirmation.gif" /></Frame> 

- 具体参考代码如下：
  ```swift
  class ViewController: UIViewController {

      let selfUserID: String = "userID"
      let selfUserName: String = "userName"
      let yourAppID: UInt32 = YourAppID // 替换为您的 AppID，请从 ZEGO 控制台获取。
      let yourAppSign: String = "YourAppSign" // 替换为您的 AppSign，请从 ZEGO 控制台获取。
      let roomID: String = "YourRoomID" // 替换为您的 RoomID

      @IBAction func startLiveAudio(_ sender: Any) {

          // 在此处修改您的自定义配置。
          let config: ZegoUIKitPrebuiltLiveAudioRoomConfig = ZegoUIKitPrebuiltLiveAudioRoomConfig.host()
          let firmDialogInfo = ZegoLeaveConfirmDialogInfo()
          firmDialogInfo.title = "Leave the room"
          firmDialogInfo.message = "Are you sure to leave the room?"
          firmDialogInfo.confirmButtonName = "OK"
          firmDialogInfo.cancelButtonName = "Cancel"
          config.confirmDialogInfo = firmDialogInfo
          let liveAudioVC = ZegoUIKitPrebuiltLiveAudioRoomVC.init(yourAppID, appSign: yourAppSign, userID: selfUserID, userName: selfUserName, roomID: roomID, config: config)
          liveAudioVC.modalPresentationStyle = .fullScreen
          self.present(liveAudioVC, animated: true, completion: nil)
      }
  }
  ```
