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
- A **stateful** adapter (one that keeps what create / update / delete changed, so the next GET
  reads it) put in `meta.parameters` is built once when the file loads and shared by every story
  of the file: one story's change (a rename, a deletion) leaks into the next and makes it fail.
  Build one per story (`parameters: { mockApi: catalogueApi() }` on each story).

## Play functions run as Vitest browser tests

- A story run by `@storybook/addon-vitest` opens at **1200 × 900** unless the story sets
  `globals: { viewport: { value: 'mobile1' } }` (any `MINIMAL_VIEWPORTS` key, or one from
  `parameters.viewport.options`): breakpoint behavior is tested that way, not with a wrapper.
- Clicking a real `<a href>` in a play function navigates the test iframe: the run ends with an
  unhandled error and no failing test named. To test "the click calls the app's handler instead of
  following the link", register `window.addEventListener('click', e => { prevented =
  e.defaultPrevented; e.preventDefault() }, { once: true })` before the click (it runs after
  React's handler), then assert `prevented`.
- `getByRole` / `queryByRole` skip elements hidden with `display: none`; to assert that something
  is hidden, query it with `{ hidden: true }` and expect `not.toBeVisible()`.
- A Recharts tooltip does not open on `userEvent.hover` over a bar: Recharts reads the pointer
  position on its wrapper and the hover carries none. Send
  `fireEvent.mouseMove(canvasElement.querySelector('.recharts-wrapper'), { clientX, clientY })`
  with the center of the bar's `getBoundingClientRect()`. The default tooltip splits each line
  into name, separator and value spans: compare each `listitem`'s `textContent`
  (`'Exceptions: 10'`), not `getByText` (Recharts 2.15).
