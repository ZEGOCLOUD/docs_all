# Desktop Platform Template (@midscene/computer)

Use for desktop example projects (Electron, native desktop apps).

## Connection

```bash
# Connect to desktop session
npx -y @midscene/computer@1 connect
```

## act() Function

```bash
act() {
  local prompt="$1"
  npx -y @midscene/computer@1 act --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
}
```

## Disconnection

```bash
npx -y @midscene/computer@1 disconnect 2>/dev/null || true
```

## Single-Session Script Skeleton

```bash
#!/bin/bash
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

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
  local prompt="$1"
  npx -y @midscene/computer@1 act --prompt "$prompt" 2>&1 | tee -a "$LOG_FILE"
}

mkdir -p "$REPORT_DIR/log" "$REPORT_DIR/report"
echo "Test Run - $(date)" > "$LOG_FILE"

# Connect
log "Connecting desktop..."
npx -y @midscene/computer@1 connect
sleep 3

# ===== TC-01: Test Case Name =====
log_tc "01" "Test Case Name"
R=$(act "Description of what to verify on the desktop screen.")
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

npx -y @midscene/computer@1 disconnect 2>/dev/null || true
log "Test run completed at $(date)"
```
