# CI pitfalls (GitHub Actions)

## Browser tests (Puppeteer)

- **Chrome's download in `npm ci`'s `postinstall` can fail without failing the install** (signs:
  an unusually long `npm ci`, then browser tests failing within seconds). Add a step
  `npx puppeteer browsers install chrome` after `npm ci`.
- **Reading a failed job without `gh`**: job logs require sign-in, even on a public repository.
  Without it, compare step durations with a green run
  (`api.github.com/repos/<owner>/<repo>/actions/runs/<id>/jobs`), or run the suite locally
  (`npx puppeteer browsers install chrome`, about 330 MB in `~/.cache/puppeteer`).
