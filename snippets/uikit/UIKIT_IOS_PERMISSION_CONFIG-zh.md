
a. open the `your_project/ios/Podfile` file, and add the following to the `post_install do |installer|` part:

```plist
# Start of the permission_handler configuration
target.build_configurations.each do |config|
  config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] ||= [
    '$(inherited)',
    'PERMISSION_CAMERA=1',
    'PERMISSION_MICROPHONE=1',
  ]
end
# End of the permission_handler configuration
```

<Frame width="512" height="auto" caption="">
  <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/live/permission_podfile.png" />
</Frame>

b. open the `your_project/ios/Runner/Info.plist` file, and add the following to the `dict` part:

```plist
    <key>NSCameraUsageDescription</key>
    <string>We require camera access to connect to a live</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>We require microphone access to connect to a live</string>
```

<Frame width="512" height="auto" caption="">
  <img src="https://doc-media.zego.im/sdk-doc/Pics/ZegoUIKit/Flutter/live/permission_ios.png" />
</Frame>

