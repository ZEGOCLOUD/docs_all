import { useEffect, useState } from 'react'
import './index.css'

const toNumber = (value, fallback) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

// 从环境变量获取配置
// Get configuration from environment variables
const clientConfig = {
  appId: toNumber(import.meta.env.VITE_APP_ID, 0),
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'
}

// 生成随机用户 ID。实际请按业务需求生成用户 ID
// Generate random user ID. Please generate user ID according to business requirements in actual use.
const generateUserId = () => `user_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`

function App() {
  const [status, setStatus] = useState('Initializing...')
  const [roomInfo, setRoomInfo] = useState(null)

  useEffect(() => {
    let stopped = false
    let engine = null
    let currentRoom = null

    const bootstrap = async () => {
      try {
        // 检查配置
        // Check configuration
        if (!clientConfig.appId) {
          setStatus('Please check VITE_APP_ID')
          return
        }

        // 步骤1：从业务后台获取播报列表
        // Step 1: Fetch broadcast list from backend
        setStatus('Fetching broadcast list from backend...')
        const broadcastResponse = await fetch(`${clientConfig.apiBaseUrl}/api/broadcast`, { cache: 'no-store' })

        if (!broadcastResponse.ok) {
          setStatus('Failed to fetch broadcast list')
          return
        }

        const payload = await broadcastResponse.json()
        const broadcasts = payload.broadcastList || {}
        const broadcastKeys = Object.keys(broadcasts)

        if (broadcastKeys.length === 0) {
          setStatus('No available broadcast, please start broadcast task on configuration page first')
          return
        }

        // 选择第一个播报
        // Select first broadcast
        const firstIndex = broadcastKeys[0]
        const broadcast = broadcasts[firstIndex]

        if (stopped) return

        // 步骤2：获取用于登录 RTC 房间的 Token
        // Step 2: Get token for RTC room login
        setStatus('Fetching token...')
        const userId = generateUserId()
        const tokenResponse = await fetch(`${clientConfig.apiBaseUrl}/api/token?userId=${userId}`)

        if (!tokenResponse.ok) {
          setStatus('Failed to fetch token')
          return
        }

        const tokenData = await tokenResponse.json()

        currentRoom = {
          roomId: broadcast.roomId,
          streamId: broadcast.streamId,
          userId,
          token: tokenData.token
        }

        if (stopped) return
        setRoomInfo(currentRoom)

        setStatus('Initializing stream player...')

        // 步骤3：动态导入并初始化 ZegoExpressEngine
        // Step 3: Dynamically import and initialize ZegoExpressEngine
        const { ZegoExpressEngine } = await import('zego-express-engine-webrtc')
        engine = new ZegoExpressEngine(clientConfig.appId, "")

        // 步骤4：登录实时音视频 (RTC) 房间
        // Step 4: Login to Real-Time Communication (RTC) room
        await engine.loginRoom(currentRoom.roomId, currentRoom.token, {
          userID: currentRoom.userId,
          userName: currentRoom.userId
        })

        // 步骤5：拉取数字人音视频流
        // Step 5: Play digital human audio/video stream
        const remoteStream = await engine.startPlayingStream(currentRoom.streamId)
        const remoteView = engine.createRemoteStreamView(remoteStream)
        remoteView.play('remote-video')
        setStatus('Playing...')
      } catch (error) {
        setStatus(`Startup failed: ${error?.message || 'Unknown error'}`)
      }
    }

    bootstrap()

    return () => {
      stopped = true
      if (engine && currentRoom) {
        engine.stopPlayingStream(currentRoom.streamId)
        engine.logoutRoom(currentRoom.roomId)
        engine.destroyEngine()
      }
    }
  }, [])

  return (
    <div className="grid">
      <section className="card">
        <h1>Digital Human Quick Start (React + Vite)</h1>
        <p className="meta">Status: {status}</p>
        {roomInfo && (
          <p className="meta">
            Room: {roomInfo.roomId} | Stream: {roomInfo.streamId}
          </p>
        )}
      </section>

      <section className="card">
        <div
          id="remote-video"
          className="video-container"
        />
      </section>
    </div>
  )
}

export default App
