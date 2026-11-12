# Builds, config and tooling (EAS, prebuild, native modules, Metro, lint)

## EAS and local builds

- **SDK 58: EAS Android build stuck on Skia** (free machine, 4 vCPU / 15.6 GB, Skia 2.14): "Gradle
  build daemon disappeared unexpectedly", or a silent log then cancellation at the limit (45 min
  on the free plan, `buildDuration` in `eas build:view --json`), always at the start of
  `shopify_react-native-skia:buildCMakeDebug`; in production (release, 4 ABIs) the daemon
  disappears earlier, in `react-native-worklets:buildCMakeRelWithDebInfo`. Neither
  `android.buildArchs: ['arm64-v8a']` nor `org.gradle.workers.max=1` (a `withGradleProperties`
  plugin under `EAS_BUILD`) changes anything; at SDK 57 the same machine passes (Skia 2.6, 22 min),
  and so does `expo run:android` on the Mac. Do not burn builds trying: `eas build --local` (same
  profile, same EAS variables and credentials, on the Mac, `ANDROID_HOME` exported), then
  `eas upload --platform android --build-path <apk>` for an install link on expo.dev (no cable, no
  EAS build), or `eas submit --path` for the store. It copies the project into a temporary folder:
  ~15 GB free ("No space left on device" otherwise, in the middle of copying Skia's libraries).
- A build's log downloads through `logFiles` (Brotli: `zlib.brotliDecompressSync`), JSON per line
  with its `phase`.
- `buildArchs: ['arm64-v8a']` stays useful in dev: phones and emulators of an Apple Silicon Mac
  (`abi.type` in the AVD's `config.ini`).
- `expo run:android` from an agent session: "SDK location not found" after a `prebuild --clean`
  (it deletes `android/local.properties`, and the session's shell has no `ANDROID_HOME`). Run with
  `ANDROID_HOME=$HOME/Library/Android/sdk`, without writing any file in `android/`.

## Native modules

- **An added native module breaks the existing dev client at startup**, even if only used in a
  screen never opened: expo-router loads every route at launch
  (`TurboModuleRegistry.getEnforcing(...): 'RNSkiaModule' could not be found`). Build the new dev
  client before reloading the app; with EAS Update, that JS must never go to a build that lacks
  the module.
- `@shopify/react-native-skia` 2.x pulls its prebuilt binaries as npm packages
  (`react-native-skia-apple-ios`, `-android`, `-apple-macos`, `-apple-tvos`): ~750 MB in
  `node_modules`, plan for it on a tight disk.
- `react-native-view-shot` (5.1 and 6.1): on iOS, the options' `width` / `height` are in
  **points**, multiplied by the screen density (`rendererFormat.scale = 0`); on Android, in pixels.
  A poster requested at 1080×1920 came out at 3240×5760 (12 MB) on a 3x iPhone: divide by
  `PixelRatio.get()` on iOS only, and check the captured file's size (`sips -g pixelWidth`).
- A patch that replaces a whole file (`patches/` + `postinstall`) can become wrong after a version
  upgrade with no build error.

## Permissions and locales

- **`locales` (iOS permission texts) breaks the Android release build**: a key at the root of a
  `locales/<lang>.json` file also goes into `values-b+<lang>/strings.xml`, missing from the default
  `values/strings.xml` → `lintVitalRelease` fails (`[ExtraTranslation]`), invisible in dev (SDK
  58, after a 21-minute compile). Put the keys under `"ios": { … }` (and `"android"` for the other
  platform): the plugin gives each platform only the root and its own section
  (`getResolvedLocalesAsync`, also at SDK 57). Alternative: a `withStringsXml` plugin that sets the
  default values.
- Translated iOS permission texts: `locales: { fr: './locales/ios/fr.json', en: … }` at the `expo`
  level (`NS…UsageDescription` keys, written as `InfoPlist.strings` at prebuild); the plugins' text
  stays the base (language of `CFBundleDevelopmentRegion`). Check without a build:
  `npx expo config --type introspect --json` (`_internal.modResults`).
- `microphonePermission: false` on `expo-image-picker` also removes `RECORD_AUDIO` from the
  Android manifest (`tools:node="remove"`), whatever `android.permissions` or `expo-camera`'s
  `recordAudioAndroid` say.

## Environment variables

- Metro's cache ignores a change of `EXPO_PUBLIC_*` (same bundle hash): `--clear`.
- `process.env.APP_VARIANT` is `undefined` inside the app: a `disabled: APP_VARIANT !==
'production'` turned PostHog off **in every build**. Read `EXPO_PUBLIC_APP_VARIANT` in app code.
- A file already tracked by git stays tracked despite `.gitignore` (a committed `.env`).

## Tooling

- **`expo lint` without arguments only lints `src/`, `app/` and `components/`** (the CLI's
  `DEFAULT_INPUTS`): with code at the root, `containers/`, `hooks/`, `queries/`, `services/`,
  `utils/`… are never linted, not even by this layer's ESLint preset. Script
  `"lint": "expo lint ."` (or `eslint .`); `npx eslint .` shows what was waiting.
- `npx expo install` of a package with thousands of files (`@expo/material-symbols`) started ~1,700
  VS Code `rg` processes: `pkill -f ripgrep-universal` then "Reload Window".
