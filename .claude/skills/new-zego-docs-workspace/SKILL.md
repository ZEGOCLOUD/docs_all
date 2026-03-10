---
name: new-zego-docs-workspace
description: "This skill prepares a clean git workspace for new ZEGO documentation tasks. Use when starting a new docs task with a clean git state. 触发短语: 'create new workspace', '新建工作区', 'start new docs task', '开始新任务', 'prepare clean workspace', '准备干净工作区', 'sync and create branch', '同步并创建分支', 'new zego docs task', '新文档任务', 'clean slate', '重新开始'."
---

# ZEGO 文档新工作空间技能

为处理 ZEGO 文档的新任务准备一个干净的工作环境。

## 使用场景

当用户有新的文档修改任务时，使用此 skill 来：
1. 确保工作区干净或创建临时工作区
2. 同步上游代码（如果是 fork 仓库）
3. 拉取最新代码
4. 创建新分支并开始任务

## 工作流程

### Step 1: 检查仓库状态

```bash
# 检查是否有未提交的内容
git status --porcelain
```

**判断逻辑**：
- 如果输出为空 → 仓库干净，继续 Step 2
- 如果有输出 → 有未提交内容，需要创建临时工作区

---

### Step 2: 处理未提交内容（如果需要）

如果仓库有未提交内容，创建临时工作区：

1. 创建临时副本
```bash
TEMP_WORKSPACE="${REPO_PATH}_temp_$(date +%s)"
cp -r "$REPO_PATH" "$TEMP_WORKSPACE"
```

2. 进入临时工作区
```bash
cd "$TEMP_WORKSPACE"
```

3. 清理临时工作区中未暂存内容
```bash
git reset --hard    # 丢弃所有未暂存的修改
```

**注意**：任务完成后需要删除临时工作区

---

### Step 3: 检查远程仓库配置

```bash
# 检查是否有 upstream
git remote -v
```

**判断逻辑**：
- 如果有 `upstream` → 这是 fork 仓库，需要同步上游
- 如果只有 `origin` → 直接拉取即可

---

### Step 4: 同步上游代码（如果是 fork）

如果有 upstream 远程仓库：

```bash
# 使用 gh 命令同步 fork
gh repo sync --source upstream
```

---

### Step 5: 拉取最新代码

```bash
# 切换到主分支
git checkout main  # 或 master，根据实际情况

# 拉取最新代码
git pull origin main
```

---

### Step 6: 创建新分支

```bash
# 创建并切换到新分支
# 分支名格式建议：feature/xxx, fix/xxx, docs/xxx
git checkout -b <branch-name>
```

**分支命名建议**：
按产品功能模块划分，如：
- `callkit`
- `real-time-voice`
- `whiteboard`

---

### Step 7: 开始处理任务

现在工作区已准备好，可以：
1. 按用户要求修改文档内容
2. 完成后提交代码

**如果使用了临时工作区，完成后清理：**
```bash
rm -rf "$TEMP_WORKSPACE"
```


## 注意事项

1. **保护现有工作** - 有未提交内容时一定要创建临时工作区。除非用户明确表示可以丢弃未暂存内容。
2. **同步上游** - fork 仓库务必先同步再开始工作
3. **分支命名** - 使用有意义的分支名，方便后续管理
4. **清理工作区** - 临时工作区用完记得删除，避免占用磁盘
