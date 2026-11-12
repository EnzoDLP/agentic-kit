---
name: expo-revenuecat
description: Integrate or change RevenueCat in an app — Pro subscription, paywall (RevenueCatUI), entitlement, offerings, purchase restore, gating Pro features, offer or trial wording — plus the AppsFlyer attribution and ATT prompt wired to it. Use whenever payments, the paywall, "Pro", AppsFlyer or ATT are touched.
---

# RevenueCat (+ AppsFlyer / ATT)

Pitfalls: the `expo` layer's pitfalls (`.claude/agentic-kit/layers/expo/gotchas/`), third-party
services section (REST API v2 on the server). Store guidelines cited here:
`.claude/agentic-kit/layers/expo/reference/store-compliance.md`. The project states its entitlement,
its offerings, what Pro unlocks and its deviations in its own rules.

## RevenueCat

- Keys through `process.env.EXPO_PUBLIC_*`, never hard-coded.
- **Only in a production build on a real device** (`IS_REVENUECAT_ENABLED`: key +
  `Device.isDevice` + production build). Elsewhere (simulator, dev, preview) no SDK call at all: the
  app starts free, without a key, the paywall does not open; Pro is tested through a "Force Pro
  (dev)" toggle absent from the production bundle.
- **Trust the entitlement, not the paywall result**: a purchase or a restore only counts once
  RevenueCat confirms the entitlement is active (an empty restore returns "restored"). A wrong
  entitlement name = nobody is Pro, with no error.
- Paywalls from `RevenueCatUI`, configured remotely. Imperative `presentPaywall` by default, through
  a single project entry point that names the offering and the `source` (analytics). The
  `<RevenueCatUI.Paywall />` component bypasses `presentPaywall`: its side effects (analytics,
  checks) are rewired by hand, its `onDismiss` can arrive after a successful purchase (guard), and
  it **never goes inside a React Native `Modal`**.
- **No free trial promised in the UI unless it really exists** (App Store 3.1.2): wording of Pro
  cards and paywalls rechecked on every offer change. A legacy `*trial*` identifier is not a
  description of the offer.
- Offerings read by store builds stay as they are while any of those builds is supported. Paywalls
  follow the device language, not the app's.
- `Purchases.setLogLevel`: `WARN` / `ERROR` (`DEBUG` only occasionally).
- Pro status for a server or a website: read from RevenueCat by the server (REST API v2, webhook),
  never copied from the app.
- **A Pro feature that costs on the server** (upload, storage) is checked in the function that runs
  it, not only in the app: a shared module in `supabase/functions/_shared/` (e.g.
  `revenueCatProStatus.ts`, unit-tested), secrets `REVENUECAT_SECRET_KEY` (v2, read-only) and
  `REVENUECAT_PROJECT_ID`. The local stack (`SUPABASE_URL` as `http://kong:`) skips the check; the
  app turns Pro through the dev toggle.

## AppsFlyer + ATT

- Plugins `react-native-appsflyer` and `expo-tracking-transparency` (`userTrackingPermission`),
  `NSAdvertisingAttributionReportEndpoint: 'https://appsflyer-skadnetwork.com/'`. An app that
  advertises (and shows no ads): never `SKAdNetworkItems`.
- The AppsFlyer id is passed to RevenueCat (`syncPurchasesAppsFlyerAttribution`) and the IDFA is
  read again after ATT (`refreshPurchasesDeviceIdentifiersAfterAtt`); RevenueCat sends purchases to
  AppsFlyer itself. The app only sends the registration (`af_complete_registration`, once).
- ATT prompt on a tap after the value has been seen (e.g. the landing's main button), never right
  next to another system prompt. Returning users: on the tap on the "I already have an account"
  link, not on the Google / Apple buttons (their sign-in sheet would follow the ATT prompt).
- RevenueCat, AppsFlyer, PostHog and Sentry follow the same identity at the same moment.
- All AppsFlyer calls in one module (e.g. `lib/appsFlyer.ts`): key and App Store ID in
  `EXPO_PUBLIC_APPSFLYER_DEV_KEY` / `EXPO_PUBLIC_APP_STORE_ID` (EAS variables of the builds),
  **nothing without a key** (no `initSdk`, no identity, no event: the local case), a failure as
  `console.warn` under `__DEV__` only (a `console.error` shows a red banner in dev). Never an "app
  opened" event: AppsFlyer counts sessions.
