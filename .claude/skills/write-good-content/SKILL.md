---
name: write-good-content
description: This skill should be used when the user asks to "write documentation", "edit documentation", "create a doc", "update documentation", "rewrite content", "write a guide", "write a tutorial", "improve writing", "fix writing style", "编写文档", "修改文档", "更新文档", "重写文档", "优化文案", or any task that involves writing, editing, or refining MDX documentation content. Load this skill before writing or editing any documentation to ensure compliance with writing and formatting standards.
---

# Documentation Writing Standards

Follow these rules when writing or editing any documentation content. Apply them consistently across all MDX files.

## Expression Standards

### Titles and Headings

- Maintain consistent sentence structure across headings at the same level.
- Keep headings concise and focused on the section's central topic.
- Do not add any punctuation to headings.

### Vocabulary

Avoid these categories of words:

- **Degree/emphasis words** — replace with concrete data or examples. Avoid: 较多, 较好, 完全地, 基本地, 决定性的, 最后的, 仅仅, 事实上, 值得注意的.
- **Contrast words** — avoid: 当然, 然而, 但是.
- **Vague words** — avoid: 有些, 非常, 大量, 一些, 少许, 部分, 一段时间, 几乎.
- **Overly colloquial words** — avoid: 接下来, 总的来说, 点击一下按钮.

### Technical Terms

When a technical term appears in a document, add an explanation at the beginning of the document and include a link to a detailed description where possible.

### Abbreviations

On first occurrence, abbreviations must be expanded:

- **Chinese documents**: 缩略语（英文全称，中文解释）. Example: VPN（Virtual Private Network，虚拟专用网络）.
- **English documents**: Full Name (Abbreviation). Example: Virtual Private Network (VPN).

### Notes and Warnings

- Use `<Note>` for informational tips and hints for developers.
- Use `<Warning>` when ignoring the notice could cause errors or adverse outcomes.

## Formatting Standards

### Tables

- Every table must have a header row using nouns or noun phrases. Only one header row per table.
- No blank cells allowed. Fill empty cells with `-`, or use `!mu` / `!md` / `!ml` / `!mr` to merge cells.

### Punctuation

- Separate directory levels with `/` and do not add a trailing slash. Example: `/ZegoExpressExample/Mixer`.
- Use full-width Chinese punctuation in Chinese documents and half-width English punctuation in English documents (except in code and quoted content).
- End all declarative sentences with a period.
- In Chinese documents, add a space before and after English text and numbers. Example: `可以设置 FPS 为 15 。`
- Add a space before and after inline code and links.
- Connect menu paths with ` > ` and wrap in quotation marks. Example: `"文件 > 新建 > 新建工程"`.
- Use ` ~ ` (with spaces) to express numeric ranges. Example: `300 ~ 600`.
- Use closed intervals `[min, max]` for parameter value ranges. Example: `volume 取值范围为 [1, 100]`.
- Both numbers in a range must either both carry units or both omit units. Example: `10 ms ~ 100 ms`.

### Date and Time

- Date format: `YYYY-MM-DD` (zero-padded). Example: `2023-07-20`.
- Time format: `hh:mm:ss` (zero-padded). Example: `14:42:35`.
- Combined format uses a space: `2023-07-20 14:42:35`.

## Pre-Writing Checklist

Before writing or editing documentation, verify:

1. Headings are concise, unpunctuated, and structurally consistent.
2. No degree, vague, contrast, or colloquial words remain.
3. Technical terms and abbreviations are explained on first use.
4. `<Note>` and `<Warning>` components are used appropriately.
5. Tables have proper headers and no empty cells.
6. Punctuation matches the document language (full-width for Chinese, half-width for English).
7. Spaces are placed around inline code, links, English text, and numbers in Chinese documents.
8. Numeric ranges and parameter ranges follow the correct format.
9. Dates and times follow the `YYYY-MM-DD hh:mm:ss` format.

## Post-Writing Review

After writing, review the content for:

- Readability and clarity — remove unnecessary words and ensure each sentence adds value.
- Consistency — check that terminology, formatting, and style are uniform throughout the document.
- Accuracy — verify that technical details, parameter names, and code examples are correct.
