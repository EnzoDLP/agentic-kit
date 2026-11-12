# Storybook

## Capturing a story with Playwright

- On `storybook dev`, `page.goto(…, { waitUntil: 'networkidle' })` never resolves: the HMR
  websocket keeps the network busy. Wait for `load`, then for a selector of the render:
  `#storybook-root > *` (URL `iframe.html?id=<story-id>&viewMode=story`, ids in `/index.json`).
- A drawer or modal (MUI Joy, portal) renders **outside** `#storybook-root`: wait for
  `.MuiDrawer-content` / `.MuiModal-root` instead.
- Running `vitest run` (the in-browser `storybook` project) right after stopping `storybook dev`
  fails whole files with no red test (Vite re-optimizes its dependencies): run it again.
- When a story starts importing a heavy dependency that `storybook dev` had not pre-bundled yet
  (e.g. recharts), the iframe answers `504 (Outdated Optimize Dep)` and the story no longer loads,
  even after a reload: restart `storybook dev`.

## Mocking the hey-api axios client per endpoint

- `@hey-api/client-axios` serializes the query **into `config.url`** (`/orders?status=open`) and
  leaves `config.params` empty, unless a `paramsSerializer` is configured. A story's axios adapter
  that routes on `config.url` must compare the path without the query
  (`config.url?.split('?')[0]`) and read the filters from the URL, not from `params`.
