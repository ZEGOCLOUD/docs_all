# Conditional Rendering

Display content based on platform, version, or other conditions.

## How It Works

Conditional rendering uses conditions passed via props when the MDX file is used as a React component. Common use case: multi-platform documentation reuse.

## Syntax

### Current Platform Condition

Content visible only on current platform (where `props.platform` is undefined):

```mdx
:::if{props.platform=undefined}
这段内容仅在当前平台显示。
:::
```

### Specific Platform Condition

Content visible only on specified platform:

```mdx
:::if{props.platform="iOS"}
这段内容仅在 iOS 平台显示。
:::

:::if{props.platform="Android"}
这段内容仅在 Android 平台显示。
:::
```

## Multiple Conditions (OR)

Use `|` to combine conditions. **Note: Only OR conditions supported, not AND.**

```mdx
:::if{props.platform="undefined|iOS|Android|Web"}
本文件、iOS、Android 和 Web 专属内容
:::
```

## Common Patterns

### Shared Content with Exceptions

We assume the following example is written on the Android platform:

```mdx
:::if{props.platform="undefined|iOS"}
This applies to iOS and Android platforms.
:::

:::if{props.platform="Web"}
This is Web-specific content.
:::
```

## Best Practices

1. **Always include `undefined` for self-referencing** - When the MDX file views itself, platform is undefined
2. **Use OR conditions for shared platforms** - Combine multiple platforms with `|`
3. **Keep conditional blocks clear** - Avoid deeply nested conditions
4. **Test all platform combinations** - Verify content appears correctly on each platform
