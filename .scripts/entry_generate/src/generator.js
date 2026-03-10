const { 
  PRODUCT_CONFIG, 
  STEP_ICONS, 
  SIDEBAR_TO_STEP_MAPPING 
} = require('./config');

const {
  loadSidebars,
  getInstanceConfig,
  generateFeatures,
  groupFeaturesByTag,
  shouldIncludeStep,
  getStepOrder
} = require('./utils');

/**
 * 生成entry文档的头部按钮
 */
function generateButtons(productConfig, sidebarData, routeBasePath) {
  const buttons = [];
  const hasClientApi = sidebarData.clientApi && Array.isArray(sidebarData.clientApi) && sidebarData.clientApi.length > 0;

  // 获取 mySidebar 中的所有 category 标签
  const categoryLabels = (sidebarData.mySidebar || [])
    .filter(item => item.type === 'category')
    .map(item => item.label);

  // 下载 SDK - 检查是否有"客户端 SDK" category
  if (categoryLabels.includes('客户端 SDK')) {
    buttons.push(`<Button primary-color="NavyBlue" target="_blank" href="./../client-sdk/download-sdk.mdx">下载 SDK</Button>`);
  }

  // 快速开始 - 检查是否有"快速开始" category
  if (categoryLabels.includes('快速开始')) {
    buttons.push(`<Button primary-color="NavyBlue" target="_blank" href="./../quick-start/${productConfig.quickStartPath}.mdx">快速开始</Button>`);
  }

  // 客户端 API - 检查是否有 clientApi 字段
  if (hasClientApi) {
    buttons.push(`<Button primary-color="NavyBlue" target="_blank" href="/${routeBasePath}${productConfig.apiPaths.client}">客户端 API</Button>`);
  }

  // 服务端 API - 始终显示（所有产品都有服务端 API）
  buttons.push(`<Button primary-color="NavyBlue" target="_blank" href="${productConfig.apiPaths.server}">服务端 API</Button>`);

  return buttons.join('\n');
}

/**
 * 生成entry文档的头部内容
 */
function generateHeader(productType, platform, locale = 'zh', routeBasePath) {
  const productConfig = PRODUCT_CONFIG[productType];
  if (!productConfig) {
    throw new Error(`Unknown product type: ${productType}`);
  }

  const instanceConfig = getInstanceConfig(productType, platform, locale);
  const sidebarData = loadSidebars(productType, platform, locale);

  const buttons = generateButtons(productConfig, sidebarData, routeBasePath);

  return `---
show_toc: false
---
import FeatureList from "${getFeatureListImportPath(productType)}";

# <img src="${productConfig.icon}" alt="${productConfig.name}" style={{display: 'inline', marginRight: '8px', verticalAlign: 'middle', width: '32px', height: '32px'}} /> ${productConfig.name}

${productConfig.description}

${buttons}

---

<Steps titleSite="h3">`;
}

/**
 * 获取FeatureList组件的导入路径
 */
function getFeatureListImportPath(productType) {
  // 实时语音和超低延迟直播都使用实时音视频的FeatureList组件
  if (productType === 'real-time-voice' || productType === 'low-latency-live-streaming') {
    return "../../../../real-time-voice-video/zh/snippets/FeatureList.jsx";
  }
  return "../../snippets/FeatureList.jsx";
}

/**
 * 生成单个Step
 */
function generateStep(stepName, sidebarData, instanceConfig, productConfig) {
  const icon = STEP_ICONS[stepName];
  const routeBasePath = instanceConfig.routeBasePath;
  
  let stepContent = `  <Step title="${stepName}" icon="${icon}">`;

  // 处理特殊的参考文档Step - 始终生成，不依赖sidebar
  if (stepName === "参考文档") {
    stepContent += generateReferenceStep(productConfig, instanceConfig, sidebarData);
  } else {
    // 查找对应的sidebar category
    const sidebarCategory = findSidebarCategory(stepName, sidebarData);
    if (!sidebarCategory) {
      return null;
    }

    // 按tag分组生成FeatureList
    const featureGroups = groupFeaturesByTag(sidebarCategory.items, routeBasePath);
    stepContent += generateFeatureListsForGroups(featureGroups, routeBasePath);
  }
  
  stepContent += `
  </Step>`;
  
  return stepContent;
}

/**
 * 查找对应的sidebar category
 */
function findSidebarCategory(stepName, sidebarData) {
  const sidebarLabel = Object.keys(SIDEBAR_TO_STEP_MAPPING).find(
    key => SIDEBAR_TO_STEP_MAPPING[key] === stepName
  );
  
  if (!sidebarLabel) return null;
  
  return sidebarData.mySidebar.find(category => 
    category.type === 'category' && category.label === sidebarLabel
  );
}

