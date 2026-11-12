---
name: workflow-build
description: Implement a scope that is already settled — an open OpenSpec change, a ticket, or a bug with a known cause — test-first, one test per scenario, then run the repository's own checks and report an evidence block. Use when the user says a change or ticket is ready to build, or invokes /workflow-build. A loose request goes to workflow-feature instead.
---

# Build

Read `.claude/agentic-kit/layers/workflow/reference/build-loop.md` and follow it as written.

## The input

- **An open OpenSpec change** (`openspec/changes/<change>/`): read
  `.claude/agentic-kit/layers/workflow/reference/openspec.md`. Several open changes and nothing
  tells which one: ask.
- **A ticket or a bug**: before the first test, write the expected results as numbered lines and
  have the user approve them. A bug's first unit is a test that reproduces it.
- **A loose request** with open questions: stop and hand over to `workflow-feature`.

## After the loop

- Route what the build itself decided
  (`.claude/agentic-kit/layers/workflow/reference/decision-records.md`): into the open change's
  `design.md`, or an ADR through `workflow-decide`.
- Report the evidence block, then propose the commit with `workflow-review` in the same question.
  With OpenSpec, once the user says the change is done, archive it in that commit
  (`openspec archive <change> --yes`).

This skill commits nothing on its own.
