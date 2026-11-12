# React Query

## Callbacks lost when the screen unmounts

- An invalidation can leave the screen before the `mutate` callbacks run: the factory's
  `onSuccess` waits for the refetch of active queries; if that refetch unmounts the screen,
  TanStack Query no longer calls the callbacks passed to `mutate`. Only mark the screen's query
  stale (`refetchType: 'none'`).
- Same trap when a form's data disappears (a deletion): keep the data from the moment the form
  opened in a state set during render (`if (data && !kept) setKept(data)`).
- **A form mounted with a `key` taken from the data it saves** (`key={rating?.id ?? 'new'}`) is
  remounted as soon as the mutation's `onSuccess` puts that data in the cache: the `mutate`
  callbacks, the state and the timers of the old instance are lost (an animation followed by a
  delayed close never happened). Use a stable key, with the initial state read once on mount.
