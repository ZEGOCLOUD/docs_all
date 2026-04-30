# HarmonyOS Screenshot Capture Template (@midscene/harmony)

Use for HarmonyOS NEXT example projects (ArkTS).

## Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

DEVICE_MAIN="FMR0223B13000649"
ASSET_DIR="blog/assets"

act() {
  local device="$1"
  local prompt="$2"
  npx -y @midscene/harmony@1 act --deviceId "$device" --prompt "$prompt" 2>&1
}

screenshot() {
  local device="$1"
  local filename="$2"
  local tmp_path
  tmp_path=$(npx -y @midscene/harmony@1 take_screenshot --deviceId "$device" 2>&1 | grep "Screenshot saved:" | awk '{print $NF}')
  if [ -n "$tmp_path" ] && [ -f "$tmp_path" ]; then
    cp "$tmp_path" "$ASSET_DIR/$filename"
    echo "Captured: $ASSET_DIR/$filename"
  else
    echo "WARNING: Failed to capture $filename"
  fi
}

mkdir -p "$ASSET_DIR"

# Connect
echo "Connecting HarmonyOS device..."
npx -y @midscene/harmony@1 connect --deviceId "$DEVICE_MAIN"
sleep 3

# ===== Screenshot 1: Initial Screen =====
echo "Capturing initial screen..."
screenshot "$DEVICE_MAIN" "initial-screen.png"

# ===== Screenshot 2: Main Feature View =====
act "$DEVICE_MAIN" "SELF-CONTAINED PROMPT: Describe exactly what to do to reach the target screen."
sleep 2
screenshot "$DEVICE_MAIN" "main-feature.png"

# ===== Screenshot 3-N: Additional Screens =====

# Disconnect
npx -y @midscene/harmony@1 disconnect 2>/dev/null || true
echo "Screenshot capture completed at $(date)"
```
