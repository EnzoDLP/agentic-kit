# App Store and Google Play compliance

What has caused a rejection, a binary rejection or a blocked submission for Expo / React Native
apps, and how to never hit it again. Each rule carries its source:

- **[seen]**: a rejection actually received;
- **[rule]**: a requirement documented by Apple or Google, not yet hit, to follow from the start.

Guideline texts change: when in doubt, reread the current
[App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) and
[Play Console policies](https://support.google.com/googleplay/android-developer/topic/9858052).

---

## 1. Before every submission — checklist

Run it for every store build, even a small fix.

**Code and binary**

- [ ] No dev tool in the store build: no screen, no route, no label (§2.1).
- [ ] No feature that a remote setting can **show or hide** (§2.1).
- [ ] Sign in with Apple: Apple's official button on every sign-in button, and never the name or
      email asked again afterwards (§2.2).
- [ ] No dead button: a disabled button looks disabled, otherwise it does something (§2.8). Flow
      tried on iPad if the app is available there (`supportsTablet`).
- [ ] Every declared permission matches a real feature, with a precise usage text (§2.5, §3.1).
- [ ] The text of the paywall and of the screens before it matches the configured offer
      **exactly** (trial, price, duration) (§2.3).
- [ ] `git log --oneline -1`: the built commit is the right one (EAS builds the HEAD at launch time,
      without warning).

**App Store Connect / Play Console**

- [ ] Review notes: how to reach each feature, a demo account if sign-in is required, and a
      description of any remote configuration (§4).
- [ ] App Privacy questionnaire / Data safety form up to date with the SDKs actually integrated.
- [ ] Age rating consistent with **all** displayable content, including content from an external
      source (§2.6).
- [ ] Terms and privacy policy links valid, in the app and in the store listing.

**During review**

- [ ] Touch **no** remote configuration (feature flags, kill switches, minimum version) until the
      review is over.

---

## 2. Apple — App Review

### 2.1 Guideline 5.6 — "features hidden during review" **[seen]**

Wording: _"the app contains features that appear to have been intentionally hidden during the
review process"_. Apple **never** says which one. It is a serious rejection that affects trust in
the developer account, but it is resolved with a transparent answer and a new build.

Apple reads the **binary**, not only the screen. What triggers this rejection:

- **A remote switch able to make a feature disappear** (`HIDDEN`, a feature flag that removes a
  card, a menu entry…). Even set to "visible" during review, the mechanism is in the code.
- **Dev tools only hidden** in the store build (a "Dev" settings section hidden by a runtime
  condition): their labels stay in the bundle.
- **A dev route**: with Expo Router, every file in `app/` is a route of the production build, which
  a deep link can open even with no button leading to it.

Rules:

- A remote switch only **closes** a broken feature, and the closing is **visible** ("temporarily
  unavailable"). Never a disappearance, never an unlock.
- Dev tools are removed **from the code** of the store build, not hidden. With Expo: an
  `EXPO_PUBLIC_APP_VARIANT` variable set in every `eas.json` profile is inlined at build time, and
  the minifier removes dead code:
  ```ts
  const devItems = process.env.EXPO_PUBLIC_APP_VARIANT === 'production' ? [] : [/* dev tools */]
  ```
  Check: `APP_VARIANT=production EXPO_PUBLIC_APP_VARIANT=production npx expo export --clear
--platform ios --no-bytecode`, then search the bundle for the dev labels. `--clear` is required:
  Metro's cache ignores a change of `EXPO_PUBLIC_*`.
- A lab or temporary test screen is deleted (route included) as soon as it has served its purpose.
- Describe any remote configuration in the review notes (§4).
- **Anything that works out of the user's sight** is described too (an off-screen web view reading
  a product link the user pasted). Described precisely in the reply to the rejection (what it
  loads, for how long, no cookies, no affiliation), the 5.6 was lifted without removing anything.

**Guideline 2.5.19 [rule]** (added in October 2026, restating 2.3.1): _"Don't include any hidden,
dormant, or undocumented features in your app"_; hiding a feature in the binary (obfuscated code or
otherwise) means removal of the app and closure of the account. With **2.3.1(a)**: every new
feature is described **precisely** in the review notes (a generic description is refused) and
reachable by the reviewer. OTA updates remain allowed for fixes, never to add a feature the review
has not seen.

### 2.2 Guideline 4 — Sign in with Apple **[seen]**

Wording: _"Sign in with Apple button includes logo artwork that is not downloaded from Apple Design
Resources"_. Rejected form: a **text** option "Continue with Apple" in a system action sheet, on
the welcome screen. The wording also targets any **redrawn Apple logo** (custom SVG): avoid it the
same way.

