---
name: write-blog
description: >
  This skill should be used when the user asks to "write a blog", "generate a blog article",
  "create a tutorial blog", "write a technical blog post", "generate blog content from example code",
  "write a blog about this project", or mentions blog writing with personas. Generates high-quality,
  persona-driven technical blog articles based on ZEGO example code projects.
version: 0.2.0
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
- **SEO content structure template** (mandatory four-section format)
- Required blog sections and their exact order
- Step format rules (What + Why + Code, 40–80 words for What+Why)
- Passive voice limits (≤10%) and simple verb preferences
- Code snippet precision rules
- Mermaid diagram guidelines (sequence, architecture, flowchart)
- Anti-AI-writing patterns (banned phrases and structures)
- Content prohibitions (no dividers, no code-only steps, no extra H2s)
- Screenshot integration guidelines
- Quality checklist

### Step 5: Capture Screenshots (MANDATORY — Do Not Skip)

Screenshots are **required** for the blog to be valid. A blog without screenshots is incomplete and should not be considered finished.

**Generate a `capture-screenshots.sh` script, then execute it step by step via the Skill tool. Do NOT use `mcp__chrome-devtools__take_screenshot` or any other MCP tool directly.**

Steps:

1. Start the application (e.g., `npm run dev` for web projects)
2. Determine the platform and select the matching screenshot template:
   - **Web apps** → `references/screenshot-templates/web.md` (uses `@zegocloud/auto-web`, Skill: `zego-browser-automation`)
   - **Android apps** → `references/screenshot-templates/android.md` (uses `@midscene/android@1`, Skill: `android-device-automation`)
   - **iOS apps** → `references/screenshot-templates/ios.md` (uses `@midscene/ios@1`, Skill: `ios-device-automation`)
   - **HarmonyOS apps** → `references/screenshot-templates/harmonyos.md` (uses `@midscene/harmony@1`, Skill: `harmonyos-device-automation`)
   - **Desktop apps** → `references/screenshot-templates/desktop.md` (uses `@midscene/computer@1`, Skill: `desktop-computer-automation`)
3. Read the selected template file for the script skeleton.
4. Generate a `capture-screenshots.sh` script based on the template. For each key screen identified in Step 2's source analysis, fill in:
   - A `screenshot` call with a descriptive filename (e.g., `login-page.png`, `conversation-list.png`)
   - An `act` call before it with a **self-contained prompt** that describes exactly what to do to reach that screen from the previous state. Do not assume prior context; each prompt must work independently.
   - A `sleep` between navigation and capture (2–5 seconds depending on the expected transition time)
   - For multi-user scenarios (chat, calling), use the multi-tab/multi-device variant from the template
5. Write the script to `<project-path>/blog/assets/capture-screenshots.sh`
6. Execute the script by running each `act`/`screenshot` command **one at a time** through the Skill tool. Run each command synchronously and read its output before proceeding to the next. This ensures you can verify each screenshot and recover from errors.
7. Save all captured screenshots to `<project-path>/blog/assets/`

**Example generated script (web app):**
```bash
#!/bin/bash
# capture-screenshots.sh for zim-group-chat
set +e
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true

TAB_MAIN="main"
URL="http://localhost:3000"
ASSET_DIR="blog/assets"

act() {
  local tab="$1"
  local prompt="$2"
  npx -y @zegocloud/auto-web act --tab "$tab" --prompt "$prompt" 2>&1
}

screenshot() {
  local tab="$1"
  local filename="$2"
  local tmp_path
  tmp_path=$(npx -y @zegocloud/auto-web take_screenshot --tab "$tab" 2>&1 | grep "Screenshot saved:" | awk '{print $NF}')
  if [ -n "$tmp_path" ] && [ -f "$tmp_path" ]; then
    cp "$tmp_path" "$ASSET_DIR/$filename"
    echo "Captured: $ASSET_DIR/$filename"
  else
    echo "WARNING: Failed to capture $filename"
  fi
}

mkdir -p "$ASSET_DIR"
npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB_MAIN"
sleep 3

# Screenshot 1: Login page
screenshot "$TAB_MAIN" "login-page.png"

# Screenshot 2: Conversation list (after login)
act "$TAB_MAIN" "Enter the UserID 'testuser1' in the User ID field and click the Login button. Wait for the conversation list to appear."
sleep 3
screenshot "$TAB_MAIN" "conversation-list.png"

# Screenshot 3: Chat view (after entering a conversation)
act "$TAB_MAIN" "Click on the first conversation in the list to open the chat view."
sleep 2
screenshot "$TAB_MAIN" "chat-view.png"

npx -y @zegocloud/auto-web disconnect 2>/dev/null || true
```

