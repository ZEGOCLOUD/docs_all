/**
 * trans-api-short-link 主入口
 * 处理 API 文档内部短链接
 */

import fs from 'fs';
import path from 'path';
import {
  HeadingData,
  MethodAttrData,
  UrlMap,
  ParsedShortLink,
  InstanceWithClientApi,
  ProcessedInstanceData,
  ParentType,
  PARENT_TYPES,
} from './types';
import { generateSlug } from './slug';
import { parseHeadingData, parseMethodAttrData } from './parser';

/**
 * API 短链接转换控制器
 */
export class ApiShortLinkTransController {
  private docsRoot: string;
  private instanceDataMap: Map<string, ProcessedInstanceData> = new Map();

  constructor(docsRoot: string) {
    this.docsRoot = docsRoot;
  }

  /**
   * 初始化：加载配置并构建数据
   */
  async init(configPath: string): Promise<void> {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    const instances = this.extractInstancesWithClientApi(config);

    for (const instance of instances) {
      const data = this.buildInstanceData(instance);
      this.instanceDataMap.set(instance.id, data);
    }
  }

  /**
   * 从配置中提取含 clientApiPath 的 instances
   */
  private extractInstancesWithClientApi(config: any): InstanceWithClientApi[] {
    const instances: InstanceWithClientApi[] = [];

    for (const inst of config.instances || []) {
      if (inst.clientApiPath) {
        instances.push({
          id: inst.id,
          path: inst.path,
          routeBasePath: inst.routeBasePath || '',
          clientApiPath: inst.clientApiPath,
        });
      }
    }

    return instances;
  }

  /**
   * 构建单个 instance 的数据
   */
  private buildInstanceData(instance: InstanceWithClientApi): ProcessedInstanceData {
    const clientApiDir = path.join(this.docsRoot, instance.path, instance.clientApiPath);
    const urlMap = this.buildUrlMap(instance);
    const headingData = parseHeadingData(clientApiDir);
    const methodAttrData = parseMethodAttrData(clientApiDir);

    return { instance, urlMap, headingData, methodAttrData };
  }

  /**
   * 构建 URL 映射
   */
  private buildUrlMap(instance: InstanceWithClientApi): UrlMap {
    const baseUrl = `/${instance.routeBasePath}/${instance.clientApiPath}`.replace(/\/+/g, '/');
    const urlMap: UrlMap = {
      class: `${baseUrl}/class`,
      interface: `${baseUrl}/interface`,
      enum: `${baseUrl}/enum`,
      protocol: `${baseUrl}/protocol`,
      struct: `${baseUrl}/struct`,
    };
    return urlMap;
  }

  /**
   * 解析短链接
   */
  parseShortLink(shortLink: string): ParsedShortLink {
    // 类/枚举短链接：以 - 开头，如 @-ZegoEngine 或 @-ZegoEngine-class
    if (shortLink.startsWith('-')) {
      return this.parseHeadingShortLink(shortLink.slice(1));
    }
    // 方法/属性短链接
    return this.parseMethodShortLink(shortLink);
  }

  /**
   * 解析标题类短链接（类/枚举）
   */
  private parseHeadingShortLink(raw: string): ParsedShortLink {
    let specifiedType: ParentType | undefined;
    let anchorText = raw;

    // 检查是否有类型后缀
    for (const type of PARENT_TYPES) {
      const suffix = `-${type}`;
      if (raw.toLowerCase().endsWith(suffix)) {
        specifiedType = type;
        anchorText = raw.slice(0, -suffix.length);
        break;
      }
    }

    return {
      type: 'heading',
      raw,
      anchor: generateSlug(anchorText),
      specifiedType,
    };
  }

  /**
   * 解析方法类短链接
   */
  private parseMethodShortLink(raw: string): ParsedShortLink {
    // 处理重载后缀：__1 → -1
    const normalizedRaw = raw.replace(/__(\d+)$/, '-$1');
    return {
      type: 'method',
      raw,
      anchor: generateSlug(normalizedRaw),
    };
  }

