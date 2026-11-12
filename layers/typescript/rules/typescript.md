# TypeScript — language and conventions

- `strict: true`; never relax a compiler option to silence an error.
- **No `any`** (no `as any`, no `@ts-ignore`): truly unknown data → `unknown` + narrowing (or a
  tested `parse…` function); a SQL enum → its generated type; a typed route → its type (`Href`),
  never `as never`. A truly unavoidable case (untyped third-party library): disabled on its line
  only, with a comment saying why.
- `interface` for component and hook props (`interface Props`, `interface UseCartTotalsProps`);
  `type` for domain models, unions and enum-like values. Props as `Readonly<…>` (or `readonly`
  fields) when nothing is mutated.
- Explicit return types on functions exported from services and utils.
- A **generated** file (API client, database types, route types) is never edited by hand.
- Imports: the `@/` alias across folders, relative only within the same folder (`./x`), never
  `../`. **No `index.ts` barrel files**: import the target file directly. External imports first,
  then internal ones, sorted.
- **Prettier**:

  ```json
  { "semi": false, "tabWidth": 2, "printWidth": 100, "singleQuote": true, "trailingComma": "none" }
  ```

- No `console.log` in production; `console.error` / `console.warn` tolerated in the `catch` of a
  third-party SDK call whose failure must not block the user.
- **Colocation**: a helper used by a single module stays in its file; if it does not depend on
  props or state, it is defined **at module level** as `function name() {}` (hoisted, named in
  stack traces). A handler that captures props or state: `const name = () => {}`.

## Shared naming

| Item                | Convention                                         | Example               |
| ------------------- | -------------------------------------------------- | --------------------- |
| Hook                | `use` + name, `.ts` (`.tsx` only with JSX)         | `useBottomPadding.ts` |
| Util                | `[name].util.ts`, one export, test next to it      | `formatPrice.util.ts` |
| Store               | `[name].store.ts`, default export `use[Name]Store` | `onboarding.store.ts` |
| `persist` key       | `[name]-storage`, **never renamed** (data loss)    | `onboarding-storage`  |
| Enum                | `Enum[Name]`, SCREAMING_SNAKE values               | `EnumCurrency.EUR`    |
| Constant            | SCREAMING_SNAKE                                    | `MAX_FILE_SIZE`       |
| Variable / function | camelCase                                          | `formatPrice`         |
| Props               | booleans `is…` / `has…`, events `on…`              | `isOpen`, `onPress`   |
| Analytics event     | snake_case                                         | `onboarding_click`    |

Naming of components, containers and files by role depends on the platform: see the expo and
react-web layers' rules.
