# 自定义呼叫邀请用户界面


## 介绍

在呼叫邀请发起后，主叫用户和被叫用户将看到不同的呼叫页面，开发者可以自定义相关页面。

- 主叫用户发送呼叫邀请后，将看到此等待页面。

    <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/Prebuilt_Web/waitingPage.png" /></Frame>

- 被叫收到邀请时，将看到此弹窗。

    <Frame width="512" height="auto" caption=""><img src="https://doc-media.zego.im/sdk-doc/Pics/Prebuilt_Web/calledDialog.png" /></Frame>

## 如何自定义等待页面？

您可以通过定义一个 `div` 标签用于展示自定义的等待页面。并调用 SDK 提供的 `setCallInvitationConfig` 方法设置 `enableCustomCallInvitationWaitingPage` 为 `true` 以启用自定义等待页面的能力，然后通过监听 `onWaitingPageWhenSending` 以获取相关的被呼叫者信息以填充到您自定义的等待页面中。

<Accordion title="完整示例代码" defaultOpen="false">
```html {12-18,37-56}
<html>
    <head>
        <style>
        #root {
            width: 100vw;
            height: 100vh;
        }
    </style>
    </head>
    <body>
        <div id="root">
            <!-- 自定义呼叫等待页面。 -->
            <div id="waitingPage" style="display: none">
                <!-- 通过 onWaitingPageWhenSending 回调的 callees 获取被呼叫者信息然后放入 calleesBox 以展示 -->
                <div id="calleesBox"></div>
                <!-- 把 cancelButton 的点击事件绑定至 onWaitingPageWhenSending 回调返回的 cancel 方法以实现取消呼叫 -->
                <button id="cancelButton">Cancel</button>
            </div>
            <!-- 点击该按钮发起呼叫邀请 -->
            <button onclick="invite()">invite</button>
            <!-- 其他页面元素... -->
        </div>
    </body>
    <script src="https://unpkg.com/@zegocloud/zego-uikit-prebuilt/zego-uikit-prebuilt.js"></script>
    <script src="https://unpkg.com/zego-zim-web@2.9.0/index.js"></script>
    <script>
        // 将以下参数设置成您业务中实际有效的值并生成 TOKEN
        const userID = "";
        const userName = "";
        const appID = 0;
        const serverSecret = "";
        const TOKEN = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, null, userID, userName);

        const zp = ZegoUIKitPrebuilt.create(TOKEN);
        zp.addPlugins({ ZIM });
        zp.setCallInvitationConfig({
            enableCustomCallInvitationWaitingPage: true,
            onWaitingPageWhenSending: (callType, callees, cancel) => {
                // 在此处添加您的自定义逻辑。
                // waitingPageDom 用于展示发送呼叫邀请时的等待页面。
                const waitingPageDom = document.querySelector('#waitingPage');
                waitingPageDom.style.display = 'block';
                // 根据回调返回的 callees 参数生成对应的被呼叫者 UI
                // calleesBoxDom 是页面里用展示装被呼叫者 UI 的父容器 
                const calleesBoxDom = document.querySelector('#calleesBox');
                for (var i = 0; i < callees.length; i++) {
                    const div = document.createElement('div');
                    div.id = callees[i].userID;
                    div.innerHTML = callees[i].userName;
                    calleesBoxDom.appendChild(div);
                }
                // cancelButtonDOM 是呼叫等待页面的一个按钮，在此绑定取消呼叫邀请操作的方法。
                const cancelButtonDOM = document.querySelector('#cancelButton');
                cancelButtonDOM.onclick = () => {
                    cancel();
                }
            },
            onSetRoomConfigBeforeJoining: (callType) => {
                // 在加入房间之前设置房间配置的回调函数，在此时您可以在加入房间之前隐藏等待页面。
                const waitingPageDom = document.querySelector('#waitingPage');
                waitingPageDom.style.display = 'none';
            },
            onCallInvitationEnded: (reason) => {
                // 当您的呼叫邀请未成功连接时，您需要隐藏自定义等待页面。
                const waitingPageDom = document.querySelector('#waitingPage');
                waitingPageDom.style.display = 'none';
            }
            // 其他设置...
        })

        function invite() {
            const targetUser = {
                userID: '',
                userName: ''
            };
            zp.sendCallInvitation({
                callees: [targetUser],
                callType: ZegoUIKitPrebuilt.InvitationTypeVideoCall,
                timeout: 60, // 超时时长（秒）。默认为60秒，范围为[1-600秒]。
            }).then((res) => {
                console.warn(res);
            }).catch((err) => {
                console.warn(err);
            });
        }
    </script>

</html>
```
</Accordion>