### Step 6: Generate the Blog

Write the blog following the **SEO structure template** from `references/blog-structure.md`. The structure is mandatory — do not deviate.

**Mandatory Structure:**
```
Introduction (no H2, 40–60 words, single paragraph)

## How to Build XXX (Step-by-Step Guide)
Brief transition paragraph (1–2 sentences) between H2 and first H3, summarizing the project's tech stack or core approach.
### Architecture Overview (Mermaid diagrams)
### Preparation (bullet list format)
### Step 1: XXX (What + Why + Code)
### Step 2: XXX (What + Why + Code)
...

## Conclusion (40–60 words, single paragraph)

## FAQ
### Q: ...
### Q: ...
```

**Pre-Generation Checklist (MANDATORY):**

Before writing any blog content, output the following checklist and confirm each rule. This step is not optional — it forces awareness of critical constraints that are easy to lose during long-form generation.

```
Critical Rules Checklist:
- [ ] Structure: Introduction (no H2) → Single H2 (Architecture Overview → Preparation → Steps) → Conclusion → FAQ. NO extra H2s.
- [ ] Introduction: 40–60 words, single paragraph, core keyword 1–2 times, no brand name
- [ ] H2 → H3 transition: A brief 1–2 sentence paragraph between the tutorial H2 heading and the Architecture Overview H3, providing a smooth transition (e.g., summarizing the tech stack or core approach). Do NOT jump directly from H2 to H3.
- [ ] Architecture Overview: first H3 under tutorial H2, with Mermaid diagrams before any steps
- [ ] Preparation: bullet list format (not prose), includes .env.example and SDK version
- [ ] Steps: Each step has What + Why + Code. What+Why = 40–80 words.
- [ ] Conclusion: 40–60 words, single paragraph, core keyword 1–2 times
- [ ] FAQ: 3–5 search-type questions with "Q:" prefix, answers as exactly 2-sentence paragraphs (no lists, no 3-sentence answers)
- [ ] Brand name: English = "ZEGOCLOUD" (NOT "ZEGO"), Chinese = "ZEGO" or "即构科技"
- [ ] Brand placement: Do NOT appear in the opening hook (first 2-3 paragraphs). Introduce naturally after the problem/context.
- [ ] Sentence length: Average under 20 words. No sentence over 30 words. Split any sentence over 25 words.
- [ ] Passive voice: ≤10%. Prefer active (Developers use / This step does / The SDK handles).
- [ ] Simple verbs: use (not utilize), build (not implement), help (not facilitate).
- [ ] Expression quality: No caption-style fragments, no instructional tone (Let's, Now, Just, You can). Every sentence is complete and informative.
- [ ] Sentence variety: No consecutive same-pattern starts. Merge ideas with subordinate clauses and connectors.
- [ ] Paragraph coherence: Main sentence + supporting sentences with logical connectors (while, meanwhile, which, so).
- [ ] Em dashes: Do NOT use em dashes (`—`) anywhere. Rewrite with commas, periods, or parentheses. Zero em dashes.
- [ ] Data-backed claims: Latency, size, limits — no vague adjectives.
- [ ] No banned AI phrases (see blog-structure.md).
- [ ] No dividers, no code-only steps, no overly colloquial expressions (frankly, I think, I'd recommend).
```

