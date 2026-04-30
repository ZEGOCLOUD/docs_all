# Blog Structure & Quality Guidelines

## SEO Content Structure Template

All blogs MUST follow this exact four-section structure. No additional top-level sections are permitted.

```plaintext
Introduction（40–60 words, no H2 heading）

H2: How to Build XXX (Step-by-Step Guide)
  [Transition paragraph: 1–2 sentences between H2 and first H3]
  H3: Architecture Overview  (Mermaid diagrams: architecture + sequence)
  H3: Preparation  (bullet list format)
  H3: Step 1: XXX  (What + Why + Code, 40–80 words for What+Why)
  H3: Step 2: XXX
  ...

H2: Conclusion（40–60 words, single paragraph）

H2: FAQ
  Q: ...
  A: ...（exactly 2 sentences per answer）
```

Do NOT introduce additional H2 sections. The Architecture Overview H3 comes before Preparation to give readers a system-level understanding before diving into setup. Screenshots and troubleshooting content are embedded within the step H3 sections where relevant.

---

## Required Blog Sections

### 1. Introduction (No H2 Heading)

- Located at the article opening with NO H2 heading — it appears before any heading
- Immediately followed by the main tutorial H2, with no extra description between them
- **Single natural paragraph**, 40–60 words
- Contains core keyword 1–2 times
- Must include:
  - A topic definition
  - A brief statement of what problem the article solves or what content it provides
- Do NOT mention the brand name here. Follow: Problem → Architecture → SDK Introduction → Implementation

### 2. Main Tutorial (Single H2)

All implementation content lives under one H2 heading: **"How to Build XXX (Step-by-Step Guide)"**

The H2 title must include target keywords (e.g., "How to Build a Real-Time Group Chat App with ZIM SDK (Step-by-Step Guide)").

**H2 → First H3 Transition:** Between the tutorial H2 heading and the Architecture Overview H3, include a brief 1–2 sentence paragraph that summarizes the project's tech stack or core approach. This provides a smooth transition instead of jumping directly from the heading into diagrams. Do NOT skip this transition.

**Example:**
```markdown
## How to Build a Real-Time Group Chat App with ZIM SDK (Step-by-Step Guide)

The project uses a single-file Next.js architecture where `page.jsx` holds all client logic and an API route handles token generation. Below is the system layout before diving into the implementation steps.

### Architecture Overview
```

#### H3: Architecture Overview
- Placed as the **first H3** under the tutorial H2, before Preparation
- Contains at minimum one Mermaid architecture diagram and one sequence diagram
- Gives readers a system-level understanding before diving into implementation
- Use `sequenceDiagram` for message flows, `graph TB` for system overview, `flowchart TD` for user flows
- **Mermaid label syntax**: Do NOT use ordered list (`1. text`) or unordered list (`- text`) syntax in Mermaid labels or `Note` blocks. Use parenthesized numbers: `(1) text`, `(2) text`.

#### H3: Preparation
- Presented in **bullet list format** (not prose paragraphs)
- Required knowledge level, environment setup (Node.js version, package versions)
- Account setup (ZEGO Console, AppID, ServerSecret)
- Project initialization commands (copy-paste ready)
- Include `.env.example` here

#### H3: Step N: XXX (Each Step)

Each step MUST contain three elements in this order:

1. **What** — One sentence stating what this step does
2. **Why** — One sentence explaining why this matters
3. **Code** — A code snippet extracted from the actual example code

**Length rule:** What + Why combined = 40–80 words. Each step must include a brief explanation alongside the code — never present code without explanation.

**Example structure:**
```markdown
### Step 3: Initialize the ZIM SDK and Log In

The ZIM SDK instance is created with the AppID from the ZEGOCLOUD console, establishing the connection between the client and the messaging service. This initialization is required before any messaging operations can proceed, as it registers the user session with the server and prepares the event listeners for incoming messages.

\`\`\`javascript
const zim = ZIM.create({ appID: APP_ID });
await zim.login({ userID: 'user_123', userName: 'User 123' }, token);
\`\`\`
```

Typical step order: Token generation → SDK init & login → Group creation → Message send/receive → Conversation list → History messages → Member management

