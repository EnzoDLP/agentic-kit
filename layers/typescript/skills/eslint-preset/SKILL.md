---
name: typescript-eslint-preset
description: Install or update the kit's ESLint blocks in a project. Copies each linked layer's block (typescript, react, expo, react-web) to the project root as agentic-kit.<layer>.eslint.cjs and extends it from eslint.config.js. Use when setting up ESLint or lint rules in a project, editing eslint.config.js, wiring the kit's lint rules, or when a layer's ESLint block has changed.
---

# ESLint preset

Each technology layer with rules that a linter can check ships them as an ESLint flat-config
block (a CommonJS module exporting an array) in its `eslint/` folder. The rules files stay the
reference; the block only enforces the checkable part.

## 1. Find the blocks

- The layers linked in the project are the `kit-<layer>` entries of `.claude/rules/`.
- Each one's block, if it has one: `.claude/agentic-kit/layers/<layer>/eslint/<layer>.cjs`.

## 2. Personal or team repository

- **Personal repository**: copy the files (step 3).
- **Team repository** (other contributors, shared CI): never without the user's explicit
  request, since the rules would apply to the whole team and its CI. On request, copy the rules
  **inline** into the project's `eslint.config.js`: no separate file, no comment pointing to the
  kit; for the team they are just project rules. A later change to a block is carried over by
  hand.
- When unsure which one it is, ask.

## 3. Copy

- Copy each block, unchanged, to the project root as `agentic-kit.<layer>.eslint.cjs`
  (`agentic-kit.typescript.eslint.cjs`, `agentic-kit.react.eslint.cjs`…).
- The copies are never edited in the project. To update: diff each copy against the layer's
  block, show the user what changes, then re-copy.
- When a layer's block changes, propose re-copying it in the projects that have it.

## 4. Extend from `eslint.config.js`

Order: the base config (which registers the ESLint plugins), then the kit blocks (typescript,
react, then expo or react-web), then the project's own rules.

```js
const { defineConfig } = require('eslint/config')
const typescript = require('./agentic-kit.typescript.eslint.cjs')
const react = require('./agentic-kit.react.eslint.cjs')

module.exports = defineConfig([
  baseConfig,
  ...typescript,
  ...react,
  { rules: { 'max-lines': 'warn' } } // the project's own rules
])
```

In an ESM config: `import typescript from './agentic-kit.typescript.eslint.cjs'`.

- Each block's header names the ESLint plugins the base config must register
  (`@typescript-eslint` for typescript, `react-hooks` v7 for react). If one is missing, propose
  adding it; do not drop the rule.
- In flat config, a later entry that gives a rule **options** replaces the earlier options
  entirely; a severity alone (`'max-lines': 'warn'`) keeps them. If the project's own rules set
  `no-restricted-imports` or `no-restricted-syntax` with options, merge the kit's patterns and
  selectors into that entry instead of losing them.

## 5. Existing debt

- Run the lint. A kit rule with existing violations that are not fixed now stays at `"warn"` in
  the project's own rules (severity only), and the debt is noted where the project tracks it.
  New code follows the rule.
- Never turn a kit rule off globally, and never edit the copied file to do it. A truly
  unavoidable case is disabled on its line, with a comment saying why.

## 6. Verify

- The lint script covers the whole project: `expo lint` without arguments lints only `src/`,
  `app/` and `components/`, so code in other root folders is never linted. Use `expo lint .` or
  `eslint .`; run `npx eslint .` once to see what was waiting.
- 0 errors and no new warnings; report the warning count, and say what was not checked.
