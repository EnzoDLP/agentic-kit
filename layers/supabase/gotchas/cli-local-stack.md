# CLI and local stack

## Versions

- **CLI 3.0.0 (early November 2026) rejects a 2.x `config.toml`**: _"[inbucket] in
  supabase/config.toml is no longer supported. Use [local_smtp] instead"_, as early as
  `supabase stop`. An unversioned `npx supabase` and workflows on `supabase/setup-cli@v1` +
  `version: latest` move to 3.0 without warning: pin the version (the one used for types)
  everywhere, and migrate the config on purpose. **Pin a recent 2.x, not an old one**: in 2.106.0,
  `supabase gen types typescript --local` (positional form) asked for an access token in CI
  ("Access token not provided"); 2.122.1, the last 2.x, matches what `latest` installed. The
  `--lang=typescript` form works in 2.120.0.
- The CLI is not global: `npx supabase@<version>` (it still pulls missing images, ~1.5 GB).
- `gen types` changes format from one CLI version to the next: a pinned CLI in a script
  (`scripts/gen-types.sh`), the same locally and in CI. `> file 2>&1` corrupts the file.
- Supabase's example workflow ("Verify generated types are checked in") generates `types.gen.ts`:
  if the project's types live elsewhere (`lib/database.types.ts`), the `git diff` runs on an
  untracked file and the job always passes. Compare the committed file.

## Starting the stack

- Rancher Desktop: `npx supabase start -x vector,logflare` (`vector` cannot reach Rancher's Docker
  socket).
- **One stack at a time** on a small Docker VM (2 CPU / 4 GB): otherwise `HealthCheckTimeoutError`.
  `npx supabase stop` in the other project (data kept).
- `supabase start` while the database already runs (started by `db start`) reports "setup is
  running" and starts **nothing else** (no auth, API or storage): `supabase stop`, then `start`.
- `supabase/snippets/` must exist before `start` (otherwise `chown` is refused on the share and
  Studio does not start).
- After a Postgres image upgrade, `collation version mismatch`: `npx supabase db start`, then
  `REINDEX DATABASE …` and `ALTER DATABASE … REFRESH COLLATION VERSION` on `postgres`,
  `_supabase`, `template1` (`-U supabase_admin`).

## Edge runtime

- **Edge function created after `start`: "Function not found"** (the list is frozen when the
  container starts) → `npx supabase functions serve`, or `stop` / `start`. The runtime caches
  modules per worker → `docker restart supabase_edge_runtime_<project>` after a change; it can die
  silently (`docker ps`). From Postgres, the local API is `http://supabase_kong_<project>:8000`.
- Photos uploaded to the local database from a real phone: the stored address must be the one the
  device called (the dev machine's LAN IP); Kong forwards `x-forwarded-host` / `-port`. Build the
  URL from them in a `_shared` helper, copied with its test into every function that returns a
  Storage URL. A photo already stored with `127.0.0.1` still does not show on a phone: upload it
  again.

## Migrations

- `supabase migration new` without `< /dev/null` in a pipe: empty file, recorded as applied.
  Remove it from `supabase_migrations.schema_migrations` **locally** before running it again.
- `migration up` "already exists" (applied by hand) → `migration repair --status applied <ts>`,
  never `db reset`.
