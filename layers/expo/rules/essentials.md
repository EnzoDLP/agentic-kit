# Expo — essentials

> Details load on demand: startup, splash, version gating, auth, onboarding, app variants, OTA →
> skill `expo-app-shell`; Liquid Glass, `@expo/ui`, native headers, animations, gestures → skill
> `expo-native-ui`; SDK upgrade → `expo-sdk-upgrade`. The _why_ is in this layer's gotchas files
> (`.claude/agentic-kit/layers/expo/gotchas/`).

## Versions and build

- **Every** dependency through `npx expo install <pkg>` (never `npm install`); `npx expo install
--check` and `npx expo-doctor` before every EAS build. No pinned version without a reason written
  in the project's docs. `node -v` = `.nvmrc` before any `npm`.
- **Never trust memory of an Expo API**: read the versioned docs of the project's SDK
  (`https://docs.expo.dev/versions/v<SDK>.0.0/`). No `@react-navigation/*` dependency (expo-router
  bundles it).
- `ios/` and `android/` are generated: every native change goes through `app.config.js`, a config
  plugin, `targets/` or `patches/`. Every native change needs a new build (dev client included). A
  file replaced through `patches/` is compared with upstream before any version upgrade.
- EAS builds the HEAD at launch time: `git log --oneline -1` before a production build. Before a
  store submission: `.claude/agentic-kit/layers/expo/reference/store-compliance.md`.
- `tsc` rejects a route that exists: `.expo/types/router.d.ts` is stale (`npx expo start`); do not
  cast.

## Screens and components

- The project's themed text component (never React Native's `Text`), **`expo-image`** (never
  React Native's `Image`; `cachePolicy="memory-disk"`, `key` + `recyclingKey={uri}` in a list), the
  project's buttons and inputs. Targeting iOS 26+: native control first (skill `expo-native-ui`).
- **No toast**: a success shows on screen, with haptics; an error goes through the project's error
  alert helper; a confirmation through a native `Alert`. Haptics, alerts and navigation are
  triggered from the container.
- **Never a React Native `Modal`** for content that can show while a native modal is open: a modal
  route, or `FullWindowOverlay`.
- **No bottom sheet**: a modal page (`presentation: 'modal'`, the project's modal page component),
  main action in the header (native `prominent` button). A multi-step modal has its own stack
  (`router.replace` within the same sheet); a value sent back goes through a modal result
  (subscription, no `setState` in an effect).
- Header: declarative `Stack.Toolbar` buttons (SF Symbols), never a custom view in `headerLeft` /
  `headerRight`.
- Router: never a `<Redirect>` nor a navigation during a layout's render; `app/+native-intent.ts`
  returns `null` for a link the app opens itself.
- Link input: `autoCapitalize="none"` + `keyboardType="url"`; single-line text:
  `numberOfLines={1}`.

## Judge on device, and what ships to the store

- Labs (N variants side by side) live in `containers/dev/*Lab.tsx`.
- **A lab or dev tool is never in the production bundle** (Apple reads the bundle, rejection 5.6):
  condition `process.env.EXPO_PUBLIC_APP_VARIANT === 'production'` written in the file itself. No
  feature that a remote setting can make disappear.
- **Two system prompts never follow each other** (ATT, notifications, photos, camera); never ask
  for notifications at launch. The current onboarding step is never set in an effect.
- Every `EXPO_PUBLIC_*` variable is also added to the EAS environments.
- Rating prompt (`expo-store-review`) only after a successful action, never at launch, during input
  or in onboarding.
- Payment and attribution → skill `expo-revenuecat`; analytics → `expo-posthog`; errors →
  `expo-sentry`.
