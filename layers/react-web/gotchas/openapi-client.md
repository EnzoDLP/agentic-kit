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
