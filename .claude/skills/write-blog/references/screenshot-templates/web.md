# Web Screenshot Capture Template (@zegocloud/auto-web)

Use for browser-based example projects (React, Vue, Next.js, vanilla HTML/JS).

## Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

TAB_MAIN="main"
URL="http://localhost:3000"
ASSET_DIR="blog/assets"

act() {
  local tab="$1"
  local prompt="$2"
  npx -y @zegocloud/auto-web act --tab "$tab" --prompt "$prompt" 2>&1
}

screenshot() {
  local tab="$1"
  local filename="$2"
  local tmp_path
  tmp_path=$(npx -y @zegocloud/auto-web take_screenshot --tab "$tab" 2>&1 | grep "Screenshot saved:" | awk '{print $NF}')
  if [ -n "$tmp_path" ] && [ -f "$tmp_path" ]; then
    cp "$tmp_path" "$ASSET_DIR/$filename"
    echo "Captured: $ASSET_DIR/$filename"
  else
    echo "WARNING: Failed to capture $filename"
  fi
}

mkdir -p "$ASSET_DIR"

# Connect
echo "Connecting browser..."
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_MAIN"
sleep 3

# ===== Screenshot 1: Initial Screen =====
echo "Capturing initial screen..."
screenshot "$TAB_MAIN" "initial-screen.png"

# ===== Screenshot 2: Main Feature View =====
# Navigate to the main feature, then capture
act "$TAB_MAIN" "SELF-CONTAINED PROMPT: Describe exactly what to do to reach the target screen."
sleep 2
screenshot "$TAB_MAIN" "main-feature.png"

# ===== Screenshot 3-N: Additional Screens =====
# Repeat act + screenshot for each additional screen
# act "$TAB_MAIN" "Do X to reach screen Y"
# sleep 2
# screenshot "$TAB_MAIN" "screen-y.png"

# Disconnect
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true
echo "Screenshot capture completed at $(date)"
```

## Multi-User Variant

For multi-user scenarios (chat, collaboration), use multiple tabs to capture interaction:

```bash
TAB_USER_A="user_a"
TAB_USER_B="user_b"

npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_USER_A"
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_USER_B"

# User A performs action
act "$TAB_USER_A" "Login as Alice and send a message to Bob"
sleep 3

# User B receives — capture both sides
act "$TAB_USER_B" "Login as Bob and check for Alice's message"
sleep 2
screenshot "$TAB_USER_A" "chat-sender.png"
screenshot "$TAB_USER_B" "chat-receiver.png"

npx -y @zegocloud/auto-web disconnect 2>/dev/null || true
```
