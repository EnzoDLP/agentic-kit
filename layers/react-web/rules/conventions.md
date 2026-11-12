# React web — conventions

## File naming

Suffix files by their role: `*.container.tsx`, `*.page.tsx`, `*.util.ts`, `*.type.ts`,
`*.config.ts`, `*.mapper.ts`, `*.map.ts`, `*.stories.tsx`, `*.test.tsx` / `*.test.ts`. Components
are default-exported function components (`export default function ComponentName(props: Props)`).

## Tests

- Vitest. Beyond pure functions (see the testing rules of the `typescript` layer), **mutation and
  data hooks are tested** (`hooks/api/<domain>/useXxx/useXxx.test.ts`, next to the hook), and
  components are covered through **Storybook** stories (`*.stories.tsx`, Storybook test runner).

## i18n

Translation files live at `public/locales/{lang}/translation.json` (keys and language rules: the
i18n rules of the `react` layer).
