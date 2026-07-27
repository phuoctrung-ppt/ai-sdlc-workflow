# Avoid Double Fetch

**When:** Client component mounts and parent RSC also fetches the same resource.

**Do:** Single source — RSC passes `initialData` prop; client query uses `initialData` / `placeholderData`.

**Don't:** `useEffect` + fetch when parent already fetched.

**Verify:** Network tab shows one request per navigation.
