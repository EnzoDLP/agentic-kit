# Edge functions: outbound calls, shared code, testing without the runtime

## Outbound calls

- **Corporate TLS proxy on macOS** (a ZTNA client that decrypts HTTPS): the local edge runtime
  (a Docker container) refuses every outbound HTTPS call, "invalid peer certificate:
  UnknownIssuer": the Mac trusts the proxy's authority, the container does not. Replay the
  function's request from the Mac with Node, which does not use the keychain:
  `NODE_EXTRA_CA_CERTS=ca.pem node --env-file=supabase/.env.local try.mjs`, the authority exported
  by `security find-certificate -a -c "<authority>" -p /Library/Keychains/System.keychain` (its
  name: `openssl s_client -connect <host>:443 | grep issuer`). The script prints only the
  responses, never the credentials.
- **`FormData` and a forced `Content-Type`**: `fetch` (Node and Deno alike, and `axiod`, which
  passes it through) keeps a hand-written `Content-Type: multipart/form-data` **without a
  boundary**. Never force it with a `FormData`: `fetch` writes it with its boundary. A lenient
  server accepts the broken header; another will not.
- A third-party service credential never goes into GET parameters: it ends up in the access logs
  of every intermediary. Use a POST form.

## Code shared with the app (`_shared/`)

- **A `_shared` module that imports another one** (`./x.ts`, extension required by Deno) and that
  the app imports: TypeScript rejects the extension (TS5097) without
  `"allowImportingTsExtensions": true` in the app's `tsconfig` (allowed: `expo/tsconfig.base` has
  `noEmit`). Metro and Jest resolve the explicit extension with no setting. What is only a type:
  `import type`.
- To compare an old and a new version of a pure module without Jest:
  `node --experimental-strip-types` (Node 22) runs them as they are, provided type imports are
  `import type` and relative imports end in `.ts`.

## Without the local runtime (cloud sessions)

- **Real Deno**: the `deno` npm package in a scratch directory, the function copied out of the
  repository with a `deno.json` (`"nodeModulesDir": "none"`, the `esm.sh` import of supabase-js
  mapped to `npm:@supabase/supabase-js@<v>`), `deno check` for types, `deno run` of a script that
  replaces `globalThis.fetch` towards the third-party service, then imports `index.ts`. `pg_net`
  reaches it from the Postgres container through the Docker network gateway (`docker inspect`).
- Failing that: transpile the handler and its `_shared` modules (`typescript.transpileModule`),
  replace `Deno.serve` / `Deno.env.get`, intercept `fetch`; it does not replace a try on the real
  runtime.
- Cloud session (Linux container): `dockerd &`, the `mirror.gcr.io` mirror in
  `/etc/docker/daemon.json`, `SUPABASE_INTERNAL_IMAGE_REGISTRY=docker.io npx supabase@<v> db start`
  (database only); a shallow clone → `git fetch --unshallow` before a contracts check that reads
  git history.
