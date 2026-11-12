# React — React Query

Shared by every React project. `useQuery` or `useSuspenseQuery`, and where mutations live, depend
on the platform: see the expo and react-web layers' rules.

- **Never query options written inside a component or a hook**: reusable `queryOptions`
  factories, grouped by domain in `queries/<domain>/` (`constants.ts` for the keys,
  `query-options.ts` for the `create…QueryOptions` factories). Several components share the same
  options: React Query deduplicates and caches.
- **Keys**: `all` to invalidate a whole type, and for one entry a function that takes its
  parameters as an object and **derives its key from `all`** (`detail`, or a more telling name:
  `byId`, `search`…):

  ```ts
  export const USER_QUERY_KEYS = {
    byId: {
      all: ['userById'],
      detail: ({ userId }: { userId: string }) => [...USER_QUERY_KEYS.byId.all, userId]
    }
  }
  ```

  If TypeScript reports a circular reference (object `as const`), give the function an explicit
  return type rather than writing the key out by hand. A query derived from a domain descends
  from that domain's prefix, otherwise it escapes invalidations. Existing hand-written keys stay
  as they are (aligned when the file is touched).

- `enabled` lives in the factory when it depends only on its parameters; spread the options
  (`{ ...createX(…), enabled }`) only to override a field from the caller.
- **Default `staleTime` in the `QueryClient`** (`defaultOptions.queries.staleTime`, 30 s by
  default): with 0, every screen mount and every return to the foreground refetches every query.
  A factory overrides it only for a reason: near-static data (catalog, configuration: several
  minutes) or data that must be fresh on every open (0).
- `select` for a real derivation (unwrapping a response envelope, projecting), not to copy.
- Invalidate through the same key constants; `invalidateQueries` by default. An optimistic update
  (`setQueryData`) only where the network wait is visible, in `onMutate`, returning `oldData` when
  it is absent, on **exactly** the query's key.
- **Never filter a paginated list client-side**: filter server-side; read a single item through
  its own call rather than from the loaded pages.
