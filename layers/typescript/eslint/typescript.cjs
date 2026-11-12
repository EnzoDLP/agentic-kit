// agentic-kit ESLint block — typescript plugin (rules/typescript.md, and the 300-line limit of
// the workflow plugin's working rules).
// Copied into a project as agentic-kit.typescript.eslint.cjs by the typescript-eslint-preset
// skill. Do not edit the copy: change this file, then re-copy.
//
// Usage in the project's eslint.config.js, after the base config and before the project's own
// rules (so the project can keep a rule at "warn" for existing debt):
//
//   const typescript = require('./agentic-kit.typescript.eslint.cjs')
//   // ESM: import typescript from './agentic-kit.typescript.eslint.cjs'
//   module.exports = defineConfig([baseConfig, ...typescript, ...react, projectRules])
//
// The base config must register the @typescript-eslint plugin (typescript-eslint, or a framework
// config that includes it, such as eslint-config-expo).

module.exports = [
  // Git worktrees of Claude Code sessions are copies of the project: never lint them.
  { ignores: ['.claude/**'] },
  {
    files: ['**/*.{ts,tsx}'],
    rules: {
      // "No any (no as any, no @ts-ignore) [...] A truly unavoidable case: disabled on its line
      // only, with a comment saying why."
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/ban-ts-comment': ['error', { 'ts-ignore': 'allow-with-description' }],
      // "The @/ alias across folders, relative only within the same folder (./x), never ../"
      // A later block that sets no-restricted-imports with options replaces this pattern:
      // repeat it there.
      'no-restricted-imports': [
        'error',
        { patterns: [{ group: ['../*'], message: 'Use the @/ alias across folders.' }] }
      ],
      // "No console.log in production; console.error / console.warn tolerated"
      'no-console': ['error', { allow: ['warn', 'error'] }],
      // "300 lines per file at most" (warn: existing files over the limit are debt)
      'max-lines': ['warn', { max: 300, skipBlankLines: true, skipComments: true }]
    }
  }
]
