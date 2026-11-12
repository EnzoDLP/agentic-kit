# API keys, database-called functions and advisors

## New API keys

- `SUPABASE_ANON_KEY` and `SUPABASE_SERVICE_ROLE_KEY`, injected by default into edge functions,
  are the legacy JWT keys, marked "Deprecated" (end planned for late 2026), and still work. The new
  ones: `SUPABASE_PUBLISHABLE_KEYS` / `SUPABASE_SECRET_KEYS`, JSON indexed by name
  (`JSON.parse(Deno.env.get('SUPABASE_SECRET_KEYS')!).default`), and on the app side an
  `sb_publishable_…` key. **Never disable the legacy keys** in the dashboard while a supported
  store build embeds the legacy anon key: it would stop working.
- An older project has no new keys until they are created (Settings → API Keys): create them
  **before** deploying functions that read them.
- supabase-js (2.118 included) sends an `sb_…` key as `apikey` **and** as `Authorization: Bearer`
  to the database, storage and auth (only `functions.invoke` leaves it out of `Bearer`): the
  gateway accepts it, an admin client `createClient(url, secretKey)` works as is.
- Local runtime (CLI 2.106): it injects `SUPABASE_PUBLISHABLE_KEYS` / `SUPABASE_SECRET_KEYS`
  (`{"default": …}`) into functions, but its `verify_jwt` requires a real JWT: an `sb_…` key alone
  is refused with 401.

## Functions called by the database

- A dashboard Database Webhook is a trigger (`supabase_functions.http_request`) outside the
  migrations: absent locally, its key in clear text in the trigger definition (often the
  `service_role` key), and a function that only accepts it often checks nothing (callable with the
  anon key). Replace it with a trigger in a migration that reads the URL and a dedicated secret
  from Vault (`net.http_post`), the function in `verify_jwt = false` (`[functions.<name>]` in
  `config.toml`, read by `functions deploy`) comparing `Authorization: Bearer <secret>`.
- Switching over with no gap or duplicate: create the secrets before pushing; until the functions
  are deployed, the old one serves the webhook and refuses the trigger (no JWT), then the new one
  refuses the webhook, which is deleted afterwards.
- From the local database container, functions are at `http://kong:8000/functions/v1/…`.

## Advisors

- `authenticated_security_definer_function_executable`: one line per RPC, that is the
  architecture; check that each name is called by the app, a store build or the website, otherwise
  it is an internal function missing its `REVOKE`.
- `anon_security_definer_function_executable`: exactly the project's allowlist.
- `extension_in_public` on `pg_net`: Supabase's own location, do not move it.
- `auth_leaked_password_protection`: no effect without passwords (anonymous, Google, Apple
  sign-in).