/**
 * 为分组的features生成FeatureList组件
 */
function generateFeatureListsForGroups(featureGroups, routeBasePath) {
  let content = '';

  // 检查是否为小程序快速开始的特殊情况
  if (routeBasePath && routeBasePath.includes('miniprogram') &&
      (featureGroups['微信小程序'] || featureGroups['支付宝小程序'])) {

    // 小程序快速开始的特殊处理
    const platformOrder = ['微信小程序', '支付宝小程序'];

    platformOrder.forEach((platformName, index) => {
      if (featureGroups[platformName] && featureGroups[platformName].length > 0) {
        if (index > 0) {
          content += '\n    <br/>';
        }

        content += `
    <FeatureList
      type="${platformName}"
      features={${JSON.stringify(featureGroups[platformName], null, 8).replace(/^/gm, '        ')}}
    />`;
      }
    });

    return content;
  }

  // 普通的tag分组处理
  const groupOrder = ['基础', '进阶', '特色', '其他'];

  groupOrder.forEach((groupName, index) => {
    if (featureGroups[groupName] && featureGroups[groupName].length > 0) {
      if (index > 0 && content.includes('<FeatureList')) {
        content += '\n    <br/>';
      }

      content += `
    <FeatureList`;

      if (groupName !== '其他') {
        content += `
      type="${groupName}"`;
      }

      content += `
      features={${JSON.stringify(featureGroups[groupName], null, 8).replace(/^/gm, '        ')}}
    />`;
    }
  });

  return content;
}

/**
 * 生成参考文档Step的特殊内容
 */
function generateReferenceStep(productConfig, instanceConfig, sidebarData) {
  const routeBasePath = instanceConfig.routeBasePath;
  const features = [];

  // 客户端 API - 检查是否有 clientApi 字段
  const hasClientApi = sidebarData.clientApi && Array.isArray(sidebarData.clientApi) && sidebarData.clientApi.length > 0;
  if (hasClientApi) {
    features.push({ title: "客户端 API", link: "/" + routeBasePath + "/" + productConfig.apiPaths.client });
  }

  // 服务端 API - 始终显示
  features.push({ title: "服务端 API", link: productConfig.apiPaths.server });

  // 常见错误码 - 检查 mySidebar 中是否有错误码文档
  const hasErrorCode = hasDocInSidebar(sidebarData, 'client-sdk/error-code') ||
                      hasDocInSidebar(sidebarData, 'error-code');
  if (hasErrorCode) {
    features.push({ title: "常见错误码", link: `/${routeBasePath}/client-sdk/error-code` });
  }

  // 常见问题 - 检查 mySidebar 中是否有 FAQ
  const hasFaq = hasDocInSidebar(sidebarData, 'faq');
  if (hasFaq) {
    features.push({ title: "常见问题", link: `/${routeBasePath}/faq` });
  }

  return `
    <FeatureList
      features={${JSON.stringify(features, null, 6).replace(/^/gm, '      ')}}
    />`;
}

/**
 * 检查sidebar中是否存在指定文档
 */
function hasDocInSidebar(sidebarData, docId) {
  if (!sidebarData.mySidebar) return false;

  function checkItems(items) {
    if (!items || !Array.isArray(items)) return false;

    for (const item of items) {
      if (item.type === 'doc' && item.id === docId) {
        return true;
      }
      if (item.type === 'category' && item.items) {
        if (checkItems(item.items)) {
          return true;
        }
      }
    }
    return false;
  }

  return checkItems(sidebarData.mySidebar);
}

/**
 * 生成完整的Steps内容
 */
function generateSteps(productType, platform, locale = 'zh') {
  const productConfig = PRODUCT_CONFIG[productType];
  const instanceConfig = getInstanceConfig(productType, platform, locale);
  const sidebarData = loadSidebars(productType, platform, locale);
  
  const stepOrder = getStepOrder(productConfig);
  const steps = stepOrder
    .filter(stepName => shouldIncludeStep(stepName, productConfig))
    .map(stepName => generateStep(stepName, sidebarData, instanceConfig, productConfig))
    .filter(step => step !== null);
  
  return steps.join('\n');
}

/**
 * 生成完整的entry文档内容
 */
function generateEntryContent(productType, platform, locale = 'zh', routeBasePath) {
  const header = generateHeader(productType, platform, locale, routeBasePath);
  const steps = generateSteps(productType, platform, locale);
  const footer = '</Steps>';
  
  return `${header}\n${steps}\n${footer}`;
}

module.exports = {
  generateHeader,
  generateStep,
  generateSteps,
  generateEntryContent
};
