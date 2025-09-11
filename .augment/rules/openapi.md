---
type: "manual"
---

# OpenAPI 文档生成与维护规范（ZEGO 服务端 API 通用）

以下规则总结自本轮改造工作，适用于 ZEGO 所有服务端 API 文档（各产品线/语言/区域）对应的 OpenAPI YAML 的生成与后续维护。

## 目录与命名
- 每个 mdx 对应一个同名 yaml，目录结构与 mdx 所在目录一致。
- operationId 使用 mdx 文件名（不带扩展名），如 start-cdn-recrod.mdx → operationId: start-cdn-recrod。
- tags 取 mdx 所在目录名，例如：cdn、room、media-service、stream-mixing、moderation、scene。

## OpenAPI 基本骨架
- openapi 版本统一为 3.0.0，info 中保持 title=open-api-desc、version=1.0.0、contact 为 ZEGO 支持邮箱。
- 每个 YAML 必须显式包含 servers，且使用共享文件统一维护：
  - 在 paths 节点前加入：
    servers:
      $ref: '../shared-components.yaml#/servers'
  - 特例（如 scene/set-scene-template 走 metaworld 域名）如需差异化，先与维护者确认；缺省仍引 shared-components.yaml。

## 公共参数与 Action
- 公共参数统一从 shared-components.yaml 引用：
  - AppId、SignatureNonce、Timestamp、Signature、SignatureVersion、IsTest。
- GET/POST 的参数顺序：
  1) Action
  2) 公共参数（如上）
  3) 业务参数（按 mdx 定义）
- Action 字段要求：
  - 必填，in=query，schema.enum 为具体 Action 值（例如 MergeMedia）。
  - description 使用固定 MD 块，格式如下：
    > 接口原型参数
    >
    > https://rtc-api.zego.im?Action=YourAction

## paths 与方法
- paths 下仅保留根路径 /。
- 请求方法遵循 mdx：GET 或 POST。POST 场景使用 requestBody.application/json，Schema 从组件中引用。

## 类型与格式
- 明确的数值类型补充 format：
  - int32、int64、uint32、float 等；时间戳统一 int64 秒（按 mdx）。
- 枚举使用 enum 指定合法值；必要时 default 与 enum 同步约束。
- array 参数采用 style=form + explode=true 以支持多值形态。

## 响应结构
- 统一包含 Code、Message、RequestId、Data 四层结构（除非 mdx 特别说明返回为空）。
- Data 内的厂商差异（如 Tencent、Huawei、Ws）要按照 mdx 列表精确还原结构与字段。

## 生成流程（操作步骤）
1) 读取对应 mdx，确定：请求方法、Action、业务参数、响应结构与示例、频率限制与注意事项。
2) 新建同名 yaml，填充固定骨架：openapi、info、tags、servers（$ref）、paths:/、方法、Action 描述块、公共参数 $ref。
3) 按 mdx 定义补充业务参数，保持顺序与约束（required、enum、format、样例）。
4) 依据 mdx 的“响应参数/示例” 定义 components.schemas，注意多厂商差异结构与字段。
5) 保存并在 TASKS.md 勾选条目。

## 其他约定
- 禁止在 YAML 内手写 servers 列表，统一引用 shared-components.yaml。
- 如需新增服务器域或特殊域名，先在 shared-components.yaml 维护后再通过 $ref 引用。
- 不要在 YAML 内定义或复制公共参数实体，统一从 shared-components.yaml 引用，避免漂移。
- 对于 POST 接口，Headers 信息在文档说明即可，不在 OpenAPI 中强制定义。
- 如 mdx 中存在“厂商限定生效”的参数/字段，需在 description 中明确。

## 示例片段
- 引用 servers：
  servers:
    $ref: '../shared-components.yaml#/servers'
- 引用公共参数：
  - $ref: '../shared-components.yaml#/components/parameters/AppId'
  - $ref: '../shared-components.yaml#/components/parameters/IsTest'
- Action 描述模板：
  description: |
    > 接口原型参数
    >
    > https://rtc-api.zego.im?Action=MergeMedia'
