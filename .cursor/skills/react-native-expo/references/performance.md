# React Native performance checklist

## Threads (mental model)

| Thread | Runs | Stall symptom |
|--------|------|----------------|
| JS | React render, business logic, bridge work | Frozen JS animations, laggy touchables |
| UI / main | Native views, scroll, native-stack transitions | Janky scroll / transform |

Target ≥60 FPS → ≤16.67ms/frame. Prefer **native-stack** so transitions survive JS stalls.

## Hard checklist

- [ ] Measure in **release** only
- [ ] Production: strip `console.*`
- [ ] Large lists: virtualized + `getItemLayout` when fixed height (or FlashList)
- [ ] `Animated` / Reanimated: native driver when possible
- [ ] Prefer `transform: [{ scale }]` over animating width/height on images
- [ ] Defer expensive `onPress` work (`requestAnimationFrame` / interaction-complete)
- [ ] Hardware texture / rasterize only while moving views; profile memory

## Anti-patterns

| Don't | Why |
|-------|-----|
| Tune in dev mode | JS artificially slow |
| Ship redux-logger / console spam | JS thread tax |
| Unvirtualized long lists | Scroll FPS collapse |
| JS work mid-transition | Dropped frames |

## Sources

- https://reactnative.dev/docs/performance
- https://reactnative.dev/docs/optimizing-flatlist-configuration
