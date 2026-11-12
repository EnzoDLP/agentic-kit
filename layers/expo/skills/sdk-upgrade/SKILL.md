---
name: expo-sdk-upgrade
description: Upgrade an Expo app from one SDK to another (e.g. 57 → 58), with the breaking changes and fixes known for SDKs 55 to 58. Use whenever an Expo SDK, React Native or expo-router upgrade comes up.
---

# Expo SDK upgrade

Pitfalls already met during upgrades are in the `expo` layer's pitfalls
(`.claude/agentic-kit/layers/expo/gotchas/`), per-SDK sections: **read them before starting**. The
reference is the target SDK's **versioned** docs and its upgrade guide
(`https://docs.expo.dev/versions/v<SDK>.0.0/`, Expo's changelog for every SDK crossed) — never
memory.

## 0. Scope

- A dedicated branch (e.g. `feat/sdk-<target>`).
- List every SDK crossed and its breaking changes. Known so far:

  - **55**: New Architecture mandatory, Android edge-to-edge mandatory.
  - **56**: global `fetch` = `expo/fetch`, expo-router without React Navigation, iOS 16.4 minimum.
  - **57**: Xcode 26.4 minimum, React 19.2, RN 0.86, TypeScript 6, Reanimated 4.5.
  - **58**: Node 22.13+ (Node 20 refused), RN 0.88 and its strict TypeScript API, React 19.3,
    Reanimated 4.7, gesture-handler 3, iOS scene-based lifecycle, R8 on in Android release.

- List the third-party native libraries and find, for each, a version known to work on the target
  SDK (compatibility table, release notes, issues). Known to work on SDK 57:
  `react-native-purchases` 10.x, `posthog-react-native` 4.62, `react-native-appsflyer` 6.18,
  `@react-native-google-signin/google-signin` 16.1, `@gorhom/bottom-sheet` 5.2.14. A library with no
  known compatible version: check its repository before starting, and tell the user.
- Record the starting state: `npm run typecheck`, `npm run lint`, `npm test`, `npx expo-doctor`
  (number of errors and warnings), to compare against.

## 1. Packages

1. `nvm use` (the `.nvmrc` Node, supported by the target SDK: Node 20.19.4 is enough for 57, 58
   needs 22.13+: change the `.nvmrc`).
2. `npx expo install expo@^<target>.0.0 --fix`. With a dynamic `app.config.js`, it **exits with code
   1** listing the plugins to add by hand: the packages are installed, add the plugins (SDK 57:
   `@react-native-community/datetimepicker`, `expo-font`, `expo-image`, `expo-status-bar`).
3. devDependencies (`typescript`, `eslint-config-expo`, `@types/react`):
   `npx expo install … -- --save-dev` puts them in `dependencies` → move them back to
   `devDependencies` by hand and remove the duplicates.
4. Remove what the SDK no longer provides or what is no longer imported: `@react-navigation/*` (SDK
   56+), `@expo/vector-icons` if unused, `expo-blur` if native glass replaces it.
5. Bump third-party native SDKs to the versions found above; read their release notes (RevenueCat 9
   → 10: the only breaking change is restoring consumed one-time purchases on Android).
6. Patched libraries (`patches/`): compare each upstream file between the old and new version
   (`npm diff --diff=pkg@old --diff=pkg@new -- <file>`) and carry the patch over.
7. **Fresh resolution**: `npm install --package-lock-only` on a copy of `package.json` without a
   lockfile (a peer conflict can stay hidden by the lockfile: `i18next` 25.6 refused TS 6).

## 2. Configuration

- `app.config.js`: remove `newArchEnabled` and `edgeToEdgeEnabled` (they no longer exist), add the
  listed plugins, check `deploymentTarget` (iOS 16.4 minimum since SDK 56).
- `tsconfig`: TypeScript 6 → `types` is `[]`; tests import from `@jest/globals`. Deno edge functions
  (`supabase/functions`) excluded from the `tsconfig` and from lint.
- ESLint: the target SDK's `eslint-config-expo` turns on the React Compiler rules; set them to
  **warning** in `eslint.config.js` for existing code, so the upgrade adds no lint errors.

## 3. Code — search and replace (SDK 57, 58)

```bash
grep -rn "@react-navigation/\|absoluteFillObject\|headerLargeTitle[^E]\|experimentalBlurMethod\|expo-file-system/next\|onChange=" app components containers hooks src 2>/dev/null
# SDK 58 as well:
grep -rnE "useRef<TextInput>|forwardRef<TextInput|setButtonStyleAsync|InteractionManager|<StatusBar[^>]*(backgroundColor|translucent)" app components containers hooks src 2>/dev/null
```

- SDK 58: `TextInputInstance`, `<NavigationBar>`, removed `StatusBar` props, false positive of
  `import/namespace` on `AndroidImportance` → the `expo` layer's pitfalls
  (`.claude/agentic-kit/layers/expo/gotchas/`), SDK 58 section.
- `@react-navigation/*` → `useHeaderHeight` from `expo-router/react-navigation`, `ThemeProvider` /
  `DarkTheme` / `Theme` from `expo-router`.
- `StyleSheet.absoluteFillObject` → `absoluteFill`; `headerLargeTitle` → `headerLargeTitleEnabled`;
  `experimentalBlurMethod` → `blurMethod`; `expo-file-system/next` →
  `import { File } from 'expo-file-system'`.
- DateTimePicker: `onChange` → `onValueChange(event, date)` (called only on selection);
  `DateTimePickerAndroid.open` likewise.
- **Uploads**: `fetch` = `expo/fetch`, which refuses `FormData` parts `{ uri, name, type }` → append
  a `File` from `expo-file-system`. Without it, no upload goes through.
- Reanimated 4.5: animated style props typed `ReturnType<typeof useAnimatedStyle<ViewStyle>>`.
- `useColorScheme()` can be `'unspecified'`.
- Navigation theme (dark app): the native stack derives the bar style from `theme.dark` and paints
  `theme.colors.background` on its container (symptom: glass buttons on a white background, the
  background gradient gone).

## 4. Verify

- `npm run typecheck` (0 errors), `npm run lint` (0 errors, warnings counted), `npm test`,
  `npx expo-doctor` (all green), `npx expo install --check`.
- Exported bundles: `npx expo export --platform ios`, then `--platform android`.
- `npm audit` reports dozens of tooling vulnerabilities: **never** run `npm audit fix --force`.
- Write a test plan (e.g. `docs/test-plans/sdk<target>.md`): every flow of the app (startup, gating,
  onboarding, auth, each screen, uploads, paywall, sharing, links, notifications), to run on the
  simulator then on a device. A **new dev client** is needed (`expo prebuild --clean` / EAS
  `development` build): a long native build, propose it to the user rather than running it.
- Run the plan on the simulator once the dev client is installed; the startup with skill
  `expo-startup-check`. Say what remains to do on a device and on Android.
- Note the before / after versions, what was removed, bumped, fixed and what is not tested.
