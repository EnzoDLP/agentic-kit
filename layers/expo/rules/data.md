# Expo — data

In addition to the React Query rules of the `react` layer.

- **`useQuery`, not `useSuspenseQuery`**: the screen handles its own states (skeleton,
  `data === undefined`); no route sets a `<Suspense>` / `ErrorBoundary`. Default value of a list:
  `const { data = [] } = useQuery(…)`.
- **Mutations as factories**, not hooks: `queries/<domain>/mutation-options.ts` →
  `createXMutationOptions(queryClient)`, called by `useMutation(...)` in the container.
  **Invalidations live in the factory** (return the promise, `Promise.all`, so that `isPending`
  covers the refetch), including those of caches a server trigger feeds. **The factory never shows
  an alert** and reads no store: the container handles the UX in
  `mutate(body, { onSuccess, onError })` (alert, haptics, navigation). No `hooks/api/` folder.
- `setQueryData` goes in `queries/<domain>/set-query-data/<action>.ts`.
- A search run on demand is a mutation; a search whose results must change after another action is
  an invalidated query (`placeholderData: keepPreviousData`, input debounced in the handler, not in
  an effect).
