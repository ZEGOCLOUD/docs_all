---
name: run-zego-docs
description: "This skill should be used when previewing or running the ZEGO documentation local server. Triggers when user asks to preview docs, run docs, start documentation server, view local docs, or launch documentation preview in Chinese or English (预览文档, 启动文档, 查看文档, 本地文档, run docs, preview docs, 预览中文, 预览英文)."
---

# ZEGO 文档预览技能

启动本地文档服务器，预览 ZEGO 文档内容。

## 使用场景

当用户需要本地预览 ZEGO 文档时使用此 skill：
- 预览修改后的文档效果
- 在本地查看文档内容
- 验证文档渲染是否正确

## 工作流程

### Step 1: 确定预览语言

根据用户请求确定语言版本：
- 如果用户提到 "英文"、"English"、"en" → 使用英文版
- 默认使用中文版

### Step 2: 切换到文档目录

```bash
cd /path/to/zego/docs/docs_all
```

### Step 3: 启动文档服务

**中文文档（默认）**：
```bash
./run.sh --zh
```

**英文文档**：
```bash
./run.sh --en
```

### Step 4: 等待服务初始化

服务启动后，首次页面渲染可能需要约 60 秒。请告知用户耐心等待后再访问文档站点。

## 注意事项

1. **后台运行** - 文档服务需要持续运行，建议在后台启动
2. **端口占用** - 如果默认端口被占用，docuo 会使用其他端口
3. **首次运行** - 首次运行可能需要安装 docuo CLI，run.sh 会自动处理

## 常见问题

### docuo 命令未找到

运行 setup.sh 安装：
```bash
bash /path/to/zego/docs/docs_all/setup.sh
```

### 端口被占用

如果用户明确要求终止其他 docuo 服务，请检查并终止占用端口的进程：

> ⚠️ **注意**: `kill -9` 会强制终止进程
