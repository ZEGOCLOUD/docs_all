#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

function usage() {
  console.error("Usage: node generate-test-artifacts.js <test-cases.json>");
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function slug(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function requireField(value, name) {
  if (value === undefined || value === null || value === "") {
    throw new Error(`Missing required field: ${name}`);
  }
}

function normalizeDependents(value) {
  if (value === null || value === "" || value === undefined) return [];
  if (Array.isArray(value)) return value.filter((item) => item !== null && item !== "");
  return [value];
}

function statusVar(id) {
  return `STATUS_${String(id).replace(/[^A-Za-z0-9_]/g, "_")}`;
}

function validate(data) {
  requireField(data.schemaVersion, "schemaVersion");
  if (data.schemaVersion !== "auto-test-demo/v1") {
    throw new Error(`Unsupported schemaVersion: ${data.schemaVersion}`);
  }
  requireField(data.meta && data.meta.projectDir, "meta.projectDir");
  requireField(data.meta && data.meta.reportDir, "meta.reportDir");
  requireField(data.runtime && data.runtime.platform, "runtime.platform");
  if (!Array.isArray(data.targets) || data.targets.length === 0) {
    throw new Error("targets must be a non-empty array");
  }
  if (!Array.isArray(data.cases) || data.cases.length === 0) {
    throw new Error("cases must be a non-empty array");
  }

  const targets = new Map();
  for (const target of data.targets) {
    requireField(target.id, "targets[].id");
    requireField(target.type, `targets[${target.id}].type`);
    targets.set(target.id, target);
  }

  const ids = new Set();
  const seenIds = new Set();
  for (const testCase of data.cases) {
    requireField(testCase.id, "cases[].id");
    requireField(testCase.title, `cases[${testCase.id}].title`);
    requireField(testCase.target, `cases[${testCase.id}].target`);
    if (!Object.prototype.hasOwnProperty.call(testCase, "dependent")) {
      throw new Error(`Missing required field: cases[${testCase.id}].dependent`);
    }
    requireField(testCase.precondition, `cases[${testCase.id}].precondition`);
    requireField(testCase.action, `cases[${testCase.id}].action`);
    requireField(testCase.expected, `cases[${testCase.id}].expected`);
    if (ids.has(testCase.id)) throw new Error(`Duplicate case id: ${testCase.id}`);
    if (!targets.has(testCase.target)) {
      throw new Error(`Unknown target "${testCase.target}" in ${testCase.id}`);
    }
    for (const dependent of normalizeDependents(testCase.dependent)) {
      if (dependent === testCase.id) {
        throw new Error(`Case ${testCase.id} cannot depend on itself`);
      }
      if (!seenIds.has(dependent)) {
        throw new Error(`Case ${testCase.id} depends on "${dependent}", which must appear before it`);
      }
    }
    ids.add(testCase.id);
    seenIds.add(testCase.id);
  }
}

function buildPrompt(testCase) {
  const precondition = String(testCase.precondition || "").trim();
  const action = String(testCase.action || "").trim();
  const expected = String(testCase.expected || "").trim();
  if (precondition && precondition !== "无") {
    return `先确认前提条件：${precondition}。如果前提条件不满足，直接报告失败并说明当前界面状态；不要继续执行后续操作。前提条件满足后，执行操作：${action}。然后确认预期结果：${expected}。`;
  }
  return `执行操作：${action}。然后确认预期结果：${expected}。`;
}

function commandFor(data, target, command, prompt) {
  const platform = data.runtime.platform;
  if (platform === "web") {
    if (command === "connect") return `npx -y @zegocloud/auto-web connect --url ${shellQuote(target.url)} --tab ${shellQuote(target.tab || target.id)}`;
    if (command === "act") return `npx -y @zegocloud/auto-web act --tab ${shellQuote(target.tab || target.id)} --prompt ${shellQuote(prompt)}`;
    if (command === "screenshot") return `npx -y @zegocloud/auto-web take_screenshot --tab ${shellQuote(target.tab || target.id)}`;
    if (command === "disconnect") return "npx -y @zegocloud/auto-web disconnect";
  }
  if (platform === "android") {
    const device = target.deviceId ? ` --device-id ${shellQuote(target.deviceId)}` : "";
    const scrcpy = target.useScrcpy ? " --use-scrcpy" : "";
    if (command === "connect") return `npx -y @midscene/android@1 connect${device}${scrcpy}`;
    if (command === "act") return `npx -y @midscene/android@1 act${device}${scrcpy} --prompt ${shellQuote(prompt)}`;
    if (command === "assert") return `npx -y @midscene/android@1 assert${device}${scrcpy} --prompt ${shellQuote(prompt)}`;
    if (command === "screenshot") return `npx -y @midscene/android@1 take_screenshot${device}${scrcpy}`;
    if (command === "disconnect") return "npx -y @midscene/android@1 disconnect";
  }
  if (platform === "ios") {
    const args = [
      target.deviceId ? `--device-id ${shellQuote(target.deviceId)}` : "",
      target.wdaHost ? `--wda-host ${shellQuote(target.wdaHost)}` : "",
      target.wdaPort ? `--wda-port ${shellQuote(target.wdaPort)}` : "",
      target.sessionId ? `--session-id ${shellQuote(target.sessionId)}` : "",
      target.useWDA ? "--use-w-d-a true" : "",
      target.wdaMjpegPort ? `--wda-mjpeg-port ${shellQuote(target.wdaMjpegPort)}` : "",
    ].filter(Boolean).join(" ");
    const suffix = args ? ` ${args}` : "";
    if (command === "connect") return `npx -y @midscene/ios@1 connect${suffix}`;
    if (command === "act") return `npx -y @midscene/ios@1 act${suffix} --prompt ${shellQuote(prompt)}`;
    if (command === "assert") return `npx -y @midscene/ios@1 assert${suffix} --prompt ${shellQuote(prompt)}`;
    if (command === "screenshot") return `npx -y @midscene/ios@1 take_screenshot${suffix}`;
    if (command === "disconnect") return "npx -y @midscene/ios@1 disconnect";
  }
  if (platform === "desktop") {
    if (command === "connect") return "npx -y @midscene/computer@1 connect";
    if (command === "act") return `npx -y @midscene/computer@1 act --prompt ${shellQuote(prompt)}`;
    if (command === "screenshot") return "npx -y @midscene/computer@1 take_screenshot";
    if (command === "disconnect") return "npx -y @midscene/computer@1 disconnect";
  }
  if (platform === "harmonyos") {
    const device = target.deviceId ? ` --deviceId ${shellQuote(target.deviceId)}` : "";
    if (command === "connect") return `npx -y @midscene/harmony@1 connect${device}`;
    if (command === "act") return `npx -y @midscene/harmony@1 act${device} --prompt ${shellQuote(prompt)}`;
    if (command === "screenshot") return `npx -y @midscene/harmony@1 take_screenshot${device}`;
    if (command === "disconnect") return "npx -y @midscene/harmony@1 disconnect";
  }
  throw new Error(`Unsupported command/platform: ${command}/${platform}`);
}

function renderShell(data) {
  const targetMap = new Map(data.targets.map((target) => [target.id, target]));
  const lines = [];
  lines.push("#!/bin/bash");
  lines.push("set +e");
  lines.push("set -o pipefail");
  lines.push("");
  lines.push('SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"');
  lines.push(`REPORT_DIR="${data.meta.reportDir}"`);
  lines.push(`PROJECT_DIR="${data.meta.projectDir}"`);
  lines.push('REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"');
  lines.push('if [ ! -d "$PROJECT_DIR" ]; then PROJECT_DIR="$REPO_ROOT/$PROJECT_DIR"; fi');
  lines.push('if [ ! -d "$REPORT_DIR" ]; then REPORT_DIR="$REPO_ROOT/$REPORT_DIR"; fi');
  lines.push('LOG_DIR="$REPORT_DIR/logs"');
  lines.push('SCREENSHOT_DIR="$REPORT_DIR/screenshots"');
  lines.push('RESULTS_JSONL="$REPORT_DIR/test-results.jsonl"');
  lines.push('LOG_FILE="$LOG_DIR/test-run.log"');
  lines.push("");
  lines.push('mkdir -p "$LOG_DIR" "$SCREENSHOT_DIR"');
  lines.push(': > "$LOG_FILE"');
  lines.push(': > "$RESULTS_JSONL"');
  lines.push("");
  for (const [key, value] of Object.entries(data.runtime.env || {})) {
    lines.push(`export ${key}=${shellQuote(value)}`);
  }
  lines.push("");
  lines.push("PASS_COUNT=0");
  lines.push("FAIL_COUNT=0");
  lines.push("SKIP_COUNT=0");
  lines.push(`TOTAL_COUNT=${data.cases.length}`);
  for (const testCase of data.cases) {
    lines.push(`${statusVar(testCase.id)}="pending"`);
  }
  lines.push("");
  lines.push('log() { echo "[$(date \'+%Y-%m-%d %H:%M:%S\')] $1" | tee -a "$LOG_FILE"; }');
  lines.push('json_escape() { printf "%s" "$1" | sed \'s/\\\\/\\\\\\\\/g; s/"/\\\\"/g; s/\\t/\\\\t/g\'; }');
  lines.push('record_result() {');
  lines.push('  local id="$1"; local title="$2"; local status="$3"; local target="$4"; local screenshot="$5"; local log_path="$6"; local message="$7"');
  lines.push('  printf \'{"id":"%s","title":"%s","status":"%s","target":"%s","screenshot":"%s","log":"%s","message":"%s"}\\n\' "$(json_escape "$id")" "$(json_escape "$title")" "$(json_escape "$status")" "$(json_escape "$target")" "$(json_escape "$screenshot")" "$(json_escape "$log_path")" "$(json_escape "$message")" >> "$RESULTS_JSONL"');
  lines.push("}");
  lines.push("");
  lines.push('skip_case() {');
  lines.push('  local id="$1"; local title="$2"; local target_id="$3"; local message="$4"');
  lines.push('  SKIP_COUNT=$((SKIP_COUNT + 1))');
  lines.push('  record_result "$id" "$title" "skipped" "$target_id" "" "" "$message"');
  lines.push('  log "RESULT $id: skipped - $message"');
  lines.push("}");
  lines.push("");
  lines.push("# Agent-editable setup hook. Keep test cases in test-cases.json; put environment preparation here or in runtime.setupCommands.");
  for (const cmd of data.runtime.setupCommands || []) lines.push(cmd);
  lines.push("");
  lines.push("# Agent-editable pre-connect hook.");
  for (const cmd of data.runtime.preConnectCommands || []) lines.push(cmd);
  lines.push("");
  lines.push('cd "$PROJECT_DIR" || exit 1');
  lines.push("");
  lines.push("log \"Connecting test targets\"");
  for (const target of data.targets) {
    lines.push(`${commandFor(data, target, "connect")} 2>&1 | tee -a "$LOG_FILE"`);
  }
  lines.push("");
  lines.push("run_case() {");
  lines.push('  local id="$1"; local title="$2"; local target_id="$3"; local act_cmd="$4"; local assert_cmd="$5"; local wait_after="$6"; local screenshot_cmd="$7"; local screenshot_name="$8"');
  lines.push('  local case_log="$LOG_DIR/${id}.log"');
  lines.push('  local screenshot_path="$SCREENSHOT_DIR/$screenshot_name"');
  lines.push('  log "========================================"');
  lines.push('  log "Running $id: $title"');
  lines.push('  log "Target: $target_id"');
  lines.push('  echo "[$id] $title" > "$case_log"');
  lines.push('  eval "$act_cmd" 2>&1 | tee -a "$case_log" "$LOG_FILE"');
  lines.push('  local ec=${PIPESTATUS[0]}');
  lines.push('  if [ "$ec" -eq 0 ] && [ -n "$assert_cmd" ]; then');
  lines.push('    eval "$assert_cmd" 2>&1 | tee -a "$case_log" "$LOG_FILE"');
  lines.push('    ec=${PIPESTATUS[0]}');
  lines.push("  fi");
  lines.push('  if [ "$wait_after" -gt 0 ]; then sleep "$wait_after"; fi');
  lines.push('  eval "$screenshot_cmd" 2>&1 | tee -a "$case_log" "$LOG_FILE" | grep -o "Screenshot saved:.*" | awk \'{print $NF}\' | xargs -I{} cp {} "$screenshot_path" 2>/dev/null || true');
  lines.push('  if [ "$ec" -eq 0 ]; then');
  lines.push('    PASS_COUNT=$((PASS_COUNT + 1))');
  lines.push('    record_result "$id" "$title" "passed" "$target_id" "screenshots/$screenshot_name" "logs/${id}.log" "passed"');
  lines.push('    log "RESULT $id: passed"');
  lines.push("  else");
  lines.push('    FAIL_COUNT=$((FAIL_COUNT + 1))');
  lines.push('    record_result "$id" "$title" "failed" "$target_id" "screenshots/$screenshot_name" "logs/${id}.log" "exit code $ec"');
  lines.push('    log "RESULT $id: failed (exit code $ec)"');
  lines.push("  fi");
  lines.push('  return "$ec"');
  lines.push("}");
  lines.push("");
  const caseCommands = [];
  for (const testCase of data.cases) {
    const target = targetMap.get(testCase.target);
    const titleSlug = slug(testCase.title);
    const screenshot = testCase.screenshot || `${testCase.id}${titleSlug ? `-${titleSlug}` : ""}.png`;
    const prompt = buildPrompt(testCase);
    const screenshotCmd = commandFor(data, target, "screenshot");
    const actCmd = commandFor(data, target, "act", prompt);
    caseCommands.push({
      testCase,
      dependents: normalizeDependents(testCase.dependent),
      command: `run_case ${shellQuote(testCase.id)} ${shellQuote(testCase.title)} ${shellQuote(testCase.target)} ${shellQuote(actCmd)} '' ${Number(testCase.waitAfterSec || 0)} ${shellQuote(screenshotCmd)} ${shellQuote(screenshot)}`,
    });
  }
  for (const item of caseCommands) {
    const currentStatusVar = statusVar(item.testCase.id);
    if (item.dependents.length > 0) {
      const condition = item.dependents.map((dependent) => `[ "${"$"}${statusVar(dependent)}" = "passed" ]`).join(" && ");
      const message = `skipped because dependent case ${item.dependents.join(", ")} did not pass`;
      lines.push(`if ${condition}; then`);
      lines.push(`  ${item.command}`);
      lines.push("  CASE_EC=$?");
      lines.push(`  if [ "$CASE_EC" -eq 0 ]; then ${currentStatusVar}="passed"; else ${currentStatusVar}="failed"; fi`);
      lines.push("else");
      lines.push(`  skip_case ${shellQuote(item.testCase.id)} ${shellQuote(item.testCase.title)} ${shellQuote(item.testCase.target)} ${shellQuote(message)}`);
      lines.push(`  ${currentStatusVar}="skipped"`);
      lines.push("fi");
    } else {
      lines.push(item.command);
      lines.push("CASE_EC=$?");
      lines.push(`if [ "$CASE_EC" -eq 0 ]; then ${currentStatusVar}="passed"; else ${currentStatusVar}="failed"; fi`);
    }
  }
  lines.push("");
  lines.push('log "Total: $TOTAL_COUNT | Passed: $PASS_COUNT | Failed: $FAIL_COUNT | Skipped: $SKIP_COUNT"');
  lines.push("");
  lines.push("# Agent-editable teardown hook.");
  for (const cmd of data.runtime.teardownCommands || []) lines.push(cmd);
  lines.push(`${commandFor(data, data.targets[0], "disconnect")} 2>/dev/null || true`);
  lines.push("");
  lines.push('if [ "$FAIL_COUNT" -gt 0 ]; then exit 1; fi');
  lines.push("exit 0");
  return `${lines.join("\n")}\n`;
}

function main() {
  const input = process.argv[2];
  if (!input) {
    usage();
    process.exit(1);
  }

  const data = readJson(input);
  validate(data);

  const reportDir = path.resolve(data.meta.reportDir);
  fs.mkdirSync(reportDir, { recursive: true });

  const jsonPath = path.join(reportDir, "test-cases.json");
  const shPath = path.join(reportDir, "test-cases.sh");
  fs.writeFileSync(jsonPath, `${JSON.stringify(data, null, 2)}\n`);
  fs.writeFileSync(shPath, renderShell(data), { mode: 0o755 });
  fs.chmodSync(shPath, 0o755);

  console.log(`Generated ${jsonPath}`);
  console.log(`Generated ${shPath}`);
}

main();
