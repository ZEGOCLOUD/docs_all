# Event



## ZegoUIKitListener

`ZegoUIKitListener` 定义了一组回调函数，用于监听与 ZegoUIKit 相关的事件。

### 接口定义

```typescript
export interface ZegoUIKitListener {
    onLocalUserUpdated?: (user: ZegoUIKitUser) => void;
    onUserLeaved?: (user: ZegoUIKitUser) => void;
    onUserListUpdated?: (userList: ZegoUIKitUser[]) => void;
    onReconnected?: () => void;
    onTokenWillExpire?: (roomID: string) => void;
}
```

### 回调函数说明

- `onLocalUserUpdated?: (user: ZegoUIKitUser) => void`：当本地用户信息更新时，将触发此回调。

- `onUserLeaved?: (user: ZegoUIKitUser) => void`：当用户离开时，将触发此回调。

- `onUserListUpdated?: (userList: ZegoUIKitUser[]) => void`：当用户列表更新时，将触发此回调。

- `onReconnected?: () => void`：当重新连接成功时，将触发此回调。

- `onTokenWillExpire?: (roomID: string) => void`：当 token 即将过期时，将触发此回调。

### 示例代码

```js 示例代码
import { ZegoUIKitPrebuiltCall } from '@zegocloud/zego-uikit-prebuilt-call-mini-program';

const listener = {
    onLocalUserUpdated: (user) => {
        console.log('本地用户信息更新:', user);
    },
    onUserLeaved: (user) => {
        console.log('用户离开:', user);
    },
    onUserListUpdated: (userList) => {
        console.log('用户列表更新:', userList);
    },
    onReconnected: () => {
        console.log('重新连接成功');
    },
    onTokenWillExpire: (roomID) => {
        console.log('Token 即将过期，房间ID:', roomID);
        // 重新获取 token 并刷新
        const newToken = generateNewToken();
        ZegoUIKitPrebuiltCall.renewToken(newToken, roomID);
    },
};

ZegoUIKitPrebuiltCall.addUIKitListener('uniqueListenerID', listener);
```