Rule: every Sign in with Apple entry goes through the native `AppleAuthenticationButton` from
`expo-apple-authentication` (logo, font, label and translation provided by iOS). Wrap it in a
shared component (e.g. `AppleSignInButton`), never draw the logo yourself. It must be at least as
visible as the other sign-in buttons (same size).

- The neighboring Google button is its **twin**: a `GoogleSignInButton` copies the rendering of
  Apple's button (47 pt capsule, which is what Apple draws in a 50 pt frame; 16 pt logo), since
  Apple's button cannot be restyled.
- Outside sign-in buttons, a settings row "Apple — linked / not linked" in an account-linking
  screen kept an SVG logo and passed review.

**Never ask again for what Sign in with Apple provided [seen]**: _"users are required to provide
their name and/or email address after using Sign in with Apple"_. A new account created through
"Sign in" with Apple landed on the onboarding's "Your first name" step. Rules:

- After an Apple sign-in (or Google, for consistency), onboarding skips any name or email step. A
  nickname is still allowed: it is neither a name nor an email.
- The name comes from `credential.fullName` (`AppleAuthentication.formatFullName`). Apple gives it
  only on the **first** authorization: store it on the account right away
  (`supabase.auth.updateUser({ data: { full_name } })`); Supabase does not receive it in the token.
- Without a name (authorization already given once), plan a fallback (the nickname), never a
  question.
- Test on device: iOS Settings → Apple account → Sign in with Apple → the app → "Stop using", so
  that Apple gives the name again.

**[rule] Guideline 4.8**: an app that offers a third-party sign-in (Google, Facebook…) must also
offer Sign in with Apple, or an equivalent privacy-respecting sign-in.

### 2.3 Guideline 3.1.2 — subscriptions **[seen, fixed before rejection]**

The screens before the paywall, copied from another project, promised a free trial that did not
exist in the offer. Announcing terms that do not match the product is grounds for rejection.

- The text of every purchase screen matches the **real** configured offer (RevenueCat, App Store
  Connect). Changing the offer = rereading those screens.
- **[rule]** The paywall shows title, duration, price, auto-renewal and how to cancel, with links
  to the terms (EULA) and the privacy policy. Those links also appear in the App Store listing.

### 2.4 User-generated content (guideline 1.2) **[rule]**

Any app where users publish content visible to others (reviews, comments, profiles) must have,
from the first submission:

- a "Report" action on every piece of content;
- a "Block" action on a user, which hides their content;
- a contact address in the app and in the store listing.

### 2.5 Permissions and usage texts **[seen, fixed before rejection]**

- **No permission without a feature.** `expo-image-picker` declares camera and microphone by
  default: `cameraPermission: false` and `microphonePermission: false` in its plugin if the app
  only picks a photo (`false` removes the key from `Info.plist`).
- Each usage text says precisely **why** ("to choose your profile photo").
- **ATT**: ask at the right moment (after showing value, on the tap of the first CTA), with
  `NSUserTrackingUsageDescription`. **Never two system prompts in a row** (ATT then
  notifications): the second is refused by reflex.
- **Privacy manifest**: `PrivacyInfo.xcprivacy` is generated by Expo. Careful:
  `NSPrivacyTracking: true` requires `NSPrivacyTrackingDomains`, and iOS then **blocks** requests
  to those domains until ATT is granted (attribution and postbacks included). Weigh that cost
  before changing it; the declaration also goes through the App Privacy questionnaire.
- **Account deletion [rule, guideline 5.1.1(v)]**: any app that allows creating an account must
  allow deleting it **from the app**.

### 2.6 Age rating **[seen]**

The App Store Connect questionnaire blocks any app that ticks anything other than "None" for
sexual content. An app that shows an **external catalog** (games, films, books) potentially shows
all of its content: filter at the source (e.g. IGDB: exclude the "Erotic" theme,
`themes != (42)`) rather than under-declare.

### 2.7 Binary rejections (`ITMS-…`) **[seen]**

- **They arrive by email, asynchronously.** `eas submit` succeeds, EAS shows "finished", and
  nothing appears in App Store Connect: check the Apple account's mailbox, not the EAS logs.
- **`ITMS-90361`**: `NSExtensionActivationSupportsText` is a **boolean** (`true`), never `1`.
  Plugins often pass the object as is to the plist: a `1` becomes `<integer>1</integer>`. The
  `…WithMaxCount` keys do expect a number.
