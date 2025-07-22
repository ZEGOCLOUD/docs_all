To add a permission statement, open the "app/AndroidManifest.xml" file and add the following content:
   ```xml
       <!-- Permissions that SDK must use -->
       <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
       <uses-permission android:name="android.permission.INTERNET" />
       <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
       <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
       <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
   ```


![https://doc-media.zego.im/sdk-doc/Pics/superboard/new_project_4.png](//doc.oa.zego.imhttps://doc-media.zego.im/sdk-doc/Pics/superboard/new_project_4.png)


The permissions are explained as follows:

|     Permissions     |     Necessity               | Permission description            | Reason for need                                                    |
| :------- | ---------------------- | -------------------- | ------------------------------------------------------------ |
| INTERNET |       Necessary permissions       | Network access permissions         | The basic functions of the SDK can only be used when connected to the Internet.                   |
| ACCESS_WIFI_STATE |   Necessary permissions    | Get current WIFI status permissions|The SDK will perform different operations according to changes in the network status. For example, when the network is reconnected, the SDK will internally restore the status when the network was disconnected, and the user does not need to perform additional operations. |
| ACCESS_NETWORK_STATE |  Necessary permissions  | Get the current network status permissions | The SDK will perform different operations according to changes in the network status. For example, when the network is reconnected, the SDK will internally restore the status when the network was disconnected, and the user does not need to perform additional operations. |
| WRITE_EXTERNAL_STORAGE | Necessary permissions | Built-in SD card write permissions      | If you need to use a media player or sound player to load media resource files in Android external storage, you need to apply for this permission, otherwise the SDK cannot load the resources.                |
| READ_EXTERNAL_STORAGE |  Necessary permissions |Built-in SD card read permission      | The SDK will save logs and related configuration files in the built-in SD card.         |







