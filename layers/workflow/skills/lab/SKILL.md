---
name: workflow-lab
description: After two blind attempts at the same problem have failed (a layout, an animation, a native behavior, a flaky config), stop iterating in place and build a disposable lab with several variants side by side that the user compares in one pass; then port the chosen one and delete the lab. Use when a second attempt has failed, or when the user asks to "compare options", "try variants" or invokes /workflow-lab.
---

# Lab

A third blind attempt costs as much as the first two and teaches as little. A lab turns guessing
into one comparison.

1. **Read the pitfalls first**: the project's `docs/GOTCHAS.md` and the kit's pitfalls for the
   stack (`.claude/agentic-kit/layers/<layer>/gotchas/`). The answer may already be written down.
2. **State the problem in one line** and what "right" looks like, so the variants are judged on
   it.
3. **Build N variants side by side** (usually 3 to 5) that differ on the one dimension in doubt,
   each labeled with what it changes. Put them where they are cheap to show together: a dev-only
   screen or route, a story, a scratch page, a script printing each result. Keep the lab out of
   the production bundle and out of the commit.
4. **Let the user compare them in one pass** — or capture each one (screenshot, recording,
   output) when the user is away — and wait for the choice.
5. **Port the chosen variant** into the real code, then **delete the lab** and anything it added
   (routes, flags, dependencies).
6. If the lesson is durable, record it with `workflow-gotcha`.
