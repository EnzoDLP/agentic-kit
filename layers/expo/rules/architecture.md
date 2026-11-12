# Expo — architecture

| Folder        | Does                                                                                                 | Does not                          |
| ------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------- |
| `app/`        | Routing **only**: route, params, navigation (`router.*`), layouts, options                           | Business logic, API calls, styles |
| `containers/` | Assembled screen: data (`queries/` factories or stores), orchestration, local state, alerts, haptics | Low-level styling                 |
| `components/` | Rendering, styling, visual feedback                                                                  | API calls, store access, business |
| `queries/`    | `queryOptions` / `mutationOptions`, keys, invalidations                                              | JSX, direct backend client calls  |
| `services/`   | Backend calls, snake_case → camelCase mapping                                                        | React, hooks, i18n                |
| `stores/`     | Persisted client state + setters, `persist` migrations                                               | Server state, native calls        |
| `utils/`      | Testable pure functions (native orchestrators apart, never in the same file)                         | React, hooks, JSX                 |

- **One screen = one file in `app/`** (bare routing) that renders a container. No `pages/` folder,
  no `hooks/api/`, no barrel files.
- **The container receives `on…Press` callbacks** and never knows the router:

```tsx
// app/(main)/note/[id].tsx
export default function NotePage() {
  const router = useRouter()
  const { id } = useLocalSearchParams<{ id: string }>()

  return <Note id={id} onBackPress={() => router.back()} />
}
```

- Containers never import each other: share a pure data file instead.
- **Containers never import `@expo/ui` directly**, only the project's components that wrap it (this
  is what allows an Android fallback component by component).
- Navigation shared by several layouts lives outside `app/` (which holds routes only).
