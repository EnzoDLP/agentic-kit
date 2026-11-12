# Decision records

`workflow-decide` reads this file before anything else; `workflow-feature` and `workflow-build`
read it when they have a decision to file. The reason it exists: an agent opening a repository can
read every line of code and still not know why any of it is that way, because a commit shows the
diff and not the options that were dropped. A record is how that "why" reaches whoever works on
the code next.

## Picking the home

A decision lands in one of three places. Ask these questions in this order and stop at the first
one that gets a clear answer:

1. **How far does it reach?** If it binds code beyond the current feature — the database, the
   runtime, how users authenticate, where the app is deployed, how directories are laid out, a
   dependency every part of the repository now carries — write an **ADR**. If it only shapes what
   a user sees in this one feature, it goes in that feature's OpenSpec change, in `design.md`.
2. **What would undoing it take?** A data migration, a rewrite or a release several parties must
   coordinate: ADR. Edits to a few files: the change's `design.md`.
3. **Does it outlive the feature?** If it would still hold after the feature is removed: ADR.

Some things look like decisions and are not: a naming convention, a script to run, the shape of a
folder. Anyone can read those off the code, so they are **state**, and state belongs in
`AGENTS.md` / `CLAUDE.md`.

## Only at the moment of deciding

The options that lost are known only while the choice is open; a week later nobody can list them
honestly. So a record is written at that moment, from what the user tells you. Refuse any request
to rebuild past decisions from the code ("write the ADRs for this repo"): the result would read
well and be made up. Point the user to `AGENTS.md` for what the code shows instead.

## ADR files

- Path: `docs/adr/NNNN-kebab-title.md`. Take the highest number already in the folder and add
  one; the very first is `0001`. A number, once used, is never given to another record.
- Start from `.claude/agentic-kit/layers/workflow/reference/templates/adr.md`.
- **Consequences** list what the choice costs and what it rules out. Put nothing there that has
  not been checked: either check it before writing, or write it as an open gap and name what
  would close it.

## Once an ADR is committed

- **The folder only grows, and a committed ADR is frozen.** Freezing starts at the commit, not at
  the push. Before its first commit an ADR is a draft that you may fix as much as needed; run
  `git log -- <file>` to see which case you are in.
- **To reverse a decision, write a new ADR** that names the old one in its Supersedes row
  (`Supersedes ADR-NNNN`). In the old ADR, change the Status row to `Superseded by ADR-NNNN` and
  nothing else, not one word.
- **Read every ADR as of its date.** "The API has no rate limit" means it had none on the day of
  writing. When such a consequence is later fixed, the ADR is not wrong and is not superseded: the
  new fact is state and is written where state is kept.

## In the `design.md` of an open change

The rules in `.claude/agentic-kit/layers/workflow/reference/openspec-config.yaml` make OpenSpec
create these sections; the kit fills them:

- **Decisions**: each rule followed by why it was preferred.
- **Rejected alternatives**: one line per option dropped, with the reason. When the build is
  reconciled with the plan, every place where the shipped code departed from the plan is added
  here, together with what the code revealed.
- **Known gaps**: a `Left out | Add it when` table. A substantive review finding that the user
  chose not to fix is written here, so the next review does not bring it up again.

Once a change has been archived and that archive committed, it is history: nothing adds to it.

## Personal, health or payment data

Ask whether the feature handles personal, health or payment data as a **question of fact**. Do not
answer it yourself by guessing which law or regime applies. If the answer is yes, `design.md` gets
a `Regulated data` section with five fields:

- **Date**
- **Trigger**
- **Consulted**: the team or role that gave the answer
- **Decision**
- **Reference**: where that answer is written down

If nobody has answered yet, the section says the question is unanswered.
