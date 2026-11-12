# iOS simulator — taps, keyboard, Metro from an agent session, what cannot be tested

Checking a startup frame by frame: skill `expo-startup-check`.

## Network

- **Every HTTPS call can fail on a simulator** ("A TLS error caused the secure connection to
  fail", for every host, seen on iOS 27.2 simulators): only HTTP to a local backend goes through.
  Do not conclude the app is broken from a failed HTTPS call in the simulator.

## Taps and screenshots

- A simulated tap on a `Switch` is not received: a short swipe, or a tap held 0.15 s.
- The first tap after typing only dismisses the keyboard. A screenshot right after a tap can show
  the previous screen (wait 1 to 2 s); taps less than 0.3 s apart get lost.
- Native header buttons (`Stack.Toolbar`) receive the simulated taps of the Claude Code simulator
  tool; with a tool that does not deliver them, use a deep link
  (`xcrun simctl openurl booted "<scheme>://…"`), which stacks the screen (restart the app first).
- System alerts (ATT, photo library, a link's "Open in …?") often take the simulated tap only on
  the second try. In dev, the screen can lag 2 to 5 s behind the capture: take another screenshot
  before concluding a button does not work.
- `simctl openurl` on the app in the foreground does not show "Open in …?": tapping there touches
  the app.
- Pasting into an input asks "Allow Paste" once per app on a fresh device.

## Keyboard and text input

- The software keyboard only shows if the Mac keyboard is disconnected (⌘K / ⇧⌘K). An agent
  session cannot send that shortcut (`osascript`: "not allowed to send keystrokes"); it can write
  the device preference (`ConnectHardwareKeyboard` to `false` under `DevicePreferences` → the UDID,
  in `com.apple.iphonesimulator`, then `killall cfprefsd`) and reboot the device (`simctl shutdown`
  / `boot`); remove it afterwards. The simulator tool's text input reconnects the Mac keyboard: do
  it before, or tap the keys.
- The simulator tool's text input goes through the clipboard: non-ASCII characters arrive mangled
  ("û" → "√ª", UTF-8 reread as MacRoman) and are saved as such. Type test text in ASCII.

## Metro from an agent session

- `CI=1` (with `run:ios` or `expo start`) starts Metro without file watching ("Metro is running in
  CI mode, reloads are disabled"): even a restarted app gets the old code. Start `expo start`
  without `CI`, standard input on `/dev/null` for an agent session.
- Metro started from an agent session does not read `.env` (sandbox): pass it the `EXPO_PUBLIC_*`
  variables; `--clear` as soon as a variable changes; `--no-dev --minify` for screenshots without
  LogBox.
- Status bar: `xcrun simctl status_bar <udid> override --time 9:41`. Dev client floating button:
  `defaults write <bundle> EXDevMenuShowFloatingActionButton -bool NO` through `simctl spawn`, and
  `&__expo_disable_fab=1&__expo_disable_onboarding=1` in the `expo-development-client/?url=…` URL:
  without that parameter it comes back on every restart.
- Evaluating JS in Hermes through Metro's inspector from a session: `Origin` required, then the
  connection drops (1006). Unsolved.

## Not testable on the simulator

- No push token (`getExpoPushTokenAsync` never returns, JS freezes): stop if `!Device.isDevice`.
  Simulate a notification with `xcrun simctl push <device> <bundle> file.apns`; tapping the
  notification does not reach the app (test on an iPhone), and nothing shows if the build lacks
  notification permission ("Notification sent" anyway).
- No App Store: `Linking.openURL('https://apps.apple.com/app/id…')` opens Safari, which redirects
  to `itms-appss://` and shows "invalid address". An App Store page opened from the app is checked
  on an iPhone; whatever the app saves at the same moment goes in one request, applied to the
  cache beforehand (the app moves to the background).
