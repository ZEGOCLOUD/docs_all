---
name: write-blog
description: >
  This skill should be used when the user asks to "write a blog", "generate a blog article",
  "create a tutorial blog", "write a technical blog post", "generate blog content from example code",
  "write a blog about this project", or mentions blog writing with personas. Generates high-quality,
  persona-driven technical blog articles based on ZEGO example code projects.
version: 0.1.0
---

# Write Blog

Generate high-quality, persona-driven technical blog articles from ZEGO example code projects. The output is a complete, publishable blog article that reads like a real developer wrote it — not AI-generated content.

## Purpose

Transform working example code into a compelling technical blog that teaches readers how to build the same feature. The blog includes architecture diagrams, precise code snippets, implementation rationale, and screenshots from device automation.

## When to Use

Trigger this skill when the user wants to write a blog article about a ZEGO example code project. The input is always an existing example code project directory.

## Workflow

### Step 1: Gather Requirements

Collect the following from the user or infer from context:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| Topic | Yes | — | Blog topic (e.g., "Build a group chat app with ZIM") |
| Keywords | No | Auto-detected | SEO keywords to include |
| Persona | No | Random | Name of a specific persona (see references/) |
| Language | No | `en` | `en` for English, `zh` for Chinese |
| Project path | Yes | — | Path to the example code project |

If the user does not specify a persona, randomly select one appropriate for the language. Do not ask the user to choose — just pick one and note the choice in the output.

### Step 2: Analyze the Example Code

Before writing any content, thoroughly analyze the example code project:

1. **Read the project structure** — Understand files, dependencies, and architecture
2. **Read all source files** — Understand the complete implementation
3. **Identify the SDK** — Determine which ZEGO SDK is used (ZIM, Express Video, AI Agent, etc.) and its version
4. **Map the data flow** — Trace how data moves through the application
5. **Identify key APIs** — List the core SDK methods used
6. **Note interesting patterns** — Find non-obvious implementation decisions worth explaining
7. **Check for test cases** — Read any test-case files for validation scenarios

This analysis informs the architecture diagrams and code snippet selection.

### Step 3: Select Persona

Load only the single persona file needed — one file per persona, on demand:

**English personas** (`references/personas-en/`):

| File | Persona | Style |
|------|---------|-------|
| `jake.md` | Jake — Pragmatic American Full-Stack Dev | Casual, direct, production-ready |
| `priya.md` | Priya — Detail-Oriented Indian Tech Lead | Structured, thorough, diagram-heavy |
| `marcus.md` | Marcus — British Software Architect | Dry wit, flowing prose, elegant code |
| `lukas.md` | Lukas — Methodical German Engineer | Precise, comprehensive, production-quality |
| `lucia.md` | Lucia — Brazilian Creative Developer | Enthusiastic, visual, design-minded |
| `kenji.md` | Kenji — Japanese Precision Coder | Calm, meticulous, mechanism-focused |
| `amara.md` | Amara — Nigerian Community Builder | Warm, storytelling, progressive examples |
| `sophie.md` | Sophie — Australian No-Nonsense Dev | Blunt, practical, copy-paste ready |
| `chen-wei.md` | Chen Wei — Canadian Polyglot Engineer | Reflective, cross-cultural, balanced |
| `raj.md` | Raj — Singaporean Solutions Architect | Professional, enterprise-grade, efficient |

**Chinese personas** (`references/personas-zh/`):

| File | Persona | Style |
|------|---------|-------|
| `lao-zhang.md` | 老张 — 资深技术专家 | 专业严谨，协议层深度分析 |
| `xiao-li.md` | 小李 — 轻松程序员博主 | 口语化，通俗易懂，自嘲式幽默 |
| `professor-chen.md` | 陈教授 — 学术型博主 | 理论支撑，形式化表述，学术引用 |
| `a-ming.md` | 阿明 — 故事型博主 | 叙事结构，场景描写，特稿风格 |
| `engineer-wang.md` | 工科老王 — 简洁工程师 | 极简高效，信息密度高，直入主题 |

Read the full persona description and adopt its characteristics. The persona affects:
- Sentence structure and rhythm
- Paragraph length and density
- Humor style and frequency
- Code example depth and commenting style
- Section transitions and openings
- Vocabulary and phrase choices

### Step 4: Load Quality Guidelines

Read `references/blog-structure.md` for:
- Required blog sections and their order
- Code snippet precision rules
- Mermaid diagram guidelines (sequence, architecture, flowchart)
- Anti-AI-writing patterns (banned phrases and structures)
- Screenshot integration guidelines
- Quality checklist

### Step 5: Capture Screenshots (Important)

Capture screenshots of key UI states:

1. Check which device automation skills are available
2. Connect to the running app using the appropriate skill
3. Capture screenshots at key interaction points (login, main view, feature demos)
4. Save screenshots to `blog/assets/` within the project directory

Available device automation skills:
- **zego-browser-automation** — Web apps via headless Chrome
- **android-device-automation** — Android device testing
- **ios-device-automation** — iOS device testing
- **harmonyos-device-automation** — HarmonyOS device testing
- **desktop-computer-automation** — Desktop app testing

