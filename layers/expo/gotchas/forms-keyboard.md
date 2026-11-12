# Forms and keyboard (KeyboardAvoidingView, modal sheets, multiline inputs)

- Link input without `autoCapitalize="none"`: iOS writes "Https://".
- Keyboard in a modal sheet: Android edge-to-edge no longer resizes the window (without
  `behavior`, nothing pushes the content; `height` with the keyboard open, removed on close). iOS:
  `KeyboardAvoidingView` compares its frame measured **inside** the sheet with the keyboard
  position **on** the screen (offset = window height − page height); `measureInWindow` returns 0
  in a modal under the New Architecture.
- That measured offset arrives too late with an input focused at opening: the sheet is first laid
  out at window size (874 pt) then shrinks (742 pt), and `KeyboardAvoidingView` only rereads its
  offset at the next keyboard event (132 pt of page under the keyboard, measured). A sheet ends at
  the bottom of the screen:
  - on iOS, move the page up by the keyboard height (`keyboardWillShow` / `Hide`,
    `Keyboard.metrics()` at mount);
  - a scrolling page without a footer: `automaticallyAdjustKeyboardInsets` on the `ScrollView`
    (native computation, brings the focused input into view), **with
    `contentInsetAdjustmentBehavior="never"`**, the header (`useHeaderHeight`) and the home
    indicator as `contentInset` (and `scrollIndicatorInsets`), and an initial `contentOffset` at
    `-header height`. React Native bounds the offset it gives for the keyboard with
    `contentInset` alone, without the header inset (`adjustedContentInset`). With `automatic`, a
    focused input went under the transparent header, and the page stayed offset when the keyboard
    closed after a scroll (verified, software keyboard, iOS 26.5). Header and indicator as content
    margins also fix the keyboard, but iOS 27 then draws the header as on a scrolled page;
  - Android: the keyboard-avoiding view starts at the top of the screen, React Native header
    included, otherwise it measures itself short by the header height.
- Never keyboard avoidance inside an input component: nested in the page's, it shrinks the input.
- Multiline input that grows with its content: 10 approaches tried, none stays aligned during the
  transition (`RCTUITextView -contentSize` returns `MAX(text, placeholder)`). Fixed height +
  inner scrolling.
- `Alert.prompt`: iOS only.