## 如何自定义呼叫邀请对话框？

您可以通过定义一个 `div` 标签用于展示自定义的呼叫邀请对话框。并调用 SDK 提供的 `setCallInvitationConfig` 方法设置 `enableCustomCallInvitationDialog` 为 `true` 以启用自定义呼叫邀请对话框的能力，然后通过监听 `onConfirmDialogWhenReceiving` 以获取呼叫者的信息以填充到您自定义呼叫邀请对话框中。

<Accordion title="完整示例代码" defaultOpen="false">
```html {12-20,37-57}
<html>
    <head>
        <style>
        #root {
            width: 100vw;
            height: 100vh;
        }
    </style>
    </head>
    <body>
        <div id="root">
          <!-- 自定义呼叫邀请对话框 -->
          <div id="confirmDialog" style="display: none">
            <!-- 通过 onConfirmDialogWhenReceiving 回调的 caller 获取呼叫者信息然后放入 caller 标签以展示 -->
            <div id="caller"></div>
            <!-- 把 acceptButton 的点击事件绑定至 onConfirmDialogWhenReceiving 回调返回的 accept 方法以实现接受呼叫邀请 -->
            <button id="acceptButton">Accept</button>
            <!-- 把 refuseButton 的点击事件绑定至 onConfirmDialogWhenReceiving 回调返回的 refuse 方法以实现接受呼叫邀请 -->
            <button id="refuseButton">Refuse</button>
          </div>
          <!-- 其他页面元素... -->
        </div>
    </body>
    <script src="https://unpkg.com/@zegocloud/zego-uikit-prebuilt/zego-uikit-prebuilt.js"></script>
    <script src="https://unpkg.com/zego-zim-web@2.9.0/index.js"></script>
    <script>
        // 将以下参数设置成您业务中实际有效的值并生成 TOKEN
        const userID = "";
        const userName = "";
        const appID = 0;
        const serverSecret = "";
        const TOKEN = ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, null, userID, userName);

        const zp = ZegoUIKitPrebuilt.create(TOKEN);
        zp.addPlugins({ ZIM });
        zp.setCallInvitationConfig({
            enableCustomCallInvitationDialog: true,
            // 以下是在收到呼叫邀请时触发的回调，此回调返回 [accept] 和 [refuse] 可用于在自定义页面中接受或拒绝呼叫邀请。
            onConfirmDialogWhenReceiving: (callType,caller,refuse,accept,data) =>{
                // 在此处添加您的自定义逻辑。
                // 以下是一个示例，confirmDialogDom 是用于表示对话框元素的 DOM 对象，在此处表示您自定义的呼叫邀请对话框。 
                const confirmDialogDom = document.querySelector('#confirmDialog');
                confirmDialogDom.style.display = 'block';
                // 根据回调返回的 caller 参数生成呼叫者 UI
                const callerDom = document.querySelector('#caller');
                callerDom.innerHTML = caller.userName;
                // 绑定拒绝和接受的方法
                const refuseButtonDOM = document.querySelector('#refuseButton');
                refuseButtonDOM.onclick = () => { 
                    refuse();          
                    confirmDialogDom.style.display = 'none';
                }
                const acceptButtonDOM = document.querySelector('#acceptButton');
                acceptButtonDOM.onclick = () => { 
                    accept();          
                    confirmDialogDom.style.display = 'none';
                }
            },
            onCallInvitationEnded:(reason)=> {
                // 当呼叫邀请超时或被取消时，需要隐藏自定义的呼叫邀请对话框。
                const confirmDialogDom = document.querySelector('#confirmDialog');
                confirmDialogDom.style.display = 'none';
            }
            // 其他设置...
        })
    </script>

</html>
```
</Accordion>