**Mermaid diagrams**: At minimum one sequence diagram + one architecture diagram, embedded within relevant steps.
- Use `sequenceDiagram` for message flows, `graph TB` for system overview, `flowchart TD` for user flows
- **Mermaid label syntax**: Do NOT use ordered list (`1. text`) or unordered list (`- text`) syntax in Mermaid labels or `Note` blocks. Use parenthesized numbers: `(1) text`, `(2) text`.

**Screenshots**: Capture at key interaction points and embed within relevant steps. Reference format:
```markdown
![Login page with user ID input](./assets/login-page.png)
*The login screen presents a minimal interface where users enter a unique ID to join the chat system*
```

**Troubleshooting**: Embed a troubleshooting table within the relevant step or at the end of the steps section (still under the same H2).

### 3. Conclusion

- H2 heading: "Conclusion"
- **Single natural paragraph**, 40–60 words
- Contains core keyword 1–2 times
- Must include:
  - A summary of the topic
  - Emphasis on value or application scenarios
- Do NOT use generic AI closing phrases ("Happy coding!", "We hope this guide helps")
- Do NOT introduce new technical information
- Naturally guide readers to the next action (try the SDK, read documentation, explore advanced features)

**Example structure:** "[Recap what was built] → [Why this approach matters] → [Suggest next step with natural link to docs or advanced topics]"

Reference: https://www.zegocloud.com/blog/audio-moderation (see conclusion section)

### 4. FAQ

- Located after Conclusion
- H2 heading: "FAQ"
- Contains 3–5 questions
- Each question prefixed with "Q:" (e.g., `### Q: What is the ZIM SDK?`)
- Questions must be **search-type questions** — the kind developers actually search for on Reddit, Quora, Dev.to, Stack Overflow
- Question types: How (implementation), What (definition), Cost/Time, Tech Stack
- Target audience: developers, product managers, entrepreneurs
- Each answer: **exactly 2 sentences** as a single paragraph (no lists, no bullet points, no 3-sentence answers)
- Answers should be concise, direct, and self-contained. Each answer must be completable in 2 sentences — cut any third sentence.

**Example:**
```markdown
### Q: What is the ZIM SDK?

The ZIM SDK is a real-time messaging SDK provided by ZEGOCLOUD that handles message delivery, group management, and conversation persistence across platforms. It supports one-on-one chat, group chat, and room messaging with delivery confirmation and offline message storage, making it suitable for building chat features without managing backend infrastructure.
```

Reference: https://www.zegocloud.com/blog/healthcare-api (see FAQ section)

---

## Professional Writing Standards

Apply regardless of persona. Persona defines *voice*; these define *quality*.

### Expression Quality & Paragraph Coherence (HIGHEST PRIORITY)

These rules override persona voice characteristics when they conflict. Every sentence must be complete, informative, and suitable for an international technical audience.

**1. No caption-style fragments:**
Avoid disjointed noun phrases, telegraphic shorthand, or remark-style expressions. Every sentence must stand on its own with a subject and verb.

| Bad (caption/fragment) | Good (complete sentence) |
|------------------------|--------------------------|
| "The login interface — simple and functional." | "The login interface is designed to be simple and functional, allowing users to quickly enter their credentials and access the chat system without unnecessary steps." |
| "Token generation — the backbone." | "Token generation serves as the backbone of the authentication flow, ensuring that every client connection is verified before accessing messaging resources." |

**2. No instructional/colloquial tone:**
Avoid "Let's", "Now", "Just", "You can" constructions. These read like a tutorial transcript, not a professional article. Write in descriptive, professional prose.

| Bad (instructional) | Good (professional) |
|---------------------|---------------------|
| "Let's scaffold the project." | "The first step is to scaffold the project and install the required dependencies." |
| "Now we need to handle the token." | "The next consideration is token handling, which secures every client connection." |
| "You can see the results below." | "The results demonstrate how the SDK handles message delivery under concurrent conditions." |
| "Just add this to your config." | "Adding this configuration entry enables the SDK to reconnect automatically." |

