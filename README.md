# Agentic Kit

A shared context for coding agents (Claude Code), added to a project as a git submodule. It is
made of two families of layers, and the line between them is the point of the kit:

- **`workflow`, the process.** It covers how a change is decided, specified, built and reviewed.
  It works with any technology. Feature specs are written by
  [OpenSpec](https://github.com/Fission-AI/OpenSpec). The kit adds what OpenSpec has no place
  for: a round of questions before anything is written, decision records (ADRs), a test-first
  build loop with evidence, an independent review, pitfalls, and working rules with guards.
- **Technology layers, the knowledge.** `typescript`, `react`, `expo`, `react-web` and
  `supabase` hold what is true of a stack: rules, pitfalls, and skills for the topics touched
  now and then (an SDK upgrade, payments, analytics). They never mention the process. The build
  and the review read them.

A project links `workflow` plus the layers of its stack. Its own repository keeps only what is
specific to it: its domain, its decisions, and its deliberate departures from a kit rule.

## Why a submodule

The kit is plain files linked into the project's `.claude/` folder, not a Claude Code plugin:

- it works whatever Claude Code login is used, including organizations that only allow approved
  plugin marketplaces;
- it travels with the repository: a teammate who clones it has it, with nothing to install;
- each project pins the kit's version and updates it on purpose, in a commit.

## Add it to a project

From the project's root. **Shared** (committed with the repository, the default):

```
git submodule add https://github.com/<owner>/agentic-kit .claude/agentic-kit
python3 .claude/agentic-kit/scripts/link.py
```

**Local** (a team that has not agreed to it, a client's repository): nothing is committed, and
every path the kit writes goes into the repository's exclude file.

```
git clone https://github.com/<owner>/agentic-kit .claude/agentic-kit
python3 .claude/agentic-kit/scripts/link.py --local
```

Then start a new Claude Code session and run `/workflow-init`. It reads the project, links the
layers of its stack, writes or merges `AGENTS.md` / `CLAUDE.md`, and offers OpenSpec. In the
shared mode, commit `.gitmodules`, `.claude/agentic-kit`, `.claude/settings.json`,
`.claude/agentic-kit.state.json` and the links under `.claude/rules/`, `.claude/skills/` and
`.claude/agents/` (`git status` lists them); never `.claude/settings.local.json`.

Someone who clones a project that has it runs `git clone --recurse-submodules`, or
`git submodule update --init` in an existing clone.

## Update it

```
git submodule update --remote .claude/agentic-kit
python3 .claude/agentic-kit/scripts/link.py
```

Without arguments, `link.py` keeps the layers already linked and refreshes their links (a new
skill gets its link). Review the kit's `CHANGELOG.md`, then commit. In the local mode:
`git -C .claude/agentic-kit pull`, then the same `link.py`: the mode is remembered.

To change the selection, pass the layers: `link.py expo supabase` (`workflow` is always there,
and a layer brings the ones it requires). To take it all out: `link.py --remove`.

## Use

| Skill | When |
| --- | --- |
| `/workflow-init` | Once per repository: links the layers, writes `AGENTS.md` / `CLAUDE.md`, offers OpenSpec with the kit's rules |
| `/workflow-feature <description>` | Something to build. Questions first, then an OpenSpec change you approve, then a test-first build, then reconcile and archive |
| `/workflow-decide` | A decision that produces no code (a stack, a boundary, reversing an ADR): writes an ADR |
| `/workflow-build` | A scope that is already settled: an open change, a ticket, a bug |
| `/workflow-review [target]` | Before a commit. A fresh agent reads the change and grades its findings, and you pick which ones to apply. Given `openspec/changes/<change>`, it reviews the spec instead |
| `/workflow-gotcha` | Records a pitfall you verified, in the project or in the kit |
| `/workflow-lab` | After two failed attempts: several variants side by side, compared in one pass |

You rarely need to type them: the working rules tell the agent which one fits a request. The
technology skills load on their own when a task matches them, for example `expo-sdk-upgrade`,
`expo-revenuecat` or `supabase-rpc`.

## What it puts in a project

| Part | Where | Loaded |
| --- | --- | --- |
| Rules | `.claude/rules/kit-<layer>/` | At every session start |
| Skills | `.claude/skills/<layer>-<skill>/` | The description always; the body when used |
| Review agent | `.claude/agents/workflow-reviewer.md` | When `workflow-review` starts it |
| Guards | `permissions` in `.claude/settings.json` (or `.local.json`) | Always: pushes, remote database commands, store builds and production deploys ask first; edits to installed dependencies and generated files are refused |
| Pitfalls | `.claude/agentic-kit/layers/<layer>/gotchas/` | Never: read before retrying an approach |

The links are relative and stay inside the repository. The project's own rules, skills and
permissions sit beside them and are never touched: `link.py` records its mode, the linked layers
and the permission rules it wrote in `.claude/agentic-kit.state.json`, and only ever replaces
those.

## Requirements

- Claude Code. Developed against 2.1.32x.
- git and python3 (for `link.py`).
- For specs: OpenSpec 2.x. The kit uses your installed `openspec`, or `npx @fission-ai/openspec@2`
  (Node.js 22.12 or later). Without OpenSpec, specs are agreed in the conversation.
- Cloud sessions load what the repository holds, so the kit applies there once the submodule is
  checked out. If your cloud environment does not do it, add `git submodule update --init` to
  its setup script.

## Contributing

Read [`AGENTS.md`](AGENTS.md). It says where a new rule, pitfall or skill goes and how it is
written. Run `sh scripts/check.sh` before committing.

## License

[MIT](LICENSE).