- **SKAdNetwork**: an **advertised** app (one that buys ads) does not declare `SKAdNetworkItems`,
  only `NSAdvertisingAttributionReportEndpoint` (see Apple's "Configuring an advertised app").
  `SKAdNetworkItems` is for apps that **show** ads.

### 2.8 Guideline 2.1(a) — a button that does nothing **[seen]**

Seen on iPad Air, iPadOS 27: _"When we tapped 'Continue' at 'Choose a profile picture' page, it
produced no further action"_. The button was disabled until a photo was chosen, but a glass button
tinted black at 70% opacity looks active.

- A button that cannot act looks disabled; otherwise it does something. An optional step moves on
  without the data ("Continue" = "Later").
- App Review often tests on **iPad** when the app is available there: run the onboarding there
  before submitting.

---

## 3. Google Play

### 3.1 Photo and video permissions **[seen]**

Rejection under the "Photo and video permissions" policy: an app targeting API 33+ may declare
`READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` only if media access is its core function. The system
photo picker is enough for an avatar.

- `expo-media-library` declares those permissions by default: `granularPermissions: []` in its
  plugin if the app only **saves** an image.
- Safety net against a dependency that would add them back: `android.blockedPermissions` on
  `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_MEDIA_AUDIO`.

### 3.2 `ACTIVITY_RECOGNITION` permission **[seen]**

`expo-sensors` declares it for its pedometer. Its presence makes Google require the **health apps
declaration**. If the app only uses the accelerometer or orientation (which need no permission):
`android.blockedPermissions` on `android.permission.ACTIVITY_RECOGNITION`.

General rule: with every new native dependency, read the merged manifest (`npx expo prebuild`, then
`android/app/src/main/AndroidManifest.xml`) and block every unused permission.

### 3.3 App Links and Play App Signing **[rule]**

Once the app is published with Play App Signing, Google re-signs the APK with its own key: add the
Play Console's "App signing key" SHA-256 to `assetlinks.json`, **in addition** to the EAS
keystore's. Otherwise `https://<domain>/…` links no longer open the app in production.

### 3.4 Required forms **[rule]**

- **Data safety**: reflect every SDK (analytics, attribution, crash reporting, payment).
- **Account deletion**: on top of deletion in the app, Google requires a **web link** where users
  can request deletion of their account, entered in the Play Console.

### 3.5 Release build failures **[seen]**

`:app:lintVitalRelease` fails on `[ExtraTranslation]`: `expo.locales` (meant for the iOS
`Info.plist`) is also copied by the Android plugin into `values-b+<lang>/strings.xml`, with no
default value. Fix: put the keys under `"ios": { … }` in each `locales/<lang>.json` (the plugin
gives each platform only the root and its own section). Alternative: a small config plugin that
sets the English default in `values/strings.xml` (`withStringsXml` +
`AndroidConfig.Strings.setStringItem`).

---

## 4. Review process

### Review notes (every submission)

Always describe:

- how to reach each important feature (screen path);
- a demo account if part of the app requires sign-in;
- **any remote configuration** (kill switch, maintenance, minimum version): what it can do (close,
  never reveal) and its current state.

Example used successfully after a 5.6 rejection:

> All features are available to every user without an account. [Path to the features.] A
> server-side setting can temporarily mark [feature] as unavailable if [third-party service]
> breaks. It then stays visible with a warning message, and nothing can be hidden or unlocked
> remotely. Everything is currently available. Internal developer tools have been removed from this
> build.

### Answering a rejection

- **Reply in App Store Connect first, and only then send a new build.** Sending a build closes the
  current conversation and sends you to the back of the queue. A build that fixes nothing of what
  was asked can look like fishing for another reviewer, especially after a 5.6.
- Be factual and transparent: describe precisely the suspected mechanism, do not deny wholesale.
  Ask which feature is targeted if the rejection does not say.
- Observed delays: from a few days to more than a week without an answer. Beyond that: the form
  <https://developer.apple.com/contact/app-store/> → "appeal an app rejection or app removal" (the
  only fitting topic; there is no "status request"). Worded as a request for explanation, not a
  dispute ("we are not disputing the decision: we simply want to understand it"), it unblocked a
  review after 7 days of silence: 5.6 lifted, new build requested. One appeal per rejection.
- **Expedited review** (same form) only applies to a build waiting for review: keep it for the
  build that follows the lifted rejection, with the reason (season, event).
- **"Bug Fix Submissions"**: some rejections are marked as fixable in the next update. Replying
  that the version contains bug fixes is enough to get it approved, without a new build. (Fixing
  and resubmitting remains possible if the answer is slow.)
- If the rejection is wrongly upheld: appeal to the App Review Board.

### Builds

- EAS builds the HEAD at launch time: `git log --oneline -1` first, and
  `eas build --platform ios --profile production --auto-submit` to chain the submission.
- A production build talks to the **production** backend: deploy any migration or server function
  it depends on **before** testing it in TestFlight.
- Before submitting, test it in TestFlight on the affected flows.
