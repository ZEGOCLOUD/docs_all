A user can monitor the connection state of the user in the current room in real time by listening for the [`onRoomStateChanged`](@onRoomStateChanged) callback. If the connection state of the user changes, the SDK triggers the callback, and the current connection state and related error code are returned in the callback. 

The SDK will retry internally if the connection to the room is interrupted due to poor network quality.

#### Room connection states


![https://doc-media.zego.im/sdk-doc/Pics/Video_call/13763_1.png](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/Video_call/13763_1.png)

The room connection states flow. The developer can determine a state based on the returned reason and handle corresponding logic based on the return value of the `errorCode` parameter.











