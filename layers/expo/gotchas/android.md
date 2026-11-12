# Android — emulator, dev client, alerts, text, blur

- Dev client on the emulator: "Failed to open app" when it targets Metro through the LAN IP.
  `adb reverse tcp:8081 tcp:8081` (and `tcp:54321` for a local Supabase), then
  `adb shell am start -a android.intent.action.VIEW -d
"exp+<scheme>://expo-development-client/?url=http%3A%2F%2Flocalhost%3A8081"`.
- A Metro started before a config plugin was removed keeps the old config: its Android manifest
  answers "Failed to resolve plugin for module …"; restart it.
- `Alert.alert(message)` puts the message in the title, cut after two lines: empty title + message
  as body.
- `Alert.alert` shows only **three buttons** on Android (positive, negative, neutral): a fourth
  disappears without error. Three choices plus "Cancel": on Android, the three choices and
  `{ cancelable: true }` (a tap outside closes); otherwise a native menu.
- A text measured on N lines can draw on N+1 and lose its last line (`StaticLayout` measurement ≠
  `TextView` drawing); neither `textBreakStrategy`, `lineHeight` nor `letterSpacing` helps. One
  line: `numberOfLines={1}`. Root fix: `enablePreparedTextLayout` (native, experimental in RN
  0.86).
- `BlurView` (`expo-blur`, SDK 55+) only blurs what is inside a `BlurTargetView` passed as
  `blurTarget`, otherwise nothing (warning in the log).
- Backup rules (`dataExtractionRules`): AppsFlyer declares its own; a plugin that imposed others
  (from a removed library) broke the build (`resource xml/… not found`).
- Emulator: `-gpu host` (software rendering skews every measurement); smoothness with
  `adb shell dumpsys gfxinfo <pkg>`. Small Android: `adb shell wm density 520` +
  `settings put system font_scale 1.5`, cold restart, reset afterwards. Language:
  `adb shell cmd locale set-app-locales <pkg> --locales fr-FR`.
- `formSheet` and the RevenueCat paywall on Android: see `third-party-services.md`.
