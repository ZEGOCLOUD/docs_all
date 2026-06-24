#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

function usage() {
  console.error(`Usage:
  prepare-feishu-report-content.js --run-dir doc-test-reports/{run-name}

Prepare local Markdown reports before writing them to Feishu:
- align report H1 titles with Feishu skeleton titles in manifest;
- replace role report links in doc-eval summary with Feishu URLs from manifest;
- add the required role-report review note;
- merge build-verification/build-issues.md into build-test-report.md as "问题详情";
- validate the corrected doc-eval summary's required sections and issue ID alignment.

Run validate-report-locations.js first. This script does not fix invalid source locations.`);
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

const manifestPath = path.join(runDir, "feishu-report-manifest.json");
if (!fs.existsSync(manifestPath)) {
  console.error(`Manifest not found: ${manifestPath}`);
  process.exit(1);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const documents = manifest.documents || {};

function readIfExists(file) {
  if (!fs.existsSync(file)) return null;
  return fs.readFileSync(file, "utf8");
}

function write(file, content) {
  fs.writeFileSync(file, content.endsWith("\n") ? content : `${content}\n`);
  console.log(`Prepared ${file}`);
}

function normalizeH1(file, title) {
  if (!title) return;
  const content = readIfExists(file);
  if (content == null) return;
  const next = content.match(/^#\s+/)
    ? content.replace(/^#\s+.*$/m, `# ${title}`)
    : `# ${title}\n\n${content}`;
  if (next !== content) write(file, next);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function insertBeforeNextH2(content, headingPattern, insertText) {
  const heading = content.match(headingPattern);
  if (!heading || heading.index == null) return content;
  const start = heading.index + heading[0].length;
  const rest = content.slice(start);
  const nextHeading = rest.match(/\n##\s+/);
  const insertAt = nextHeading && nextHeading.index != null
    ? start + nextHeading.index
    : content.length;
  return `${content.slice(0, insertAt).trimEnd()}\n\n${insertText.trim()}\n\n${content.slice(insertAt).trimStart()}`;
}

function insertAfterTableFollowingHeading(content, headingPattern, insertText) {
  const heading = content.match(headingPattern);
  if (!heading || heading.index == null) return insertBeforeNextH2(content, headingPattern, insertText);

  let cursor = heading.index + heading[0].length;
  const afterHeading = content.slice(cursor);
  const leadingBlank = afterHeading.match(/^(\s*\n)*/);
  cursor += leadingBlank ? leadingBlank[0].length : 0;

  const lines = content.slice(cursor).split(/\n/);
  let tableLineCount = 0;
  for (const line of lines) {
    if (/^\|.*\|\s*$/.test(line)) tableLineCount += 1;
    else break;
  }

  if (tableLineCount < 2) return insertBeforeNextH2(content, headingPattern, insertText);

  const tableText = lines.slice(0, tableLineCount).join("\n");
  const insertAt = cursor + tableText.length;
  return `${content.slice(0, insertAt).trimEnd()}\n\n${insertText.trim()}\n\n${content.slice(insertAt).trimStart()}`;
}

function replaceOrInsertSection(content, sectionTitle, sectionMarkdown, afterHeadingPattern) {
  const sectionPattern = new RegExp(`\\n##\\s+${escapeRegExp(sectionTitle)}\\s*\\n`);
  const existing = content.match(sectionPattern);
  const section = `## ${sectionTitle}\n\n${sectionMarkdown.trim()}\n`;

  if (existing && existing.index != null) {
    const start = existing.index + 1;
    const restStart = existing.index + existing[0].length;
    const rest = content.slice(restStart);
    const next = rest.match(/\n##\s+/);
    const end = next && next.index != null ? restStart + next.index : content.length;
    return `${content.slice(0, start)}${section}${content.slice(end).replace(/^\n+/, "\n")}`;
  }

  return insertBeforeNextH2(content, afterHeadingPattern, section);
}

function sectionBody(content, headingRe) {
  const match = content.match(headingRe);
  if (!match || match.index == null) return "";
  const start = match.index + match[0].length;
  const rest = content.slice(start);
  const next = rest.match(/\n##\s+/);
  const end = next && next.index != null ? start + next.index : content.length;
  return content.slice(start, end);
}

function failSummaryValidation(errors) {
  if (errors.length === 0) return;
  console.error("Corrected doc-eval summary validation failed. Fix the local Markdown before Feishu publishing.");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(2);
}

function validateCorrectedSummary(content, file) {
  const errors = [];
  const required = [
    [/^##\s+总体结论\s*$/m, "## 总体结论"],
    [/^##\s+角色评分(?:（校正后）)?\s*$/m, "## 角色评分 或 ## 角色评分（校正后）"],
    [/^##\s+问题摘要\s*$/m, "## 问题摘要"],
    [/^##\s+问题详情\s*$/m, "## 问题详情"],
  ];

  for (const [re, label] of required) {
    if (!re.test(content)) errors.push(`${file} missing required section: ${label}`);
  }

  const forbidden = [
    "集成验证校正记录",
    "集成验证校正",
    "集成验证新增文档问题",
    "非文档问题说明",
    "共性问题",
    "改进建议排序",
    "产物索引",
    "加权维度评分",
    "接入测试综合报告",
  ];
  for (const title of forbidden) {
    const re = new RegExp(`^##\\s+${escapeRegExp(title)}\\s*$`, "m");
    if (re.test(content)) errors.push(`${file} contains retired section: ## ${title}`);
  }

  const summaryBody = sectionBody(content, /\n##\s+问题摘要\s*\n/);
  const detailBody = sectionBody(content, /\n##\s+问题详情\s*\n/);
  const summaryIds = [];
  for (const line of summaryBody.split(/\r?\n/)) {
    const m = line.match(/^\|\s*((?:DOC|BUILD|TEST|FS|CS|P\d|DOC-N)-[A-Za-z0-9_-]+)\s*\|/i);
    if (m) summaryIds.push(m[1]);
  }

  const detailBlocks = new Map();
  const detailHeadingRe = /^###\s+((?:DOC|BUILD|TEST|FS|CS|P\d|DOC-N)-[A-Za-z0-9_-]+)[^\n]*$/gim;
  const matches = Array.from(detailBody.matchAll(detailHeadingRe));
  for (let i = 0; i < matches.length; i += 1) {
    const current = matches[i];
    const next = matches[i + 1];
    const start = current.index == null ? 0 : current.index + current[0].length;
    const end = next && next.index != null ? next.index : detailBody.length;
    detailBlocks.set(current[1], detailBody.slice(start, end));
  }

  for (const id of summaryIds) {
    if (!detailBlocks.has(id)) errors.push(`${file} summary issue ${id} missing matching detail heading`);
  }
  for (const id of detailBlocks.keys()) {
    if (!summaryIds.includes(id)) errors.push(`${file} detail issue ${id} is not listed in problem summary`);
  }
  for (const [id, block] of detailBlocks.entries()) {
    if (!/^\s*-\s*角色\s*[:：]\s*\S+/m.test(block)) {
      errors.push(`${file} detail issue ${id} missing required "- 角色：" field`);
    }
  }

  failSummaryValidation(errors);
}

function demoteBuildIssues(content) {
  const lines = content.split(/\r?\n/);
  let skippedFirstH1 = false;
  return lines
    .filter((line) => {
      if (!skippedFirstH1 && /^#\s+/.test(line)) {
        skippedFirstH1 = true;
        return false;
      }
      return true;
    })
    .map((line) => (/^#{1,5}\s+/.test(line) ? `#${line}` : line))
    .join("\n")
    .trim();
}

function prepareBuildReport() {
  const buildReport = path.join(runDir, "build-test-report.md");
  const buildIssues = path.join(runDir, "build-verification", "build-issues.md");
  let content = readIfExists(buildReport);
  const issues = readIfExists(buildIssues);
  if (content == null) return;

  const title = documents["build-test-report"] && documents["build-test-report"].title;
  if (title) {
    content = content.match(/^#\s+/)
      ? content.replace(/^#\s+.*$/m, `# ${title}`)
      : `# ${title}\n\n${content}`;
  }

  if (issues != null && issues.trim()) {
    const sectionMarkdown = [
      `以下内容合并自 [build-verification/build-issues.md](build-verification/build-issues.md)。`,
      "",
      demoteBuildIssues(issues),
    ].join("\n");
    content = replaceOrInsertSection(content, "问题详情", sectionMarkdown, /\n##\s+关键问题\s*\n/);
  }

  write(buildReport, content);
}

function roleDisplayName(roleId, entry) {
  if (entry && entry.title) {
    return entry.title.replace(/^【文档评测报告】/, "").trim();
  }
  return roleId;
}

function prepareDocEvalSummary() {
  const summary = path.join(runDir, "doc-eval-corrected", "doc-eval-summary.md");
  let content = readIfExists(summary);
  if (content == null) return;

  const summaryTitle = documents["doc-eval-summary"] && documents["doc-eval-summary"].title;
  if (summaryTitle) {
    content = content.match(/^#\s+/)
      ? content.replace(/^#\s+.*$/m, `# ${summaryTitle}`)
      : `# ${summaryTitle}\n\n${content}`;
  }

  const roles = documents["doc-eval-role"] || {};
  for (const [roleId, entry] of Object.entries(roles)) {
    if (!entry || !entry.url) continue;
    const label = roleDisplayName(roleId, entry);
    const url = entry.url;
    const roleMd = `${roleId}.md`;

    content = content.replace(
      new RegExp(`\\[([^\\]]*?)\\]\\((?:\\.\\.?/)?(?:doc-eval-corrected/)?${escapeRegExp(roleMd)}(?:#[^)]+)?\\)`, "g"),
      (_match, text) => `[${!text || text === roleMd ? label : text}](${url})`,
    );

    content = content.replace(
      new RegExp(`(?<![\\[\\]\\w/-])${escapeRegExp(roleMd)}(#[A-Za-z0-9_.\\-\\u4e00-\\u9fa5]+)?`, "g"),
      `[${label}](${url})`,
    );
  }

  const note = "**请阅读各角色详细报告文档并评论问题解决方案！**";
  if (!content.includes(note)) {
    content = insertAfterTableFollowingHeading(content, /\n##\s+角色评分[^\n]*\n/, note);
  }

  validateCorrectedSummary(content, summary);

  write(summary, content);
}

function prepareRoleReports() {
  const dir = path.join(runDir, "doc-eval-corrected");
  if (!fs.existsSync(dir)) return;
  const roles = documents["doc-eval-role"] || {};
  for (const fileName of fs.readdirSync(dir)) {
    if (!/^role-.*\.md$/.test(fileName)) continue;
    const roleId = fileName.replace(/\.md$/, "");
    const title = roles[roleId] && roles[roleId].title;
    normalizeH1(path.join(dir, fileName), title);
  }
}

prepareBuildReport();
prepareDocEvalSummary();
prepareRoleReports();
