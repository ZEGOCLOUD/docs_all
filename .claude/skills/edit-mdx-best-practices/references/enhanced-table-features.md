# Table Features

Enhanced table syntax for column width, alignment, and cell merging.

## Column Width

Add `-width` after header cell:

```markdown
| 名称-30% | 描述-50% | 备注-20% |
|----------|----------|----------|
| 内容1    | 内容2    | 内容3    |
```

### Supported Formats

- **Percentage**: `标题-30%`
- **Pixels**: `标题-120px`

## Alignment

Add alignment suffix after header:

```markdown
| 左对齐-l | 居中-c | 右对齐-r |
|----------|--------|----------|
| 左       | 中     | 右       |
```

| Suffix | Meaning |
|--------|---------|
| `-l` | Left align |
| `-c` | Center align |
| `-r` | Right align |

## Combined Width and Alignment

```markdown
| 名称-30%-l | 数值-20%-r | 描述-50%-c |
|------------|------------|------------|
| 苹果       | 100        | 水果       |
```

## Cell Merging

### Merge Markers

| Marker | Description |
|--------|-------------|
| `!mu` or `!m` | Merge up (with cell above) |
| `!md` | Merge down (with cell below) |
| `!ml` | Merge left (with cell to the left) |
| `!mr` | Merge right (with cell to the right) |

### Vertical Merge Example (Up)

```markdown
| 类别   | 项目   | 说明   |
|--------|--------|--------|
| 水果   | 苹果   | 红色   |
| !mu    | 香蕉   | 黄色   |
| !mu    | 橙子   | 橙色   |
| 蔬菜   | 白菜   | 绿色   |
```

Result: "水果" cell spans 3 rows vertically.

### Horizontal Merge Example (Left)

```markdown
| 姓名   | 联系方式       | !ml    |
|--------|----------------|--------|
| 张三   | 电话           | 邮箱   |
```

Result: "联系方式" header spans 2 columns horizontally.

## Best Practices

1. **Use percentages for responsive layouts** - Tables adapt better to different screen sizes
2. **Keep merges simple** - Complex merges can be hard to maintain
3. **Align numbers right** - For columns with numerical data, use `-r` alignment
4. **Test rendering** - Verify merged cells render correctly in preview
