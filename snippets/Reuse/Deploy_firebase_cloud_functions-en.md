## Deploy the Firebase Cloud Functions

ZEGO Call uses the  Firebase Cloud Functions as the business server by default, we recommend you activate and deploy it before integrating the Call SDK.
 

<div class="mk-hint">

To use your own business server instead of using the Firebase, refer to the [Use ZEGO Call with your business server](!users).

</div>

1. Create a Firebase project in the [Firebase console](https://console.firebase.google.com/). For details, see [Firebase Documentation](https://firebase.google.com/docs/functions/get-started).

2. Create a new Realtime Database in Firebase. 

    ![/Pics/ZEGOCall/rtd.png](https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/rtd.png)

3. Edit the rules of the Realtime Database by adding the following:

```json
{
  "rules": {
        ".read": "auth.uid != null",
        ".write": "auth.uid != null",
  }
}
```

![https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/firebase_rules.png](https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/firebase_rules.png)

4. Install the CLI via npm.
    ```
    npm install -g firebase-tools
    ```
5. Run the `firebase login` to log in via the browser and authenticate the firebase tool.   
6. Go to your Firebase project directory.
7. Run `firebase init functions`. The tool gives you an option to install dependencies with npm. It is safe to decline if you want to manage dependencies in another way, though if you do decline you'll need to run npm install before emulating or deploying your functions.
8. Download the [Cloud function sample code](https://github.com/ZEGOCLOUD/call_firebase_funcitons). 
9. Copy the `firebase.json` and `functions\index.js` files in the sample code to your cloud function project, overwrite files with the same name.  
10. Copy the `functions\token04` folder from the cloud function project directory, and put it in the same folder together with the `index.js`.

    ![https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/copy_cf.png](https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/copy_cf.png)

11. Modify the `index.js` file, fill in the AppID and ServerSecret you get from [ZEGOCLOUD Admin Console](https://console.zegocloud.com) correctly.

    ![https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/index_appid.png](https://doc-media.zego.im/sdk-doc/Pics/ZEGOCall/index_appid.png)

12. In Firebase CLI, run the `firebase deploy --only functions` command to deploy the cloud functions. 





















