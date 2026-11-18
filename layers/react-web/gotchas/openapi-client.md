# OpenAPI generated client (hey-api)

## A `format: date` field shows the day before

- With `@hey-api/transformers` (`dates: true`), a `format: date` field (`'2026-07-01'`) becomes
  `new Date('2026-07-01')`: **midnight UTC**. Formatted in local time (`date-fns` `format`,
  `toLocaleDateString` without `timeZone`), it shows **June 30** for a user west of Greenwich (the
  Americas).
- Format these fields in UTC: `new Intl.DateTimeFormat(locale, { …, timeZone: 'UTC' })`, or
  `getUTCMonth()` / `getUTCFullYear()` for a month or quarter label. `format: date-time` fields
  stay in local time.
- Test: run the mapper's test with `TZ=America/Los_Angeles npx vitest run …`.

## A multipart upload is sent as JSON

- A global `Content-Type: application/json` set through `client.setConfig({ headers })` must be
  spelled **`'Content-Type'`** exactly. For a `multipart/form-data` operation the generated SDK
  clears the header by writing `'Content-Type': null`, and the client's `mergeHeaders` deletes
  only that exact key. Any other casing (`'Content-type'`) survives, axios sees a JSON content type
  and serializes the `FormData` as JSON: the file arrives as `{"file":{}}`.
- Keep the header (requests without a body then still carry a Content-Type, which some gateways
  require) and fix its casing.
- Test through `setConfig`, as the app does: `createClient({ adapter })`, then the app's
  configuration, then the upload operation; assert the adapter received a `FormData`. Passing the
  headers to `createClient(config)` instead goes into `axios.create` defaults, which behave
  differently.
