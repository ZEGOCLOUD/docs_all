# iOS Screenshot Capture Template (@midscene/ios)

Use for iOS native example projects (Swift/Objective-C).

## Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

ASSET_DIR="blog/assets"

act() {
  local prompt="$1"
  npx -y @midscene/ios@1 act --prompt "$prompt" 2>&1
}

screenshot() {
  local filename="$1"
  local tmp_path
  tmp_path=$(npx -y @midscene/ios@1 take_screenshot 2>&1 | grep "Screenshot saved:" | awk '{print $NF}')
  if [ -n "$tmp_path" ] && [ -f "$tmp_path" ]; then
    cp "$tmp_path" "$ASSET_DIR/$filename"
    echo "Captured: $ASSET_DIR/$filename"
  else
    echo "WARNING: Failed to capture $filename"
  fi
}

mkdir -p "$ASSET_DIR"

# Connect
echo "Connecting iOS device..."
npx -y @midscene/ios@1 connect
sleep 3

# ===== Screenshot 1: Initial Screen =====
echo "Capturing initial screen..."
screenshot "initial-screen.png"

# ===== Screenshot 2: Main Feature View =====
act "SELF-CONTAINED PROMPT: Describe exactly what to do to reach the target screen."
sleep 2
screenshot "main-feature.png"

# ===== Screenshot 3-N: Additional Screens =====

# Disconnect
npx -y @midscene/ios@1 disconnect 2>/dev/null || true
echo "Screenshot capture completed at $(date)"
```
