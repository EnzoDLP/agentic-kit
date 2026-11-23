# Intl pitfalls

- Formatting a currency in French, Node writes U+00A0 (no-break space) before the symbol and U+202F
  (narrow no-break space) between thousands: tests write them as ` ` / ` `, never as a
  plain space.
- A French **percentage** (`style: 'percent'`) puts U+00A0 before `%` (`87,3\u00a0%`), while a
  French integer groups thousands with U+202F (`1\u202f004`): the two spaces differ within the
  same locale.
