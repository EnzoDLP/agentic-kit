# SQL, grants and PostgREST

## Functions and grants

- **`CREATE OR REPLACE FUNCTION` cannot** change `RETURNS TABLE` (even a column appended at the end,
  SQLSTATE 42P13), the argument list, the return type, nor remove an enum value → `DROP FUNCTION` +
  `CREATE`, then put `REVOKE` / `GRANT` back (beware of ambiguous functions if the old type is
  renamed).
- **Grants**: depending on the project's default privileges, `REVOKE … FROM PUBLIC` also removes
  the right from `authenticated` (`permission denied` without the `GRANT`), or removes it **from
  neither `anon` nor `authenticated`**, which hold their own explicit `EXECUTE`. Hence the full
  template (`REVOKE … FROM PUBLIC, anon` + `GRANT … TO authenticated`) and a check of `proacl`
  after every `DROP` + `CREATE`.
- **No default grants on a new table in `public` anymore** (Supabase, all projects as of
  2026-10-30): a table, view or materialized view **created** after that date (the date the
  migration **runs** on the remote database, not the date it was written), and its sequences, are
  born without `SELECT` / `INSERT` / `UPDATE` / `DELETE` for `anon`, `authenticated` or
  `service_role`: `42501 permission denied for table` through the Data API (`.from()`,
  `/rest/v1`, an edge function using `service_role` included). Existing tables keep their grants;
  a `DROP` + `CREATE` (a recreated view) loses them. No effect on what a `SECURITY DEFINER` RPC or
  a trigger reads (owner's rights), nor on functions' `EXECUTE`. A table read through `.from()`:
  its `GRANT`s go in its migration (discussion supabase#45329).
- **A `SECURITY DEFINER` RPC that filters by `arg_user_id` without comparing it to `auth.uid()`**
  lets any signed-in account, anonymous ones included, read or write on someone else's behalf (a
  `DELETE` filtered on `id` and `user_id`, two ids readable in public feeds). To find them: RPCs
  called from `services/` whose **latest** definition does not contain `auth.uid()`. Fix without a
  `_v2` if the guard is **silent** (another user's id → empty, `FALSE`, nothing deleted; a `RAISE`
  would be a new refusal) and lets through a NULL id that a function read as "no viewer". Take the
  body from `pg_get_functiondef`; first check that **every** build sends the session's id (older
  services: git history).
- Every new table touched by `service_role` needs its `GRANT` (the upsert fails silently, visible
  only in the function's logs).

## Types and values

- **`DOUBLE PRECISION` returned by PostgREST is rounded to 15 digits** (`extra_float_digits = 0`):
  a cursor key in seconds with microseconds comes back wrong (the page starts over). Cursor in
  `timestamptz` or an integer of milliseconds.
- Dividing a `NUMERIC` changes how it is written (`130.00 / 1` → `130.0000000000000000`); on the
  app side, add before rounding.
- **An enum value added cannot be used in the same transaction** (`unsafe use of new value`): add
  it in one migration, use it in the next, never in the same file.
- `GREATEST(…, COALESCE(x, 0))` never returns NULL: "not set" becomes 0. To keep NULL:
  `GREATEST(NULLIF(sum, 0), x)`.
- A new column filtered with `IS TRUE` empties the list in production until it is backfilled (it
  is born NULL): a temporary value that reproduces the current behavior, or `IS NOT FALSE`.
- Reserved words as a returned column name: `position` (and check `count`, `month`).
- `now()` **does not move inside a transaction**: a column that must order rows written in the
  same transaction takes `clock_timestamp()` (or a tiebreak on `id`); a time-dependent function
  takes `arg_now DEFAULT now()` so it can be tested.

## Constraints

- A non-deferrable `UNIQUE (user_id, sort_order)` breaks a full reordering in one `UPDATE` →
  `DEFERRABLE INITIALLY IMMEDIATE`.
- **Two `SET NULL` cascades on the same row make the delete fail** (the first update checks the
  other key, which still points to a deleted row → `23503`): keys `DEFERRABLE INITIALLY DEFERRED`.
  A pgTAP test sees it; production does not, until the day it happens.
- A unique constraint turned into a partial index breaks `ON CONFLICT`: each one must repeat the
  predicate. Find every `ON CONFLICT` on the table before migrating.
- PL/pgSQL with temporary tables: `DROP TABLE IF EXISTS pg_temp.x` at the top and `ON COMMIT DROP`.

## Reading, Storage, hosted database

- Reading a table page by page: stop on an **empty** page, not on a short one (the server may cap
  it); cross-check with `count: 'exact'` before any delete.
- `DELETE` on `storage.objects` is refused (`storage.protect_delete`), and it would only delete the
  row: use the Storage API.
- The `postgres` role of the hosted SQL Editor is not a superuser (`ALTER DATABASE … SET` refused):
  secrets go in Vault.
- A PostgREST `.in()` query over GET: split into batches (URL > 260,000 characters →
  `Invalid URL`). Bulk import: batches + a proactive delay, a safety cap (the edge function's CPU
  time limit).
