---
name: expo-native-ui
description: Liquid Glass (GlassView), @expo/ui SwiftUI (Host, Menu, TextField), native iOS headers (Stack.Toolbar, large title, badges, menus), modals and expo-router pitfalls, Reanimated 4 animations and gestures in an Expo app. Load before writing or changing a header, a modal, navigation between stacks, a glass surface, an @expo/ui component, an animation or a gesture.
---

# Expo native UI — headers, Liquid Glass, modals, animations

The _why_ behind each point: the `expo` layer's pitfalls
(`.claude/agentic-kit/layers/expo/gotchas/`), sections on the @expo/ui bridge, Liquid Glass,
navigation and headers, Reanimated.

## Native first

Every control that has a native equivalent (menu, picker, date, alert, empty state, progress) is
built natively; redraw it in React Native only when `@expo/ui` does not cover the need. Screens
never import `@expo/ui` directly: only the project's components that wrap it (Android fallback
component by component, a single `Platform.OS !== 'ios'` condition).

## Liquid Glass and `@expo/ui`

- Glass (`GlassView`) on iOS 26+ only: fall back to the previous look if the project supports older
  versions, no fallback branch when the target is iOS 26+. **The native material beats the pixel**:
  never fake glass with `rgba`. Always the app theme's `colorScheme`.
- No glass under a parent that starts at opacity 0, nor around a child that changes size; a badge
  sits next to the glass, not inside it.
- SwiftUI `<Host>` with an **explicit size**, `ignoreSafeArea="all"`; `matchContents` as a last
  resort. Styles through `modifiers` (values from the constants), `foregroundStyle`, a measured
  `frame({ width })`, `useNativeState` for a `TextField`.
- Rejected after trials: `@expo/ui`'s `BottomSheet` and full-width `Button`. `Menu`: React Native
  content in the flow, a `Menu` with an empty label on top that catches the tap, placed next to a
  glass card, not inside it.

## Native headers (iOS)

- Transparent native bar, **declarative** `Stack.Toolbar` buttons (SF Symbols, glass on iOS 26)
  declared as **children** of the `Stack.Screen`; title and transparency through
  `Stack.Screen.Title` / `Stack.Header`, not `options` (lost the first time a modal is shown: check
  after a cold restart). `unstable_headerLeftItems` / `RightItems`: older API, iOS only.
- **Never** a custom view in `headerLeft` / `headerRight`, **never** a photo in a bar button: SF
  Symbols. A count: native button + `Stack.Toolbar.Badge`. A native menu that is not a picker:
  `multiselectable: true`.
- Double tap on a header button: a synchronous lock (a single-flight helper), not React state.
- **Large title**: the scroll view is the first child at every level under the screen, and a
  `ScrollView` (not a `FlashList`); the screen background set in the `_layout`.
- Navigation theme: the native stack's `theme.dark` matches the app theme, transparent background
  for a Stack laid over a gradient.
- Bar height: `useHeaderHeight` (`expo-router/react-navigation`), never a constant.
- A native prop that must be replayed on every mount (`contentInset`): a sub-pixel offset drawn once
  per mount (Fabric recycles `ScrollView`s).
- A screen reached directly (from a modal): explicit back chevron.

## Animations (Reanimated 4)

- `.get()` / `.set()`, never `.value =`. Worklets **at module level**, values passed as arguments.
- Replay: remount (`key`) + start on mount through `useEffectEvent`.
- A gesture in a scrolling page: `PanResponder` (not gesture-handler), `scrollEnabled` and
  `gestureEnabled` turned off during the gesture; mutable state in a small class
  (`useState(() => new …)`).

## Modals

- **No bottom sheet**: a **modal page** (route with `presentation: 'modal'`, content inside the
  project's modal page container).
- **Primary action in the header**: a tinted `prominent` native button (checkmark, arrow for a next
  step, disabled while the form is incomplete), never a button at the bottom of the page.
- A multi-step modal: its own stack (folder + `_layout` with a `Stack`), the next step through
  `router.replace` in the same sheet. A modal page that replaces another: `replace`, not `back()` +
  `push()`.
- A value returned to the screen below: modal result through a subscription (`useEffectEvent`),
  never a `setState` in an effect. Opening another screen from a modal: `router.back()` then
  `router.push(…)`.

## Router

- "Root of this sub-Stack" = `navigation.getState()?.index === 0` (`canGoBack()` looks up to the
  parents).
- Never a `<Redirect>` nor navigation while a **layout** renders; never navigate before the
  navigator is mounted; do not navigate again to the screen already shown.
- Back to the tabs from a screen outside them: `router.dismissTo`. No nested `Stack` under a tab for
  pushed screens; no shared `(a,b)/` routes for a screen that also has a modal entry. Helpers passed
  to a layout: functions that return `<Stack.Screen>` elements.
- **Incoming links**: `app/+native-intent.ts` returns `null` for every link the app opens itself
  (received share, universal link); the home screen opens it once signed in.
