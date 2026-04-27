# Blog Structure & Quality Guidelines

## Required Blog Sections

### 1. Title & Hook
- Title: Specific, benefit-driven, includes technology name. Prefer "Building Real-Time Group Chat with ZEGO ZIM: A Complete Guide for React Developers"
- Hook (first 2-3 paragraphs): Start with the **problem** and technical challenges. Do NOT mention the brand name prominently here. Build credibility first, introduce the SDK naturally in section 2-3.

### 2. Prerequisites & Setup
- Required knowledge level, environment setup (Node.js version, package versions)
- Account setup (ZEGO Console, AppID, ServerSecret)
- Project initialization commands (copy-paste ready)

### 3. Architecture Overview
- **Mermaid diagrams**: At minimum one sequence diagram + one architecture diagram
- Brief explanation of key components and design rationale
- Use `sequenceDiagram` for message flows, `graph TB` for system overview, `flowchart TD` for user flows
- **Mermaid label syntax**: Do NOT use ordered list (`1. text`) or unordered list (`- text`) syntax in Mermaid labels or `Note` blocks. These break rendering. Use parenthesized numbers instead: `(1) text`, `(2) text`. Examples:
  - Bad: `Note over A,B: Phase 1:\n1. Get token\n2. Login`
  - Good: `Note over A,B: (1) Get token, (2) Login`
  - Bad: `A["/api/token\n- Token04 Generation"]`
  - Good: `A["/api/token\nToken04 Generation"]`

### 4. Implementation Steps (Step-by-Step Format)
Use numbered steps. Each step has: a **bold step label**, a 1-2 sentence objective, a code block, and a concise explanation of non-obvious decisions.

Typical order: Token generation → SDK init & login → Group creation → Message send/receive → Conversation list → History messages → Member management

### 5. Running & Testing
- How to start the app, expected behavior, troubleshooting table

### 6. FAQ (Required)
3-5 entries as `###` headings, targeting core keywords. Cover: What is... / How do I... / Comparison / Pricing / Troubleshooting.

### 7. Conclusion & Next Steps
- Summary, 2-3 concrete next steps, link to docs

---

## Professional Writing Standards

Apply regardless of persona. Persona defines *voice*; these define *quality*.

### Sentence & Style Rules
- **Sentence length**: Under 20 words average. Split any sentence over 25 words.
- **Dashes**: Em dashes (`—`) max 2 per article. Use periods or commas instead.
- **First person**: Minimize ("I think" → "This is a critical consideration"; "I should mention" → "Note that"). Acceptable in 1-2 anecdotes per article.
- **Colloquialisms**: Avoid filler ("shall we say", "I'll grant you", "if I'm honest"). Persona quirks (e.g., "rather") max 1-2 times per article.
- **Transitions**: Use at least one per paragraph in implementation sections (Therefore, In addition, For example, However, First/Next/Then/Finally).

### Data-Driven Expression
Back technical claims with data. Use realistic estimates when exact data is unavailable.

| Weak | Strong |
|------|--------|
| "Messages arrive quickly" | "Average delivery latency is under 100ms within the same region" |
| "The SDK is lightweight" | "The ZIM Web SDK is ~200KB gzipped with zero external dependencies" |
| "The token system is secure" | "Tokens use AES-256-CBC encryption with a configurable expiry (default: 3600s)" |

### Brand Name Placement
Brand should appear naturally after the problem/context. Structure: Problem → Architecture → SDK Introduction → Implementation. Do not lead with the brand in the opening hook.

**CRITICAL: Brand name must match the target language exactly:**
- English: "ZEGOCLOUD" — never "ZEGO" as shorthand
- Chinese: "ZEGO" or "即构科技"

**Negative Examples (DO NOT do this):**

| Violation | Bad Example | Why It's Wrong |
|-----------|-------------|----------------|
| Wrong brand name | "ZEGO's ZIM SDK handles messaging" | English blog must say "ZEGOCLOUD", not "ZEGO" |
| Brand in opening hook | "I built this with ZEGOCLOUD's ZIM SDK" | Brand appears before establishing the problem |
| Brand in first paragraph | "The ZIM SDK from ZEGOCLOUD makes this easy" | Hook should focus on technical challenge, not product |

**Correct Examples:**

| Good Example | Why It Works |
|-------------|-------------|
| Hook: "Group chat gets complicated fast. Message ordering, delivery receipts, sync — each piece has edge cases." | Establishes problem first, no brand |
| Section 2: "The ZIM Web SDK from ZEGOCLOUD handles delivery, persistence, and group operations." | Brand appears naturally after context |

---

## SEO Rules

### H2 Headings
Every H2 must include a target keyword or long-tail phrase. Replace generic labels:

| Weak | Strong |
|------|--------|
| Architecture | Real-Time Group Chat Architecture with ZIM SDK |
| Setup | Setting Up the Next.js Group Chat Project |
| Sending Messages | Sending and Receiving Group Chat Messages in Real-Time |

### Readability Structure
- Numbered lists for sequential operations
- Tables for comparisons and troubleshooting
- Blockquotes (`>`) for warnings and tips
- Inline code for all API names and parameters
- Alt text on every image

---

## Code Snippet Guidelines

1. **Include imports** — never show a bare function call
2. **Real API signatures** — match the actual SDK version
3. **Show error handling** — wrap async calls in try/catch
4. **Include `.env.example`** in the setup section
5. **Note SDK version** used

Don't show pseudo-code, don't omit error handling "for brevity", don't show full files when a section suffices (use `// ... existing code ...`).

---

## Anti-AI-Writing Patterns

**Banned phrases**: "In today's fast-paced digital world", "Let's dive in", "Whether you're a beginner or an experienced developer", "As we can see", "Seamless integration", "Robust solution", "Cutting-edge", "Game-changer", "Empower/empowering", "Happy coding!"

**Banned structures**: Summary paragraph at end of every section, "In this article, we will cover..." opening, every paragraph exactly 3-4 sentences, excessive "However/Moreover/Furthermore".

**Do**: Vary paragraph length (1-8 sentences), use contractions, include specific version numbers and dates.

---

## Screenshot Integration

Capture at key points: login, conversation list, chat view with messages, member list. Place in `blog/assets/`. Reference format:

```markdown
![Login page with user ID input](./assets/login-page.png)
*The login interface — simple and functional*
```

Screenshots must show the specific feature, exclude sensitive data, and have descriptive alt text.

---

## Quality Checklist

- [ ] Title includes technology name; hook starts with problem, not brand
- [ ] At least one Mermaid sequence + one architecture diagram
- [ ] Code snippets have imports, error handling, real API signatures
- [ ] `.env.example` included; SDK version noted
- [ ] Implementation uses numbered step-by-step format
- [ ] FAQ section with 3-5 keyword-targeted entries
- [ ] H2 headings include target keywords
- [ ] Average sentence length under 20 words; max 2 em dashes total
- [ ] Technical claims backed with data
- [ ] No banned AI phrases; no colloquial filler
- [ ] Screenshots included for UI features
- [ ] Troubleshooting table covers common issues
- [ ] Brand names and links match target language (see below)
- [ ] Length appropriate (3000-6000 words EN / 4000-8000 chars ZH)

---

## ZEGO Brand & Link Reference

| | English | Chinese |
|---|---------|---------|
| Brand | ZEGOCLOUD | ZEGO / 即构科技 |
| Site | https://www.zegocloud.com/ | https://www.zego.im/ |
| Docs | https://www.zegocloud.com/docs | https://doc-zh.zego.im/ |
| Console | https://console.zegocloud.com/ | https://console.zego.im/ |
