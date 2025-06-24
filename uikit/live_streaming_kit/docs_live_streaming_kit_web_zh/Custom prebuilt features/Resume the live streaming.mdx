# 恢复直播

## 功能概述

在直播过程中，用户如果刷新浏览器，就会退出直播。如需实现刷新浏览器后仍保持在相同直播中，可参考本文档。

## 实现流程

### 1 获取房间 ID

在调用 `joinRoom` 方法时，监听 `onJoinRoom` 回调函数，并在 `onJoinRoom` 回调函数中调用 `getRoomID` 方法，以在成功加入直播间后，获取该房间的 ID 并妥善记录。例如存储在 `sessionStorage` 中，以便在刷新浏览器后返回到该房间。

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
用户退出直播后，应用需删除存储于 `sessionStorage` 的 `roomID`。
</Note>

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
