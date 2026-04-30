# Android Screenshot Capture Template (@midscene/android)

Use for Android native example projects (Java/Kotlin).

## Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

DEVICE_MAIN="emulator-5554"
ASSET_DIR="blog/assets"

act() {
  local device="$1"
  local prompt="$2"
  npx -y @midscene/android@1 act --device-id "$device" --prompt "$prompt" 2>&1
}

screenshot() {
  local device="$1"
  local filename="$2"
  local tmp_path
  tmp_path=$(npx -y @midscene/android@1 take_screenshot --device-id "$device" 2>&1 | grep "Screenshot saved:" | awk '{print $NF}')
  if [ -n "$tmp_path" ] && [ -f "$tmp_path" ]; then
    cp "$tmp_path" "$ASSET_DIR/$filename"
    echo "Captured: $ASSET_DIR/$filename"
  else
    echo "WARNING: Failed to capture $filename"
  fi
}

mkdir -p "$ASSET_DIR"

# Connect
echo "Connecting Android device..."
npx -y @midscene/android@1 connect --deviceId "$DEVICE_MAIN"
sleep 3

# ===== Screenshot 1: Initial Screen =====
echo "Capturing initial screen..."
screenshot "$DEVICE_MAIN" "initial-screen.png"

# ===== Screenshot 2: Main Feature View =====
act "$DEVICE_MAIN" "SELF-CONTAINED PROMPT: Describe exactly what to do to reach the target screen."
sleep 2
screenshot "$DEVICE_MAIN" "main-feature.png"

# ===== Screenshot 3-N: Additional Screens =====
# Repeat act + screenshot for each additional screen

# Disconnect
npx -y @midscene/android@1 disconnect 2>/dev/null || true
echo "Screenshot capture completed at $(date)"
```

## Multi-Device Variant

```bash
DEVICE_USER_A="emulator-5554"
DEVICE_USER_B="emulator-5556"

npx -y @midscene/android@1 connect --deviceId "$DEVICE_USER_A"
npx -y @midscene/android@1 connect --deviceId "$DEVICE_USER_B"

# User A action, User B verification
act "$DEVICE_USER_A" "Tap the 'Call' button to start a call"
sleep 5
screenshot "$DEVICE_USER_A" "call-sender.png"
screenshot "$DEVICE_USER_B" "call-receiver.png"

npx -y @midscene/android@1 disconnect 2>/dev/null || true
```
