/**
 * trans-api-short-link 类型定义
 *
 * 此文件定义了 trans-api-short-link 模块使用的所有 TypeScript 类型
 * 被以下文件导入：
 * - index.ts: 主控制器
 * - parser.ts: MDX 文件解析器
 * - slug.ts: 锚点生成函数
 */

/**
 * 父类型：class, interface, enum, protocol, struct
 */
export type ParentType = 'class' | 'interface' | 'enum' | 'protocol' | 'struct';

/**
 * 所有支持的父类型列表（按优先级排序）
 */
export const PARENT_TYPES: ParentType[] = ['class', 'interface', 'enum', 'protocol', 'struct'];

/**
 * 标题数据结构
 * 存储每种类型下的所有标题锚点
 */
export interface HeadingData {
  class: string[];
  interface: string[];
  enum: string[];
  protocol: string[];
  struct: string[];
}

/**
 * 方法/属性数据结构
 * 存储每种类型下的所有方法/属性锚点
 */
export interface MethodAttrData {
  class: string[];
  interface: string[];
  enum: string[];
  protocol: string[];
  struct: string[];
}

/**
 * URL 映射结构
 * 存储每种类型对应的基础 URL
 */
export interface UrlMap {
  class: string;
  interface: string;
  enum: string;
  protocol: string;
  struct: string;
}

/**
 * 解析后的短链接结构
 */
export interface ParsedShortLink {
  type: 'heading' | 'method';
  raw: string;
  anchor: string;
  specifiedType?: ParentType;
}

/**
 * 配置了 clientApiPath 的 instance
 */
export interface InstanceWithClientApi {
  id: string;
  path: string;
  routeBasePath: string;
  clientApiPath: string;
}

/**
 * 处理后的 instance 数据
 */
export interface ProcessedInstanceData {
  instance: InstanceWithClientApi;
  urlMap: UrlMap;
  headingData: HeadingData;
  methodAttrData: MethodAttrData;
}

/**
 * ParamField 组件的属性
 */
export interface ParamFieldAttrs {
  name: string;
  parent_name?: string;
  parent_type?: ParentType;
  anchor_suffix?: string;
}

