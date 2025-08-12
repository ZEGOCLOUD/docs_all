## Overview

To avoid unauthorized service access or operations, ZEGOCLOUD uses digital Tokens to control and validate users' login privileges.



## The validation process


Before you log in to a room, your app clients request Tokens from your app server and provide the Token for privilege validation when logging in to a room.

The following diagram shows the process of room login privilege validation:

![/Pics/ZIMChatRoom/en/tokenvalidation_EN.png](https://doc-media.zego.im/sdk-doc/Pics/ZIMChatRoom/en/tokenvalidation_EN.png)



## Generate a Token

<div class="mk-warning">

For business security, you must generate Tokens on your app server.
</div>


1. Go to [ZEGOCLOUD Admin Console](https://console.zegocloud.com), and do the following:
    - Create a project, get the AppID and AppSign.
    - Subscribe to the In-app Chat service.

2. Use the `token generator` plug-in provided by ZEGOCLOUD to generate Tokens on your app server.


<table>
  <colgroup>
    <col width="10%">
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="15%">
    <col width="15%">
  </colgroup>
  <tbody><tr>
    <th rowspan="2">Language</th>
    <th rowspan="2">Supported version</th>
    <th rowspan="2">Core function</th>
    <th rowspan="2">Code base</th>
    <th colspan="2">Sample code</th>
  </tr>
  <tr>
    <th>User identity Token</th>
    <th>User privilege Token</th>
  </tr>
  <tr>
    <td>Go</td>
    <td>Go 1.14.15 or later</td>
    <td>GenerateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/go/src/token04">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/go/sample/sample-base.go">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/go/sample/sample-for-rtcroom.go">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>C++</td>
    <td>C++ 11&nbsp; or later</td>
    <td>GenerateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/c%2B%2B">GitHub</a></li></ul></td>
    <td colspan="2"><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/c%2B%2B/sample/demo/main.cc">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>Java</td>
    <td>Java 1.8&nbsp; or later</td>
    <td>generateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/java/token04">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/java/token04/src/im/zego/serverassistant/sample/Token04SampleBase.java">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/java/token04/src/im/zego/serverassistant/sample/Token04SampleForRtcRoom.java">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>Python</td>
    <td>Python 3.6.8&nbsp; or later</td>
    <td>generate_token04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/python/token04">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/python/token04/test/base_sample.py">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/python/token04/test/rtcroom_sample.py">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>PHP</td>
    <td>PHP 7.0&nbsp; or later</td>
    <td>generateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/php/token04">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/php/token04/test/test.php">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/php/token04/test/testForRtcRoom.php">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>.NET</td>
    <td>.NET Framework 3.5&nbsp; or later</td>
    <td>GenerateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/.net">GitHub</a></li></ul></td>
    <td colspan="2"><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/.net/demo/WindowsFormsApp1/Form1.cs">GitHub</a></li></ul></td>
  </tr>
  <tr>
    <td>Node.js</td>
    <td>Node.js 8&nbsp; or later</td>
    <td>generateToken04</td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/nodejs">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/nodejs/sample/sample-base.js">GitHub</a></li></ul></td>
    <td><ul><li><a target="_blank" href="https://github.com/ZEGOCLOUD/zego_server_assistant/blob/master/token/nodejs/sample/sample-rtc-room.js">GitHub</a></li></ul></td>
  </tr>
</tbody></table>



Take Go language as an example, you can do the following steps to generate a Token：

1. go get github.com/ZEGOCLOUD/zego_server_assistant
2. import "github.com/ZEGOCLOUD/zego_server_assistant/token/go/src/token04"
3. Call the `GenerateToken04` method to generate a Token.

The following code shows how to generate a user identity Token:


```go
var appId uint32 = <Your AppId>   // type: uint32
userId := <Your userID>  // type: string
secret := <ServerSecret>  // type: 32 byte length string
var effectiveTimeInSeconds int64 = <Your token effectiveTime> //type: int64; unit: s

token, err := zsa.GenerateToken04(appId, userId, secret, effectiveTimeInSeconds)
if err != nil {
    fmt.Println(err)
    return
}
fmt.Println(token)
```




