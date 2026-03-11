---
name: modify-server-api
description: "This skill handles editing server API documentation in ZEGO/ZEGOCLOUD docs. Server API docs use a dual-file structure where YAML files define OpenAPI specs and MDX files are auto-generated. Always edit the YAML source file, never the MDX directly. 触发短语: 'update server API', '更新服务端API', 'edit API docs', '编辑API文档', 'modify API description', '修改API描述', 'change API parameter', '更改API参数'. Also triggers when an MDX file's frontmatter contains both 'id' and 'api' keys."
---

# modify-server-api

This skill handles editing server API documentation in ZEGO/ZEGOCLOUD documentation projects. Server API documentation follows a special dual-file structure where:

- **YAML files**: Define the OpenAPI specification (the source of truth)
- **MDX files**: Auto-generated from yaml files by the `docuo god <openapi-group-name>` command

## When to Use This Skill

Trigger this skill when:
1. User explicitly states they want to edit **server API** documentation
2. User provides a file path and the mdx file's frontmatter contains both `id` and `api` keys

Example mdx frontmatter for server API:
```yaml
---
id: close
title: "CloseRoom"
description: "调用本接口将把房间内所有用户从房间移出，并关闭房间。"
api: eJztWWtTE1ka...
---
```

## Workflow

### Step 1: Identify the YAML File

When given an mdx file path, always find and edit the corresponding yaml file instead:
- If user provides: `path/to/api-name.mdx`
- Edit: `path/to/api-name.yaml`

The yaml file is always in the same directory with the same name but different extension.

### Step 2: Verify OpenAPI Configuration

Check that the yaml file is properly configured in `docuo.config.json` under the `openapi` node:

```json
"openapi": {
  "rtc": [
    {
      "specPaths": ["core_products/real-time-voice-video/zh/server/api-reference/room/*"],
      "outputDir": "core_products/real-time-voice-video/zh/server/api-reference/room"
    }
  ],
  "zim": [...],
  "aiagent": [...],
  ...
}
```

To verify:
1. Find the yaml file's directory path
2. Search for that path pattern in the `specPaths` arrays
3. Note the openapi group name (e.g., "rtc", "zim", "aiagent")

If the yaml file is NOT configured in openapi, inform the user before proceeding.

### Step 3: Edit the YAML File

Make the requested changes to the yaml file. The yaml file follows OpenAPI 3.0 specification:

```yaml
openapi: 3.0.0
info:
  title: open-api-desc
  version: 1.0.0

tags:
  - name: room

servers:
  $ref: '../shared-components.yaml#/servers'

paths:
  /:
    get:
      tags:
        - room
      summary: CloseRoom
      description: |
        API description in markdown format...
      operationId: close
      parameters:
        - name: Action
          in: query
          description: Parameter description
          required: true
          schema:
            type: string
            enum: [CloseRoom]
      responses:
        "200":
          description: Success response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseSchema'

components:
  schemas:
    ResponseSchema:
      type: object
      properties:
        Code:
          type: integer
          description: Response code
```

### Step 4: Run `docuo god` Command

After editing the yaml file, regenerate the mdx file:

```bash
cd <documentation_root>
docuo god <openapi-group-name>
```

### Step 5: Verify MDX File Update

Check if the corresponding mdx file has been updated:

```bash
git status path/to/api-name.mdx
# or
git diff path/to/api-name.mdx
```

If the mdx file shows changes, the server API edit is complete.

## Important Rules

1. **Never edit mdx files directly** for server API documentation - they are auto-generated and will be overwritten
2. **Always edit the yaml file** - it's the source of truth
3. **Always verify openapi configuration** before making changes
4. **Always run `docuo god <openapi-group-name>`** after editing to regenerate mdx files
5. **Always verify the mdx was updated** to confirm the edit was successful

## OpenAPI Groups Reference

Common openapi groups in `docuo.config.json`:

run `docuo god --list` to see all available groups.

## Example Usage

User: "Please update the CloseRoom API description"

1. Find the yaml file: `core_products/real-time-voice-video/zh/server/api-reference/room/close.yaml`
2. Verify it's in openapi config under "rtc" group
3. Edit the yaml file's `description` field
4. Run `docuo god rtc`
5. Verify `close.mdx` was updated
