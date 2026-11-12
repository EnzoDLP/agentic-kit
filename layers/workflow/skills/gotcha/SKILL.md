---
name: workflow-gotcha
description: Record a pitfall verified in this session ("X fails because Y", a workaround, a version trap) where the next session will find it — the project's docs/GOTCHAS.md, or the kit layer it belongs to when it is true of a whole technology. Use right after such a lesson is confirmed, or when the user says "note this", "add a gotcha" or invokes /workflow-gotcha.
---

# Record a pitfall

## Is it worth recording

Only what was **verified** (reproduced, or fixed and confirmed), and **durable** (still true
after this session). A guess, an attempt that failed for a reason not understood, or a story of
the session is not a pitfall.

## Where it goes

- **Specific to this project** (its schema, its config, its build) → `docs/GOTCHAS.md`, created by
  its first entry, grouped under topic headings.
- **True of a technology in any project** → the matching layer of the kit: its `gotchas/` file
  for the topic (`.claude/agentic-kit/layers/<layer>/gotchas/`). The kit is a submodule pinned by
  the project: never edit it in place. Write the entry, show it to the user, and offer to
  contribute it — a pull request to the kit's repository, or the user's own fork.
- **A rule rather than a pitfall** (something to always do or never do) → the project's
  `CLAUDE.md` / `AGENTS.md`, or a rules file of the kit through the same contribution path. A
  rule loaded in every session costs context: propose it, do not add it silently.

## How it is written

- One bullet: **the symptom or trap in bold**, then the cause, then the fix or workaround, with
  exact versions, commands and identifiers.
- Nothing that identifies a person, a client, a product or a machine in a kit contribution: no
  names, absolute paths, account ids or domains. Versions stay.
- Replace an entry that no longer holds rather than appending a contradiction.
