// ESLint flat-config block for Expo / React Native apps (expo plugin of the agentic kit).
// Copy this file into the project; change it in the kit, then copy it again.
//
// Usage in a project's eslint.config.js, after the base config (eslint-config-expo) and the
// typescript and react blocks of the kit, before the project's own rules (so a project can keep a
// rule at "warn" for existing debt):
//
//   const expo = require('./agentic-kit.expo.eslint.cjs')
//   // ESM: import expo from './agentic-kit.expo.eslint.cjs'
//   module.exports = defineConfig([expoConfig, ...typescript, ...react, ...expo, ...])
//
// With a themed text component named other than ThemedText:
//   ...expo.create({ textComponent: 'AppText', wrapperFiles: ['**/AppText.tsx'] })
//
// Uses ESLint core rules only: the base config needs no extra plugin for this block.
// A flat config replaces a rule's options instead of merging them, so this block repeats the
// typescript block's `../*` import pattern.
// Lint the whole project (`expo lint .`): `expo lint` alone skips folders outside src/, app/ and
// components/.

function create({ textComponent = 'ThemedText', wrapperFiles = ['**/ThemedText.tsx'] } = {}) {
  return [
    // Native folders are generated (Continuous Native Generation): never lint them.
    { ignores: ['ios/**', 'android/**'] },
    {
      files: ['**/*.tsx'],
      rules: {
        // "The project's themed text component (never React Native's Text), expo-image (never
        // React Native's Image)"
        'no-restricted-imports': [
          'error',
          {
            patterns: [{ group: ['../*'], message: 'Use the @/ alias across folders.' }],
            paths: [
              {
                name: 'react-native',
                importNames: ['Image', 'Text'],
                message: `Use expo-image's Image and the project's ${textComponent}.`
              }
            ]
          }
        ],
        // "Inline styles; no StyleSheet.create in new code" (warn: existing files are debt).
        // A separate rule from no-restricted-syntax, so the react block's defaultValue error
        // keeps its severity.
        'no-restricted-properties': [
          'warn',
          {
            object: 'StyleSheet',
            property: 'create',
            message: 'Inline styles; StyleSheet only for hairlineWidth / absoluteFill.'
          }
        ]
      }
    },
    // The wrappers themselves may import the primitives they wrap.
    {
      files: wrapperFiles,
      rules: { 'no-restricted-imports': 'off', 'no-restricted-properties': 'off' }
    }
  ]
}

const expo = create()
expo.create = create

module.exports = expo
