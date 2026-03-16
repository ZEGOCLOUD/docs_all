---
name: create-zego-docs-pr
description: "Create a GitHub pull request following project conventions. Use when the user asks to create a PR, submit changes for review, or open a pull request of ZEGO docs. Handles commit analysis, branch management, PR template usage, and PR creation using the gh CLI tool."
---

# Create a ZEGO Docs PR

Create a GitHub pull request for ZEGO documentation that follows project conventions.

## Prerequisites Check

Before proceeding, verify the following:

### 1. Check if `gh` CLI is installed

```bash
gh --version
```

If not installed, inform the user:
> The GitHub CLI (`gh`) is required but not installed. Please install it:
> - macOS: `brew install gh`
> - Other: https://cli.github.com/

### 2. Check if authenticated with GitHub

```bash
gh auth status
```

If not authenticated, guide the user to run `gh auth login`.

### 3. Verify clean working directory

```bash
git status
```

If there are uncommitted changes, ask the user whether to:
- Commit them as part of this PR
- Stash them temporarily
- Discard them (with caution)

## Gather Context

### 1. Identify the current branch

```bash
git branch --show-current
```

Ensure you're not on `main` or `master`. If so, ask the user to create or switch to a feature branch.

### 2. Find the base branch

```bash
git remote show origin | grep "HEAD branch"
```

This is typically `main` or `master`.

### 3. Analyze recent commits relevant to this PR

```bash
git log origin/main..HEAD --oneline --no-decorate
```

Review these commits to understand:
- What changes are being introduced
- The scope/product of the PR (ZIM, AIAgent, RealTimeVoiceVideo, etc.)
- Whether commits should be squashed or reorganized

### 4. Review the diff

```bash
git diff origin/main..HEAD --stat
```

This shows which files changed and helps identify the type of change.

## Information Gathering

Before creating the PR, you need the following information. Check if it can be inferred from:
- Commit messages
- Branch name (e.g., `callkit`, `real-time-voice-video`, `zim`, `aiagent`, `digital-human`, etc.)
- Changed files and their content

## Git Best Practices

Before creating the PR, consider these best practices:

### Push Changes

Ensure all commits are pushed:
```bash
git push origin HEAD
```

If the branch was rebased, you may need:
```bash
git push origin HEAD --force-with-lease
```

## Create the Pull Request

**IMPORTANT**: Read and use the PR template below. The PR body format must **strictly match** the template structure. Do not deviate from the template format.


```markdown
## 涉及产品

- [ ] RTC (实时音视频/实时语音/超低延迟直播)
- [ ] ZIM (即时通讯)
- [ ] AIAgent (AI 智能体)
- [ ] Digital Human (数字人)
- [ ] UIKit (CallKit/LiveStreamingKit/LiveAudioRoomKit/VideoConferenceKit)
- [ ] Extension Service (超级白板/云端播放器/云端实时 ASR/云端录制/AI美颜/本地服务端录制/星图)
- [ ] Solution
- [ ] General(控制台/政策与协议/词汇表)
- [ ] FAQ(常见问题)
- [ ] 其他

## 变更描述

<!-- 请简要描述本次变更的内容和原因 -->



## 相关 Issue

<!-- 选填，例如: #1234 -->

```

When filling out the template:
- Replace `#XXXX` with the actual issue number, or keep as `#XXXX` if no issue exists (for small fixes)
- Fill in all sections with relevant information gathered from commits and context
- Mark the appropriate "Type of Change" checkbox(es)
- Complete the "Pre-flight Checklist" items that apply

### Create PR with gh CLI

**Use a temporary file for the PR body** to avoid shell escaping issues, newline problems, and other command-line flakiness:

1. Write the PR body to a temporary file:
   ```
   /tmp/pr-body.md
   ```

2. Create the PR using the file:
   ```bash
   gh pr create --title "PR_TITLE" --body-file /tmp/pr-body.md --base main
   ```

3. Clean up the temporary file:
   ```bash
   rm /tmp/pr-body.md
   ```

For draft PRs:
```bash
gh pr create --title "PR_TITLE" --body-file /tmp/pr-body.md --base main --draft
```

**Why use a file?** Passing complex markdown with newlines, special characters, and checkboxes directly via `--body` is error-prone. The `--body-file` flag handles all content reliably.

## Post-Creation

After creating the PR:

1. **Display the PR URL** so the user can review it
2. **Remind about CI checks**: Tests and linting will run automatically
3. **Suggest next steps**:
   - Add reviewers if needed: `gh pr edit --add-reviewer USERNAME`
   - Add labels if needed: `gh pr edit --add-label "bug"`

## Error Handling

### Common Issues

1. **No commits ahead of main**: The branch has no changes to submit
   - Ask if the user meant to work on a different branch

2. **Branch not pushed**: Remote doesn't have the branch
   - Push the branch first: `git push -u origin HEAD`

3. **PR already exists**: A PR for this branch already exists
   - Show the existing PR: `gh pr view`
   - Ask if they want to update it instead

4. **Merge conflicts**: Branch conflicts with base
   - Guide user through resolving conflicts or rebasing

## Summary Checklist

Before finalizing, ensure:
- [ ] `gh` CLI is installed and authenticated
- [ ] Working directory is clean
- [ ] All commits are pushed
- [ ] Branch is up-to-date with base branch
- [ ] Related issue number is identified, or placeholder is used
- [ ] PR description follows the template exactly
- [ ] Appropriate type of change is selected
- [ ] Pre-flight checklist items are addressed
