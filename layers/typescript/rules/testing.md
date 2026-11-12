# TypeScript — tests

Test first where there is logic: write the test, see it **fail**, then code until it passes.
Required in three cases:

1. **Pure logic**, new or changed (utils, mappers, the logic of a hook or a store): expected
   cases, edge cases, invalid input.
2. **A fixed bug** whose cause lies in testable code: a test that reproduces it (red), then the
   fix (green). An input that was parsed wrong (a page, a file) → that input, trimmed down,
   becomes the fixture.
3. **A decision made in a container** ("should we…?", "which state to show?"): extracted into a
   pure function, with its tests written before the extraction.

A test that has never failed proves nothing: if it passes on the first run, break the code on
purpose to check that it fails. Do not mock a whole framework to force a test: extract the pure
logic. The only fakes allowed are those declared in the project's test config.

- Tool: the project's own (Jest or Vitest), `*.test.ts` files next to the file under test.
- TypeScript 6: `types` defaults to `[]`, so test globals are no longer loaded on their own:
  import `describe` / `expect` / `it` (from `@jest/globals` or `vitest`).
- What is tested beyond pure functions (hooks, components, SQL) depends on the stack: see the
  expo, react-web and supabase layers' rules.
