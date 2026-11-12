# Expo — conventions

## Naming

| Item      | Convention                                                                  | Example                    |
| --------- | --------------------------------------------------------------------------- | -------------------------- |
| Component | PascalCase, file = component name, no role suffix                           | `CardNote.tsx`             |
| Container | PascalCase, no suffix, in `containers/`                                     | `containers/Note.tsx`      |
| Route     | kebab-case                                                                  | `app/(main)/note/[id].tsx` |
| Service   | `[feature].service.ts`                                                      | `notes.service.ts`         |
| Queries   | `queries/[feature]/constants.ts`, `query-options.ts`, `mutation-options.ts` | `NOTES_QUERY_KEYS`         |

## Styles

- **Inline** styles (`style={{ … }}`); no `StyleSheet.create` in new code, except
  `StyleSheet.hairlineWidth` / `StyleSheet.absoluteFill`.
- **No hardcoded color, font size or spacing**: everything comes from the project's tokens (e.g.
  `Colors`, `Typography`, `Spacings`, `Radii`). A missing token is added **named by its role** (not
  `white` / `black`). Exceptions: decorative gradients, third-party brand colors, values passed to
  native code. Typography lives in one typed file (e.g. `constants/Typography.ts`,
  `as const satisfies Record<string, TextStyle>`); the themed text component only applies it.

## Tests

- Jest **without** a framework preset (`jest-expo` conflicts with the React Native patch version):
  `babel-preset-expo` compiles TypeScript and the `@/` alias. **Pure functions only**, no component
  or hook tests. A util that imports a native module is not tested: move its logic out.
- UI and native behavior (rendering, keyboard, paywall, images, haptics, sensors) are checked on
  the simulator, then on a device, and in a lab when needed.

## i18n

Files `public/locales/<lang>/translation.json`.
