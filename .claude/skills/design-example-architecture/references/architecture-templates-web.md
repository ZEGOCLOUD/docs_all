# Web 示例代码架构模板

基于"单文件实现"原则的 Web 示例代码架构模板。

## 项目结构

```
Web-Example/
├── src/
│   ├── App.tsx                        # 主应用组件（所有逻辑在此文件）
│   ├── index.tsx                      # 入口文件
│   └── styles.css                     # 样式文件
├── .env.example                       # 环境变量示例
├── package.json
├── tsconfig.json
└── README.md
```

## .env.example

```bash
# AppID / AppID
VITE_APP_ID=1234567890

# Token 服务端地址 / Token server URL
VITE_TOKEN_SERVER_URL=https://your-server.com
```

## App.tsx（完整示例）

```tsx
import { useState, useRef, useEffect } from 'react';
import { ZegoExpressEngine } from 'zego-express-engine-webrtc';
import './styles.css';

function App() {
  // ========== 状态管理 / State management ==========
  const [engine] = useState(() => new ZegoExpressEngine(
    Number(import.meta.env.VITE_APP_ID) || 0,
    null
  ));
  const [roomId, setRoomId] = useState('room1');
  const [userId, setUserId] = useState('user1');
  const [isJoined, setIsJoined] = useState(false);

  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideosRef = useRef<Map<string, HTMLVideoElement>>(new Map());

  // ========== 设置回调 / Setup event handlers ==========
  useEffect(() => {
    // 房间状态更新回调 / Room state update callback
    engine.on('roomStateChanged', (roomID, reason, errorCode) => {
      if (reason === 'LOGINED') {
        console.log('登录房间成功 / Login room success');
        setIsJoined(true);
        startPublishing();
      } else if (reason === 'LOGIN_FAILED') {
        console.error('登录失败 / Login failed:', errorCode);
      }
    });

    // 流更新回调 / Stream update callback
    engine.on('roomStreamUpdate', async (roomID, updateType, streamList) => {
      if (updateType === 'ADD') {
        for (const stream of streamList) {
          await startPlayingStream(stream.streamID);
        }
      } else if (updateType === 'DELETE') {
        for (const stream of streamList) {
          engine.stopPlayingStream(stream.streamID);
          const videoEl = remoteVideosRef.current.get(stream.streamID);
          if (videoEl) {
            videoEl.remove();
            remoteVideosRef.current.delete(stream.streamID);
          }
        }
      }
    });

    return () => {
      engine.destroyEngine();
    };
  }, [engine]);

  // ========== 从服务端获取 Token / Get token from server ==========
  const getToken = async (roomId: string, userId: string): Promise<string> => {
    const response = await fetch(`${import.meta.env.VITE_TOKEN_SERVER_URL}/api/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roomId, userId }),
    });

    const data = await response.json();
    return data.token;
  };

  // ========== 登录房间 / Login room ==========
  const loginRoom = async () => {
    const token = await getToken(roomId, userId);
    await engine.loginRoom(roomId, token, { userID: userId, userName: userId }, { userUpdate: true });
  };

  // ========== 开始推流 / Start publishing ==========
  const startPublishing = async () => {
    const localStream = await engine.createZegoStream();
    localStream.playVideo(localVideoRef.current);
    engine.startPublishingStream(userId, localStream);
  };

  // ========== 拉取远端流 / Play remote stream ==========
  const startPlayingStream = async (streamID: string) => {
    const videoEl = document.createElement('video');
    videoEl.autoplay = true;
    videoEl.playsInline = true;
    document.getElementById('remote-container')?.appendChild(videoEl);
    remoteVideosRef.current.set(streamID, videoEl);

    const remoteStream = await engine.startPlayingStream(streamID);
    const remoteView = engine.createRemoteStreamView(remoteStream);
    remoteView.play(videoEl);
  };

  // ========== 退出房间 / Leave room ==========
  const leaveRoom = () => {
    engine.logoutRoom(roomId);
    setIsJoined(false);
  };

  return (
    <div className="app">
      <h1>Zego RTC Video Call / Zego 音视频通话</h1>

      <div className="input-section">
        <input
          type="text"
          placeholder="房间 ID / Room ID"
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
          disabled={isJoined}
        />
        <input
          type="text"
          placeholder="用户 ID / User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={isJoined}
        />
        <button onClick={loginRoom} disabled={isJoined}>
          加入房间 / Join Room
        </button>
        <button onClick={leaveRoom} disabled={!isJoined}>
          离开房间 / Leave Room
        </button>
      </div>

      <div className="video-section">
        <div className="video-container">
          <h3>本地预览 / Local Preview</h3>
          <video ref={localVideoRef} autoPlay muted playsInline />
        </div>
        <div className="video-container">
          <h3>远端视频 / Remote Video</h3>
          <div id="remote-container" />
        </div>
      </div>
    </div>
  );
}

export default App;
```

## 关键点说明

1. **所有逻辑在 App.tsx 单文件内完成**
2. **AppID 从环境变量读取**（`import.meta.env.VITE_APP_ID`）
3. **RoomID、UserID 通过页面输入**
4. **Token 从服务端 API 获取**
5. **使用 React Hooks 管理状态**
