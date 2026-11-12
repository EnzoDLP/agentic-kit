# Expo — layout, scrolling, states

Apply from the start on every screen that scrolls.

## The rule

**A screen's content always fills at least 100% of the visible height**, and slides behind the
transparent header when scrolled (never a `paddingTop` that makes the scroll area start below the
header). No dead band at the bottom, no scrollable void.

## How

- `style={{ flex: 1 }}` alone bounds the container, not the content: `contentContainerStyle={{
flexGrow: 1 }}` with `ScrollView`, `FlatList`, `FlashList`.
- **`flexGrow: 1` and `contentInsetAdjustmentBehavior="automatic"` never go together** (header
  height counted twice → scrollable void).
- **Pushed screen with a transparent header**: `automatic` inset + a **computed** `minHeight` on
  the `contentContainerStyle` (`window − insets.top − header − insets.bottom`). It is required:
  without it the empty area no longer responds to scrolling. Large title: also subtract the whole
  gap between expanded and collapsed title, otherwise the title stays collapsed after a bounce.
- **Screen in a modal**: the `ScrollView` does not cover the window → `minHeight` **measured with
  `onLayout`** if some content must fill the height; no computed `minHeight`.
- **Native tab**: `useSafeAreaInsets().bottom` there already includes the tab bar: do not add it
  again to a `paddingBottom`.
- Space below the last item: the project's bottom padding hook (safe area), never a hardcoded
  number. A `paddingBottom` added on top of a state already at the visible height = scrollable
  void: only when a real list is rendered.
- Android: `contentInsetAdjustmentBehavior` is iOS only → add the header inset explicitly.
- A SwiftUI `Host` with `flex: 1` inside a `ScrollView` measures against its whole height (under
  the header): give it an explicit computed height.
- **A negative `zIndex` on a `LinearGradient` makes the view disappear**: rely on JSX order.
- Measure rather than guess: a temporary text showing `contentOffset`, `contentSize`,
  `layoutMeasurement` from `onScroll`.

## Loading / error / empty states

Shared rule: the `react` layer's rules on loading, error and empty states. Every startup screen
that waits for data has a path for the error (otherwise a blank screen).
