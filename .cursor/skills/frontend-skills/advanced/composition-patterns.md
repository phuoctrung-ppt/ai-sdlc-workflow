# Composition Patterns (Advanced)

Prefer hooks over HOC/render-props for new code. Use these when integrating legacy or library APIs.

## Compound Components

```tsx
<Select>
  <Select.Trigger />
  <Select.Options>
    <Select.Option value="a">A</Select.Option>
  </Select.Options>
</Select>
```

Share state via Context inside the compound root.

## Render Props

```tsx
<DataLoader url="/api/users">
  {({ data, loading }) => loading ? <Spinner /> : <List items={data} />}
</DataLoader>
```

## HOC

```tsx
const withAuth = (Component) => (props) => {
  const user = useAuth();
  if (!user) return <Redirect to="/login" />;
  return <Component {...props} user={user} />;
};
```

**Avoid wrapper hell** — extract custom hooks when possible.
