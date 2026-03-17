# API Documentation

ParamField component for documenting API parameters, methods, and properties.

## ParamField Component

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| name | `string` | Parameter/method name (required) |
| prototype | `string` | Function prototype signature (required) |
| desc | `string` | Brief description |
| prefixes | `string[]` | Prefix tags (e.g., static, async) |
| suffixes | `string[]` | Suffix tags (e.g., deprecated) |
| parent_file | `string` | Parent file path |
| parent_name | `string` | Parent class/interface name |
| parent_type | `"class" \| "interface" \| "protocol" \| "enum"` | Parent type |
| titleSize | `1 \| 2 \| 3 \| 4 \| 5 \| 6` | Heading level (default 4) |

### Example

```mdx
<ParamField
  name="createEngine"
  prototype="static createEngine(appID: number, server: string): ZegoExpressEngine"
  desc="创建 ZegoExpressEngine 实例"
  prefixes={["static"]}
  parent_name="ZegoExpressEngine"
  parent_type="class"
>
  详细说明和参数表格...
</ParamField>
```

## Anchor Generation

ParamField automatically generates anchors for linking.

### Basic Anchor

`name` attribute generates the base anchor:

```mdx
<ParamField name="createEngine" ... />
<!-- Generates anchor: #createengine -->
```

### Anchor with Suffix

Use `anchor_suffix` to differentiate methods with same name:

```mdx
<ParamField name="init" anchor_suffix="-v2" ... />
<!-- Generates anchor: #init-v2 -->
```

### Parent Context Anchors

When `parent_name` and `parent_type` are set, generates 3 anchors:

```mdx
<ParamField
  name="startPreview"
  parent_name="ZegoExpressEngine"
  parent_type="class"
  ...
/>
<!-- Generates anchors:
     #startpreview
     #startpreview-zegoexpressengine
     #startpreview-zegoexpressengine-class -->
```

### Objective-C Colon Methods

For OC methods with colons, generates additional first-segment anchor:

```mdx
<ParamField name="createEngineWithProfile:eventHandler:" ... />
<!-- Generates:
     #createenginewithprofileeventhandler
     #createenginewithprofile (first segment) -->
```

### Anchor Transformation Rules

1. All anchors are lowercase
2. Special characters are removed
3. Spaces become hyphens
4. Examples:
   - `Quick Start` → `#quick-start`
   - `createEngine` → `#createengine`

## Best Practices

1. **Always include prototype** - Shows the full method signature
2. **Use parent context for class methods** - Enables linking from multiple contexts
3. **Add descriptive desc** - Brief summary for quick reference
4. **Use prefixes appropriately** - Mark static, async methods clearly
