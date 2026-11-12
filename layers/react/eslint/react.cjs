// agentic-kit ESLint block — react plugin (rules/react.md, rules/i18n.md).
// Copied into a project as agentic-kit.react.eslint.cjs by the typescript-eslint-preset skill.
// Do not edit the copy: change this file, then re-copy.
//
// Usage in the project's eslint.config.js, after the base config and the typescript block, before
// the project's own rules (so the project can keep a rule at "warn" for existing debt):
//
//   const react = require('./agentic-kit.react.eslint.cjs')
//   // ESM: import react from './agentic-kit.react.eslint.cjs'
//   module.exports = defineConfig([baseConfig, ...typescript, ...react, projectRules])
//
// The base config must register the react-hooks plugin (eslint-plugin-react-hooks v7, which
// provides set-state-in-effect).
//
// Optional, for "no hardcoded text": add eslint-plugin-i18next's flat/recommended config in the
// project and set its no-literal-string rule to warn, in jsx-text-only mode.

module.exports = [
  {
    files: ['**/*.{ts,tsx}'],
    rules: {
      // "Never a synchronous setState in a useEffect [...] A truly unavoidable case: disable
      // react-hooks/set-state-in-effect on that line only, with a comment saying why."
      // Error for new projects; a project may keep it at warn for existing debt.
      'react-hooks/set-state-in-effect': 'error',
      // "Never t(key, { defaultValue: … })"
      // A later block that sets no-restricted-syntax with options replaces this selector:
      // repeat it there.
      'no-restricted-syntax': [
        'error',
        {
          selector: "CallExpression[callee.name='t'] Property[key.name='defaultValue']",
          message: 'No defaultValue: add the key to the translation files.'
        }
      ]
    }
  }
]
