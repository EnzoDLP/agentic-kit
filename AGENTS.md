# Agentic Kit — how this repository is written

What the kit does is in [`README.md`](README.md). This file holds how it is built and the rules
every contribution follows.

## Layout

```
layers/<layer>/
  rules/*.md                  always loaded in a project that links the layer
  gotchas/*.md                pitfalls, never loaded: read on demand
  skills/<skill>/SKILL.md     loaded on demand from their description
  agents/*.md                 subagents (workflow only)
  reference/                  files a skill reads at runtime
  eslint/<layer>.cjs          the lint-checkable part of the rules (typescript-eslint-preset)
  permissions.json            guards: ask / deny permission rules merged by link.py
  requires                    layers this one needs, one per line
scripts/link.py               links layers into a project (run from the project)
scripts/check.sh              maintainer check: names, references, sizes, sensitive content
```

A project holds the kit at `.claude/agentic-kit` and runs `scripts/link.py`, which links each
layer's rules to `.claude/rules/kit-<layer>`, each skill to `.claude/skills/<layer>-<skill>`, each
agent to `.claude/agents/`, and merges `permissions.json` into the project's settings.

Two families of layers, and the boundary is the point of the kit:

- **`workflow`** is the process: how a change is decided, specified, built and reviewed. It
  names no technology. It delegates feature specs to
  [OpenSpec](https://github.com/Fission-AI/OpenSpec) and owns what OpenSpec has no place for:
  decision records, the test-first build loop, the review, pitfalls, the working rules.
- **Technology layers** (`typescript`, `react`, `expo`, `react-web`, `supabase`) are knowledge:
  what is true of a stack. They never mention the process. The process consumes them: the build
  and the review read the linked rules.

## Where a new piece of knowledge goes

1. True in any project, whatever the language (a way of working) → `workflow/rules/`. It is loaded
   everywhere: keep it short.
2. True for a whole technology → that layer's `rules/`. A real difference between two
   technologies goes into each one, never into a shared layer.
3. A pitfall ("X fails because Y") → that layer's `gotchas/`. The rule it implies, if any, goes
   into `rules/`.
4. Know-how on a topic touched now and then (an SDK, a service, a multi-step procedure) → a skill.
5. A command that must always ask first, or never run → that layer's `permissions.json`. A file
   that must never be edited → one `Edit(<glob>)` deny rule, which covers every file-editing tool
   (Claude Code rejects a `Write(...)` rule as never matched).
6. Specific to one project → that project's own `CLAUDE.md`, `.claude/rules/` or
   `docs/GOTCHAS.md`. Never here.

## Writing rules

- **English, plain and short.** The rule before its reason; no narrative, no session history.
- **Nothing from a real project.** No product, client, employer or person name, no absolute
  path, no account id, no domain, no date recording when or where a lesson was learned. Versions
  stay: they are the fact. Examples are invented. `scripts/check.sh` scans for the obvious cases;
  the rest is the reviewer's job.
- **Only verified, durable knowledge.** A guess is not a rule; a lesson that no longer holds is
  deleted, not kept as history.
- **A rules file stays under 9,000 characters** (`wc -c`) and carries no frontmatter: it is
  always loaded, so its size is paid in every session of every project that links its layer.
- **Kit files are named by their path in a project**: `.claude/agentic-kit/layers/<layer>/...`,
  which `scripts/check.sh` resolves against this repository. A skill is named `<layer>-<skill>`
  (the `name:` of its `SKILL.md` matches the link `link.py` creates), and another layer's skill by
  that name (`supabase-rpc`).
- **Cost in context.** A skill's description is paid for always, its body only when used.
- Markdown wrapped at 100 columns (`.prettierrc`).

## Commands

```
sh scripts/check.sh
```

Run before committing. To try a change in a throwaway repository:

```
git init demo && cd demo
git -c protocol.file.allow=always submodule add <path to this checkout> .claude/agentic-kit
python3 .claude/agentic-kit/scripts/link.py expo
```

A submodule takes the committed state: commit first, or copy the working tree over
`.claude/agentic-kit` while iterating.

## Versioning

The kit is versioned as a whole: note each change that alters behavior in
[`CHANGELOG.md`](CHANGELOG.md) and tag releases (`v0.1.0`). Projects pin a commit through their
submodule.