**3. Sentence variety:**
Avoid consecutive sentences starting with the same pattern (e.g., multiple "The..." sentences in a row). Merge related ideas using subordinate clauses and logical connectors. Vary subjects: Developers / The SDK / This step / The configuration.

Bad: "The browser runs the React UI and ZIM SDK client. The Next.js API route handles token generation server-side, keeping the ServerSecret out of the browser. The ZIM server manages message routing, group state, and persistence."

Good: "The browser is responsible for rendering the React UI and initializing the ZIM SDK client, while the Next.js API route securely handles token generation on the server. Meanwhile, the ZIM server manages message routing, group state, and persistence."

**4. Paragraph coherence:**
Each paragraph must have:
- A main sentence establishing the topic
- Supporting sentences that expand, illustrate, or qualify the main point
- Logical connectors between ideas (while, meanwhile, which, so, therefore, however, as a result)
- No more than 2 consecutive short sentences without a connector

Bad: "Tokens are the gatekeeper. The client requests one from our API route. It passes the token to the ZIM SDK during login. The token uses AES-256-CBC encryption with the ServerSecret."

Good: "Tokens serve as the authentication gatekeeper for the entire system, ensuring that only verified clients can send and receive messages. The client requests a token from the API route, which generates it using AES-256-CBC encryption with the ServerSecret before passing it to the ZIM SDK during the login process."

### Sentence & Style Rules

- **Sentence length**: Under 20 words average. Split any sentence over 25 words. No sentence may exceed 30 words.
- **Dashes**: Do NOT use em dashes (`—`) anywhere in the article. They look unprofessional in technical writing. Rewrite using commas, periods, parentheses, or colon instead. Zero em dashes is the target.
- **First person**: Minimize ("I think" → "This is a critical consideration"; "I should mention" → "Note that"). Acceptable in 1-2 anecdotes per article.
- **Colloquialisms**: Avoid filler ("shall we say", "I'll grant you", "if I'm honest"). Persona quirks (e.g., "rather") max 1-2 times per article. Also avoid "frankly", "I think", "I'd recommend" — these undermine professional authority.
- **Transitions**: Use at least one per paragraph in implementation sections (Therefore, In addition, For example, However, First/Next/Then/Finally).

### Passive Voice Control

- Passive voice must not exceed **10%** of all sentences
- Prefer active constructions:
  - "Developers use..." (not "...is used by developers")
  - "This step does..." (not "...is done in this step")
  - "The SDK handles..." (not "...is handled by the SDK")
  - "The configuration enables..." (not "...is enabled by the configuration")

### Word Complexity

Prefer simple, direct verbs over complex alternatives:

| Prefer | Avoid |
|--------|-------|
| use | utilize |
| build | implement |
| help | facilitate |
| start | commence |
| show | demonstrate (when "show" works) |
| try | endeavor |

### Data-Driven Expression

Back technical claims with data. Use realistic estimates when exact data is unavailable.

| Weak | Strong |
|------|--------|
| "Messages arrive quickly" | "Average delivery latency is under 100ms within the same region" |
| "The SDK is lightweight" | "The ZIM Web SDK is ~200KB gzipped with zero external dependencies" |
| "The token system is secure" | "Tokens use AES-256-CBC encryption with a configurable expiry (default: 3600s)" |

---

## SEO Rules

### H2 Headings
Every H2 must include a target keyword or long-tail phrase. Replace generic labels:

| Weak | Strong |
|------|--------|
| Architecture | Real-Time Group Chat Architecture with ZIM SDK |
| Setup | Setting Up the Next.js Group Chat Project |
| Sending Messages | Sending and Receiving Group Chat Messages in Real-Time |

Note: The SEO structure template only has 3 H2s (main tutorial, conclusion, FAQ), so keyword optimization focuses on the main tutorial H2 title.

### Readability Structure
- Numbered lists for sequential operations
- Tables for comparisons and troubleshooting
- Blockquotes (`>`) for warnings and tips
- Inline code for all API names and parameters
- Alt text on every image

---

## Brand Name Placement

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

## Code Snippet Guidelines

1. **Include imports** — never show a bare function call
2. **Real API signatures** — match the actual SDK version
3. **Show error handling** — wrap async calls in try/catch
4. **Include `.env.example`** in the Preparation section
5. **Note SDK version** used

