```js
declare interface ZegoCloudRoomConfig {
  // 1 UI controls
  // 1.1 Global
  container?: HTMLElement | undefined | null; // Component container.
  maxUsers?: number; // In-call participants range from [2 - 20]. The default value is unlimited.
  scenario?: {
    mode?: ScenarioModel; // Scenario selection.
    config?: ScenarioConfig[ScenarioModel]; // Specific configurations in the corresponding scenario.
  };
  console?: ConsoleLevel; // Used to problem localization, not a regular setup. While setting this can decide what severity of logs you want to print.
  screenSharingConfig?: {
    resolution?: ScreenSharingResolution;
    width?: number;
    height?: number;
    frameRate?: number;
    maxBitRate?: number;
    onError?: (errorCode: number) => string | undefined // Screen sharing failure callback. If custom prompt text is required, the corresponding string can be returned based on the error code. If custom UI is required, an empty string will be returned.
  }; // Screen sharing settings, resolution settings
  language?: ZegoUIKitLanguage; // UIKit language setting.
  sendMessageChannel?: "RTC" | "ZIM"; // Message sending channel configuration.
  videoScreenConfig?: {
		objectFit?: "cover" | "contain" | "fill" // Video display mode, default "contact".
		localMirror?: boolean // Whether the local video image is mirrored, default to true.
		pullStreamMirror?: boolean // Whether the video image on the streaming end is mirrored, default false.
	}

  // 1.2 Prejoin view
  showPreJoinView?: boolean; // Whether to display the prejoin view. Displayed by default.
  preJoinViewConfig?: {
    title?: string; // The title of the prejoin view. Uses "enter Room" by default.
  };
  turnOnMicrophoneWhenJoining?: boolean; // Whether to enable the microphone when joining the call. Enabled by default.
  turnOnCameraWhenJoining?: boolean; // Whether to enable the camera when joining the call. Enabled by default.
  useFrontFacingCamera?: boolean; // Whether to use the front-facing camera when joining the room. Uses a front-facing camera by default.
  videoResolutionDefault?: VideoResolution; // The default video resolution.
  enableStereo?: boolean; // Whether to enable the stereo mode. Disabled by default.

  // 1.3 Room view
  // You can use this button to mute other Participant's camera.
  showTurnOffRemoteCameraButton?: boolean; // Whether to display the button for turning off the remote camera. Not displayed by default.
  // You can use this button to mute other Participant's microphone.
  showTurnOffRemoteMicrophoneButton?: boolean; // Whether to display the button for turning off the remote microphone. Not displayed by default.
  showMyCameraToggleButton?: boolean; // Whether to display the button for toggling my camera. Displayed by default.
  showMyMicrophoneToggleButton?: boolean; // Whether to display the button for toggling my microphone. Displayed by default.
  showAudioVideoSettingsButton?: boolean; // Whether to display the button for audio and video settings. Displayed by default.
  showBackgroundProcessButton?: boolean; // Whether to display the button for background process settings. Not displayed by default.
  showTextChat?: boolean; // Whether to display the text chat on the right side. Displayed by default.
  showUserList?: boolean; // Whether to display the participant list. Displayed by default. 
  showRemoveUserButton?: boolean; // Whether to display the button for removing participants. Not displayed by default.
  lowerLeftNotification?: {
    showUserJoinAndLeave?: boolean; // Whether to display notifications on the lower left area when participants join and leave the room. Displayed by default.
    showTextChat?: boolean; // Whether to display the latest messages on the lower left area. Displayed by default.
  };
  branding?: {
    logoURL?: string; // The branding LOGO URL.
  };
  layout?: "Sidebar" | "Grid" | "Auto"; // The layout modes. Uses the Auto mode by default.
  showLayoutButton?: boolean; // Whether to display the button for switching layouts. Displayed by default.
  showNonVideoUser?: boolean; // Whether to display the non-video participants. Displayed by default.
  showOnlyAudioUser?: boolean; // Whether to display audio-only participants. Displayed by default.
  sharedLinks?: { name?: string; url?: string }[]; // Description of the generated shared links.
  showScreenSharingButton?: boolean; // Whether to display the Screen Sharing button. Displayed by default.
  showPinButton?: boolean; // Whether to display the Pin button. Displayed by default.
  whiteboardConfig?: {
    showAddImageButton?: boolean; // It's set to false by default. To use this feature, activate the File Sharing feature, and then import the plugin. Otherwise, this prompt will occur: "Failed to add image, this feature is not supported."
    showCreateAndCloseButton?: boolean; // Whether to display the button that is used to create/turn off the whiteboard. Displayed by default.
  };
  showRoomTimer?: boolean; // Whether to display the timer. Not displayed by default.
  showRoomDetailsButton?: boolean; // Whether to display the button that is used to check the room details. Displayed by default.
  showInviteToCohostButton?: boolean; // Whether to show the button that is used to invite the audience to co-host on the host end.
  showRemoveCohostButton?: boolean; // Whether to show the button that is used to remove the audience on the host end.
  showRequestToCohostButton?: boolean; // Whether to show the button that is used to request to co-host on the audience end.
  rightPanelExpandedType?: RightPanelExpandedType; // Controls the type of the information displayed on the right panel, display "None" by default.
  autoHideFooter?: boolean; // Whether to automatically hide the footer (bottom toolbar), auto-hide by default. This only applies to mobile browsers.
  enableUserSearch?: boolean; // Whether to enable the user search feature, false by default.
  showMoreButton?: boolean; // Whether to enable the more button, true by default.
  showUserName?: boolean; // Whether to display the user name on chat. true by default
  hideUsersById?: string[]; // Hide the screen corresponding to the user id
  videoViewConfig?: {
    userID?: string; // user ID
    showAvatarWhenCameraOff?: boolean; // Whether to display the user profile picture when the camera is off. The default value is true
  }[];
  backgroundUrl?: string; // background
  liveNotStartedTextForAudience?: string; // Custom text displayed for the audience before the live broadcast starts.
  startLiveButtonText?: string; // Custom Start Live button Text.
  // When a user is invited during a call, the Invite User window appears on the inviting party. If you want to hide this view, set it to false. Display by default.
  // You can cancel the invitation to this user in this view.
  showWaitingCallAcceptAudioVideoView?: boolean;
  // Configure the call invitation list during a call
  callingInvitationListConfig?: {
    waitingSelectUsers: ZegoUser[]; // Waiting for selected members
    defaultChecked?: boolean; // Whether it is selected by default, the default value is true
  };
  // Member List Configuration
  memberViewConfig?: {
		operationListCustomButton?: () => Element // Customize the operation list button.
	}
  showRotatingScreenButton?: boolean; // Whether to display the rotation screen button, it is not displayed by default.
  requireRoomForegroundView?: () => HTMLElement; // Custom view in the room, located above the video.
  addInRoomMessageAttributes?: () => any // add in room message message attribute. return custom message attribute.
  customMessageUI?: (msg: InRoomMessageInfo) => HTMLElement // Customize message UI

  // 1.4 Leaving view
  showLeavingView?: boolean; // Whether to display the leaving view. Displayed by default.
  showLeaveRoomConfirmDialog?: boolean; // When leaving the room, whether to display a confirmation pop-up window, the default is true

  // 2 Related event callbacks
  onJoinRoom?: () => void; // This will be triggered when you join the room. 
  onLeaveRoom?: () => void; // This will be triggered when you left the room.
  onUserJoin?: (users: ZegoUser[]) => void; // This will be triggered when in-room participants join the room.
  onUserLeave?: (users: ZegoUser[]) => void; // This will be triggered when in-room participants left the room.
  onUserAvatarSetter?: (user: ZegoUser[]) => void; // Callback for the user avatar can be set.
  onLiveStart?: (user: ZegoUser) => void; //  Callback for livestream starts.
  onLiveEnd?: (user: ZegoUser) => void; // Callback for livestream ends.
  onYouRemovedFromRoom?: () => void; // Callback for you removed from the room.
  onInRoomMessageReceived?: (messageInfo: InRoomMessageInfo) => void; // Callback for in-room chat message received.
  onInRoomCustomCommandReceived?: (command: ZegoSignalingInRoomCommandMessage[]) => void;
  onReturnToHomeScreenClicked?: () => void; // When the "Return to home screen" button is clicked, this callback is triggered. After setting up this callback, clicking the button will not navigate to the home screen; instead, you can add your own page navigation logic here.
  onSendMessageResult?: (response: { errCode: number, message: string, timestamp?: string, fromUser?: ZegoUser, sendTime?: number, messageID?: number }) => void // Send message callback.
  onScreenRotation?: (currentScreen: 'landscape' | 'portrait') => void; // Screen rotation callback.
  onUserStateUpdated?: (status: ZegoUserState) => void // User status update callback.
  onStreamUpdate?: (streamId: string) => void // Stream add callback, which can obtain the stream ID when the stream is added.
	onLocalStreamUpdated?: (state: "created" | "published" | "stopped", streamId: string, stream?) => void // Local stream status update callback.
	onScreenSharingStreamUpdated?: (state: "created" | "published" | "closed", streamId: string, stream?) => void // Screen sharing stream status update callback.
	onWhiteboardUpdated?: (state: "created" | "closed", whiteboardId: string) => void // Whiteboard status update callback.
	onCameraStateUpdated?: (state: "ON" | "OFF") => void // Camera status update callback.
	onMicrophoneStateUpdated?: (state: "ON" | "OFF") => void // Microphone status update callback.
}

// Here’s an example that hides the prejoin view page:
zp.joinRoom({
          container: document.querySelector("#root"),
          showPreJoinView: false
});
```






