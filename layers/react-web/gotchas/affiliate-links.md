# Affiliate links

- **Amazon: a short link loses the affiliate tag.** `amzn.eu/d/…` and `a.co/d/…` (the Amazon
  app's "Share" button) or `amzn.to` (other affiliates' links) redirect to the product page without
  keeping a `?tag=` added to the short link: the tracking ID earns nothing. First follow the
  redirects (server side, `redirect: 'manual'`, without downloading the body, only to Amazon
  hosts), then set `tag` on the product page URL and strip another affiliate's `linkCode` /
  `linkId` / `ascsubtag`.
- **Disclosure is mandatory**: the Amazon Associates agreement requires stating that you earn a
  commission on qualifying purchases; put a "Partner link" mention near the link and the sentence
  in the terms of use. On the web, add `rel="sponsored"` to the link.
- **A browser cannot read another site's redirect** (CORS): resolving a short link happens on a
  server (e.g. an edge function), not in the page. And a `window.open` fired after a network call
  is blocked as a popup: compute the link on load, not on click.
