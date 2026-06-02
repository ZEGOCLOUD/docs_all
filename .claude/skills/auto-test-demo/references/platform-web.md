# Web Platform Template (@zegocloud/auto-web)

Use for browser-based example projects (React, Vue, vanilla HTML/JS).

## Connection

```bash
act() {
  local tab="$1"
  local prompt="$2"
  set -o pipefail
  npx -y @zegocloud/auto-web act --tab "$tab" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
  local _ec=$?
  set +o pipefail
  return $_ec
}

# Connect named tabs (one per user)
npx -y @zegocloud/auto-web connect --url "$URL" --tab user_alice
npx -y @zegocloud/auto-web connect --url "$URL" --tab user_bob
```

## Disconnection

```bash
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true
```

## Single-User Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

TAB_MAIN="main"
URL="http://localhost:3000"
REPORT_DIR="midscene_run"
LOG_FILE="midscene_run/test_results.log"
SCREENSHOT_DIR="midscene_run/screenshots"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=N  # Replace N with actual test case count

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
  local tab="$1"
  local prompt="$2"
  set -o pipefail
  npx -y @zegocloud/auto-web act --tab "$tab" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
  local _ec=$?
  set +o pipefail
  return $_ec
}

mkdir -p "$REPORT_DIR/log" "$REPORT_DIR/report" "$SCREENSHOT_DIR"
echo "Test Run - $(date)" > "$LOG_FILE"

# Clean up stale browser sessions before connecting
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true

# Connect
log "Connecting browser..."
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_MAIN"
sleep 3

# ===== TC-01: Test Case Name =====
log_tc "01" "Test Case Name"
R=$(act "$TAB_MAIN" "Description of what to verify. Do not click anything, just confirm.")
EC=$?
log "act result (exit=$EC): $R"
if [ $EC -ne 0 ]; then
  tc_fail "01" "Command execution failed (exit code $EC), see output above"
elif echo "$R" | grep -qi "EXPECTED_KEYWORD"; then
  tc_pass "01" "Description"
else
  tc_fail "01" "Expected result not found in output"
fi
npx -y @zegocloud/auto-web take_screenshot --tab "$TAB_MAIN" 2>&1 | grep -o "Screenshot saved:.*" | awk '{print $NF}' | xargs -I{} cp {} "$SCREENSHOT_DIR/01-test-case-name.png" 2>/dev/null || true

# ===== TC-02: ... =====

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

npx -y @zegocloud/auto-web disconnect 2>/dev/null || true
log "Test run completed at $(date)"
```

## Multi-User Script Skeleton

For multi-users scenarios (chat, collaboration), use multiple tabs:

```bash
TAB_USER_A="user_alice"
TAB_USER_B="user_bob"
URL="http://localhost:3000"
SCREENSHOT_DIR="midscene_run/screenshots"

mkdir -p "$SCREENSHOT_DIR"

# Clean up stale browser sessions before connecting
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true

# Connect both users
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_USER_A"
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_USER_B"
sleep 3

# TC-01: User A sends message
log_tc "01" "User A sends message"
R=$(act "$TAB_USER_A" "Type 'Hello' in the message input and press Enter. Confirm the message was sent.")
EC=$?
log "act result (exit=$EC): $R"
if [ $EC -ne 0 ]; then
  tc_fail "01" "Command execution failed (exit code $EC), see output above"
elif echo "$R" | grep -qi "sent\|sent successfully\|消息已发送"; then
  tc_pass "01" "User A sent message successfully"
else
  tc_fail "01" "Message send not confirmed in output"
fi
npx -y @zegocloud/auto-web take_screenshot --tab "$TAB_USER_A" 2>&1 | grep -o "Screenshot saved:.*" | awk '{print $NF}' | xargs -I{} cp {} "$SCREENSHOT_DIR/01-user-a-sends.png" 2>/dev/null || true

# TC-02: User B receives message
sleep 5
log_tc "02" "User B receives message"
R=$(act "$TAB_USER_B" "Check if a new message 'Hello' appeared in the chat. Confirm it is visible.")
EC=$?
log "act result (exit=$EC): $R"
if [ $EC -ne 0 ]; then
  tc_fail "02" "Command execution failed (exit code $EC), see output above"
elif echo "$R" | grep -qi "Hello\|received\|收到"; then
  tc_pass "02" "User B received message successfully"
else
  tc_fail "02" "Message receive not confirmed in output"
fi
npx -y @zegocloud/auto-web take_screenshot --tab "$TAB_USER_B" 2>&1 | grep -o "Screenshot saved:.*" | awk '{print $NF}' | xargs -I{} cp {} "$SCREENSHOT_DIR/02-user-b-receives.png" 2>/dev/null || true
```
