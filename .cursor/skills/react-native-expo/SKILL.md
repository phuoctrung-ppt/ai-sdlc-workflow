---
name: react-native-expo
description: React Native + Expo implementation — Expo Router, lists, animations, SecureStore, perf. Not mobile UX rules (mobile-app-ui-ux); not Next.js RSC (frontend-skills).
---

# React Native + Expo

Portable implement skill for **RN / Expo apps**. Complements `mobile-app-ui-ux` (UX) and `frontend-skills` (web React).

## When to use

| Task | This skill |
|------|------------|
| Screens, navigation, lists, storage, animations on RN/Expo | Yes |
| Expo Router file routes, deep links as input | Yes |
| Product mobile UX only (touch, IA) | Pair with **mobile-app-ui-ux** |
| Next.js / RSC / web DOM | **No → frontend-skills** |

## Hard rules

1. **Release builds for perf claims** — never tune FPS only in dev (`dev=false` / release).
2. **Strip `console.*` in production** (Babel `transform-remove-console` or equivalent), including noisy middleware loggers.
3. **Lists** — virtualize (`FlatList` / FlashList); `getItemLayout` when row height fixed; stable `keyExtractor`.
4. **Animations** — native driver when properties allow; animate `transform` / `opacity`, not image width/height layout thrash.
5. **Navigation** — prefer native-stack transitions; Expo Router routes under `app/` with typed routes when available; deep-link params are **untrusted input**.
6. **Secrets** — never ship API secrets in the JS bundle; `EXPO_PUBLIC_*` / env libs are public config only.
7. **Token storage** — `expo-secure-store` / Keychain / Keystore — **not** AsyncStorage.
8. **Network / auth** — HTTPS only; OAuth **PKCE** for mobile; scrub tokens/PII from crash reporters.
9. **Safe area root** — `SafeAreaProvider` at root when the template does not already wrap it.
10. **New Architecture** — follow current [reactnative.dev](https://reactnative.dev) (not deprecated WG essays); check library compatibility before enabling.

## Anti-patterns

- Secrets in `EXPO_PUBLIC_*` or committed `.env`
- Tokens in AsyncStorage or unencrypted redux-persist
- Huge `ScrollView` of hundreds of rows
- Heavy JS work during stack transitions
- OAuth custom scheme without PKCE
- Profiling only on Debug builds

## References (lazy)

| File | When |
|------|------|
| `references/performance.md` | threads, lists, animations |
| `references/security-storage.md` | storage matrix + PKCE |
| `references/expo-router.md` | file routes, deep links |
| `references/sources.md` | URLs + SPDX |

## Attribution

Distilled from React Native docs (MIT) and Expo docs (MIT). See `references/sources.md`.
