#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

function usage() {
  console.error(`Usage:
  validate-report-locations.js --run-dir doc-test-reports/{run-name}

Validate report Markdown before Feishu publishing.
This script only detects invalid document source locations. It does not auto-fix reports.`);
}

let runDir = "";
for (let i = 2; i < process.argv.length; i += 1) {
  const arg = process.argv[i];
  if (arg === "--run-dir") {
    runDir = process.argv[++i] || "";
  } else if (arg === "-h" || arg === "--help") {
    usage();
    process.exit(0);
  } else {
    console.error(`Unknown argument: ${arg}`);
    usage();
    process.exit(1);
  }
}

if (!runDir) {
  usage();
  process.exit(1);
}

const githubUrlRe = /https:\/\/github\.com\/[^)\s]+/i;
const githubUrlGlobalRe = /https:\/\/github\.com\/[^)\s]+/ig;
const mdxHintRe = /\b[\w./@-]+\.mdx\b/i;
const weakLocationRe = /(^|[\s:：])(?:无|暂无|待补充|未定位|N\/A|-)\s*$/i;

function listMarkdownFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...listMarkdownFiles(full));
    else if (entry.isFile() && entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

function rel(file) {
  return path.relative(process.cwd(), file);
}

function currentIssueId(lines, index) {
  for (let i = index; i >= 0; i -= 1) {
    const m = lines[i].match(/^#{2,4}\s+((?:DOC|BUILD|TEST|FS|CS|P\d)-[A-Za-z0-9_-]+)/i);
    if (m) return m[1];
  }
  return "-";
}

function normalizeGithubUrl(url) {
  return url.replace(/[),.;，。；]+$/g, "");
}

function githubUrls(text) {
  return Array.from(text.matchAll(githubUrlGlobalRe), (m) => normalizeGithubUrl(m[0]));
}

function currentIssueBlock(lines, index) {
  let start = index;
  for (let i = index; i >= 0; i -= 1) {
    if (/^#{2,4}\s+/.test(lines[i])) {
      start = i;
      break;
    }
  }

  let end = lines.length;
  for (let i = index + 1; i < lines.length; i += 1) {
    if (/^#{2,4}\s+/.test(lines[i])) {
      end = i;
      break;
    }
  }

  return lines.slice(start, end).join("\n");
}

function issueBlocks(file) {
  if (!fs.existsSync(file)) return new Map();
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  const blocks = new Map();

  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^#{2,4}\s+((?:DOC|BUILD|TEST|FS|CS|P\d)-[A-Za-z0-9_-]+)/i);
    if (!m) continue;
    const id = m[1];
    let end = lines.length;
    for (let j = i + 1; j < lines.length; j += 1) {
      if (/^#{2,4}\s+/.test(lines[j])) {
        end = j;
        break;
      }
    }
    blocks.set(id, lines.slice(i, end).join("\n"));
  }

  return blocks;
}

function issueHeadingLines(file) {
  if (!fs.existsSync(file)) return new Map();
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  const out = new Map();
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^#{2,4}\s+((?:DOC|BUILD|TEST|FS|CS|P\d)-[A-Za-z0-9_-]+)/i);
    if (m) out.set(m[1], i + 1);
  }
  return out;
}

function isDocumentationIssueBlock(block) {
  return /(?:类别|问题归类)\s*[:：].*(?:📄|🔗|📖|文档问题|链接问题|概念缺失)/.test(block);
}

function isLocationLine(line) {
  return /^\s*(?:-\s*)?(?:文档定位|定位|位置)\s*[:：]/.test(line);
}

function validateLocationLine(file, lines, index, failures, options = {}) {
  const line = lines[index];
  const value = line.replace(/^\s*(?:-\s*)?(?:文档定位|定位|位置)\s*[:：]\s*/, "").trim();

  if (githubUrlRe.test(value)) return;

  if (options.onlyDocumentationIssues) {
    const block = currentIssueBlock(lines, index);
    if (!isDocumentationIssueBlock(block)) return;
  }

  const looksLikeDocLocation = mdxHintRe.test(value);
  const isWeak = !value || weakLocationRe.test(value);

  if (looksLikeDocLocation || isWeak) {
    failures.push({
      file: rel(file),
      line: index + 1,
      issue: currentIssueId(lines, index),
      location: value || "(empty)",
    });
  }
}

const failures = [];

for (const file of listMarkdownFiles(path.join(runDir, "doc-eval-corrected"))) {
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  lines.forEach((line, index) => {
    if (isLocationLine(line)) validateLocationLine(file, lines, index, failures);
  });
}

const buildIssues = path.join(runDir, "build-verification", "build-issues.md");
if (fs.existsSync(buildIssues)) {
  const lines = fs.readFileSync(buildIssues, "utf8").split(/\r?\n/);
  lines.forEach((line, index) => {
    if (isLocationLine(line)) {
      validateLocationLine(buildIssues, lines, index, failures, { onlyDocumentationIssues: true });
    }
  });
}

const originalDocEvalDir = path.join(runDir, "doc-eval");
const correctedDocEvalDir = path.join(runDir, "doc-eval-corrected");
if (fs.existsSync(originalDocEvalDir) && fs.existsSync(correctedDocEvalDir)) {
  for (const correctedFile of listMarkdownFiles(correctedDocEvalDir)) {
    const base = path.basename(correctedFile);
    if (!/^role-.*\.md$/.test(base)) continue;

    const originalFile = path.join(originalDocEvalDir, base);
    if (!fs.existsSync(originalFile)) continue;

    const originalBlocks = issueBlocks(originalFile);
    const correctedBlocks = issueBlocks(correctedFile);
    const correctedHeadingLines = issueHeadingLines(correctedFile);

    for (const [issueId, originalBlock] of originalBlocks.entries()) {
      const originalUrls = githubUrls(originalBlock);
      if (originalUrls.length === 0) continue;

      const correctedBlock = correctedBlocks.get(issueId);
      if (!correctedBlock) continue;

      const correctedUrls = new Set(githubUrls(correctedBlock));
      const missing = originalUrls.filter((url) => !correctedUrls.has(url));
      if (missing.length > 0) {
        failures.push({
          file: rel(correctedFile),
          line: correctedHeadingLines.get(issueId) || 1,
          issue: issueId,
          location: `missing original GitHub location(s): ${missing.join(", ")}`,
        });
      }
    }
  }
}

if (failures.length > 0) {
  console.error("Invalid document locations found. Fix the local Markdown before Feishu publishing.");
  for (const item of failures) {
    console.error(`- ${item.file}:${item.line} ${item.issue} -> ${item.location}`);
  }
  process.exit(2);
}

console.log("Location validation passed.");
