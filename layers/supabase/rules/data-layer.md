# Supabase — data layer

A service (`services/<feature>.service.ts`, one function named after the action) = one Supabase
call (`rpc()` / `functions.invoke()`) **and** the snake_case → camelCase mapping: the rest of the
app never sees snake_case.

```ts
export const fetchNoteDetails = async (noteId: string): Promise<IResponseNoteDetails> => {
  const { data, error } = await supabase.rpc('fetch_note_details', { arg_note_id: noteId })
  if (error) throw error

  const item = data?.[0]
  if (!item) throw new Error(`Note not found: ${noteId}`)

  return { id: item.id, title: item.title, coverUrl: item.cover_url }
}
```

- **Always check that the row exists** before mapping (an unguarded `data[0]` crashes in
  production).
- Several parameters → one `IBody…` object; responses typed `IResponse…`. `if (error) throw error`,
  no `try/catch`: the error goes up to React Query. No reference to React, i18n or the theme.
- Services and query factories do not receive the user (RPCs read `auth.uid()`); a caller never
  sends a `userId`.
- Services already return mapped data: no `select: (d) => d.data` in queries.
- Keyset pagination: a tiebreaker that follows the sort direction (`… DESC, id DESC`), a cursor key
  in `timestamptz` or an integer (never a float with more than 15 digits: PostgREST rounds it);
  filter inside the RPC.

| Item          | Convention                            | Example                     |
| ------------- | ------------------------------------- | --------------------------- |
| SQL / RPC     | snake_case, arguments prefixed `arg_` | `archive_note(arg_note_id)` |
| Edge function | camelCase                             | `uploadAvatar`              |
| API types     | `IResponse[X]` / `IBody[X]`           | `IBodyArchiveNote`          |
