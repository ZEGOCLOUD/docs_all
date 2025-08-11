![](https://doc-media.zego.im/sdk-doc/Pics/FAQ/ReconnectTimeSeq.png)

<div class="mk-warning">


如果用户 A 短暂断线，但是在 90 秒内重连成功了，那么用户 B 不会收到 [onRoomStateChanged](@onRoomStateChanged) 的回调通知。
</div>


其中：
- T0 = 0s：ClientA 的 SDK 收到客户端发起的 [loginRoom](https://doc-zh.zego.im/article/api?doc=express-video-sdk_API~objectivec_ios~class~ZegoExpressEngine#login-room-user-config) 请求。
- T1 ≈ T0 + 120ms：通常在调用 [loginRoom](https://doc-zh.zego.im/article/api?doc=express-video-sdk_API~objectivec_ios~class~ZegoExpressEngine#login-room-user-config) 120 毫秒后，客户端可以加入房间。加入房间过程中，ClientA 的客户端会收到 `onRoomStateChanged(ZegoRoomStateChangedReasonLogining, 0, extendedData, roomID)` 和 `onRoomStateChanged(ZegoRoomStateChangedReasonLogined, 0, extendedData, roomID)` 回调，分别通知客户端正在连接房间以及连接房间成功。
- T2 ≈ T1 + 100ms：因网络传输延迟，ClientB 约在 100ms 后收到 `onRoomUserUpdate(roomID, ZegoUpdateTypeAdd, userList)` 回调以通知客户端 ClientA 加入房间。
- T3：某个时间点，ClientA 因网络断开等原因导致上行网络变差。SDK 会尝试重新加入房间，同时客户端会收到 `onRoomStateChanged(ZegoRoomStateChangedReasonReconnecting, 1002051, extendedData, roomID)` 回调以通知客户端 ClientA 正在断线重连。
- T4 ≈ T3 + 90S：ClientB 此时收到 `onRoomUserUpdate(roomID, ZegoUpdateTypeDelete, userList)` 回调以通知 ClientA 已断线。
- T5 = T3 + time（小于20分钟）：ClientA 在重连时间内恢复网络，重连成功。此时客户端会收到 `onRoomStateChanged(ZegoRoomStateChangedReasonReconnected, 0, extendedData, roomID)` 回调以通知客户端 ClientA 重连成功。
- T6 ≈ T5 + 100ms：因网络传输延迟，ClientB 约在 100ms 后收到 `onRoomUserUpdate(roomID, ZegoUpdateTypeAdd, userList)` 回调以通知客户端 ClientA 重连成功。
- T7 = T3 + 20min：如果 ClientA 连续 20 分钟无法重新加入房间，SDK 不再继续尝试重新连接。ClientA 将会收到 `onRoomStateChanged(ZegoRoomStateChangedReasonReconnectFailed, 1002053, extendedData, roomID)` 回调以通知客户端断开连接。
