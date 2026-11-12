# React web — React Query (TanStack Query)

Applies to `src/{containers,pages,queries}/**`.

## Rules

Factories, keys derived from `all`, invalidation and `staleTime` are in the React Query rules of
the `react` layer. Specific to web apps:

1. `queryFn` / `mutationFn` always come from `src/generated/api-client/` (see the generated API
   rules of this layer).
2. Use `select: (data) => data.data` to unwrap the response envelope.
3. Prefer `useSuspenseQuery` with `Suspense` / `ErrorBoundary` to handle loading and errors
   declaratively; fall back to `useQuery` when there is no Suspense boundary.
4. Mutations live in hooks (`hooks/api/<domain>/useXxx/useXxx.ts`, tested), which invalidate
   through the domain's query key constants and show the user feedback (i18n keys, e.g.
   `action.*`).

## File structure

```
queries/
  <domain>/
    constants.ts        # Query key constants
    query-options.tsx   # Query option factory functions

hooks/
  api/
    <domain>/
      <useXxx>/
        useXxx.ts        # Mutation hook, invalidates via the domain's query key constants
        useXxx.test.ts
```

## Query keys

```typescript
// queries/user/constants.ts
export const USER_QUERY_KEYS = {
  currentUser: { all: ['user'] },
  byId: {
    all: ['userById'],
    detail: ({ userId }: { userId: string }) => [...USER_QUERY_KEYS.byId.all, userId]
  }
}
```

## Query options

```typescript
// queries/user/query-options.tsx
import { queryOptions } from '@tanstack/react-query'
import { USER_QUERY_KEYS } from './constants'
import { getUserApi, getUserByIdApi } from '@/generated/api-client'

export const createCurrentUserQueryOptions = () =>
  queryOptions({
    queryKey: USER_QUERY_KEYS.currentUser.all,
    queryFn: () => getUserApi(),
    select: (data) => data.data,
    staleTime: 5 * 60 * 1000
  })

export const createUserByIdQueryOptions = ({ userId }: { userId: string }) =>
  queryOptions({
    queryKey: USER_QUERY_KEYS.byId.detail({ userId }),
    queryFn: () => getUserByIdApi({ path: { userId } }),
    select: (data) => data.data,
    staleTime: 5 * 60 * 1000
  })
```

## Usage in components

With Suspense (preferred when available):

```typescript
function Dashboard() {
  const { data: user } = useSuspenseQuery(createCurrentUserQueryOptions())
  if (!user) return <Navigate to="/login" />
  return <div>{user.name}</div>
}

function DashboardPage() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<Spinner />}>
        <Dashboard />
      </Suspense>
    </ErrorBoundary>
  )
}
```

Without Suspense:

```typescript
function Dashboard() {
  const { data: user, isPending, error } = useQuery(createCurrentUserQueryOptions())
  if (isPending) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  if (!user) return <Navigate to="/login" />
  return <div>{user.name}</div>
}
```

Conditional query: spread the options and add `enabled`.

```typescript
function UserProfile({ userId }: { userId?: string }) {
  const { data: user } = useQuery({
    ...createUserByIdQueryOptions({ userId: userId! }),
    enabled: !!userId
  })
  if (!userId || !user) return null
  return <div>{user.name}</div>
}
```

## Mutations

Invalidate through the same query key constants:

```typescript
const { mutate: updateUserMutation } = useMutation({
  mutationFn: updateCurrentUserFn,
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: USER_QUERY_KEYS.currentUser.all })
    await queryClient.invalidateQueries({ queryKey: USER_QUERY_KEYS.byId.all })
    await queryClient.invalidateQueries({
      queryKey: USER_QUERY_KEYS.byId.detail({ userId: '123' })
    })
  }
})
```
