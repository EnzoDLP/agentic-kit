---
name: expo-posthog
description: Add or change PostHog analytics in an app — client, provider, events, funnels, tracking helpers, user identification. Use whenever analytics, tracking, an event, a funnel or PostHog comes up.
---

# PostHog

The project states its helpers and its events in its own rules.

- Key through `process.env.EXPO_PUBLIC_*` (or the web equivalent), host of the project's region
  (EU or US).
- Client created **only in a production build with a key**, `null` otherwise: the app runs
  without a key and every helper does nothing. Read the client through the project's hook, not
  the SDK's (it throws without a provider).
- **No feature flags** (App Review 2.5.19: nothing enabled remotely):
  `disableRemoteFeatureFlags: true` in the client options. Without it, the SDK
  (`posthog-react-native` 4.x) downloads the flags on every launch and every `identify`
  (`preloadFeatureFlags` defaults to `true`). The SDK's own settings always load
  (`disableRemoteConfig` has no effect).
- **Typed helpers** (`trackOnboardingStepView`, `trackOnboardingClick`, `trackPaywallView`…):
  **no raw `capture()` in a screen** — add a helper.
- Events in **snake_case**; `source` values and screen names never renamed (funnels depend on
  them). Instrument only what answers an actionable question (funnel, paywall, purchase), not
  navigation or settings.
- An event that must not be lost if the app is killed right after (paywall viewed): `flush`
  immediately.
- Identity: the same as RevenueCat / AppsFlyer / Sentry, set in the same place; RevenueCat →
  PostHog integration through the `$posthogUserId` attribute.
- Nothing arrives outside a production build: check in PostHog after the release.
