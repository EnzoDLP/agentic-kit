# Workflow — working rules

Loaded in every session of a project that links the kit (`.claude/agentic-kit`), whatever the
language. Technology rules come from the kit's other layers linked in the project
(`.claude/rules/kit-<layer>/`); the project's own `CLAUDE.md` / `AGENTS.md` holds its domain and
its decisions, and wins where it states a deliberate departure from a rule here.

## Which skill, when

- The project's stack matches a kit layer that is not linked, and `CLAUDE.md` /
  `CLAUDE.local.md` do not decline it → propose `workflow-init` in one sentence, naming the layer.
  Run nothing without a yes. On a no, offer to record it as one line in `CLAUDE.local.md` ("Kit
  layer `<name>`: not used here"); either way, not again this session.
- A feature or a behavior change described loosely → `workflow-feature` (questions first, then an
  OpenSpec change, then the build).
- A decision that produces no code (a stack, a boundary, a dependency, reversing an ADR) →
  `workflow-decide`.
- A scope already settled (an open OpenSpec change, a ticket, a bug with a known cause) →
  `workflow-build`.
- When proposing a commit, propose `workflow-review` in the same question: the user answers yes or
  no each time. On a yes, the review runs before the commit, and its corrections are applied only
  once the user has picked them.
- A pitfall verified in this session → `workflow-gotcha`, without waiting.
- Two blind attempts failed → `workflow-lab`.

## Before writing code

- **Reuse the existing pattern**: find the closest equivalent already built and reuse its
  components, constants and structure. A pattern present **three** times is extracted.
- **Before retrying an approach**, read the project's `docs/GOTCHAS.md` and the pitfalls of the
  linked layers (`.claude/agentic-kit/layers/<layer>/gotchas/`, one file per topic).
- **After two blind attempts that failed, stop**: build a disposable lab (`workflow-lab`).
- Before changing or deleting something reused: find **every** usage, check each, remove dead
  imports. A rename updates every usage in the same change.
- **300 lines per file at most**; beyond that, split.
- A comment says only the _why_ the code cannot say. No commented-out code left in place.

## Never without the user's explicit request

- **Push** (`git push`): a branch can deploy (migrations, functions, a site). Commit only when
  asked.
- Touch a remote environment (database, cloud, deployment).
- Run a destructive or long command (native or production build, database reset…): propose it.
- **Edit an installed dependency by hand** (`node_modules`, vendored packages): use a version, a
  documented patch (`patches/`), or a workaround written in `docs/GOTCHAS.md`.
- Paste or ask for a secret in the chat: secrets live in an uncommitted `.env` (only
  `.env.example` is committed) or in the service's secret store.

## Project records

- **Feature specs**: OpenSpec (`openspec/specs/`, `openspec/changes/`), written by its propose
  step, never by hand.
- **Structural decisions**: `docs/adr/`, dated, never rewritten once committed (`workflow-decide`).
- **Pitfalls**: `docs/GOTCHAS.md`. **Debt** (code that does not follow a rule yet, fixed when the
  file is next touched): `docs/ROADMAP.md`.
- A document an agent drafted is read by a human before it is committed.

## Before concluding

Typecheck, lint (0 errors, **no new warnings**), tests and format, with the project's own
scripts. Say what was not verified rather than letting it be assumed.
