# Vercel

## Node server (`server.js`)

- **The `node` preset is required**: without `"framework": "node"` in `vercel.json`, a project
  detected as "Other" is built as a **purely static** site (no function) and the API answers 404.
  With it, `public/` is served by the CDN first and everything else is routed to `server.js`.
- **Call `server.listen()` when the module starts**, not after an async load: Vercel detects the
  server at that call (docs: "Deploy a Node.js server"). Load data in parallel and await it in the
  routes.
- `node_modules` is not served: copy the front-end files you need into `public/` (e.g. an
  `npm run vendor` script).
- **Region**: `iad1` (Washington) by default; set `"regions": ["cdg1"]` (or the region near your
  users) in `vercel.json` (a single region on the Hobby plan). Check the
  `x-vercel-id: cdg1::cdg1…` response header.
- The disk is read-only except `/tmp`, and the instance can be frozen right after the response: a
  refresh started in the background stalls until the next request. Await what the response needs.

## Checking without deploying

- `vercel build` works **without an account**: write `.vercel/project.json` by hand,

  ```json
  {
    "projectId": "prj_local",
    "orgId": "team_local",
    "settings": { "framework": "node", "nodeVersion": "24.x" }
  }
  ```

  run `npx vercel@<version> build --yes` on a copy of the project, then read
  `.vercel/output/config.json` (routes) and `.vercel/output/functions/*/.vc-config.json` (bundled
  files). `node server.cjs` in the function's folder replays it.
