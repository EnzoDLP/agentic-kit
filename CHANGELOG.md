# Changelog

Changes that affect a project using the kit, latest on top.

## Unreleased — 0.1.0

- First version, added to a project as a git submodule at `.claude/agentic-kit` and linked into
  `.claude/` by `scripts/link.py` (shared, or local with `--local`).
- The `workflow` layer: `workflow-init`, `workflow-feature`, `workflow-decide`, `workflow-build`,
  `workflow-review` (with the `workflow-reviewer` agent), `workflow-gotcha`, `workflow-lab`;
  working rules; guards as permission rules.
- Technology layers: `typescript`, `react`, `expo`, `react-web` and `supabase`.
