---
name: supabase-rpc
description: Write or change a Supabase migration, RPC, table, grants, RLS policy, pgTAP test or edge function — the RPC template, compatibility with store builds (_v2), anon / authenticated grants, Vault, Storage. Load before any SQL migration, RPC or edge function.
---

# Supabase — RPC, migrations, edge functions

Pitfalls, one file per topic, read the matching one before retrying an approach that failed:
`.claude/agentic-kit/layers/supabase/gotchas/`.

## 1. Never the cloud without the user's explicit request

**Every `supabase` command targets the local Postgres / Docker.** CI is the only deployment path: a
`git push` to a branch that deploys **is** a deployment.

- `supabase migration up` targets local by default; `--linked`, `--db-url`, `--project-ref`
  switch to the remote: **never** without a request.
- `migration list`, `gen types`: always `--local`. `db reset`, `db push`, `db pull`,
  `functions deploy`, `link`: only on request, never "to check".
- `docker exec supabase_db_<project> …` targets the local container (check the name when in
  doubt).
- `npx supabase migration new <name>` **`< /dev/null`** (otherwise it reads standard input and
  creates an empty file). Never edit a pushed migration: write a new one.
- Types: **`npm run gen:types`** (`scripts/gen-types.sh`: Supabase CLI at a pinned version +
  Prettier), never `gen types` by hand nor with `2>&1`. A project without that script: add it.
  Never write the types file through a shell redirect (`… > lib/database.types.ts`): the script is
  its only writer. Regenerate on **every** schema change; CI reruns the script and fails if the
  committed file differs.
- The project's data-model doc, if it keeps one, changes **in the same commit** as the migration.

## 2. An RPC or edge function in production: never changed in place without proof, else `_v2`

Installed versions of the app call the same functions with the same arguments for their whole life.
Change in place only if **every existing call stays valid and receives the same thing**, give or
take added columns — the **input** matters as much as the output.

- **Safe**: add a parameter with a default, at any position (PostgREST calls by **named**
  parameters); add a column to `RETURNS TABLE` (JSON objects by name) — but `CREATE OR REPLACE`
  rejects any change to `RETURNS TABLE` (42P13): `DROP FUNCTION` + `CREATE FUNCTION` + grants put
  back; edge function: a fully additive new mode, or an internal field never returned.
- **Never safe without `_v2`**: rename, remove, retype or make required a parameter; reject a value
  accepted until now (a new `RAISE`); rename, remove or retype a column; change a default
  behavior; rename a column that a deployed edge function writes (migrations run before functions).
  **When in doubt, `_v2`**, with the justification written next to the change.
- Before a production release: replay every migration on the target branch's state (a script on a
  throwaway database, as CI does), check each supported store build's calls against the schema (a
  contracts check), review the project's API compatibility log. After each store build: add it to
  that log. JS published by EAS Update counts as a build.
- What bounds compatibility in time: the **minimum supported version** (version gating; in an Expo
  app, `expo-app-shell`). Raising it is what later allows deleting old functions.

## 3. RPC — the 7 points, no exception

```sql
CREATE OR REPLACE FUNCTION public.do_something(arg_thing_id UUID)
RETURNS VOID
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_user_id UUID := (SELECT auth.uid());
BEGIN
    IF v_user_id IS NULL THEN
        RAISE EXCEPTION 'Unauthorized user';
    END IF;
    -- tables prefixed with public.
END;
$$ LANGUAGE plpgsql;

REVOKE EXECUTE ON FUNCTION public.do_something FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.do_something TO authenticated;
```

1. RLS enabled on **every** table, **with no policy** (everything goes through `SECURITY DEFINER`
   RPCs; an "owner" policy would reopen direct access).
2. `SECURITY DEFINER`.
3. `SET search_path = ''`, tables prefixed with `public.`.
4. Arguments prefixed with `arg_`.
5. **Identity read from `auth.uid()` only**: a new RPC takes **no** `arg_user_id`. Production RPCs
   that already receive one keep it (removing it needs a `_v2`) and compare it to `auth.uid()`.
6. `REVOKE … FROM PUBLIC, anon` **then** `GRANT … TO authenticated` (without the `GRANT`,
   "permission denied").
7. Business validations through `RAISE EXCEPTION`.

- **`anon` executes only the project's allowlist** (functions called without an account, public
  pages of the website): every new public function needs an explicit `GRANT … TO anon` and its
  place in the pgTAP test that pins that allowlist. The app's anonymous accounts are
  `authenticated`.
- Internal function (trigger, cron): `REVOKE … FROM PUBLIC, anon, authenticated`, no `GRANT`
  (except `service_role` if an edge function calls it). Created without explicit grants, it would
  be callable through `/rest/v1/rpc/…`.
- Every new table written by `service_role` needs its own `GRANT` (bypassing RLS does not exempt
  it; the failure only shows in the function's logs).
- Check grants after a `DROP` + `CREATE`:
  `SELECT proname, has_function_privilege('anon', p.oid, 'EXECUTE'), proacl FROM pg_proc p JOIN
pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = 'public' ORDER BY 1;`
- Database-side secrets: **Vault** (`vault.create_secret`), never in a migration.
- Storage files: deleted through the Storage API, never in SQL. No `SELECT` policy that would make
  a bucket listable.

## SQL tests

Every new or changed RPC is tested first in **pgTAP** (`supabase/tests/`, run by
`scripts/test-db.sh` against the local Postgres and in CI; each file inside a rolled-back
transaction, `SET LOCAL request.jwt.claims` to choose the user), seen red before the migration.

## Edge functions (Deno)

One per use, camelCase. They hide third-party secrets and handle uploads. **Thin handler**: the
logic goes into `supabase/functions/_shared/` (no Deno nor React Native, tested by Jest, imported
relatively with `.ts` on the Deno side and through `@/` on the app side). `supabase/functions` is
excluded from the `tsconfig` and from ESLint. A function called from a website answers 2xx to
`OPTIONS` (invisible locally: Kong answers the preflight by itself). Secrets:
`supabase/.env.local` locally, the dashboard remotely.

**Project keys**: `SUPABASE_PUBLISHABLE_KEYS` / `SUPABASE_SECRET_KEYS` (JSON indexed by name,
`default`), read by a pure helper in `_shared/` that fails at startup if the key is missing; never
`SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY` (deprecated, end planned for late 2026).
supabase-js as `npm:@supabase/supabase-js@<v>`, the app's version.

**Function called by the database**: a trigger in a migration (`net.http_post`, URL and a
dedicated secret read from Vault), never a dashboard Database Webhook. The function runs with
`verify_jwt = false` and compares `Authorization: Bearer <secret>` (a pure helper in `_shared/`).
