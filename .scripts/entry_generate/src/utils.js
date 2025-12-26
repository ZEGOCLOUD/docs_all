const fs = require('fs');
const path = require('path');
const { 
  PRODUCT_CONFIG, 
  STEP_ICONS, 
  DEFAULT_STEP_ORDER, 
  SIDEBAR_TO_STEP_MAPPING,
  TAG_COLOR_MAPPING 
} = require('./config');

/**
 * 获取项目根目录
 */
function getProjectRoot() {
  // 从当前脚本位置向上查找项目根目录
  let currentDir = __dirname;
  while (currentDir !== path.dirname(currentDir)) {
    const configPath = path.join(currentDir, 'docuo.config.json');
    if (fs.existsSync(configPath)) {
      return currentDir;
    }
    currentDir = path.dirname(currentDir);
  }
  throw new Error('Project root not found (docuo.config.json not found)');
}

/**
 * 读取docuo.config.json获取实例配置
 */
function loadDocuoConfig() {
  const projectRoot = getProjectRoot();
  const configPath = path.join(projectRoot, 'docuo.config.json');
  console.log('配置文件路径', configPath);
  if (!fs.existsSync(configPath)) {
    throw new Error('docuo.config.json not found');
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

/**
 * 读取sidebars.json文件
 */
function loadSidebars(productType, platform, locale = 'zh') {
  const projectRoot = getProjectRoot();
  const sidebarPath = path.join(
    projectRoot,
    'core_products',
    productType,
    locale,
    platform,
    'sidebars.json'
  );

  if (!fs.existsSync(sidebarPath)) {
    throw new Error(`Sidebars file not found: ${sidebarPath}`);
  }

  return JSON.parse(fs.readFileSync(sidebarPath, 'utf8'));
}

/**
 * 从docuo.config.json中获取指定产品平台的实例配置
 */
function getInstanceConfig(productType, platform, locale = 'zh') {
  const docuoConfig = loadDocuoConfig();
  
  // 构建实例ID模式
  const instanceIdPattern = new RegExp(`${productType.replace(/-/g, '_')}_${platform.replace(/-/g, '_')}_${locale}`);
  
  const instance = docuoConfig.instances.find(inst => 
    instanceIdPattern.test(inst.id) || 
    inst.path.includes(`${productType}/${locale}/${platform}`)
  );
  
  if (!instance) {
    throw new Error(`Instance config not found for ${productType}/${platform}/${locale}`);
  }
  
  return instance;
}

/**
 * 生成FeatureList的features数组
 */
function generateFeatures(items, routeBasePath, tagType = null) {
  if (!items || !Array.isArray(items)) return [];
  
  return items
    .filter(item => item.type === 'doc' && item.visible !== false)
    .map(item => {
      const feature = {
        title: item.label,
        link: `/${routeBasePath}/${item.id}`
      };
      
      // 处理特殊标签（Hot, New等）
      if (item.tag && item.tag.label && TAG_COLOR_MAPPING[item.tag.label]) {
        feature.tag = item.tag.label;
        feature.tag_color = TAG_COLOR_MAPPING[item.tag.label];
      }
      
      return feature;
    });
}

/**
 * 递归提取所有doc类型的items
 */
function extractAllDocItems(items) {
  if (!items || !Array.isArray(items)) return [];

  const docItems = [];

  items.forEach(item => {
    if (item.type === 'doc' && item.visible !== false) {
      docItems.push(item);
    } else if (item.type === 'category' && item.items) {
      // 递归处理嵌套的category
      docItems.push(...extractAllDocItems(item.items));
    }
  });

  return docItems;
}

/**
 * 检查是否为小程序快速开始的特殊情况
 */
function isMiniProgramQuickStart(items, routeBasePath) {
  return routeBasePath.includes('miniprogram') &&
         items.some(item =>
           item.type === 'category' &&
           (item.label === '微信小程序' || item.label === '支付宝小程序')
         );
}

/**
 * 处理小程序快速开始的特殊分组
 */
function groupMiniProgramQuickStart(items, routeBasePath) {
  const groups = {};

  items.forEach(item => {
    if (item.type === 'category' && (item.label === '微信小程序' || item.label === '支付宝小程序')) {
      const platformName = item.label;
      if (!groups[platformName]) {
        groups[platformName] = [];
      }

      // 只取第一个文档作为入口
      if (item.items && item.items.length > 0) {
        const firstDoc = item.items.find(subItem => subItem.type === 'doc');
        if (firstDoc) {
          groups[platformName].push({
            title: `${platformName}快速开始`,
            link: `/${routeBasePath}/${firstDoc.id}`
          });
        }
      }
    }
  });

  return groups;
}

/**
 * 按tag分组features
 */
function groupFeaturesByTag(items, routeBasePath) {
  if (!items || !Array.isArray(items)) return [];

  // 检查是否为小程序快速开始的特殊情况
  if (isMiniProgramQuickStart(items, routeBasePath)) {
    return groupMiniProgramQuickStart(items, routeBasePath);
  }

  const groups = {};

  // 递归提取所有doc items
  const allDocItems = extractAllDocItems(items);

  allDocItems.forEach(item => {
    const tagLabel = item.tag?.label || '其他';
    if (!groups[tagLabel]) {
      groups[tagLabel] = [];
    }

    const feature = {
      title: item.label,
      link: `/${routeBasePath}/${item.id}`
    };

    // 处理特殊标签
    if (item.tag && item.tag.label && TAG_COLOR_MAPPING[item.tag.label]) {
      feature.tag = item.tag.label;
      feature.tag_color = TAG_COLOR_MAPPING[item.tag.label];
    }

    groups[tagLabel].push(feature);
  });

  return groups;
}

/**
 * 检查是否应该包含某个Step
 */
function shouldIncludeStep(stepName, productConfig) {
  // 实时语音产品跳过视频能力
  if (stepName === "视频能力" && !productConfig.hasVideoCapability) {
    return false;
  }
  return true;
}

/**
 * 获取产品的Step顺序
 */
function getStepOrder(productConfig) {
  return productConfig.stepOrder || DEFAULT_STEP_ORDER;
}

/**
 * 确保目录存在
 */
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

module.exports = {
  getProjectRoot,
  loadDocuoConfig,
  loadSidebars,
  getInstanceConfig,
  generateFeatures,
  extractAllDocItems,
  groupFeaturesByTag,
  shouldIncludeStep,
  getStepOrder,
  ensureDirectoryExists
};
