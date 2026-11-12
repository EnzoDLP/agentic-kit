# TanStack Table

## Interactive cells flicker on every render

- `flexRender(columnDef.cell, ctx)` renders a `cell` function **as a React component**. Columns
  rebuilt on a render (a `useMemo` whose dependency changes: a callback, a `?? []` or
  `Object.values()` fallback, an `isUpdating` flag) give every cell a new component type: React
  **remounts every cell**, and selects or inputs flicker, close, or lose focus and state.
- Define the columns **once** (module constant, or a memo on `t` only) with named cell components,
  and pass what changes through a React context (or `table.options.meta`) that the cells read.
- Regression test: render, keep `getAllByRole('combobox')`, re-render with new props, check they
  are the same nodes (`toBe`).
