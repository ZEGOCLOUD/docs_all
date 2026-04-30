# Android Platform Template (@midscene/android)

Use for Android native example projects (Java/Kotlin).

## Connection

```bash
act() {
  local device="$1"
  local prompt="$2"
  npx -y @midscene/android@1 act --device-id "$device" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
}

# Connect devices (one per user)
npx -y @midscene/android@1 connect --deviceId device_alice
npx -y @midscene/android@1 connect --deviceId device_bob
```

## Disconnection

```bash
npx -y @midscene/android@1 disconnect 2>/dev/null || true
```

## Single-Device Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

DEVICE_MAIN="emulator-5554"
APP_PACKAGE="com.zegocloud.demo"  # Replace with actual package
REPORT_DIR="midscene_run"
LOG_FILE="midscene_run/test_results.log"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=N

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_tc() {
  echo "" | tee -a "$LOG_FILE"
  echo "========================================" | tee -a "$LOG_FILE"
  echo "[TC-$1] $2" | tee -a "$LOG_FILE"
  echo "========================================" | tee -a "$LOG_FILE"
}

tc_pass() {
  log "RESULT TC-$1: PASSED - $2"
  PASS_COUNT=$((PASS_COUNT + 1))
}

tc_fail() {
  log "RESULT TC-$1: FAILED - $2"
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

act() {
  local device="$1"
  local prompt="$2"
  npx -y @midscene/android@1 act --device-id "$device" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
}

mkdir -p "$REPORT_DIR/log" "$REPORT_DIR/report"
echo "Test Run - $(date)" > "$LOG_FILE"

# Connect
log "Connecting Android device..."
npx -y @midscene/android@1 connect --deviceId "$DEVICE_MAIN"
sleep 3

# ===== TC-01: Test Case Name =====
log_tc "01" "Test Case Name"
R=$(act "$DEVICE_MAIN" "Description of what to verify on the Android screen.")
if echo "$R" | grep -qi "EXPECTED_KEYWORD"; then
  tc_pass "01" "Description"
else
  tc_fail "01" "Description"
fi

# ===== Summary =====
log ""
log "========================================"
log "TEST SUMMARY"
log "========================================"
log "Total: $TOTAL_COUNT | Passed: $PASS_COUNT | Failed: $FAIL_COUNT"
if [ "$FAIL_COUNT" -eq 0 ]; then
  log "All $TOTAL_COUNT test cases PASSED!"
else
  log "$FAIL_COUNT test case(s) FAILED out of $TOTAL_COUNT"
fi
log "========================================"

npx -y @midscene/android@1 disconnect 2>/dev/null || true
log "Test run completed at $(date)"
```

## Multi-Device Script Skeleton

For multi-user Android scenarios:

```bash
DEVICE_USER_A="emulator-5554"
DEVICE_USER_B="emulator-5556"

# Connect both devices
npx -y @midscene/android@1 connect --deviceId "$DEVICE_USER_A"
npx -y @midscene/android@1 connect --deviceId "$DEVICE_USER_B"
sleep 3

# TC: User A performs action on device A
R=$(act "$DEVICE_USER_A" "Tap the 'Call' button. Confirm the call screen is shown.")
# ...

# TC: User B sees incoming call on device B
sleep 5
R=$(act "$DEVICE_USER_B" "Confirm an incoming call notification is visible. Tap accept.")
# ...
```
