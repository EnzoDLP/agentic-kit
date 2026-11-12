# The build loop

Three skills follow this file: `workflow-build`; `workflow-feature`, after its spec is approved;
and `workflow-review`, after the user has picked the corrections to apply.

## What the loop works from

Work from a written source, never from a summary kept in the conversation. The source is one of:

- **an OpenSpec change** on disk. Read it again from disk each time you need it. Each scenario in
  its delta specs is one unit, taken in the order `tasks.md` gives. Name a scenario by its
  requirement and its own name. The out-of-scope part of `proposal.md` lists the non-goals.
- **a review finding the user selected.** Each one is a unit.
- **numbered results the user approved in writing**, when the project has no OpenSpec. Each result
  is a unit.

## Which commands to run

Take the test, lint, typecheck and build commands from the repository. Look in `AGENTS.md` /
`CLAUDE.md` first; if they name none, read the task runner's manifest (`package.json` scripts, a
`Makefile`, …) and use its flags as written. Never make a command up.

No test suite at all: say it, then verify another way and run it: the build, a lint pass, or a
manual check that you call a manual check.

## One unit, five steps

1. **Predict the red.** Before any code, one line: the scenario, the assertion that will fail, and
   the reason it will.
2. **Write the test.** Start with the result the scenario states. Then add the nearby cases that
   earn a test: an edge value, an empty or malformed input, a dependency that errors. Add nothing
   that falls in the non-goals, and for a review finding nothing past that finding. The assertion
   reads what a caller gets back — a returned value, printed output, a saved row, a response —
   and never which function was called, how the internals are laid out, or what a mock replied.
   Stub only what lives outside the unit.
3. **Run it and check the cause of the red.** An import error, a typo or a missing fixture tells
   nothing about the behavior: repair the test and run it once more.
4. **Write only the code that failure asks for.** Anything else in the diff is scope no one
   approved.
5. **Run it again.** The test must pass because of the code you wrote, not because you loosened
   the test.

Do the steps; do not describe them. A red you predicted is normal and needs no comment. Speak up
during the loop only when something surprises you: a red with the wrong cause, a repository that
disagrees with the spec, a command that turns out not to exist.

### Two special cases

- **A test you add that the spec never listed**: name the scenario it extends and flag it as
  found. If the scenario already implies its expected result, write it and make it pass. If the
  result is a choice the spec leaves open, do not make the choice: hand it to the user as a
  **proposed scenario** to add.
- **A correction with no change in behavior** (a cleaner shape, a library function in place of a
  hand-rolled one): there is no red to predict, so say that. The tests that already cover this
  code must still pass, and for the same reasons.

## Closing, once for the whole set

These steps run a single time, after the last unit.

6. Run the repository's lint, typecheck and build on the change.
7. Read the diff. Take out, or report, whatever no unit called for.
8. With OpenSpec, check off the completed tasks in the change's `tasks.md`.
9. Write one line per item in `docs/ROADMAP.md` for what you ran into and left: debt (code that
   does not yet follow a rule) and follow-ups beyond the scope. A pitfall you confirmed on the way
   goes to `workflow-gotcha`.
10. Report the evidence block.

## When the repository disagrees with the spec

Examples: the spec relies on a pattern the code does not have, a test proves one of its
assumptions false, or a behavior cannot be reached the way it is written. **Stop.** In one line,
put what the spec expected next to what the repository shows, and ask for a fresh go-ahead. Fixing
it quietly would decide scope with nothing written down.

## The evidence block

It goes in the session or the pull request, never into a spec. In this order:

- **Per unit**: one row per scenario (or finding), with the test that covers it and what its
  command returned. A scenario with no test then shows up as a blank row.
- **Checks**: the output of lint, typecheck and build.
- **Left open**: scenarios without a test and the reason, proposed scenarios, non-goals the work
  ran into, discrepancies with the spec.

Writing "tests pass" with no command and no output proves nothing.

The loop never commits.
