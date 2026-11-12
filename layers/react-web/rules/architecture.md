# React web — architecture and folder responsibilities

Each folder under `src/` has a single responsibility. Do not mix concerns across them.

- `src/components/`: pure visual components, no business logic.
  - UI rendering and user interactions only.
  - Receive data through props, emit events to the parent.
  - No data fetching.
- `src/containers/`: connect components to business logic (reusable).
  - State management, data fetching and transformation.
  - Turn API types into component props.
  - Minimal UI code; a container can be composed several times.
- `src/pages/`: top-level routes (one per route).
  - Same responsibilities as containers, but as route entry points.
  - Compose containers and components.
- `src/hooks/`: reusable custom hooks for shared logic.
- `src/queries/`: centralized API calls with TanStack Query, organized by domain (see the React
  Query rules of this layer).
- `src/stores/`: global state with Zustand.
  - Cross-component, cross-cutting concerns only.
  - Do not store large API payloads.
- `src/types/`: UI-facing types, simplified from the generated API types (see the generated API
  rules of this layer).
- `src/utils/mappers/`: pure functions mapping API types to UI types.
- `src/utils/enum-map/`: static lookup tables from a generated API enum to a UI concern (i18n key,
  color, icon).
  - One object per concern (`xxxLabelKeyMap`, `xxxColorMap`): a plain `Record<EnumType, ...>`, not
    a transformation function.
  - Kept apart from `src/utils/mappers/`: a mapper transforms an API object into a UI shape, an
    enum map is a static lookup table. Do not merge the two.
  - Referenced directly by components, or by a shared mapper when the lookup needs further
    processing (see the i18n rules of the `react` layer).
- `src/themes/`: the UI library's theme (e.g. MUI `extendTheme`); no component logic.
- `src/styles/`: global CSS (fonts, resets, third-party widget overrides the UI library cannot
  express).
- `src/app/`: application bootstrap: provider tree, router, API client and auth wiring (used once,
  not a reusable pattern).
