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

## A number column sorts descending on the first click

- **`column.toggleSorting()` with no argument starts a number column in descending order**
  (TanStack Table 8.21): with `sortDescFirst` unset, the first direction is picked from the first
  row's value, descending for a number, ascending for a string. A header that should sort every
  column ascending first then flips only on its number columns, and `manualSorting` does not
  change it (the state still goes through `toggleSorting`).
- Set `sortDescFirst: false` in `useReactTable` options (or on the column def). With
  `enableSortingRemoval: false`, clicks then go ascending → descending → ascending.

## The page freezes on the first sort

- **A `data` array rebuilt on every render (`data: sortRows(rows, sort)`, `rows.filter(…)`) makes
  an endless render loop** (TanStack Table 8.21, React 18): each new `data` recomputes the core
  row model, which queues `resetPageIndex()` (`autoResetPageIndex`, on by default without
  `manualPagination`), a state update that renders again with yet another `data`. It starts as
  soon as the array stops being the same reference (e.g. a client sort that copies only once a
  column is sorted). A real click runs it at sync priority and freezes the tab; a simulated click
  (Testing Library, Storybook) lets it yield, so tests stay green.
- Keep `data` stable: `useMemo` on its real inputs. `autoResetPageIndex: false` also stops it on a
  table with no pagination, but leaves the extra row-model rebuilds.
- Regression test in a browser story under `StrictMode`: count commits with a React `Profiler`,
  click a sort, wait, check the count stops growing.
