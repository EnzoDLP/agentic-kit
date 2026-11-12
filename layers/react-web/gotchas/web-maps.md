# Web maps (MapLibre, basemaps)

## Basemaps

- **CARTO requires a key** (`basemaps.cartocdn.com`, styles `voyager`, `light_all`, `dark_all`):
  without one, every tile is an "API KEY REQUIRED" image (status 200, so no visible error).
  `tile.openstreetmap.org` refuses app usage. **OpenFreeMap** is free, with no key and no view
  limit (attribution required, added by MapLibre), but vector only: styles
  `https://tiles.openfreemap.org/styles/{positron,dark,liberty,bright}` with MapLibre GL.

## MapLibre GL

- **v6 is ESM only**: no UMD build any more, `import * as maplibregl from '…/maplibre-gl.mjs'`.
  The file imports `maplibre-gl-shared.mjs` and `maplibre-gl-worker.mjs` by relative path: serve
  all three from the same folder.
- **`fitBounds` adds the camera's current padding** (set by a `flyTo` / `easeTo` with `padding`)
  to its own `padding`: the padding counts twice, "Map cannot fit within canvas", and the map does
  not move. Pass only the difference: `max(0, wanted - map.getPadding()[side])`.
- **Hidden tab = frozen map**: `requestAnimationFrame` is suspended, no tile loads and
  `document.hidden` is `true`. A hidden Claude Code browser pane shows an empty map: check in
  headless Chrome instead (`puppeteer-core` with the installed Chrome, args
  `--use-angle=swiftshader --enable-unsafe-swiftshader` for WebGL).
