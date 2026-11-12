# Power BI embed (`powerbi-client-react`)

Verified with `powerbi-client-react` 2.0.2 and `powerbi-client` 2.25.0.

- **A renewed embed token passed in props reloads the whole report.** `PowerBIEmbed` re-embeds
  whenever `embedConfig` is not deep-equal to the previous one (`lodash.isequal` in
  `componentDidUpdate`): the user loses its page and slicer state. Fix the configuration at mount
  (`useState(() => config)`, remount with a `key` to embed another report) and hand a new token to
  the embedded report with `report.setAccessToken(token)`, the report coming from
  `getEmbeddedComponent`.
- **An `embedUrl` outside a Power BI host crashes the React tree.** The SDK throws synchronously
  at mount ("Invalid embed URL detected. Either URL hostname or protocol are invalid"), so a mock
  URL (`https://api.example/…`, `about:blank`) takes the page down. Wrap `PowerBIEmbed` in an error
  boundary that shows the report's error state, and use an `https://app.powerbi.com/reportEmbed?…`
  URL in mocks and story fixtures (the fake token is then rejected by Power BI, not by the SDK).
- **Event handlers keep the closure of the first render.** The component re-registers handlers
  only when the map's stringified source changes, so a handler recreated with new state is ignored.
  Do not read state or props in a handler: dispatch to a `useReducer` (the reducer sees the
  current state) or call a stable setter.
- **`import { models } from 'powerbi-client'` needs `powerbi-client` as a direct dependency**:
  `powerbi-client-react` exports only `PowerBIEmbed` and its types (`TokenType`, `TraceType`,
  `Report` live in `powerbi-client`).
