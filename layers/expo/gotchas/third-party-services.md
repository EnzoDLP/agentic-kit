# Third-party services — RevenueCat (REST, Android paywall), Google Sign-In, Sentry

The integrations are in the `expo-revenuecat` and `expo-sentry` skills.

## RevenueCat REST (server)

- **API v2, not v1** (a v1 key can change everything; a v2 key carries its own permissions). v2
  names an entitlement by its internal id (`entl…`, read from
  `GET /v2/projects/{id}/entitlements`), not by its `lookup_key`. A 404 can come from a wrong
  project id: first read the project's entitlements (404 = error), then the customer's 404
  (= free). Follow `next_page` only toward `api.revenuecat.com` (the key goes with every page).
- A Pro status written to the database (for a companion website, say) comes from the server
  (RevenueCat), never from a copy declared by the app (anyone could declare themselves Pro).

## RevenueCat paywall on Android (purchases-ui 10.14)

- `RevenueCatUI.presentPaywall` opens a full-screen RevenueCat activity, outside the app's portrait
  lock (it rotates with the phone) and under the system bars (its close button under the status
  bar, out of reach); no sheet presentation exists; in dark mode, the status bar keeps light icons
  over the light paywall. A close button from the design sits against the top of the screen, not
  the content as on iOS. A working setup: `presentPaywall` on iOS, and on Android
  `<RevenueCatUI.Paywall>` in its own sheet (`presentation: 'formSheet'`, `sheetCornerRadius`, and
  rounded corners on the view: the sheet's shape does not clip its content).
- Paywall V2: no component occupies the top safe area, except a header image (first component that
  takes height, full width). On Android, the embedded view (`<RevenueCatUI.Paywall>`) reserves the
  window's status bar height even when not under it (sheet): empty band at the top, with the close
  button inside it (verified by changing density: the band keeps the status bar height, in pixels).
  On iOS, the sheet has no top safe area. Hiding the status bar changes nothing. Cropping the band
  (paywall moved up by `insets.top`) takes away a design close button anchored to the top of the
  content; an overlay badge accepts no visibility rule (a normal row accepts "if `platform` is
  "android", hide", a variable sent by the app in `options.customVariables`), and a Z stack around
  the carousel made it scroll horizontally. A workable choice: keep the band, put the gradient on
  the paywall's background rather than in the images, and keep the original close button. The
  paywall already handles the navigation bar at the bottom (no margin to add).
- `formSheet` on Android (react-native-screens 4.30, `isDraggable` always true, `gestureEnabled`
  ignored): the sheet takes any drag that does not start on a view it knows can scroll, and a
  native view that scrolls by itself (Compose: the RevenueCat paywall) is not one. Once the content
  was scrolled, scrolling back up pulled the sheet down. Fix: put that view inside a still React
  Native `ScrollView` with nested scrolling (`scrollEnabled={false}`, `nestedScrollEnabled`,
  `contentContainerStyle={{ flexGrow: 1 }}`): the sheet takes it as its scrolling content and
  leaves gestures to the view; it then closes only from outside (close button, back). Verified on
  the emulator.
- `<RevenueCatUI.Paywall>` embedded in a page: a V2 paywall's close button is a "navigate back"
  component that only arrives in `onInteraction` (`component_value: 'navigate_back'`), never in
  `onDismiss`: without that case, it closes nothing. The paywall does not handle the system bars:
  safe-area margins in its background color.

## Google Sign-In

- Native Google Sign-In with Supabase Auth: enable "Skip nonce checks" on Supabase's Google
  provider.

## Sentry

- The region is in the plugin's URL (`https://de.sentry.io/`); a wrong region does not upload
  source maps, with no error. A test in dev never validates the upload.
- **`sentry-expo-upload-sourcemaps dist` fails with "SSL certificate problem: self-signed
  certificate in certificate chain" behind a TLS-inspecting proxy** (corporate network):
  `sentry-cli` 2.58 reads the API fine but its chunk upload does not trust the proxy's root CA,
  although `curl` does (macOS keychain). Fix: export the keychain certificates and point
  `SSL_CERT_FILE` at them — `security find-certificate -a -p /Library/Keychains/System.keychain >
  ca.pem` (plus `/System/Library/Keychains/SystemRootCertificates.keychain`), then
  `SSL_CERT_FILE=ca.pem npx sentry-expo-upload-sourcemaps dist`. Never `verify_ssl = false`.
- The script reads `SENTRY_AUTH_TOKEN` from the local `.env`: a `Secret` EAS variable is never
  downloaded by `eas update` (only "Plain text" and "Sensitive" are), and the upload runs as a
  separate command after it anyway. The source maps can be sent after the update is published,
  from the same `dist` (matched by debug id); never re-export first.
