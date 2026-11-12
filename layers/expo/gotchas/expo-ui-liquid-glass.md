# @expo/ui bridge (SwiftUI / Compose) and Liquid Glass

The patterns that work are in the `expo-native-ui` skill.

## @expo/ui

- `Host` sized by SwiftUI (`matchContents`): arrives at zero on the React Native side, drawn but
  without taps, remeasures on scroll and shifts its neighbors. `UIHostingController` applies its
  own safe areas → `ignoreSafeArea="all"`.
- `@expo/ui`'s `BottomSheet` was ruled out after three setups (full-screen inert `Host`, empty 0×0
  `Host`, 100% SwiftUI content that still breaks the React Native layout behind).
  `fitToContents` needs an intrinsic size that `RNHostView` does not provide.
- `@expo/ui` `Button`: `buttonStyle('glass')` does not fill an explicit `frame(width:)`, and accepts
  only a string `label`.
- `Menu`: a rich React Native `label` is invisible on device; composed in pure SwiftUI, it flickers
  on open and close (no modifier prevents it). Pattern: React Native content on top, invisible
  `Menu` (empty `HStack` + `contentShape(shapes.rectangle())`) underneath.
- `Menu` whose `label` is the button (a "⋯" glass circle): a long press shows a gray square (the
  system button around it). `modifiers={[menuStyle('button'), buttonStyle('plain'),
menuIndicator('hidden')]}` on the `Menu`, and `contentShape(shapes.circle(), ['interaction',
'contextMenuPreview', 'hoverEffect'])` on the label.
- iOS 26: a menu "blooms" from the nearest Liquid Glass container (a `Menu` inside a glass card
  transforms the whole card).
- Compose: `DropdownMenuItem.Text` is a slot (it needs a Compose `<Text>`); `Shape.Circle` is a
  function (`shape={Shape.Circle({})}`).

## Liquid Glass

- No `GlassView` under a parent that starts at opacity 0: iOS does not draw the material.
- `GlassView` does not follow a child whose size changes after mount.
- Tinted black, glass looks solid on a plain background (wanted for a button).
- Glass clips its content to its shape; `isInteractive` does not block the surrounding `Pressable`
  (keep the `Pressable` outside, with its `hitSlop`).
- Without an explicit `colorScheme`, glass follows the iPhone's dark mode.
- A white cross on transparent glass vanishes over a light photo: use a dark pill.
