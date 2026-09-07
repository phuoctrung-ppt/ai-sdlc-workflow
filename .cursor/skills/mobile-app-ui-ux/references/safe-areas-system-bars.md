# Safe areas & system bars

## Why

Notches, status bars, home indicators, and Android gesture/nav bars can cover content. Edge-to-edge drawing makes insets **mandatory**.

## Default stack (Expo / RN)

```tsx
import { SafeAreaProvider, SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

// Root (if template does not already wrap)
<SafeAreaProvider>{/* app */}</SafeAreaProvider>

// Full screen padding
<SafeAreaView style={{ flex: 1 }}>{/* … */}</SafeAreaView>

// Per-edge
const insets = useSafeAreaInsets();
// paddingTop: insets.top, paddingBottom: insets.bottom, …
```

## System bars (Expo)

- Status bar: `expo-status-bar` — `style="auto" | "light" | "dark"`.
- Android navigation bar: `expo-navigation-bar` when customizing contrast.
- Do not hide bars for ordinary product screens.

## Checklist

- [ ] Root SafeAreaProvider present
- [ ] Headers / tab bars account for insets (or use navigator defaults that do)
- [ ] Fixed bottom CTAs sit above home indicator
- [ ] Landscape / notch left-right insets considered for full-bleed media

## Sources

- https://docs.expo.dev/develop/user-interface/safe-areas/
- https://docs.expo.dev/develop/user-interface/system-bars/
