# React — components, effects and state

- **Never a synchronous `setState` in a `useEffect`** to reset or derive state
  (<https://react.dev/learn/you-might-not-need-an-effect>):
  - reset when something changes (a modal opening, a prop) → **remount**: the child holding the
    state is rendered only when needed, or gets a `key` that changes, and initializes with
    `useState(initialValue)`;
  - derive a value → compute it during render;
  - mirror a route into a store → in the navigation handler, or read the route where the value is
    used;
  - resolve a promise to derive a value → React Query;
  - an effect synchronizes with an **external** system (SDK, subscription, timer), never drives
    React state.
  - A **truly unavoidable** case (e.g. `react-hook-form`'s `reset()` on new server data): disable
    `react-hooks/set-state-in-effect` **on that line only**, with a comment saying why; never the
    rule globally.
- **Memoization depends on the project**:
  - **React Compiler enabled**: no `memo` / `useCallback` / `useMemo` by default; optimize only
    after measuring. Its ESLint rules (`react-hooks/refs`, `immutability`, `purity`,
    `set-state-in-effect`, `preserve-manual-memoization`) may stay at warning for existing code;
  - **without React Compiler**: `useCallback` / `useMemo` / `memo` with stable dependencies when
    they really help, never preemptively.
- Components: `export default function ComponentName(props: Props)`, typed props. A component
  **renders** (props in, events out), with no data fetching or business logic; a container (or a
  page) orchestrates.
- Principle: small single-responsibility pieces, composed; readability before cleverness.
- Network errors: messages the user can read, never the raw error.

## Loading, error, empty

- Never replace the **whole** page (header and filters included) with a spinner through an early
  return: loading takes the place of the content only (skeleton, empty state of the list). The
  real controls show right away.
- **A loading placeholder appears only after 300 ms**, then fades in: a shorter load makes
  nothing flicker (a skeleton and the card around it are delayed together).
- `data === undefined` tells the first load from a refetch; a refetch never replaces data already
  shown.

## Forms and files

- **A picked file (photo, attachment) is uploaded when the item is saved, never when it is
  picked**: otherwise every replaced file or cancelled form leaves an orphan in storage.
  Exception: a file that always overwrites the same location (an avatar) may upload on pick.

## Stores (Zustand)

- Read in a component through a **selector** (`useStore((s) => s.x)`), never the whole store;
  outside React: `useStore.getState()`. Cross-cutting state only.
- **Never server data in a store** (that is React Query), never ephemeral UI state in React Query.
- Persisted store (`persist`, saved on the device or in the browser): a field removed, renamed or
  retyped → **migration** (`version` + `migrate`, data read as `unknown`), otherwise existing
  users read back a broken shape; a field added → a default value. Routing waits for hydration
  (`persist.hasHydrated()`).
