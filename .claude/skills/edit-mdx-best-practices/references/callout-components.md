# Callout Components

Display different types of informational messages in documentation.

## Components

### Callout (Base Component)

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| type | `"check" \| "tips" \| "note" \| "warning" \| "failure"` | Yes | Callout type |
| title | `string` | No | Title text |

**Example:**
```mdx
<Callout type="note" title="注意">
  这是一条注意事项。
</Callout>

<Callout type="warning" title="警告">
  这是一条警告信息。
</Callout>
```

### Shortcut Components (Recommended)

Shorter, more convenient alternatives to the base Callout component:

```mdx
<Note title="注意">这是一条注意事项</Note>
<Tip title="提示">这是一条提示信息</Tip>
<Warning title="警告">这是一条警告信息</Warning>
<Error title="错误">这是一条错误信息</Error>
```

## When to Use Each Type

| Type | Shortcut | Use Case |
|------|----------|----------|
| `note` / `check` | `<Note>` | General notes, important information |
| `tips` | `<Tip>` | Helpful tips, best practices |
| `warning` | `<Warning>` | Warnings, things to be careful about |
| `failure` | `<Error>` | Error conditions, what not to do |

## Best Practices

1. **Use shortcuts preferentially** - `<Note>` is cleaner than `<Callout type="note">`
2. **Add descriptive titles** - Helps users quickly understand the callout's purpose
3. **Keep content concise** - Callouts work best for brief, important information
4. **Use appropriate severity** - Match the callout type to the importance of the message
