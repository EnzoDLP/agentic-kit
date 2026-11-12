---
name: workflow-feature
description: Turn a loose request for a feature or a behavior change into recorded decisions and tested code — put every open question to the user first, have OpenSpec write the change (proposal, scenarios a test can check, design with the rejected alternatives), build only after an explicit go-ahead and test-first, then reconcile and archive. Use when the user describes something to build or change, or invokes /workflow-feature with a description.
---

# Feature

A feature's choices get made while its questions are answered, and that is the last time the
options it turns down are still in view. This skill writes both onto disk before any code: they
become the contract the build is approved against, and the source its tests are written from.

Not this skill:

- a decision that brings no code → `workflow-decide`;
- a scope someone has already settled → `workflow-build`.

## Read first

- `AGENTS.md` / `CLAUDE.md`;
- `openspec/specs/`, for what the system does today, and the open changes in `openspec/changes/`;
- `docs/adr/`, for decisions that already limit the answer;
- the existing code closest to what is asked;
- `.claude/agentic-kit/layers/workflow/reference/openspec.md`.

Form no view before these are read.

**The project has no `openspec/`**: tell the user and offer `workflow-init`. If they say no, step
4 becomes numbered results written in the conversation, and the go-ahead is given on those. A
decision worth keeping then goes into an ADR, or is not kept.

## Steps

1. **Take in the request** without planning any file change.
2. **Write down every open point.** Look at behavior, scope, UX, the data model, how it fails, its
   empty and error states, who can trigger what, and anything that has more than one sensible
   implementation. Two points are on every list: whether this is a new change or amends one
   already open, and whether it touches personal, health or payment data (asked as a fact; see
   `.claude/agentic-kit/layers/workflow/reference/decision-records.md`).
3. **Ask the user, before any plan.** Offer choices where the options are known, and free text
   where they are not; group everything into as few rounds as you can. Skip anything the
   repository's conventions, an ADR or the code nearby already decides: apply it without asking.
4. **Have OpenSpec write the change.** Run its propose step (`/openspec-propose <name>`) and feed
   it the answers. Then hold the result against what the kit needs, and fill the gaps in
   `design.md`: each decision with the reason it won, the **rejected alternatives** that came up
   in step 3 with the reason each lost, and the known gaps. Every scenario must be a single result
   a test can check from outside. Run `openspec validate <change> --strict --no-interactive`. In
   one line, say whether an ADR seems called for, but do not write one yet.
5. **Offer a review of the change** in one line, giving the command
   (`/workflow-review openspec/changes/<change>`). If the user accepts, run it, pass on its
   findings unchanged, ask the user its open questions, and apply the wording fixes they choose.
6. **Get an explicit go-ahead** on the change in its current state. Write no code until then.
7. **Build** with the loop in `.claude/agentic-kit/layers/workflow/reference/build-loop.md`, read
   at this step and not sooner. If the repository disagrees with the change, stop and go back to
   step 3.
8. **Reconcile, before closing.** Wherever what shipped differs from the plan, add it to the
   Rejected alternatives in `design.md`, with what the build revealed. Then write any ADR the work
   proved necessary, through `workflow-decide`, now and not earlier, since a committed ADR cannot
   be edited. Do it in this session, never as a follow-up: by the next one, the options that lost
   are forgotten.
9. **Propose the commit**, offering `workflow-review` in the same question. Once the user says the
   change is finished, run `openspec archive <change> --yes` and include it in that commit.

No commit happens until the user says yes.