Don't show pseudo-code, don't omit error handling "for brevity", don't show full files when a section suffices (use `// ... existing code ...`).

---

## Anti-AI-Writing Patterns

**Banned phrases**: "In today's fast-paced digital world", "Let's dive in", "Whether you're a beginner or an experienced developer", "As we can see", "Seamless integration", "Robust solution", "Cutting-edge", "Game-changer", "Empower/empowering", "Happy coding!"

**Banned structures**: Summary paragraph at end of every section, "In this article, we will cover..." opening, every paragraph exactly 3-4 sentences, excessive "However/Moreover/Furthermore".

**Do**: Vary paragraph length (1-8 sentences), use contractions, include specific version numbers and dates.

---

## Content Prohibitions

The following are explicitly forbidden in all blog content:

| Prohibition | Why |
|-------------|-----|
| Em dashes (`—`) | Looks unprofessional in technical writing; use commas, periods, or parentheses instead |
| Dividers (`---` or `——`) | Breaks visual flow and adds no value |
| Step sections with only code (no explanation) | Every step must have What + Why alongside code |
| Multiple H2s scattering the tutorial structure | All steps must be under a single H2 |
| Sentences exceeding 30 words | Damages readability and comprehension |
| Overly colloquial expressions ("frankly", "I think", "I'd recommend") | Undermines professional authority |

---

## Quality Checklist

- [ ] **Structure follows the SEO template exactly**: Introduction (no H2) → single H2 (transition paragraph → Architecture Overview → Preparation → Steps) → Conclusion → FAQ
- [ ] Introduction: 40–60 words, single paragraph, core keyword 1–2 times, no H2 heading
- [ ] H2 → H3 transition: A brief 1–2 sentence paragraph between the tutorial H2 heading and the Architecture Overview H3, providing a smooth transition. Do NOT jump directly from H2 to H3.
- [ ] Architecture Overview: first H3 under tutorial H2, contains Mermaid diagrams
- [ ] Preparation: bullet list format, not prose paragraphs
- [ ] All steps under one H2 with keyword-rich title; each step has What + Why + Code (40–80 words for What+Why)
- [ ] Conclusion: 40–60 words, single paragraph, core keyword 1–2 times
- [ ] FAQ: 3–5 search-type questions with "Q:" prefix, answers as exactly 2-sentence paragraphs (no 3-sentence answers)
- [ ] At least one Mermaid sequence + one architecture diagram
- [ ] Code snippets have imports, error handling, real API signatures
- [ ] `.env.example` included in Preparation; SDK version noted
- [ ] Implementation uses numbered step-by-step format (H3 steps)
- [ ] H2 headings include target keywords
- [ ] Average sentence length under 20 words; no sentence over 30 words; max 2 em dashes total
- [ ] Passive voice ≤ 10%; prefer active constructions
- [ ] Simple verbs preferred (use/build/help over utilize/implement/facilitate)
- [ ] Technical claims backed with data
- [ ] No banned AI phrases; no colloquial filler; no overly colloquial expressions
- [ ] No caption-style fragments or instructional tone (Let's, Now, Just, You can)
- [ ] No consecutive sentences starting with the same pattern; ideas merged with connectors
- [ ] Paragraphs have main sentence + supporting sentences with logical connectors
- [ ] Screenshots included for UI features; captions are complete sentences (not fragments)
- [ ] Troubleshooting content embedded within steps section
- [ ] Brand names and links match target language
- [ ] No dividers, no em dashes (`—`), no code-only steps, no extra H2s beyond the template
- [ ] Length appropriate (3000-6000 words EN / 4000-8000 chars ZH)

---

## ZEGO Brand & Link Reference

| | English | Chinese |
|---|---------|---------|
| Brand | ZEGOCLOUD | ZEGO / 即构科技 |
| Site | https://www.zegocloud.com/ | https://www.zego.im/ |
| Docs | https://www.zegocloud.com/docs | https://doc-zh.zego.im/ |
| Console | https://console.zegocloud.com/ | https://console.zego.im/ |
