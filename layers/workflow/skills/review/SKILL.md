---
name: workflow-review
description: Have a fresh agent that did not write a change review it before a commit — against the repository's conventions and the kit's loaded rules, the OpenSpec change it implements, and the installed versions of the libraries it uses — with findings graded blocking / to fix / detail, then apply only the ones the user picks, through the build loop. Given a path under openspec/changes/, it reviews the spec instead, as a business analyst then as a tech lead. Use before committing, before a spec's go-ahead, or when the user invokes /workflow-review [target].
---

# Review

Left alone, a reviewer model always has something to say, and a flat list of every remark gets
ignored after the first read. So this review judges the change only against what the repository
has written down, backs every library claim with a source, and sorts what it finds by weight.

## What to review

- **Nothing given**: the uncommitted tree, staged and unstaged, as code.
- **A branch** (compared with the trunk), **a commit range or a path**: code.
- **A path under `openspec/changes/<change>/`**: a spec (last section).
- **A range that holds both code and spec changes**: ask the user which one to review.

## Who reviews

If this session wrote the change, planned it or talked it through, it cannot review it: it will
see in the tests what it meant them to check. Start the `workflow-reviewer` subagent and pass it
four things, nothing more:

1. the target;
2. the path of the OpenSpec change behind it, if there is one. If several are open and the diff
   does not show which, ask the user;
3. the kit's rules folders linked in the project (`.claude/rules/kit-*/`), with `AGENTS.md` /
   `CLAUDE.md`;
4. for a spec, the fact that this is a spec review.

Keep back the build's evidence block, any summary of the change and any reason behind a choice.
Each of them hands the author's view to the reviewer.

A session that has no memory of the change may review it itself, following
`.claude/agentic-kit/layers/workflow/agents/workflow-reviewer.md`. If no subagent can be started,
say so and suggest a review from a new session; do not call this one independent.

Pass the findings on exactly as they come back: their numbers, their grades, the unverified ones
still marked. Do not remove, regrade or tone down any of them. If you disagree, write it next to
the finding.

## Once the user has the report

Touch nothing until the user replies. Then:

- **Apply each finding they pick through the build loop**
  (`.claude/agentic-kit/layers/workflow/reference/build-loop.md`, opened at this point and not
  earlier). A finding is one unit, as a scenario would be. A fix that changes behavior comes with
  a test; a fix that changes none says so. The loop's closing steps run once, after all of them.
- **Change only what was picked.** Anything else you notice belongs to the next review, not to
  this diff.
- **A substantive finding the user turns down** is written into the Known gaps of the open
  change's `design.md`, with the condition under which it should come back, so the next review
  does not raise it again. A rejected detail is written nowhere. With no open change, write
  nothing and tell the user.

Then report the evidence block from the loop, which findings were turned down and where they were
recorded, and the unverified findings once more, still marked unverified. This skill never
commits.

## A spec as the target

One fresh agent reads the spec twice and returns two lists, shown next to each other and never
merged.

1. **As a business analyst, before any code is opened.** Does the change solve the problem that
   was asked? Has the scope grown? Is each scenario a single result someone can observe? What has
   nobody written down: the empty state, the error, who is allowed to do what, the case the user
   cares about most?
2. **As a tech lead, with the code open.** Can it be built as written? Does it go against an ADR
   or the system as it stands (`openspec/specs/`)? Are the decisions and rejected alternatives in
   `design.md` actual ones? Does the spec settle anything the code will not allow?

Each finding is one of three kinds:

- a **wording fix**: the ones the user picks are applied to the open change, and nothing else is;
- an **open question**: put to the user before the go-ahead;
- a **referral**: to `workflow-decide`, for an ADR.
