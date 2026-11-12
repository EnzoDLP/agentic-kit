---
name: expo-sentry
description: Integrate or change Sentry (error tracking, source maps, startup crashes) in an app. Use whenever Sentry, observability, crash reporting or source maps come up.
---

# Sentry

Pitfalls: the `expo` layer's pitfalls (`.claude/agentic-kit/layers/expo/gotchas/`), build, config
and tooling section.

- `@sentry/react-native` (or the web SDK); `Sentry.init` **at module load** of the root layout (a
  startup crash must be caught), only if the DSN exists (`EXPO_PUBLIC_SENTRY_DSN`, in all three EAS
  environments) — otherwise the SDK is inert and the app runs the same; the root exported as
  `Sentry.wrap(RootLayout)`.
- `enabled: !__DEV__` (free plan quota), `environment` set, `sendDefaultPii: false`,
  `tracesSampleRate: 0` until a question calls for it, a `beforeBreadcrumb` that strips the query
  string from URLs (tokens pass through them).
- User attached by **id only** (`Sentry.setUser({ id })`), in the same place as RevenueCat / PostHog
  / AppsFlyer; `setUser(null)` on sign-out.
- Plugin `@sentry/react-native/expo` in `app.config.js` for source map upload during the EAS build:
  `url` of the **org's region** (`https://de.sentry.io/` for the EU), `organization` / `project`
  from the environment, **never `authToken` in the config** (the plugin reads `SENTRY_AUTH_TOKEN` by
  itself). A test in dev only validates the DSN, never the upload.
- A "Test Sentry (dev)" button absent from the production bundle.
- Privacy policy and App Privacy: Sentry declared for logging technical errors.
