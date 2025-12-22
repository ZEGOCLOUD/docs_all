/**
 * MDX 文件解析器
 * 提取 headingData 和 methodAttrData
 */

import fs from 'fs';
import path from 'path';
import { HeadingData, MethodAttrData, ParamFieldAttrs, ParentType, PARENT_TYPES } from './types';
import { generateSlug, extractAnchorsFromParamField } from './slug';

/**
 * 创建空的 HeadingData 结构
 */
export function createEmptyHeadingData(): HeadingData {
  return {
    class: [],
    interface: [],
    enum: [],
    protocol: [],
    struct: [],
  };
}

/**
 * 创建空的 MethodAttrData 结构
 */
export function createEmptyMethodAttrData(): MethodAttrData {
  return {
    class: [],
    interface: [],
    enum: [],
    protocol: [],
    struct: [],
  };
}

/**
 * 从 MDX 内容中提取标题锚点
 * 匹配 ## 到 ###### 级别的标题
 */
export function extractHeadingsFromContent(content: string): string[] {
  const headingRegex = /^#{2,6}\s+(.+)$/gm;
  const headings: string[] = [];
  let match;

  while ((match = headingRegex.exec(content)) !== null) {
    const headingText = match[1].trim();
    const slug = generateSlug(headingText);
    if (slug && !headings.includes(slug)) {
      headings.push(slug);
    }
  }

  return headings;
}

/**
 * 从 MDX 内容中提取 ParamField 属性
 */
export function extractParamFieldsFromContent(content: string): ParamFieldAttrs[] {
  // 匹配 <ParamField ... > 或 <ParamField ... />
  // 先将换行符替换为空格以支持多行属性，避免使用 's' 标志
  const normalizedContent = content.replace(/\r?\n/g, ' ');
  // 使用更复杂的正则来处理属性值中包含 > 的情况
  // 匹配引号内的内容（包括>）或非>字符
  const paramFieldRegex = /<ParamField\s+((?:[^>"']|"[^"]*"|'[^']*')*?)(?:\/>|>)/g;
  const results: ParamFieldAttrs[] = [];
  let match;

  while ((match = paramFieldRegex.exec(normalizedContent)) !== null) {
    const attrsStr = match[1];
    const attrs = parseJsxAttributes(attrsStr);

    if (attrs.name) {
      results.push({
        name: attrs.name,
        parent_name: attrs.parent_name,
        parent_type: attrs.parent_type as ParentType | undefined,
        anchor_suffix: attrs.anchor_suffix,
      });
    }
  }

  return results;
}

/**
 * 解析 JSX 属性字符串
 */
function parseJsxAttributes(attrsStr: string): Record<string, string> {
  const result: Record<string, string> = {};
  // 匹配 key="value" 或 key='value'
  const attrRegex = /(\w+)=["']([^"']*)["']/g;
  let match;

  while ((match = attrRegex.exec(attrsStr)) !== null) {
    result[match[1]] = match[2];
  }

  return result;
}

/**
 * 从 clientApiPath 目录解析 HeadingData
 */
export function parseHeadingData(clientApiDir: string): HeadingData {
  const headingData = createEmptyHeadingData();

  for (const type of PARENT_TYPES) {
    const mdxPath = path.join(clientApiDir, `${type}.mdx`);
    if (fs.existsSync(mdxPath)) {
      const content = fs.readFileSync(mdxPath, 'utf-8');
      headingData[type] = extractHeadingsFromContent(content);
    }
  }

  return headingData;
}

/**
 * 从 clientApiPath 目录解析 MethodAttrData
 */
export function parseMethodAttrData(clientApiDir: string): MethodAttrData {
  const methodAttrData = createEmptyMethodAttrData();

  for (const type of PARENT_TYPES) {
    const mdxPath = path.join(clientApiDir, `${type}.mdx`);
    if (fs.existsSync(mdxPath)) {
      const content = fs.readFileSync(mdxPath, 'utf-8');
      const paramFields = extractParamFieldsFromContent(content);

      for (const attrs of paramFields) {
        const anchors = extractAnchorsFromParamField(attrs);
        for (const anchor of anchors) {
          if (!methodAttrData[type].includes(anchor)) {
            methodAttrData[type].push(anchor);
          }
        }
      }
    }
  }

  return methodAttrData;
}

