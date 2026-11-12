# 3D: three.js on expo-gl

- **three r163+ rejects expo-gl's context** ("WebGL 1 is not supported since r163"): expo-gl makes
  `WebGL2RenderingContext` inherit from `WebGLRenderingContext`, and three's `instanceof` test gets
  it wrong. Hide `globalThis.WebGLRenderingContext` for the duration of
  `new WebGLRenderer({ canvas, context: gl })` (native only), pass it a fake canvas (`width`,
  `height`, `clientWidth`, `clientHeight`, `style: {}`, `addEventListener`,
  `removeEventListener`, `getContext: () => gl`), and call `gl.endFrameEXP()` after each `render`.
- **Always `import … from 'three'`**, never `require('three')`: Metro then serves `three.cjs`,
  which calls `process.emitWarning` (missing under Hermes) and returns an empty module.
- **iOS simulator, very slow GL**: `msaaSamples > 0` on a full-screen GLView → nothing shows;
  beyond about 10 frames/s with lit materials, the command queue saturates and the view stays
  frozen on its first frame while JS runs (logic, input, timer). On the simulator
  (`!Device.isDevice`): `msaaSamples={0}`, GLView drawn at 50% then scaled up
  (`transform: [{ scale: 2 }]`, `transformOrigin: 'top left'`), rendering capped at 10 fps, logic
  at 60 Hz. Not measured on a real device.
- "Frozen" image: first check that the logic advances (log the pose), then compare two simulator
  screenshots **3 s apart** (the capture tool takes several seconds).
- `gl.readPixels` is unreliable under expo-gl (error 1282): diagnose with a lab of several GLViews
  side by side (each with its own context, one variant per view).
- After a hot reload of a file that touches GL, the GLView stays black: reload the app.