This step is important. Screenshots are required for the blog to be valid.

### Step 6: Generate the Blog

Write the blog following the structure from `references/blog-structure.md`. Key principles:

**Pre-Generation Checklist (MANDATORY):**

Before writing any blog content, output the following checklist and confirm each rule. This step is not optional — it forces awareness of critical constraints that are easy to lose during long-form generation.

```
Critical Rules Checklist:
- [ ] Brand name: English = "ZEGOCLOUD" (NOT "ZEGO"), Chinese = "ZEGO" or "即构科技"
- [ ] Brand placement: Do NOT appear in the opening hook (first 2-3 paragraphs). Introduce naturally after the problem/context.
- [ ] Hook structure: Problem → Architecture → SDK Introduction → Implementation
- [ ] Sentence length: Average under 20 words. Split any sentence over 25 words.
- [ ] Em dashes: Max 2 per article.
- [ ] H2 headings: Must include target keywords (not generic labels).
- [ ] FAQ: 3-5 entries as the last content section.
- [ ] Step-by-step: Numbered format for all implementation sections.
- [ ] Data-backed claims: Latency, size, limits — no vague adjectives.
- [ ] No banned AI phrases (see blog-structure.md).
```

**Content Generation Rules:**
1. **Brand name and placement (HIGHEST PRIORITY):** In English blogs, always use "ZEGOCLOUD" — never "ZEGO" as shorthand. In Chinese blogs, use "ZEGO" or "即构科技". The brand must NOT appear in the opening hook (first 2-3 paragraphs). Follow the structure: Problem → Architecture → SDK Introduction → Implementation. See `references/blog-structure.md` "Brand Name Placement" section for details and negative examples.
2. Write in the selected persona's voice, but follow the Professional Writing Standards in `references/blog-structure.md` (sentence length, dash limits, data-driven claims, objective tone)
3. Every code snippet must be extracted from the actual example code — not invented
4. Include at least one Mermaid sequence diagram and one architecture diagram
5. Explain WHY behind design decisions, not just WHAT the code does
6. Include error handling and edge cases in code examples
7. Add a troubleshooting section covering common issues found during testing
8. Include `.env.example` or environment configuration in the setup section
9. H2 headings must include target keywords (not generic labels like "Setup" or "Implementation")
10. Include an FAQ section with 3-5 entries as the last content section
11. Use numbered step-by-step format for all implementation sections
12. Back technical claims with data (latency, size, limits, throughput)

**Anti-AI Writing:**
- Consult the banned phrases list in `references/blog-structure.md`
- Vary paragraph length intentionally
- Use contractions and natural speech patterns
- Include specific version numbers and dates
- Show genuine opinions and preferences
- Admit uncertainty when appropriate
- Never use "Happy coding!" or similar AI signatures
- Limit em dashes to 2 per article
- Keep average sentence length under 20 words
- Minimize first-person subjective expressions

**Length Targets:**
- English: 3,000–6,000 words
- Chinese: 4,000–8,000 characters

### Step 7: Output

1. Create the output directory: `<project-path>/blog/`
2. Write the blog as `<project-path>/blog/<slugified-title>.md`
3. If screenshots were captured, they are in `<project-path>/blog/assets/`
4. Report the output to the user: persona used, word count, sections included, screenshots taken

## Additional Resources

### Reference Files

- **`references/personas-en/`** — 10 English persona files, one per persona (load only the selected one)
- **`references/personas-zh/`** — 5 Chinese persona files, one per persona (load only the selected one)
- **`references/blog-structure.md`** — Complete blog structure template, code guidelines, Mermaid patterns, anti-AI-writing rules, and quality checklist

### Device Automation Skills

These project skills handle screenshot capture for different platforms:
- `zego-browser-automation` — Web app testing via headless Chrome
- `android-device-automation` — Android device automation
- `ios-device-automation` — iOS device automation
- `harmonyos-device-automation` — HarmonyOS device automation
- `desktop-computer-automation` — Desktop app automation

## Quick Reference

```
Input:  Project path + Topic + Optional: Persona, Language, Keywords
Output: blog/<title>.md with architecture diagrams, code snippets, screenshots
```

### Example Usage

```
User: "Write a blog about the zim-group-chat example"
→ Analyzes examples/zim-group-chat/
→ Randomly selects persona (e.g., Marcus)
→ Loads references/personas-en/marcus.md (only that one file)
→ Loads references/blog-structure.md
→ Generates blog with Mermaid diagrams
→ Output: examples/zim-group-chat/blog/building-group-chat-zim.md

User: "给 zim-group-chat 写一篇中文博客，用老张的人设"
→ Analyzes examples/zim-group-chat/
→ Loads references/personas-zh/lao-zhang.md (only that one file)
→ Loads references/blog-structure.md
→ Generates Chinese blog
→ Output: examples/zim-group-chat/blog/使用ZIM构建群聊应用.md
```
