# Avoid Secret Leak

**When:** Logging, errors, API responses, or client bundles.

**Do:** Env vars for secrets; redact tokens in logs; never return secrets in API payloads.

**Don't:** Log `process.env`, JWT bodies, or API keys; don't commit `.env`.

**Verify:** Grep diff for secret patterns; client bundle has no private keys.
