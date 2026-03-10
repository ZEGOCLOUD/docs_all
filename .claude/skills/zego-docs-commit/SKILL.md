---
name: zego-docs-commit
description: "This skill creates properly formatted git commits for ZEGO documentation changes. Commits follow the standard format: module prefix + English description (e.g., 'AIAgent: Add userId parameter to APIs'). Use when the user asks to commit, submit, or create commits for documentation changes. 触发短语: 'commit zego docs', '提交文档', 'commit documentation', '提交这些修改', '帮我提交', 'create a commit', 'commit these changes', '提交代码'."
---

# ZEGO 文档提交技能

为 ZEGO 文档变更创建规范格式的 git commit。

## Commit 格式规范

### 标题格式

```
<模块名>: <简短英文描述>
```

**模块名列表**（根据 `docuo.config.zh.json` 配置）：

| 分类 | 模块名 | 说明 |
|------|--------|------|
| **核心产品** | `AIAgent` | AI 智能体 |
| | `DigitalHuman` | 数字人 |
| | `RealTimeVoiceVideo` | 实时音视频 |
| | `RealTimeVoice` | 实时语音 |
| | `LowLatencyLiveStreaming` | 低延迟直播 |
| | `ZIM` | 即时通讯 |
| **UIKit** | `CallKit` | 通话组件 |
| | `IMKit` | IM 组件 |
| | `LiveAudioRoomKit` | 语聊房组件 |
| | `LiveStreamingKit` | 直播组件 |
| | `VideoConferenceKit` | 视频会议组件 |
| **解决方案** | `LiveAudioRoom` | 语聊房 |
| | `LiveStreaming` | 直播 |
| | `VideoConference` | 视频会议 |
| | `VideoCall` | 视频通话 |
| | `VoiceCall` | 语音通话 |
| | `OnlineKTV` | 在线 K 歌 |
| | `SmallClass` | 小班课 |
| | `LargeClass` | 大班课 |
| | `LargeClassAI` | AI 大班课 |
| | `InteractivePodcast` | 互动播客 |
| | `OnlineArtTeaching` | 在线美术教学 |
| | `OnlineCodeTeaching` | 在线编程教学 |
| | `OnlineFitness` | 在线健身 |
| | `OnlineMusicTeaching` | 在线音乐教学 |
| | `RemoteMedical` | 远程医疗 |
| **扩展服务** | `AIEffects` | AI 特效 |
| | `CloudRecording` | 云端录制 |
| | `LocalRecording` | 本地录制 |
| | `CloudPlayer` | 云播放器 |
| | `SuperBoard` | 超级白板 |
| | `MiniGame` | 小游戏 |
| | `AnalyticsDashboard` | 数据分析面板 |
| | `CloudRealtimeASR` | 云端实时 ASR |
| **云市场** | `AIVoiceChanger` | AI 变声 |
| | `RealtimeTranslation` | 实时翻译 |
| | `ShumeiModeration` | 数美内容审核 |

### 规则

1. **语言**：标题和描述必须使用英文
2. **模块前缀**：标题必须以模块名开头，后接冒号和空格
3. **多模块变更**：如果修改了多个模块，选择修改文件最多的模块作为前缀
4. **简洁性**：commit 信息要简洁总结变更内容

## 工作流程

### Step 1: 查看变更文件

```bash
git status --porcelain
git diff --name-only
```

### Step 2: 统计模块变更

分析变更文件路径，统计每个模块的修改文件数量：
- `core_products/aiagent/` → AIAgent
- `core_products/digital-human/` → DigitalHuman
- `core_products/zim/` → ZIM
- `core_products/real-time-voice-video/` → RealTimeVoiceVideo
- `solutions/video-conference/` → VideoConference
- `solutions/live-streaming/` → LiveStreaming
- 等等

**未知目录处理**：
- `.claude/` → Claude
- `.scripts/` → Scripts
- Root config files → Config

**选择规则**：选择修改文件数量最多的模块

### Step 3: 分析变更内容

```bash
git diff --staged
# 或查看具体文件变更
git diff <file-path>
```

### Step 4: 生成 Commit 信息

**标题示例**：
- `AIAgent: Add userId parameter to start/stop listening APIs`
- `ZIM: Update Android integration guide`
- `CallKit: Fix broken links in quick start docs`
- `RealTimeVoice: Add error code documentation`

**描述格式**（可选）：
```
- Summary of change 1
- Summary of change 2
```

### Step 5: 执行 Commit

```bash
git add <files>
git commit -m "<模块名>: <英文描述>"
```

**或使用 HEREDOC 格式**（如果需要多行描述）：
```bash
git commit -m "$(cat <<'EOF'
AIAgent: Add userId parameter to start/stop listening APIs

- Add userId parameter to startListening method
- Add userId parameter to stopListening method
- Update related documentation

EOF
)"
```

## 注意事项

1. **始终使用英文** - 即使文档内容是中文，commit 信息也要用英文
2. **模块名大小写** - 保持模块名原有的大小写格式（如 AIAgent 不是 aiagent 或 AiAgent）
3. **标题长度** - 标题控制在 50-72 字符以内
4. **不要过度描述** - 简洁明了，正文最多 3 个要点
5. **检查敏感信息** - 提交前检查是否包含密钥、API Key 等敏感信息
