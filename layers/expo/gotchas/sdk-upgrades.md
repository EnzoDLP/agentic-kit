# Expo SDK upgrades — API changes and install pitfalls (SDK 57, 58)

The upgrade procedure itself is in the `expo-sdk-upgrade` skill.

## SDK 58

- **Node 20 is refused**: 22.13+, 24.3+ or 26 (`.nvmrc`); odd versions excluded.
- **Android, AGP 9**: `react-native-appsflyer` 6.18 breaks every build ("defaultConfig contains
  custom BuildConfig fields, but the feature is disabled"). Fix with a local config plugin that
  adds to the root `build.gradle`, **before** `apply plugin: "com.facebook.react.rootproject"` (it
  configures the modules as soon as it is applied), a `subprojects { … }` block setting
  `android.buildFeatures.buildConfig = true` for that module only. Never edit `node_modules`.
- `npx expo install expo@^58.0.0 --fix` can fail with code 1 on `Cannot find module
…/node_modules/expo/node_modules/@expo/config/build/index.js` (the tree is still being
  reorganized): the packages are installed; run `npx expo install --fix` again, which then lists
  the plugins to add by hand (still `@react-native-community/datetimepicker`, `expo-image`,
  `expo-status-bar`). It writes `expo` as `^58.0.0`: set it back to `~58.0.x`.
- Strict TypeScript API of RN 0.88: `useRef<TextInput>` → `useRef<TextInputInstance>` (same for
  `ViewInstance`…); no more deep imports from `react-native/Libraries/*`.
- RN 0.88 removes the `backgroundColor`, `translucent` and `networkActivityIndicatorVisible` props
  of `StatusBar`, `InteractionManager`, the `animated` prop of `Modal`, the root `Touchable`
  export; `keyboardShouldPersistTaps` no longer accepts a boolean.
- `expo-navigation-bar`: `setButtonStyleAsync` is gone → `<NavigationBar style="light" />` (color
  of the **buttons**, `light` in dark theme). No effect while the plugin keeps
  `enforceContrast: true`, like the old method under edge-to-edge.
- gesture-handler 3 keeps `Gesture.Pan()` / `GestureDetector` (types renamed `Legacy…`): existing
  code and `@gorhom/bottom-sheet` 5.2.14 compile and run (verified on the iOS simulator).
- iOS: scene-based lifecycle, `prebuild` generates `SceneDelegate.swift` and
  `UIApplicationSceneManifest`. A modified `AppDelegate` (by hand or by a plugin) must migrate
  (`expo.fyi/ios-scene-lifecycle`): a `prebuild --no-install` in a throwaway copy shows it.
- Android: R8 is on by default in release (`android.enableMinifyInReleaseBuilds=true`): test a
  release build (third-party native SDKs), or turn it off through `expo-build-properties`.
- `import/namespace` flags `Notifications.AndroidImportance` (the build writes `export var` on a
  comment's line): use the named import `{ AndroidImportance }`.
- `expo-file-system/next` still resolves to the main entry: import `expo-file-system`.
- `react-native-appsflyer` 6.18 plugin: "Automatic Swift AppDelegate modification failed" at
  `prebuild` (scene template). Harmless if the app does not use AppsFlyer deep links; otherwise
  the manual integration goes through the `SceneDelegate`.
- `pod install` run by an agent or a shell without a UTF-8 locale: CocoaPods' error report crashes
  (`Unicode Normalization not appropriate for ASCII-8BIT`) and hides the real error →
  `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`. A freshly bumped native SDK (RevenueCat 10.14 →
  `PurchasesHybridCommonUI`) can be missing from the local index: `pod install --repo-update`.
- `posthog-react-native` 4.81 captures screens by default: under expo-router, the provider mounted
  above navigation logs `useNavigation` / `useNavigationState` errors →
  `autocapture={{ captureScreens: false }}` (or no provider outside production).

## SDK 57

- `app.config.js`: `newArchEnabled` and `edgeToEdgeEnabled` no longer exist. `expo install --fix`
  cannot write into a dynamic config: it **fails with code 1** listing the plugins to add by hand
  (`@react-native-community/datetimepicker`, `expo-font`, `expo-image`, `expo-status-bar`); the
  packages are installed anyway.
- **A peer dependency conflict can stay hidden by the lockfile**: `npm install` passes, but any
  fresh resolution fails with `ERESOLVE` (`i18next` 25.6 refused TypeScript 6). After an upgrade:
  `npm install --package-lock-only` on a copy of `package.json` without a lockfile.
- **`npx expo install … -- --save-dev` puts the packages in `dependencies`** and leaves the old
  versions in `devDependencies`: reread `package.json`.
- expo-router bundles React Navigation: no more `@react-navigation/*`; `useHeaderHeight` →
  `expo-router/react-navigation`; `ThemeProvider`, `DarkTheme`, `Theme` → `expo-router`.
  (`posthog-react-native` declares it as an optional peer, useless without automatic screen
  capture.)
- `StyleSheet.absoluteFillObject` removed → `StyleSheet.absoluteFill`. `headerLargeTitle` →
  `headerLargeTitleEnabled`. `expo-blur`: `experimentalBlurMethod` → `blurMethod`.
  `expo-file-system/next` no longer exists → `import { File } from 'expo-file-system'`.
- **Global `fetch` = `expo/fetch` since SDK 56**: it rejects React Native style `FormData` parts
  (`{ uri, name, type }`) with a `FunctionsFetchError` before the request leaves. Append a `File`
  from `expo-file-system` (it implements `Blob`). Without it, no upload goes through.
- DateTimePicker 9: `onChange` → `onValueChange(event, date)`, called only on selection; same for
  `DateTimePickerAndroid.open`.
- Reanimated 4.5: `useAnimatedStyle` returns an `AnimatedStyleHandle`; type the prop as
  `ReturnType<typeof useAnimatedStyle<ViewStyle>>`.
- `useColorScheme()` can return `'unspecified'`: do not cast to `'light' | 'dark'`.
- `eslint-config-expo` 57 enables the React Compiler rules (set to warning for existing code).
- TypeScript 6: `types` defaults to `[]`, an `@types/*` package is no longer loaded on its own
  (Jest globals "not found" → `@jest/globals`).
- `npm audit`: ~40-50 vulnerabilities in the build tooling; `npm audit fix --force` downgrades to
  `expo@44` / `react-native@0.72`. Never run it.
- `jest-expo` pulls a React Native Jest preset whose version does not match the React Native patch
  (`expo install` refuses, peer conflict): run Jest without that preset.