**Content Generation Rules:**
1. **Structure (HIGHEST PRIORITY):** Follow the SEO content structure template exactly. All implementation content goes under one H2. No additional H2s beyond the three required (main tutorial, conclusion, FAQ). See `references/blog-structure.md` "SEO Content Structure Template" section.
2. **Brand name and placement:** In English blogs, always use "ZEGOCLOUD" — never "ZEGO" as shorthand. In Chinese blogs, use "ZEGO" or "即构科技". The brand must NOT appear in the opening hook (first 2-3 paragraphs). Follow the structure: Problem → Architecture → SDK Introduction → Implementation.
3. Write in the selected persona's voice, but follow the Professional Writing Standards in `references/blog-structure.md` (sentence length, dash limits, data-driven claims, objective tone)
4. Every code snippet must be extracted from the actual example code — not invented
5. Include at least one Mermaid sequence diagram and one architecture diagram (within the steps section)
6. Explain WHY behind design decisions, not just WHAT the code does
7. Include error handling and edge cases in code examples
8. Add troubleshooting content within the steps section (under the same H2)
9. Include `.env.example` or environment configuration in the Preparation section
10. H2 headings must include target keywords (not generic labels like "Setup" or "Implementation")
11. Include an FAQ section with 3–5 entries. Each question must use "Q:" prefix. Questions must be search-type (Reddit, Quora, Dev.to, Stack Overflow style). Answers must be exactly 2 sentences per question — concise, direct, and self-contained. No lists, no bullet points, no 3-sentence answers.
12. Use numbered step-by-step format for all implementation sections (H3 steps under single H2)
13. Back technical claims with data (latency, size, limits, throughput)
14. **Expression quality:** No caption-style fragments or telegraphic shorthand. No instructional tone (avoid "Let's", "Now", "Just", "You can"). Every sentence must be complete and informative.
15. **Sentence variety:** Avoid consecutive sentences starting with the same pattern (e.g., multiple "The..." openings). Merge related ideas using subordinate clauses and logical connectors (while, meanwhile, which, so).
16. **Paragraph coherence:** Each paragraph must have a main sentence with supporting sentences connected by logical connectors. No more than 2 consecutive short sentences without a connector.
17. **Conclusion:** Must be an independent natural paragraph of 40–60 words that summarizes the article's core value and naturally guides readers to the next action. Do NOT use generic AI closing phrases.
18. **Passive voice:** Keep under 10%. Prefer active constructions (Developers use / This step does / The SDK handles).
19. **Simple verbs:** Prefer use over utilize, build over implement, help over facilitate.
20. **Prohibitions:** No dividers (`---` or `——`). No em dashes (`—`) anywhere in the article. No step sections with only code. No sentences over 30 words. No overly colloquial expressions ("frankly", "I think", "I'd recommend").

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
- **`references/blog-structure.md`** — SEO content structure template, blog section rules, code guidelines, Mermaid patterns, anti-AI-writing rules, readability rules, content prohibitions, and quality checklist
- **`references/screenshot-templates/`** — Platform-specific script skeletons for generating `capture-screenshots.sh`
  - `web.md` — Browser apps via `@zegocloud/auto-web` (single-tab + multi-tab)
  - `android.md` — Android via `@midscene/android@1` (single-device + multi-device)
  - `ios.md` — iOS via `@midscene/ios@1`
  - `harmonyos.md` — HarmonyOS via `@midscene/harmony@1`
  - `desktop.md` — Desktop via `@midscene/computer@1`

### Device Automation Skills (for Screenshot Execution)

These project skills execute the commands from `capture-screenshots.sh`. **Always invoke them through the Skill tool — never use MCP tools directly for screenshots.**
- `zego-browser-automation` — Web app testing via headless Chrome (use for Next.js, React, and other web projects)
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
→ Generates blog following SEO structure template
→ Output: examples/zim-group-chat/blog/building-group-chat-zim.md

User: "给 zim-group-chat 写一篇中文博客，用老张的人设"
→ Analyzes examples/zim-group-chat/
→ Loads references/personas-zh/lao-zhang.md (only that one file)
→ Loads references/blog-structure.md
→ Generates Chinese blog following SEO structure template
→ Output: examples/zim-group-chat/blog/使用ZIM构建群聊应用.md
```
