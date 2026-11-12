# Working with OpenSpec

Feature specs are [OpenSpec](https://github.com/Fission-AI/OpenSpec)'s job, not the kit's. The kit
brings the parts OpenSpec does not cover: asking the open questions, keeping decision records, the
test-first build, the review. It also ships rules that steer OpenSpec into writing what those parts
need. Everything below assumes OpenSpec **2.0**.

## Is OpenSpec there?

- **In the repository**: look for an `openspec/` folder at the root. No folder, no OpenSpec.
- **On the machine**: try `openspec --version`. If it fails, run each command through
  `npx @fission-ai/openspec@2 <command>`, which needs Node.js 22.12 or newer. Tell the user which
  of the two you used.
- **As skills**: version 2.0 puts its skills in `.agents/skills/openspec-*`, a single copy linked
  into `.claude/skills/`. Call them as `/openspec-propose`, `/openspec-explore`,
  `/openspec-apply-change` and `/openspec-archive-change`. A repository that has not left 1.x
  exposes `/opsx:*` commands in their place: say which step you mean (propose, apply or archive)
  and call whatever the repository has.

## Where each piece is kept

| File                                                   | What it holds                                                |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| `openspec/changes/<change>/proposal.md`                | why the change is made and how far it goes                   |
| the out-of-scope list in `proposal.md`                 | what the change will not do                                  |
| the scenarios in the change's delta specs              | behavior to test, one test per scenario                      |
| the change's `design.md`                               | decisions, rejected alternatives, known gaps, regulated data |
| the change's `tasks.md`                                | the sequence of the work                                     |
| `openspec/specs/<capability>/spec.md`                  | current behavior of the system                               |
| `design.md` of every archived change, plus `docs/adr/` | the reasons behind that behavior                             |

## Write access

- **Changes**: only OpenSpec's propose step creates one. A kit skill never writes a `proposal.md`
  or a delta spec itself.
- **`openspec/specs/`**: never edited by anyone. It changes only as a result of archiving a change.
- **An open change**: a kit skill may append to its `design.md` (a decision, a rejected
  alternative, a known gap) and check off a completed task in its `tasks.md`.
- **A change archived in an earlier commit**: history. No one writes in it.

## Commands the kit calls

```
openspec validate <change> --strict --no-interactive
openspec archive <change> --yes
openspec list --json
```

**Archive only through the CLI, never by hand.** Merging delta specs yourself duplicates
OpenSpec's own logic, and one bad merge damages the specs it maintains. When the CLI cannot run,
leave the change open and tell the user why.

`openspec init` is run by the user, not the agent: it asks questions and writes files into the
repository. `workflow-init` suggests it with `--tools claude`, adding any other tools the team
uses, and runs it only after the user says yes.

## Rules for `openspec/config.yaml`

`.claude/agentic-kit/layers/workflow/reference/openspec-config.yaml` lists rules per artifact;
OpenSpec appends them to the prompt it uses for that artifact. `workflow-init` offers to merge
them next to the rules the project already has, translated into the language the repository's
docs are written in.
