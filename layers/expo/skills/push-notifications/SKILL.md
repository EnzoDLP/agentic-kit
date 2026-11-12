---
name: expo-push-notifications
description: Push notifications in an Expo app — token, sending from an edge function (Expo Push API), recipient language, opening the right screen on tap, and always the app icon badge (set and reset). Load whenever expo-notifications, sending a push, the app's notifications or the badge are touched.
---

# Push notifications (+ app icon badge)

Pitfalls: the `expo` layer's pitfalls (`.claude/agentic-kit/layers/expo/gotchas/`), push
notifications and iOS simulator sections.

## A push never goes without its badge

Every app that sends pushes manages the icon badge, **both ways**:

- **Set**: every push carries `badge` = the recipient's unread notification count (the counter of
  the app's bell), counted on the server at send time.
- **Reset**: the app syncs the badge to that same counter (a single query, the bell's) as soon as it
  changes: notification read, all marked read, push received with the app open, back to the
  foreground (read on another device). A `useAppIconBadge` hook mounted only when signed in.
  `setNotificationHandler` with `shouldSetBadge: true`.
- **Sign-out / account deletion**: badge to 0 (the counter belonged to that account).
- **Builds that cannot reset it**: no `badge` for their tokens (e.g. a `supports_badge` column on
  the push tokens table, sent as `true` by builds that have the hook) — otherwise the number stays
  stuck on the icon forever.

## The rest

- **Token**: only on a real device (`Device.isDevice`, the simulator hangs on
  `getExpoPushTokenAsync`); saved on every signed-in launch (it changes on reinstall). Permission
  asked after an action that justifies it, never on app open, never right next to another system
  prompt.
- **Sending**: from an edge function (Expo secret on the server), triggered by the database. Same
  `collapseId` / `tag` on all tokens of one notification; anti-spam at write time, not through
  `collapseId`.
- **Language**: the recipient's, saved by the app on their profile on every language change,
  **English if unknown** (older builds).
- **Tapping a push**: `data` says what to open (id of the item, the profile…);
  `Notifications.useLastNotificationResponse()` (app closed or open), default action only, once per
  notification (ids already opened kept at module level).
- **Testing**: `xcrun simctl push <udid> <bundle> file.apns` (`aps` + the `data` keys at the same
  level) shows nothing if the build lacks permission, and the tap does not reach the app: badge,
  language and opening are checked on an iPhone.
