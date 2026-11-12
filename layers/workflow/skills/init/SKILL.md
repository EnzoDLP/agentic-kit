---
name: workflow-init
description: Finish setting up a repository that holds the kit at .claude/agentic-kit — detect its stack and link the matching technology layers, write or merge AGENTS.md / CLAUDE.md with only what is specific to the project, and offer OpenSpec with the kit's rules. Use right after the kit was added to a project, when the user asks to "set up the kit", "set up Claude" or "bootstrap the context", or when a process skill finds a project with none of this.
---

# Set up a repository

Nothing here is written, linked or committed without the user's yes. The skill reads, then
proposes one batch of changes, then applies what was accepted.

## 1. Read before proposing

`package.json` (or the language's manifest), lockfile, bundler / framework config, `tsconfig`,
directory tree, `README`, `docs/`, CI config, and any `AGENTS.md`, `CLAUDE.md`, `.claude/`,
`openspec/` already there. Note the real test, lint, typecheck, format and build commands.

## 2. Shared or local

The way the kit was added tells it: `.claude/agentic-kit` listed in `.gitmodules` is **shared**
(committed with the repository); a plain clone listed in the repository's exclude file is
**local** (kept on this machine: a team that has not agreed to it, a client's repository). If
neither holds, ask. The answer decides every write below.

- **Shared**: `.claude/settings.json`, the links under `.claude/`, `AGENTS.md` / `CLAUDE.md`,
  `openspec/` and the project records under `docs/` are committed like any other file.
- **Local**: `.claude/settings.local.json` and `CLAUDE.local.md` instead. Every path the kit
  writes is excluded from git (`link.py --local` does it for its own links): also
  `CLAUDE.local.md`, `openspec/`, `.agents/`, `.claude/skills/openspec-*`, `docs/adr/`,
  `docs/GOTCHAS.md`, `docs/ROADMAP.md`. They go into the repository's exclude file
  (`git rev-parse --git-path info/exclude`, which also resolves inside a worktree), never into
  `.gitignore`.

## 3. Technology layers

| The repository has | Layers |
| --- | --- |
| TypeScript | `typescript` |
| React | `react` (+ `typescript`) |
| Expo / React Native | `expo` (+ `react`, `typescript`) |
| A React web app (Vite, Next.js, …) | `react-web` (+ `react`, `typescript`) |
| Supabase (`supabase/` folder, `@supabase/supabase-js`) | `supabase` |

Propose the list, then link it from the repository root. The command takes the whole selection
each time, brings the required layers, and keeps the mode the kit was linked with (`--local`
only if it never was):

```
python3 .claude/agentic-kit/scripts/link.py expo supabase
```

It links each layer's rules (`.claude/rules/kit-<layer>`), skills (`.claude/skills/<layer>-*`)
and agents, and merges the layers' permission rules (pushes, remote databases, store builds and
production deploys ask first; edits to installed dependencies and generated files are refused)
into the settings file. The project's own rules in that file are kept. Changes apply from the
next session.

## 4. AGENTS.md and CLAUDE.md

- **Local** (step 2): everything below goes into `CLAUDE.local.md`. The committed `AGENTS.md` /
  `CLAUDE.md` are read, never edited.
- Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists. A repository that needs both
  keeps the content in `AGENTS.md` (read by every agent tool) and a `CLAUDE.md` that holds
  `@AGENTS.md` plus anything Claude-specific.
- Content: commands (exact, with flags), structure, the project's own conventions and domain, its
  traps, and its **deliberate departures** from a kit rule ("Departure from the kit's rule X:
  … because …"). Never restate a rule a linked layer already holds.
- An existing file is never overwritten: read it, propose a merge, the user arbitrates. Target
  about 150 lines; report the count (`wc -l`).

## 5. OpenSpec

Read `.claude/agentic-kit/layers/workflow/reference/openspec.md`. If the repository has no
`openspec/`, offer it in one line (what it adds: specs agreed before code, one folder per change,
archived into a living spec). On a yes:

```
npx @fission-ai/openspec@2 init --tools claude
```

(add the team's other tools to `--tools`). Then offer to merge
`.claude/agentic-kit/layers/workflow/reference/openspec-config.yaml` into `openspec/config.yaml`,
beside any rule already present, and to set its `context:` from what step 1 found (stack, test
framework, conventions file). On a no, the process skills still work: specs are then agreed in
the conversation.

## 6. Project records

Create nothing empty: `docs/adr/`, `docs/GOTCHAS.md` and `docs/ROADMAP.md` are created by their
first entry.

## 7. Report

What was written and linked (and that it applies from the next session), and separately what
could not be established and what needs a human — anything written from inference rather than
evidence included. That list is an expected output, not a failure.
