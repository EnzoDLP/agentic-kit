# auth-js client

- auth-js 2.93 with `lock: processLock`: "Lock … acquisition timed out after 10000ms" is logged on
  **every** lock acquisition (a timer never cleared), even one granted at once. Noise, not a
  deadlock: `debug: true` in the auth options shows acquisitions and releases within a few ms.
  Fixed in auth-js 2.109 (timer cleared).
- In 2.118 the `lock` option is deprecated (a warning at startup): remove it from `createClient`;
  the client coordinates its refreshes without a lock, and the warning is gone.
