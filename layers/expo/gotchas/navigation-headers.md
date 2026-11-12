# Navigation, native headers and tabs (expo-router, react-native-screens)

## Headers

- Custom view in `headerLeft` / `headerRight`: iOS 26 reskins it as a glass pill, no flag
  prevents it.
- Navigation theme: the native stack derives the bar's `overrideUserInterfaceStyle` from
  `theme.dark` (a light theme in a dark app → glass buttons on a white background) and, at SDK 57,
  paints `theme.colors.background` on its container (a gradient placed behind a Stack disappears:
  use a theme with a transparent background, and each screen's background through
  `contentStyle`).
- Header `options` passed from a modal page are lost on first display (title = route name, opaque
  bar); Fast Refresh hides the problem.
- Photo in a bar button: `react-native-screens` recreates the `UIBarButtonItem`s on every
  reappearance, the image reloads (empty button, neighbors jumping), and iOS 26 pulls a color image
  out of the shared capsule.
- `Stack.Toolbar.Button` has no loading state (`disabled` only grays it): while sending, replace it
  with a `Stack.Toolbar.View hidesSharedBackground` holding a circle of the button's color (44 pt)
  and an `ActivityIndicator`.
- `Stack.Toolbar.View` is clipped to its frame (an overflowing pill comes out cut). The native
  badge (`UIBarButtonItemBadge`) has a minimum size; iOS's small `indicator` dot is not exposed.
- Native menus: without `multiselectable: true`, UIKit puts a ghost checkmark on the last item
  (`react-native-screens#3862`).

## Large titles and scroll edge

- Tab root with a large title and a short page: content taller than the visible area (expanded
  title, tab bar) stays scrolled under the collapsed title after a gesture. The large title adds
  52 pt to the header and the tab bar 49 pt above the bottom inset (measured on iOS 26.5), which JS
  does not receive: subtract them from the content's `minHeight`.
- Frozen large title: the scroll view was not on the chain of first children (`FlashList` breaks
  it, its root wraps the list). With a `ScrollView`, there is no native `onEndReached`: call it from
  `onScroll` (threshold, once per content height).
- iOS 26 scroll edge effect: `react-native-screens` finds the `ScrollView` through the **first**
  descendant (`findScrollViewInFirstDescendantChainFrom`); a gradient as first child makes
  `scrollEdgeEffects` ineffective. Technique with no effect at rest: `contentInset.top` = header
  height, initial `contentOffset` at `-inset`, banner moved up by the same amount.
- Fabric recycles `ScrollView`s: `prepareForRecycle` resets `contentInset` to zero but
  `updateProps` compares with the previous page's props → never reapplied. Add a sub-pixel offset
  (`useState(() => Math.random() / 100)`) to the inset.
- `FlashListProps extends ScrollViewProps` (`contentInsetAdjustmentBehavior` passes through); no
  native `gap` on a `FlashList` grid: gutter through inner cell padding.

## Search

- `Stack.SearchBar`: search in the iOS 26 tab bar = a `role="search"` trigger in `NativeTabs` + a
  `Stack.SearchBar` with `placement="automatic"` declared by the tab's screen. When active it hides
  the whole bar (and the `Stack.Toolbar`): `hideNavigationBar={false}`, read only at the next
  activation. `Keyboard.dismiss()` does not blur it: use its `ref` (`blur()`),
  `keyboardDismissMode="on-drag"`, `onTouchStart` on the `ScrollView`.
- Magnifier detached as a pill on the right: iOS 26 detaches the `role="search"` tab as expo-router
  58 passes it (`systemItem: 'search'` only), **iOS 27 does not**: the magnifier becomes a regular
  tab in the row again. On iOS 27 a `UISearchTab` that activates its search is needed:
  `unstable_nativeProps={{ ios: { role: 'search', automaticallyActivatesSearch: true } }}` on the
  trigger (`react-native-screens` 4.30, `TabsScreen` `role`), limited to iOS 27+ so nothing changes
  on iOS 26; tapping the magnifier then activates search directly. Verified on an iPhone on iOS 27.

## Tabs

- Under `NativeTabs` (SDK 58, `expo-router/native-tabs`), a tab screen's
  `useSafeAreaInsets().bottom` includes the tab bar: a floating button at `insets.bottom + margin`
  stays above it with no computation. Including a screen pushed inside a tab: 83 pt on an iPhone 17
  Pro (indicator 34 + bar 49).
- Pushed screens shared by tabs (`(tabs)/(a,b,c)/x`): link **without a group** (`/x`); typed
  routes refuse a partial group (`/(main)/x`). expo-router 58 resolves the group from the current
  segments, so in the current tab. From a screen above the tabs (modal, camera) or from a layout
  (push tap, global popup): dismiss what covers `(tabs)` (`router.dismiss(n)`) then
  `router.push('/x')`, resolved in the tab underneath (actions go through the same reducer in
  order); pushing directly stacks a second copy of `(tabs)`. One hook does it (e.g.
  `useOpenInTabs`), `n` read from `useNavigationContainerRef().getRootState()`: the app is wrapped
  in a `__root` route; look for `(main)` along the displayed routes.
- Badge on a native tab (`NativeTabs.Trigger.Badge`): the tab label is shifted one notch at cold
  start. Keep tab labels short: the iOS 26 selection bubble truncates quickly.
- Swipe back from anywhere (iOS 26, react-native-screens 4.26): a left-to-right stroke in a gesture
  area closes the page → `gestureEnabled: false` for the duration of the gesture.

## Startup routing

- Black screen / empty frame at launch: splash hidden before the screen is drawn (right after a
  `router.replace`, or during an empty waiting view). Hide it on the frame after the screen is
  ready.
- A module-level flag prevents the startup navigation after a remount (Android recreates the
  screen): blank screen. A navigation before the navigator mounts remounts the whole app: loop
  (symptom: a log repeated in Metro), stuck splash.
- `/` resolves to the initial route of the first group (`anchor`): a `replace` to the home already
  shown stacks a second home, animated like a push. With an `app/index.tsx` at the root (empty
  startup switch), `/` is that screen: a fallback `replace('/')` gives a white screen; target the
  group (`'/(main)'`).
- A pushed screen opened by a direct link has nothing under it (no native back button,
  `canGoBack()` false) without `export const unstable_settings = { anchor: 'index' }` in its
  group's `_layout`. Before expo-router 58: `initialRouteName`, still read but flagged deprecated
  on every layout load.
- A splash that waited for the RevenueCat entitlement **and** AppsFlyer / the offerings stayed up
  too long: wait only for what the screen shows.
- Checking a startup frame by frame: skill `expo-startup-check`.
