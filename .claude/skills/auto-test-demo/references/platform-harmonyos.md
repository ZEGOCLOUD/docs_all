# HarmonyOS Platform Template (@midscene/harmony)

Use for HarmonyOS NEXT example projects (ArkTS).

## Connection

```bash
act() {
  local device="$1"
  local prompt="$2"
  set -o pipefail
  npx -y @midscene/harmony@1 act --deviceId "$device" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
  local _ec=$?
  set +o pipefail
  return $_ec
}

# Connect devices
npx -y @midscene/harmony@1 connect --deviceId FMR0223B13000649
```

## Disconnection

```bash
npx -y @midscene/harmony@1 disconnect 2>/dev/null || true
```

## Single-Device Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

DEVICE_MAIN="FMR0223B13000649"
REPORT_DIR="midscene_run"
LOG_FILE="midscene_run/test_results.log"
SCREENSHOT_DIR="midscene_run/screenshots"

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
  set -o pipefail
  npx -y @midscene/harmony@1 act --deviceId "$device" --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
  local _ec=$?
  set +o pipefail
  return $_ec
}

mkdir -p "$REPORT_DIR/log" "$REPORT_DIR/report" "$SCREENSHOT_DIR"
echo "Test Run - $(date)" > "$LOG_FILE"

# Clean up stale sessions before connecting
npx -y @midscene/harmony@1 disconnect 2>/dev/null || true

# Connect
log "Connecting HarmonyOS device..."
npx -y @midscene/harmony@1 connect --deviceId "$DEVICE_MAIN"
sleep 3

# ===== TC-01: Test Case Name =====
log_tc "01" "Test Case Name"
R=$(act "$DEVICE_MAIN" "Description of what to verify on the HarmonyOS screen.")
EC=$?
log "act result (exit=$EC): $R"
if [ $EC -ne 0 ]; then
  tc_fail "01" "Command execution failed (exit code $EC), see output above"
elif echo "$R" | grep -qi "EXPECTED_KEYWORD"; then
  tc_pass "01" "Description"
else
  tc_fail "01" "Expected result not found in output"
fi
npx -y @midscene/harmony@1 take_screenshot --deviceId "$DEVICE_MAIN" 2>&1 | grep -o "Screenshot saved:.*" | awk '{print $NF}' | xargs -I{} cp {} "$SCREENSHOT_DIR/01-test-case-name.png" 2>/dev/null || true

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

npx -y @midscene/harmony@1 disconnect 2>/dev/null || true
log "Test run completed at $(date)"
```