## 参考信息

<Accordion title="onSetRoomConfigBeforeJoining" defaultOpen="false">
- **配置说明**

  在加入房间之前设置房间配置的回调。

- **函数原型：**

  ```ts
  onSetRoomConfigBeforeJoining?: (
      callType: ZegoInvitationType
  ) => ZegoCloudRoomConfig;
  ```

- **参数说明：**

| 参数     | 类型               | 说明       |
| :------- | :----------------- | :--------- |
| callType | ZegoInvitationType | 呼叫类型。 |


- **返回值说明：**

| 返回值              | 说明       |
| :------------------ | :--------- |
| ZegoCloudRoomConfig | 房间配置。 |

</Accordion>


<Accordion title="onCallInvitationEnded" defaultOpen="false">
- **配置说明**

  呼叫邀请结束的回调。

- **函数原型：**

  ```ts
  onCallInvitationEnded?: (
      reason: CallInvitationEndReason, 
      data: string
  ) => void;
  ```

- **参数说明：**

  | 参数   | 类型                    | 说明                 |
  | :----- | :---------------------- | :------------------- |
  | reason | CallInvitationEndReason | 呼叫邀请结束的原因。 |
  | data   | string                  | 扩展字段。           |

</Accordion>

<Accordion title="ZegoInvitationType" defaultOpen="false">
- 类型描述：通话邀请枚举类。
- 枚举说明：

  | 枚举      | 枚举值 | 描述       |
  | :-------- | :----- | :--------- |
  | VoiceCall | 0      | 语音通话。 |
  | VideoCall | 1      | 视频通话。 |

</Accordion>

<Accordion title="ZegoUser" defaultOpen="false">
- 类型描述：用户信息类。
- 参数说明：

  | 属性/方法     | 类型                        | 是否必选 | 描述                                                                                                                                                                                     |
  | :------------ | :-------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | userID        | string                      | 是       | 用户唯一标识，由开发者自定义，最长不超过 32 字节，仅支持数字，英文字符和 '!', '#', '$', '&', '(', ')', '+', '-', ':', ';', '&lt;', '=', '.', '&gt;', '?', '@', '\[', '\]', '^', '_', '\{', '\}', '|', '~'。|
  | userName      | string                      | 否       | 用户的名称。最长不超过 256 字节。                                                                                                                                                        |
  | setUserAvatar | (avatar: string) =&gt; void | 否       | 传入图片资源地址设置用户头像的方法。                                                                                                                                                     |

</Accordion>

<Accordion title="CallInvitationEndReason" defaultOpen="false">
- 类型描述：呼叫邀请结束原因枚举类。
- 枚举说明：

  | 枚举      | 枚举值    | 描述           |
  | :-------- | :-------- | :------------- |
  | Declined  | Declined  | 拒绝邀请。     |
  | Timeout   | Timeout   | 呼叫超时。     |
  | Canceled  | Canceled  | 呼叫取消。     |
  | Busy      | Busy      | 被呼叫者忙碌。 |
  | LeaveRoom | LeaveRoom | 离开房间。     |

</Accordion>

<Accordion title="onWaitingPageWhenSending" defaultOpen="false">

- **配置说明**

  收到呼叫邀请后出现弹框的回调。

- **函数原型：**

  ```ts
  onConfirmDialogWhenReceiving?: (
      callType: ZegoInvitationType,
      caller: ZegoUser,
      refuse: RefuseCallInvitationFunc,
      accept: AcceptCallInvitationFunc,
      data: string
  ) => void;
  ```

- **参数说明：**


| 参数     | 类型                                               | 说明               |
| :------- | :------------------------------------------------- | :----------------- |
| callType | ZegoInvitationType                                 | 呼叫类型。         |
| caller   | ZegoUser                                           | 主叫用户信息。     |
| refuse   | RefuseCallInvitationFunc = (data?: string) => void | 拒绝呼叫邀请方法。 |
| accept   | AcceptCallInvitationFunc = (data?: string) => void | 接受呼叫邀请方法。 |
| data     | string                                             | 扩展字段。         |

</Accordion>
