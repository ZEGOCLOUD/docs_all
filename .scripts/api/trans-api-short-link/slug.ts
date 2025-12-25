/**
 * 锚点生成函数
 * 与 ParamField 组件中的 generateSlug 保持完全一致
 */

import { ParamFieldAttrs } from './types';

/**
 * 生成锚点 slug
 * 与 ParamField.tsx 中的 generateSlug 完全一致
 */
export function generateSlug(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .trim();
}

/**
 * 从 ParamField 属性中提取所有可能的锚点
 * 规则与 ParamField.tsx 中的锚点生成逻辑完全一致
 */
export function extractAnchorsFromParamField(attrs: ParamFieldAttrs): string[] {
  const { name, parent_name, parent_type, anchor_suffix = '' } = attrs;
  const anchors: string[] = [];

  // 锚点基础名称：如果有 anchor_suffix，则拼接到 name 后面
  const anchorBaseName = anchor_suffix ? `${name}${anchor_suffix}` : name;

  // 主锚点
  const primaryAnchorId = generateSlug(anchorBaseName);
  anchors.push(primaryAnchorId);

  // 父类上下文锚点（非 enum 时生成）
  if (parent_type && parent_type !== 'enum' && parent_name) {
    anchors.push(generateSlug(`${anchorBaseName}-${parent_name}`));
    anchors.push(generateSlug(`${anchorBaseName}-${parent_name}-${parent_type}`));
  }

  // OC 冒号方法名首段锚点
  // 如 "createEngineWithProfile:eventHandler:" → 额外生成 "createenginewithprofile"
  // 以及带 parent_name 和 parent_type 的变体
  if (name.includes(':')) {
    const firstSegment = name.split(':')[0];
    if (firstSegment && firstSegment !== name) {
      const colonAnchorId = generateSlug(firstSegment);
      if (colonAnchorId !== primaryAnchorId && !anchors.includes(colonAnchorId)) {
        anchors.push(colonAnchorId);
      }
      // Also add firstSegment-parent_name and firstSegment-parent_name-parent_type
      if (parent_type && parent_type !== 'enum' && parent_name) {
        const colonWithParentAnchorId = generateSlug(`${firstSegment}-${parent_name}`);
        if (!anchors.includes(colonWithParentAnchorId)) {
          anchors.push(colonWithParentAnchorId);
        }
        const colonWithParentTypeAnchorId = generateSlug(`${firstSegment}-${parent_name}-${parent_type}`);
        if (!anchors.includes(colonWithParentTypeAnchorId)) {
          anchors.push(colonWithParentTypeAnchorId);
        }
      }
    }
  }

  return anchors;
}

