# ClientAPI（客户端 API）结构标准

## 文档结构概述

客户端 API 文档由**多个 `ParamField` 组件**构成，每个 `ParamField` 组件代表一个接口说明。

```
客户端 API 文档
├── ParamField (接口1说明)
├── ParamField (接口2说明)
├── ParamField (接口3说明)
└── ...
```

## ParamField 组件规范

### 组件属性

| 属性 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | API 名称，如 `createEngine` |
| `prototype` | ✅ | 完整的 API 原型，包含返回值类型、参数类型 |
| `desc` | ❌ | API 概述，1-2 句话说明作用 |
| `prefixes` | ❌ | 前缀标签数组，如 `["static"]`、`["public", "static"]` |
| `suffixes` | ❌ | 后缀标签数组，如 `["deprecated"]` |
| `parent_file` | ❌ | 所属文件路径，如 `Declared in \`ZegoExpressEngine.java\`` |
| `parent_name` | ✅ | 父类/父接口名称 |
| `parent_type` | ✅ | 父类型，如 `"class"`、`"interface"`、`"protocol"`、`"enum"` |
| `titleSize` | ❌ | 标题级别，1-6，默认为 4 |
| `anchor_suffix` | ❌ | 锚点后缀，用于区分同名方法，如 `-v2` |

### 组件内容结构

每个 ParamField 组件内部按以下顺序组织内容：

```
1. **参数**（如有参数）
2. **详情**
3. <Note> 调用时机等信息
4. <Warning> 版本要求、使用限制、注意事项
5. **返回值**（如有返回值）
6. **回调**（异步 API，如有回调）
```

---

## 必需内容

### 1. 参数说明（**参数**）

当 API 有参数时，使用表格说明每个参数：

```markdown
**参数**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| profile | [ZegoEngineProfile](#zegoengineprofile) | 用来创建引擎的基础配置信息。 |
| eventHandler | [IZegoEventHandler](#izegoeventhandler) | 事件通知回调。传 [NULL] 则意味着不接收任何回调通知。 |
```

**参数描述要求：**
- 说明参数的作用
- 指明是否可传 `NULL`
- 说明取值范围（如有）
- 说明与其他参数的关联关系（如有）

### 2. 详情说明（**详情**）

```markdown
**详情**

创建 ZegoExpressEngine 单例对象并初始化 SDK。
```

简要描述该 API 的核心功能和用途。

### 3. 调用时机（`<Note>`）

```markdown
<Note title="">
- **调用时机**：SDK 其他实例方法调用之前。
</Note>
```

说明该 API 应该在什么时候调用，与其他 API 的调用顺序关系。

### 4. 版本与限制（`<Warning>`）

```markdown
<Warning title="">
- **支持版本**：2.14.0 及以上。
- **使用限制**：无。
- **注意事项**：SDK 只支持创建一个实例，如需重复调用，需先销毁。
</Warning>
```

**Warning 内容规范：**

| 字段 | 说明 |
|------|------|
| **支持版本** | 最低 SDK 版本要求 |
| **使用限制** | 功能限制、平台限制等 |
| **注意事项** | 使用时需要注意的关键点，避免踩坑 |

### 5. 返回值说明（**返回值**）

```markdown
**返回值**

引擎单例对象。
```

简要说明返回值的含义，类型已在 prototype 中体现。

### 6. 回调说明（**回调**）

对于异步 API，需要说明回调参数：

```markdown
**回调**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| onResult | IZegoCallback | 执行结果回调，包含错误码。 |
```

---

## 完整示例

```mdx
<ParamField
  name="createEngine"
  prototype="public [ZegoExpressEngine](#zegoexpressengine) createEngine([ZegoEngineProfile](#zegoengineprofile) profile, [IZegoEventHandler](#izegoeventhandler) eventHandler)"
  desc="创建 ZegoExpressEngine 单例对象并初始化 SDK。"
  prefixes={["static"]}
  parent_file="Declared in \`ZegoExpressEngine.java\`"
  parent_name="ZegoExpressEngine"
  parent_type="class">

**参数**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| profile | [ZegoEngineProfile](#zegoengineprofile) | 用来创建引擎的基础配置信息。 |
| eventHandler | [IZegoEventHandler](#izegoeventhandler) | 事件通知回调。传 [NULL] 则意味着不接收任何回调通知，之后也可通过 [setEventHandler] 进行设置。 |

**详情**

创建 ZegoExpressEngine 单例对象并初始化 SDK。

<Note title="">
- **调用时机**：SDK 其他实例方法调用之前。
</Note>

<Warning title="">
- **支持版本**：2.14.0 及以上。
- **使用限制**：无。
- **注意事项**：SDK 只支持创建一个实例，如需重复调用 [createEngine]，则需在第二次调用前先调用 [destroyEngine] 函数销毁引擎，否则返回的是上次创建的对象。
</Warning>

**返回值**

引擎单例对象。
</ParamField>

<ParamField
  name="destroyEngine"
  prototype="public void destroyEngine([IZegoDestroyCompletionCallback](./interface#izegodestroycompletioncallback) callback)"
  desc="销毁 ZegoExpressEngine 单例对象并反初始化 SDK。"
  prefixes={["static"]}
  parent_file="Declared in \`ZegoExpressEngine.java\`"
  parent_name="ZegoExpressEngine"
  parent_type="class">

**参数**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| callback | [IZegoDestroyCompletionCallback](./interface#izegodestroycompletioncallback) | 销毁引擎完成的通知回调，确保设备硬件资源被释放完成。 |

**详情**

销毁 ZegoExpressEngine 单例对象并反初始化 SDK。

<Note title="">
- **调用时机**：当不再使用 SDK 时，可以通过本接口释放 SDK 使用的资源。
</Note>

<Warning title="">
- **支持版本**：1.1.0 及以上。
- **使用限制**：无。
- **注意事项**：如果单例对象未被创建或已被销毁，调用此函数不会收到相关回调。
</Warning>
</ParamField>
```

---

## 检查清单

### 属性检查
- [ ] `name` 是否与实际 API 名称一致
- [ ] `prototype` 是否与实际代码签名一致
- [ ] `desc` 是否简洁准确地描述 API 作用

### 内容检查
- [ ] 参数说明是否完整（类型、描述）
- [ ] 参数描述是否包含 NULL 说明、取值范围等
- [ ] 详情是否清晰
- [ ] Note 是否说明调用时机
- [ ] Warning 是否包含版本、限制、注意事项
- [ ] 返回值说明是否清晰（有返回值时）
- [ ] 回调说明是否完整（异步 API）

### 链接检查
- [ ] 类型链接是否正确指向锚点或文件
- [ ] API 交叉引用是否正确（如 [createEngine]）

### 格式检查
- [ ] 表格格式是否正确
- [ ] 组件标签是否正确闭合
- [ ] Markdown 语法是否正确
