# Push notifications, universal links and received shares

The push setup is in the `expo-push-notifications` skill.

## Push notifications

- Prerequisites for real sends: an APNs key in EAS; Android: Firebase, `google-services.json`, an
  FCM v1 service account key in EAS. Without them, Expo answers `InvalidCredentials`.
- A reinstalled app gets a new token and the old one still reaches the device: identical
  `collapseId` (iOS) and `tag` (Android) on every token of the same notification.
- `collapseId` only merges the display (the phone vibrates on every send): anti-spam is done at
  write time (slot reserved by `INSERT … ON CONFLICT … WHERE sent_at < …`).
- Icon badge: only for tokens of builds that know how to reset it (skill `expo-push-notifications`).
- No reminder scheduled at one country's hour (`pg_cron` runs in UTC): follow the device's time
  zone, saved with the token.

## Universal links and App Links

- iOS reads the AASA only at install / update, through Apple's CDN (cached several hours): deploy
  the site **before** the build that declares the domain
  (`https://app-site-association.cdn-apple.com/a/v1/<domain>`). No redirect is followed: the
  declared domain is the one that serves the file (`application/json`).
- A link typed in Safari does not open the app: tap it from Messages, Notes…
- Android: `autoVerify` fails until `assetlinks.json` is published; it carries **two**
  fingerprints (EAS upload key, Play signing key). Read the second one in a release's "signed
  standard APK" (Play Console → App bundle explorer) with `apksigner verify --print-certs`
  (`keytool -printcert -jarfile` does not read v2/v3).

## Receiving a share

- Receiving a share through `expo-sharing` (experimental at SDK 57): the app opens on
  `<scheme>://expo-sharing`, which is not a route (`+native-intent` returns `null`); the content
  stays in the App Group until cleared (it comes back on every return to the foreground); the
  extension and the App Group must exist at Apple at the first EAS build (interactive build if
  signing fails); a dev client opened by a share shows its launcher; a single scheme for all
  variants can open the wrong one.
