# pgTAP tests

- Never `ROLLBACK TO SAVEPOINT` (results already counted are rolled back with it). To simulate a
  failure: `CHECK (false) NOT VALID` on a table **of our own** for the duration of the test.
- A failed pgTAP assertion is only a `not ok` line: `psql` still exits 0. The script that runs the
  tests reads the output (`^not ok` or `^# Looks like you (failed|planned)` → failure), otherwise
  CI stays green on a red test.
- A test never counts over a whole table: the local database holds the data of manual tries. Count
  on the file's own data (materialized views included: neutralize **every** table they aggregate).
- **A writing function called in a `WHERE`** (`WHERE code = create_x('…')`) runs for each row
  scanned: as many rows created as the table holds, a test that flakes with the local data. Call it
  in a subquery (`= (SELECT create_x('…'))`, run once) or in a `CREATE TEMP TABLE … AS`.
- Simulated JWT: `set_config('request.jwt.claims', …, true)` does not survive the transaction →
  explicit `BEGIN` / `ROLLBACK` (a `psql` in autocommit loses it).
- A script that replays every migration in one go (as CI does) catches a migration that depends on
  a newer one: it passes locally and breaks on deploy. Such a script stubs `pg_cron` (absent from
  the throwaway database): a migration that uses anything else from `cron` extends the stub.
