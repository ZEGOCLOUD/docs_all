# FAQ 维度生成 / 迁移 / 查询工具

按 `instance.id` 过滤 FAQ 的整套工具链。**核心设计：`docuo.config.{zh,en}.json` 是产品/平台的唯一真相**，
所有 FAQ 维度数据都从 config 派生，config 改动后重跑生成脚本即可更新，无需手动维护映射表。

## 文件清单

| 文件 | 作用 | 输入 → 输出 |
|---|---|---|
| `generate_faq_dimensions.mjs` | 从 config 派生 FAQ 维度 | `docuo.config.*.json` → `general/{zh,en}/faq/faqDimensions.js` |
| `generate_static_faq.mjs` | 预生成 curl 可取的静态 JSON | `overview.mdx` + `faqDimensions.js` → `static/faq-instance/<id>.json` |

运行时（浏览器端）依赖：`general/{zh,en}/faq/` 下的 `faqDimensions.js`、`faqMatch.js`、`FilteredLink.jsx`、`FaqFilters.jsx`。

## 2种消费方式

- **浏览器**：访问 `/faq/overview?instance=<id>`，`FaqFilters` 自动用 `instanceMap` 解析出该实例的 product/platform 并选中，列表实时过滤。
- **curl / 外部程序（线上）**：`curl https://doc-zh.zego.im/faq-instance/<id>.json` → `[{href,title}]`。详见下方「curl 数据端点」。

2者共用同一份 `faqMatch.js` + `faqDimensions.js`，命中集合完全一致（零漂移）。

## curl 数据端点（`static/faq-instance/`）

docuo 是 SSG，`?instance=` 过滤只在浏览器端跑，curl 拿到的是全量 HTML。所以把每个 instance 的结果**预生成成静态 JSON**放进 `static/`（docuo 把 `static/<x>` 原样 serve 到 `/<x>`），curl 即可取：

```bash
# 取某个实例的 FAQ（按语言分目录）
curl https://doc-zh.zego.im/faq-instance/zh/real_time_video_ios_oc_zh.json
# → [{"href":"/faq/express-reconnect","title":"Express SDK 是否支持断线重连机制？"}, ...]

curl https://doc-en.zego.im/faq-instance/en/real_time_video_ios_oc.json   # 英文站

# 取某语言的合法 id 列表（发现用）
curl https://doc-zh.zego.im/faq-instance/zh/index.json
# → [{"id":"real_time_video_ios_oc_zh","product":"实时音视频","platform":"iOS"}, ...]
```

- **按 lang 分目录**（`faq-instance/zh`、`faq-instance/en`）：`static/` 是两套站点共享的同一目录，中英文 id 将来可能撞车，分目录隔离。
- 这些 JSON **必须提交进仓库**——docuo 生产构建只打包已提交的 `static/`。
- **dev 模式下新增/改动的静态文件不会被 serve**（docuo 启动时一次性拷贝 `static/`）；本地验证需**重启一次 `docuo dev`**。生产构建无此问题。

## ⭐ 维护流程：改了 docuo.config.*.json 之后怎么更新？

**第①步已全自动**：只要 pre-commit hook 装了（见下），改了 config / overview 后 `git commit`，hook 会自动重跑生成脚本并把产物加进本次提交，无需手动跑任何命令。

```
改 config（加/删/改产品或 instance）或 overview.mdx
        │
        ▼ git commit 时自动触发（pre-commit hook）
① 重跑生成脚本（全自动，产物自动 git add）
   node .scripts/faq/generate_faq_dimensions.mjs   # 浏览器下拉/instanceMap
   node .scripts/faq/generate_static_faq.mjs       # curl 静态 JSON（static/faq-instance/）
        │
        ▼ 人工（按需）
② 体检 overview 标注（半自动：报告 config 已不存在的新孤儿，人工决定清空/归并）
   node .scripts/faq/migrate_overview_products.mjs --check
```

> 生成产物（`faqDimensions.js`、`static/faq-instance/*.json`）需**提交进仓库**，docuo 生产构建才会打包——hook 已自动 `git add`，直接 commit 即可。

### pre-commit hook 自动触发条件

`.hooks/pre-commit` 在本次 staged 文件命中以下任一时自动跑 ①：

- `docuo.config.zh.json` / `docuo.config.en.json`
- `general/zh/faq/overview.mdx` / `general/en/faq/overview.mdx`

**一次性启用**：clone 后跑一次 `bash setup.sh`（会执行 `git config core.hooksPath .hooks`）。之后每次 commit 自动生效。生成脚本**幂等**，重跑只会覆盖出相同内容，没 diff 就什么都不加。

| 产物 | 自动化 | config 改动后 |
|---|---|---|
| `faqDimensions.js`（下拉 / instanceMap） | 100% 自动（hook） | commit 即更新 |
| `static/faq-instance/*.json`（curl 端点） | 100% 自动（hook） | commit 即更新 |
| `overview.mdx` 的 FilteredLink 标注（文档内容） | 半自动 | `--check` 报告新孤儿，人工处理 |

- `generate_faq_dimensions.mjs` **幂等、可随时重跑**——config 是唯一维护点，重跑即更新，不存在「手动维护映射表」。
- 若 `migrate --check` 报出新孤儿（overview 写了、config 已没有的产品），两种处理：
  - 真是退役产品 → 加进 `migrate_overview_products.mjs` 的 `clear` 表，跑一次迁移；
  - 是 config 漏了 → 在 config 补 group，再重跑 generate。
- **dev 预览也自动刷新**：`./run.sh` 在 `docuo dev` 之前会跑一次 `generate_faq_dimensions.mjs`，改完 config 下次预览直接看到新下拉（不依赖 commit）。

## 常用命令

```bash
# 1) 从 config 重新生成维度（改了 config 后必跑）
node .scripts/faq/generate_faq_dimensions.mjs

# 2) 体检 overview 标注（不改文件）
node .scripts/faq/migrate_overview_products.mjs --check

# 3) 执行迁移（改写 overview.mdx；建议随后 git diff 复核）
node .scripts/faq/migrate_overview_products.mjs
node .scripts/faq/migrate_overview_products.mjs --lang=en      # 只处理某语言

# 4) 脚本端查询
node .scripts/faq/faq-by-instance.mjs --instance real_time_video_ios_oc_zh
node .scripts/faq/faq-by-instance.mjs --instance real_time_video_ios_oc --lang en --json
```

## 实例 id 从哪来？

`docuo.config.{zh,en}.json` → `themeConfig.instanceGroups[*].instances[*].id`。
查不到时 `faq-by-instance.mjs` 会打印该语言的实例示例供对照（注意 en 的 id 通常不带语言后缀）。
