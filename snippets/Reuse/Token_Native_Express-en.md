# Control user privileges

---

## 1 Introduction

To avoid unauthorized service access or operations, ZEGO uses digital tokens to control and validate user privileges. 

Currently, ZEGO supports validating the following:

- Room login privilege: a user's privilege to log in to a specific room
- Stream publishing privilege: a user's privilege to publish streams in a specific room

<div class="mk-warning">

By default, ZEGO doesn't validate user privileges.  Your app can access ZEGO services using AppID and AppSign. To enable the user privilege control feature, contact the ZEGO team to perform the necessary system configuration.  

</div>

To improve business security, we recommend you enable the room login privilege validation for all scenarios. In particular: 

- In cases where your app provides different types of rooms dedicated to different users, such as general rooms and member-only rooms, it is necessary to validate a user's privilege to enter a room.
- In a voice chat room, it is necessary to prevent users who are not on the speaker seats from speaking in the room. 
- In voice games such as Werewolf, it is necessary to prevent the scenario that when the app is hacked, the hacker can use different user IDs to log in to the same room to cheat in the game. 

## 2 Prerequisites

Before you start to implement user privilege authentication in your app, make sure you complete the following steps:

1. Contact ZEGO Technical Support to enable the user privilege control feature and define the validation rules.

   <div class="mk-hint">

   Currently, ZEGO supports the following validation rules:

   - **Validate room login privilege only**: to check users' privilege to log in to a room, but not to check their privilege to publish streams in a room.
   - **Validate stream publishing privilege only**: to check users' privilege to publish streams in a room, but not to check their privilege to log in to a room.
   - **Validate both room login and stream publishing privileges**: to check user's privilege to log in to a room and also their privilege to publish streams in a room.

   </div>

2. Integrate the ZEGO Express SDK (version 2.8.0 or later) into your project and implement the basic audio and video features. For details, see [Quick starts - Integration](!Integration/SDK_Integration) and [Quick starts - Implementation](!Solution_Implementation).


## 3 The validation process

Your app clients request tokens from your app server and provide the token for privilege validation when logging in to a room. 

The following diagram shows the process of room login privilege validation:

![/Pics/QuickStart/authenticaiton_flow_web.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/authenticaiton_flow_web.png)

1. Your app client requests a token from your app server.
2. Your app server generates a token and passes it to the client.
3. Your app client logs in to a room with userID, roomID, and the token.
4. The ZEGO SDK sends the token to the ZEGO server for validation.
5. The ZEGO server returns the validation result to the ZEGO Express SDK.
6. The ZEGO SDK returns the validation result to the app client. If the validation passes, the user logs in to the room successfully; otherwise, the login fails.


## 4 Implementation steps

This section describes how to generate a token, how to use a token with the ZEGO Express SDK, and how to renew a token when it is about to expire.

### 4.1 Generate a token

<div class="mk-warning">
For business security, you must generate tokens on your app server.
</div>


#### 4.1.1 Get the AppID and ServerSecret

To generate a token, you need to use your ZEGO App ID and ServerSecret, which you can get from the [ZEGO Admin Console](https://console.zegocloud.com) as described below:

- On the **Overview** page, find the App ID of your project in the **My Projects** section.

  ![https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_appid.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_appid.png)

- To get the ServerSecret, do the following: 

  1. Click **Config** of your project under the **My Projects** section. 

  ![https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_serversecret.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_serversecret.png)
  
  2. In the **Basic Information** section, click **View** of the **Server Secret Keys** column. In the popup window that appears, you can see the ServerSecret as shown below:

  ![https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_serversecret2.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/web_get_serversecret2.png)

#### 4.1.2 Generate a token on your app server

<div class="mk-hint">

Upon request from your app clients, your app server generates tokens and sends the tokens to the corresponding app clients. 
</div>

ZEGO provides an open-source [token generator](https://github.com/zegoim/zego_server_assistant) plug-in on GitHub, which you can use to generate tokens on your app server using different programming languages such as Go, C++, Java, Python, PHP,.NET, and Node.js.

<table>
  <colgroup>
    <col width="20%">
    <col width="25%">
    <col width="20%">
    <col width="35%">
  </colgroup>
  <tbody><tr>
    <th>Language</th>
    <th>Supported version</th>
    <th>Core function</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Go</td>
    <td>Go 1.14.15 or above</td>
    <td>GenerateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/go/src/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>C++</td>
    <td>C++ 11 or above</td>
    <td>GenerateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/c%2B%2B/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>Java</td>
    <td>Java 1.8 or above</td>
    <td>generateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/java/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>Python</td>
    <td>Python 3.6.8 or above</td>
    <td>generate_token</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/python/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>PHP</td>
    <td>PHP 7.0 or above</td>
    <td>generateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/php/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>.NET</td>
    <td>.NET Framework 3.5 or above</td>
    <td>GenerateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/.net/token03/README_EN.md">GitHub</a></td>
  </tr>
  <tr>
    <td>Node.js</td>
    <td>Node.js 8 or above</td>
    <td>GenerateToken</td>
    <td><a target="_blank" href="https://github.com/zegoim/zego_server_assistant/blob/release/github/token/nodejs/token03/README_EN.md">GitHub</a></td>
  </tr>
</tbody></table>



Take Go language as an example, you can do the following steps to generate a token：

1. Copy the `go/zegoserverassistant` directory provided in the  [token generator](https://github.com/zegoim/zego_server_assistant) repository to your server-side project.
2. Use the command `import zsa "your-project-go-mod-path/zegoserverassistant"` to import the plug-in. Remember to replace the `your-project-go-mod-path` with your project name. 
3. Call the `GenerateToken` method to generate a token.


```go
const (
	PrivilegeKeyLogin   = 1 // Room login privilege.
	PrivilegeKeyPublish = 2 // Stream publishing privilege.
	PrivilegeEnable     = 1 // Enable privilege.
	PrivilegeDisable    = 0 // Disable privilege.
)

var appId uint32 = <Your AppId>   // type: uint32
roomId := <Your roomID>  // type: string
userId := <Your userID>  // type: string
secret := <ServerSecret>  // type: string with a length of 32 byte
var effectiveTimeInSeconds int64 = <Your token effectiveTime> //type: int64; unit: s
privilege := make(map[int]int)
privilege[zsa.PrivilegeKeyLogin] = zsa.PrivilegeEnable      // Enable room login privilege.
privilege[zsa.PrivilegeKeyPublish] = zsa.PrivilegeDisable   // Disable stream publishing privilege.

token, err := zsa.GenerateToken(appId, roomId, userId, privilege, secret, effectiveTimeInSeconds)
if err != nil {
    fmt.Println(err)
    return
}
fmt.Println(token)
```

#### 4.1.3 Get a temporary token 

<div class="mk-hint">

To make it easier for you to try and test the user authentication feature, [ZEGO Admin Console](https://console.zegocloud.com) provides a tool for generating temporary tokens, which you can use directly in a testing environment. In production, you must generate tokens on your app server.

</div>


1. Go to [ZEGO Admin Console](hhttps://console.zegocloud.com). In the **Basic Information** section, click **Generate temp token** in the **Temp token for audio/video call** column.


![/Pics/QuickStart/tem_token_1.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/tem_token_1.png)


2. Fill in the **RoomId** and **UserId** information, and click **Generate**.

![/Pics/QuickStart/tem_token_3.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/tem_token_3.png)

3. In the popup window that appears, you will get the **Temp token**, which is valid for 24 hours.

![/Pics/QuickStart/tem_token_4.png](https://doc-media.zego.im/sdk-doc/Pics/QuickStart/tem_token_4.png)







