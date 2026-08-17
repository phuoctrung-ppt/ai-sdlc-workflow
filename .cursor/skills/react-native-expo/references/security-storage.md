# Security & storage (React Native)

## Never

- API keys / client secrets in app source or `EXPO_PUBLIC_*`
- Tokens / passwords in **AsyncStorage** (unencrypted)
- Sensitive data in deep-link query strings
- Cleartext HTTP for APIs
- Tokens/PII to Sentry/Crashlytics without scrubbing

## Storage matrix

| Data | Storage |
|------|---------|
| Non-sensitive prefs, cache | AsyncStorage / MMKV (non-secret) |
| Access / refresh tokens, secrets | `expo-secure-store`, Keychain, EncryptedSharedPreferences / Keystore |
| Server secrets / private API keys | Backend only |

## Auth

- OAuth2 + **PKCE** for mobile redirects
- Treat deep links as untrusted input (validate + map server-side when possible)
- Prefer libraries that wrap platform AppAuth (e.g. `react-native-app-auth`) when IdP supports PKCE

## Network

- HTTPS always
- SSL pinning only when threat model warrants it — plan cert rotation so apps do not brick

## Sources

- https://reactnative.dev/docs/security
