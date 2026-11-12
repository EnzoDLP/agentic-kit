# Git pitfalls

## Commit identity

- **The machine's global Git identity may be a work identity** (a client or employer email). In a
  personal **public** repository every commit would expose it. Before the first commit, set
  `git config user.name` and `git config user.email` **local to the repository**, with the GitHub
  noreply address `<id>+<login>@users.noreply.github.com` (the `id` is read from
  `api.github.com/users/<login>`). After the push, check the author on
  `api.github.com/repos/<owner>/<repo>/commits/<branch>`.
- **History keeps every identity and every file ever committed.** A private repository turned
  public exposes its whole history: start a public repository from a fresh history instead, or
  rewrite it knowingly.

## Agent session moved into a repository

- When a session started without a folder moves into a project, the desktop app may copy the
  session's working files into it at the same relative paths. They show up as `??` in
  `git status` and can hold personal or client data: remove them before any `git add`, and never
  run `git add -A` right after the move.
