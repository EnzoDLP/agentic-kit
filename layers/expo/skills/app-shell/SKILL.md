---
name: expo-app-shell
description: Startup, splash, version gating and maintenance, auth (anonymous then Google / Apple), onboarding, app variants (APP_VARIANT, EXPO_PUBLIC_*), dev tools kept out of the store bundle, eas.json, store review prompt and EAS Update in an Expo app. Load before touching the root layout, startup routing, onboarding, app.config.js, environment variables or OTA updates.
---

# Expo app shell — startup, auth, onboarding, configuration

Pitfalls behind these points: the `expo` layer's pitfalls
(`.claude/agentic-kit/layers/expo/gotchas/`), startup section. To check a startup frame by frame:
skill `expo-startup-check`. Store guidelines cited here:
`.claude/agentic-kit/layers/expo/reference/store-compliance.md`.

## Startup and splash

- Splash **held** as soon as the root layout loads (`preventAutoHideAsync`), hidden **once** by the
  landing screen, **on the next frame** (`requestAnimationFrame`: the screen is already drawn
  underneath), short fade, **8 s at most** (safety net). Never `hideAsync()` anywhere else. It waits
  for fonts, hydrated stores, network and what the screen shows — never for AppsFlyer, the offerings
  or a slow SDK.
- Do not route before persisted stores are hydrated (wrong screen).
- **Version gating** derived during render (`pending` / `maintenance` / `update-required` / `ok`),
  without `setState`: versions compared **field by field** (`'1.10.0' < '1.9.0'` as strings),
  **fails open** (failed request or unreadable version → the app starts). Maintenance: a boolean
  returned by the same RPC (a sentinel version only exists in old code). An outage is shown (a
  maintenance screen), never hidden.
- Startup navigation **once per mount**, never a module-level flag: Android recreates the screen
  while the app is open (font size, density) and React remounts everything in the same process.
- A lost-connection screen when NetInfo reports offline.

## Auth and onboarding

- **Anonymous sign-in first**, Google / Apple linking afterwards. Native Google: "Skip nonce checks"
  enabled on the Supabase provider — a **known security trade-off** (the free
  `@react-native-google-signin` library does not return the nonce, so token replay protection is
  weaker), accepted by the Supabase docs; revisit if the paid library or a web flow is adopted. The
  authenticated layout renders its children only when the session exists.
- The React Query cache is cleared when the user changes (sign-out, other account): keys are not
  prefixed by user.
- RevenueCat, AppsFlyer, PostHog and Sentry follow **the same identity at the same moment** (one
  place, mounted above both onboarding and the app).
- Onboarding: one route file per step, state in a persisted store, `router.replace` between steps.
  **The current step is never set in a `useEffect`**: in the navigation handler, or derived from the
  route. Steps keep their number (analytics, saved step): never renumber.
- **Resume or restart**: reopened mid-onboarding, the app opens on the landing; "Start" offers
  "Resume" (the saved step), "Restart" (an anonymous account is deleted and recreated, a linked
  account is never deleted) or "Cancel". The decision lives in a tested pure function.
- **Two system prompts never follow each other** (ATT, notifications, photos, camera…): the second
  gets refused by reflex. Never ask for notifications when the app opens: after an action that
  justifies it. ATT on a tap after the value has been seen (e.g. the landing's main button).
- i18n init is **synchronous** (language from `Localization.getLocales()`, the saved preference
  applied afterwards with `i18n.changeLanguage`): never an un-awaited `async` init.

## Configuration and variants

- `app.config.js` driven by `APP_VARIANT` (`dev` / `preview` / `production`). **Inside the app,
  `process.env.APP_VARIANT` is `undefined`**: only `EXPO_PUBLIC_*` variables are inlined in the
  bundle — the variant goes through `EXPO_PUBLIC_APP_VARIANT` / `extra`, read by one constants
  module.
- **Dev tools absent from the production bundle, not just from the screen** (App Review 5.6): the
  condition `process.env.EXPO_PUBLIC_APP_VARIANT === 'production'` is written **in the file itself**
  (an imported constant is not folded at build time). Check before a store build:
  `expo export --platform ios --no-bytecode --clear`, then `grep` for the tool's label. No feature
  that a remote setting shows or hides.
- **A dev route does not ship in the store binary**: every file in `app/` is a route reachable by
  deep link, even an empty one. Either the tool stays an action in the dev settings, with no route,
  or the route is named `dev-…` and `metro.config.js` excludes it when `EXPO_PUBLIC_APP_VARIANT` is
  `production` (`resolver.blockList` limited to the `app/` folder; its `Stack.Screen` and links
  under the same condition). Verified by export: no trace in production, present in preview.
- Metro's cache ignores a change to an `EXPO_PUBLIC_*` variable: `--clear`.
- `.env` not committed + `.env.example` committed; every variable is **also** added to the EAS
  environments (development / preview / production), otherwise it does not exist in builds.
- iOS languages: every supported language in `CFBundleLocalizations`, `CFBundleDevelopmentRegion`
  set to the default one; Info.plist usage strings localized per language (the `locales` key of the
  app config), one per permission actually used.
- `eas.json`: `development` / `preview` / `production` profiles (`autoIncrement`,
  `appVersionSource: 'remote'`).

## Store review prompt

`expo-store-review` when the user is most satisfied (after a successful action), through a helper
that never fails towards the user. **Never** when the app opens, in the middle of input, or during
onboarding (guideline 5.6.1), and never two prompts for one gesture.

## OTA updates (EAS Update)

- An update that imports native code missing from the build crashes the app: native change → version
  bump → store build, never `eas update`.
- The dev client never reads updates; they are tested on `preview`, applied on the second launch.
  Publish to production after the migrations the JS depends on are deployed.
