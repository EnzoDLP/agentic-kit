---
name: workflow-decide
description: Write down a decision that comes with no code — a stack or architecture picked before any work, a boundary, a dependency the repository accepts to carry, or the reversal of an earlier ADR — as an ADR, an entry in an open OpenSpec change, or a line in AGENTS.md. Use when the user settles or reverses such a decision, asks to "write an ADR" or "record this decision", or invokes /workflow-decide.
---

# Decide

This skill writes a record of what the user chose. It never makes the choice.

Start by reading `.claude/agentic-kit/layers/workflow/reference/decision-records.md`: the routing
tests, why records are immutable, and how one replaces another are there.

## Steps

1. **Pick the destination** with the three tests (scope, reversal cost, lifetime): an ADR, the
   `design.md` of an open OpenSpec change, or a line in `AGENTS.md` if the decision proves to be a
   fact anyone can read in the code. Tell the user which, and why, in one line.
2. **Ask for what the record lacks.** That is: the situation when the decision was made, the
   options compared and the reason each one lost, and the price of the choice. **The options come
   from the user, not from you.** Anything they cannot answer goes in as unanswered; never fill it
   in yourself.
3. **Do not choose for them.** If they ask what you would pick, answer with analysis and write
   nothing until they have decided.
4. **Write the record.** An ADR starts from
   `.claude/agentic-kit/layers/workflow/reference/templates/adr.md` and takes the number after the
   highest one in `docs/adr/`. The first is `0001`, and writing it creates the folder.
5. **Replacing an ADR.** Run `git log -- <file>` on the old one.
   - It is committed: the new ADR states `Supersedes ADR-NNNN`, and the old one changes only its
     Status row, to `Superseded by ADR-NNNN`; leave every other word as it is.
   - It is still a draft: fix it where it is instead.
6. **Give it to the user to read before any commit.** A committed ADR cannot be changed, so the
   review must happen first. Commit only when they say yes.

## Refuse

A request to rebuild past decisions from the code ("write the ADRs for this repository"): decline
it and point to `AGENTS.md` instead. Such a record would look right and be made up.
