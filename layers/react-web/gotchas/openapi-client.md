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

## A `format: date` query parameter is sent as a timestamp

- With `@hey-api/transformers` (`dates: true`), a `format: date` **query** parameter is typed
  `Date`, and the generated `querySerializer` writes it with `toISOString()`:
  `?from=2026-10-01T00:00:00.000Z`, where the API expects `?from=2026-10-01` (seen with
  `@hey-api/openapi-ts` 0.97, `client-axios`).
- Fix once for every endpoint, without touching `src/generated/`: give the client a
  `querySerializer` function in its `setConfig` that turns each `Date` into
  `toISOString().slice(0, 10)` and hands the result to the generated `createQuerySerializer()`
  (`client/utils.gen.ts`), so arrays, objects and encoding (`%20`) stay as generated. Pass UTC
  midnight dates (`new Date('2026-10-01')`) so the slice gives back the same calendar day.
- Test: a capturing `adapter`, then the app's configuration, then the operation; assert on the
  adapter's `config.url`.

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
