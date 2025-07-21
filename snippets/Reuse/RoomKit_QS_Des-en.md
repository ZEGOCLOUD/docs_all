## Introduction
RoomKit provides different system integration solutions for different cases:

1. If your application already has a user management system and room (channel, group) management system, you can use your existing systems to manage user IDs and room IDs. 
2. If your application doesn't have a room (channel, group) management system, you can integrate ZEGO's Education Cloud Service to manage rooms. For detailed integration instructions, see [Manage rooms with Education Cloud Service](!Advanced_Function/AdvFunc_EduCS).

This document describes the implementation process based on the first scenario. 

The system architecture:

![/Pics/RoomKit/AllPlatform/roomkit_architecture_en.png](https://doc-media.zego.im/sdk-doc/Pics/RoomKit/AllPlatform/roomkit_architecture_en.png)

In this system architecture, the following components need to be implemented by yourself:

1. The component that manages users and sends user IDs to the app clients for joining rooms.
2. The component that manages rooms and sends room IDs to the app clients for joining rooms.
3. The component that handles authentication tokens. To ensure system security, we recommend that you request the SDK access token from the RoomKit server through your business server and then your business server passes the tokens to your app clients for joining rooms.  









