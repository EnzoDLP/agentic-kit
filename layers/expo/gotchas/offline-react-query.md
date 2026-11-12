# React Query on React Native — onlineManager, NetInfo, stale cache after a migration

The general React Query pitfalls are in the `react` layer's gotchas.

- **`onlineManager` wired to NetInfo: `isConnected` only, never `isInternetReachable`**. NetInfo's
  reachability test calls a Google URL; when it fails (a network that blocks it, a TLS error such
  as every HTTPS call failing in a simulator), React Query pauses **all** queries and mutations,
  with no error and no "offline" screen: buttons stop doing anything. When truly offline, the
  app's own offline screen already covers the app.
- After a migration that adds a column: restart the app (`simctl terminate` then `launch`); Fast
  Refresh keeps the React Query cache.
