# 文件分类规则

## 分类概述

扫描脚本会自动识别和分类待翻译的文档，根据文件特征采用不同的处理策略。

## 文件类型

### 1. API 文档（自动跳过）

**识别条件**：frontmatter 中包含 `docType: API`

```yaml
---
docType: API
---
```

**处理方式**：标记为跳过，不进行翻译

**原因**：这类文件是自动生成的，不需要翻译

---

### 2. YAML 生成的 MDX（自动跳过 MDX，仅翻译 YAML）

**识别条件**：同一目录下存在同名的 `.mdx` 和 `.yaml` 文件

**示例**：
```
api-reference/
├── interface.mdx    # 跳过（由 YAML 自动生成）
└── interface.yaml   # 翻译
```

**处理方式**：
- 跳过 `.mdx` 文件（自动生成）
- 只翻译 `.yaml` 文件

**原因**：MDX 是从 YAML 自动生成的，翻译 YAML 即可

---

### 3. 全复用文档（预处理）

**识别条件**：除了 frontmatter 外只有两行非空内容
- 一行以 `import Content from` 开头
- 另一行以 `<Content` 开头

**示例**：
```markdown
---
title: 常见问题
---

import Content from '@site/zh/xxx/xxx.mdx';
<Content components={all} />
```

**处理方式（调用脚本处理）**：
1. 提取 import 路径
2. 将路径中的 `/zh/` 替换为 `/en/`
3. 检查对应的英文文档是否存在
4. 如果存在：替换路径并保存，标记为"已解决"（不需要翻译）
5. 如果不存在：标记为"需要翻译"

**原因**：全复用文档只是引用其他内容，如果英文版本已存在则直接引用

---

### 4. 普通文档（按大小分类）

**识别条件**：不属于以上任何类型的 `.md` 或 `.mdx` 文件

**分类标准**：

#### 小文件（< 50 行）
- **处理方式**：每批 10-20 个文件
- **总行数控制**：不超过 1000 行
- **特点**：翻译快速，可以批量处理

#### 中等文件（50-300 行）
- **处理方式**：每批 2-5 个文件
- **总行数控制**：不超过 1500 行
- **特点**：需要适度关注，合理分批

#### 大文件（> 300 行）
- **处理方式**：单独成批
- **分段翻译**：如果超过 2000 行，需要分段处理
- **特点**：需要更多时间，可能需要中断和恢复

---

## 跳过原因代码

在进度文件中，每个跳过的文件都会标记 `reason_code`：

- `api_doc`：API 文档（docType: API）
- `yaml_generated`：YAML 生成的 MDX
- `reuse_doc_resolved`：全复用文档已解决（找到英文版本）

---

## 扫描输出示例

```json
{
  "summary": {
    "total_files": 150,
    "skipped_api_files": 20,
    "skipped_mdx_files": 15,
    "yaml_files_to_translate": 15,
    "reuse_docs": 10,
    "small_files": 60,
    "medium_files": 20,
    "large_files": 5
  }
}
```
