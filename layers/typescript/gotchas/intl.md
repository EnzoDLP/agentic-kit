# Intl pitfalls

- Formatting a currency in French, Node writes U+00A0 (no-break space) before the symbol and U+202F
  (narrow no-break space) between thousands: tests write them as ` ` / ` `, never as a
  plain space.
