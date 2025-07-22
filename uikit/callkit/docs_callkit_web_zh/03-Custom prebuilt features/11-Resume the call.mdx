# 恢复通话

- - -

## 功能概述

在通话过程中，用户如果刷新浏览器，就会退出通话。如需实现刷新浏览器后仍保持在相同通话中，可参考本文档。

## 实现流程

### 1 获取房间 ID

<Tabs>
<Tab title="基本通话">
在调用 `joinRoom` 方法时，监听 `onJoinRoom` 回调函数，并在 `onJoinRoom` 回调函数中调用 `getRoomID` 方法，以在成功加入通话房间后，获取该房间的 ID 并妥善记录。例如存储在 `sessionStorage` 中，以便在刷新浏览器后返回到该房间。

```ts
zp.joinRoom({
    onJoinRoom: () => {
        // 获取 roomID
        const roomID = zp.getRoomID();
        // 存在 sessionStorage 中
        sessionStorage.setItem('roomID', roomID);
    }   
});
```
<Note title="说明">
用户结束通话后，应用需删除存储于 `sessionStorage` 的 `roomID`。
</Note>
</Tab>
<Tab title="支持邀请的通话">
调用 `setCallInvitationConfig` 方法配置呼叫邀请时，监听 `onSetRoomConfigBeforeJoining` 回调函数。

在 `onSetRoomConfigBeforeJoining` 回调函数中调用 `getRoomID` 方法，以在成功加入通话房间后，获取该房间 的 ID 并妥善记录。例如存储在 `sessionStorage` 中，以便在刷新浏览器后返回到该房间。

接着，返回一个配置对象，其中包含 `autoLeaveRoomWhenOnlySelfInRoom` 属性设置为 `false`，以禁用当房间内只剩一个人时用户自动退出房间的功能。

```ts
zp.setCallInvitationConfig({
    onSetRoomConfigBeforeJoining: () => {
        // 获取 roomID
        const roomID = zp.getRoomID();
        // 存在 sessionStorage 中
        sessionStorage.setItem('roomID', roomID);
        return {
            // 关闭房间内只剩一个人时自动退出房间功能
            autoLeaveRoomWhenOnlySelfInRoom: false,
        }
    }
});
```

<Note title="说明">
用户结束通话后，应用需删除存储于 `sessionStorage` 的 `roomID`。
</Note>
</Tab>
</Tabs>

### 2 重新加入房间

用户刷新浏览器后，应用需从 `sessionStorage` 获取 `roomID`，调用 `joinRoom` 方法重新加入房间，且设置 `showPreJoinView` 为 false，关闭通话前检测页面，以提供更好的用户体验。

```ts
if (sessionStorage.getItem('roomID')){
    // 生成 Kit Token
    const appID = ;
    const token = "";
    const roomID = sessionStorage.getItem('roomID');
    const userID = "";
    const userName = "userName" + userID;    
    const kitToken = ZegoUIKitPrebuilt.generateKitTokenForProduction(appID, token, roomID, userID, userName);

    // 使用 Kit Token 创建实例对象。
    const zp = ZegoUIKitPrebuilt.create(kitToken);
    zp.joinRoom({
        // 隐藏通话前检测界面
        showPreJoinView: false,
    });
}
```

## 参考信息

### getRoomID

```ts
// 描述：获取房间 ID
getRoomID(): string;
```
