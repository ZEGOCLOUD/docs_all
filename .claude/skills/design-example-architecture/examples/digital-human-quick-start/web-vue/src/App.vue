<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const toNumber = (value, fallback) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

// 从环境变量获取配置
// Get configuration from environment variables
const clientConfig = {
  appId: toNumber(import.meta.env.VITE_APP_ID, 0),
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001'
}

// 生成随机用户 ID。实际请按业务需求生成用户 ID
// Generate random user ID. Please generate user ID according to business requirements in actual use.
const generateUserId = () => `user_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`

const status = ref('Initializing...')
const roomInfo = ref(null)
let engine = null
let currentRoom = null
let stopped = false

onMounted(async () => {
  try {
    // 检查配置
    // Check configuration
    if (!clientConfig.appId) {
      status.value = 'Please check VITE_APP_ID'
      return
    }

    // 步骤1：从业务后台获取播报列表
    // Step 1: Fetch broadcast list from backend
    status.value = 'Fetching broadcast list from backend...'
    const broadcastResponse = await fetch(`${clientConfig.apiBaseUrl}/api/broadcast`, { cache: 'no-store' })

    if (!broadcastResponse.ok) {
      status.value = 'Failed to fetch broadcast list'
      return
    }

    const payload = await broadcastResponse.json()
    const broadcasts = payload.broadcastList || {}
    const broadcastKeys = Object.keys(broadcasts)

    if (broadcastKeys.length === 0) {
      status.value = 'No available broadcast, please start broadcast task on configuration page first'
      return
    }

    // 仅作示例。选择第一个播报
    // For demo only. Select first broadcast
    const firstIndex = broadcastKeys[0]
    const broadcast = broadcasts[firstIndex]

    if (stopped) return

    // 步骤2：获取用于登录 RTC 房间的 Token
    // Step 2: Get token for RTC room login
    status.value = 'Fetching token...'
    const userId = generateUserId()
    const tokenResponse = await fetch(`${clientConfig.apiBaseUrl}/api/token?userId=${userId}`)

    if (!tokenResponse.ok) {
      status.value = 'Failed to fetch token'
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
    roomInfo.value = currentRoom

    status.value = 'Initializing stream player...'

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
    status.value = 'Playing...'
  } catch (error) {
    status.value = `Startup failed: ${error?.message || 'Unknown error'}`
  }
})

onUnmounted(() => {
  stopped = true
  if (engine && currentRoom) {
    engine.stopPlayingStream(currentRoom.streamId)
    engine.logoutRoom(currentRoom.roomId)
    engine.destroyEngine()
  }
})
</script>

<template>
  <div class="container">
    <header class="header">
      <h1>Digital Human Quick Start</h1>
      <p class="status">Status: {{ status }}</p>
      <p v-if="roomInfo" class="room-info">
        Room: {{ roomInfo.roomId }} · Stream: {{ roomInfo.streamId }}
      </p>
    </header>

    <div
      id="remote-video"
      class="video-container"
    />
  </div>
</template>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  margin-bottom: 1.5rem;
  text-align: center;
}

h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.status {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.room-info {
  margin: 0.5rem 0;
  font-size: 0.85rem;
  opacity: 0.7;
}

.video-container {
  width: 100%;
  aspect-ratio: 16 / 9;
  background-color: #000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}
</style>
