# Reanimated and Hermes

- `scheduleOnRN` refuses a function defined next to the worklets ("Locally defined function passed
  to scheduleOnRN"): define it in the component body. A `console.log` inside a worklet does not go
  through either.
- After a hot reload, a gesture animation can stop responding to the first stroke: restart the app
  before concluding it is a bug.
- **Under Hermes, `Intl.NumberFormat.prototype.formatToParts` only exists on Android**: do not use
  it. Node's `Intl` spacing in tests: the `typescript` layer's `intl.md` gotchas.