  /**
   * 替换文件中的短链接
   */
  replaceShortLinksInFile(filePath: string, instanceId: string): string {
    const data = this.instanceDataMap.get(instanceId);
    if (!data) return fs.readFileSync(filePath, 'utf-8');

    let content = fs.readFileSync(filePath, 'utf-8');
    // 匹配 [text](@shortLink) 格式
    const shortLinkRegex = /(\[.*?\])\(@([^)]+)\)/g;

    content = content.replace(shortLinkRegex, (match, linkText, shortLink) => {
      const fullUrl = this.resolveShortLink(shortLink, data);
      if (fullUrl) {
        return `${linkText}(${fullUrl})`;
      }
      return match; // 未匹配到则保持原样
    });

    return content;
  }

  /**
   * 解析短链接为完整 URL
   */
  private resolveShortLink(shortLink: string, data: ProcessedInstanceData): string | null {
    const parsed = this.parseShortLink(shortLink);
    const { urlMap, headingData, methodAttrData } = data;

    if (parsed.type === 'heading') {
      return this.resolveHeadingLink(parsed, urlMap, headingData);
    }
    return this.resolveMethodLink(parsed, urlMap, methodAttrData);
  }

  /**
   * 解析标题类短链接
   */
  private resolveHeadingLink(
    parsed: ParsedShortLink,
    urlMap: UrlMap,
    headingData: HeadingData
  ): string | null {
    const { anchor, specifiedType } = parsed;

    // 如果指定了类型，优先在该类型中查找
    if (specifiedType && headingData[specifiedType].includes(anchor)) {
      return `${urlMap[specifiedType]}#${anchor}`;
    }

    // 按优先级遍历所有类型查找
    for (const type of PARENT_TYPES) {
      if (headingData[type].includes(anchor)) {
        return `${urlMap[type]}#${anchor}`;
      }
    }

    return null;
  }

  /**
   * 解析方法类短链接
   */
  private resolveMethodLink(
    parsed: ParsedShortLink,
    urlMap: UrlMap,
    methodAttrData: MethodAttrData
  ): string | null {
    const { anchor } = parsed;

    // 按优先级遍历所有类型查找
    for (const type of PARENT_TYPES) {
      if (methodAttrData[type].includes(anchor)) {
        return `${urlMap[type]}#${anchor}`;
      }
    }

    return null;
  }

  /**
   * 处理指定 instance 下所有文件的短链接
   */
  async processInstance(instanceId: string): Promise<{ processed: number; replaced: number }> {
    const data = this.instanceDataMap.get(instanceId);
    if (!data) {
      return { processed: 0, replaced: 0 };
    }

    const instanceDir = path.join(this.docsRoot, data.instance.path);
    const files = this.collectMdxFiles(instanceDir);
    let processed = 0;
    let replaced = 0;

    for (const filePath of files) {
      const originalContent = fs.readFileSync(filePath, 'utf-8');
      const newContent = this.replaceShortLinksInFile(filePath, instanceId);

      if (originalContent !== newContent) {
        fs.writeFileSync(filePath, newContent, 'utf-8');
        replaced++;
      }
      processed++;
    }

    return { processed, replaced };
  }

  /**
   * 收集目录下所有 .md 和 .mdx 文件
   */
  private collectMdxFiles(dir: string): string[] {
    const files: string[] = [];

    const walk = (currentDir: string) => {
      if (!fs.existsSync(currentDir)) return;
      const entries = fs.readdirSync(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        if (entry.isDirectory()) {
          walk(fullPath);
        } else if (entry.isFile() && /\.mdx?$/.test(entry.name)) {
          files.push(fullPath);
        }
      }
    };

    walk(dir);
    return files;
  }

  /**
   * 处理所有配置了 clientApiPath 的 instances
   */
  async processAll(): Promise<Map<string, { processed: number; replaced: number }>> {
    const results = new Map<string, { processed: number; replaced: number }>();

    for (const instanceId of Array.from(this.instanceDataMap.keys())) {
      const result = await this.processInstance(instanceId);
      results.set(instanceId, result);
    }

    return results;
  }

  /**
   * 获取已加载的 instance IDs
   */
  getInstanceIds(): string[] {
    return Array.from(this.instanceDataMap.keys());
  }
}

