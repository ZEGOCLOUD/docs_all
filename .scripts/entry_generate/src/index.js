#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { generateEntryContent } = require('./generator');
const { getProjectRoot, loadDocuoConfig, ensureDirectoryExists } = require('./utils');
const { PRODUCT_CONFIG } = require('./config');

/**
 * 获取所有需要生成entry的产品和平台组合
 */
function getAllProductPlatforms() {
  const docuoConfig = loadDocuoConfig();
  const combinations = [];
  
  // 从docuo.config.json的instances中提取产品和平台信息
  docuoConfig.instances.forEach(instance => {
    // 跳过API实例、linux-java实例
    if (instance.id.includes('api') || instance.id.includes('server') || instance.id.includes('linux-java')) {
      return;
    }
    
    // 解析路径获取产品类型和平台
    const pathParts = instance.path.split('/');
    if (pathParts.length >= 4 && pathParts[0] === 'core_products') {
      const productType = pathParts[1];
      const locale = pathParts[2];
      const platform = pathParts[3];
      const routeBasePath = instance.routeBasePath;
      
      // 只处理配置中定义的产品
      if (PRODUCT_CONFIG[productType]) {
        combinations.push({
          productType,
          platform,
          locale,
          path: instance.path,
          routeBasePath
        });
      }
    }
  });
  
  return combinations;
}

/**
 * 生成单个entry文档
 */
function generateSingleEntry(productType, platform, locale = 'zh', routeBasePath) {
  try {
    console.log(`正在生成 ${productType}/${platform}/${locale} 的entry文档...`);

    const content = generateEntryContent(productType, platform, locale, routeBasePath);
    const projectRoot = getProjectRoot();
    const outputPath = path.join(
      projectRoot,
      'core_products',
      productType,
      locale,
      platform,
      'introduction',
      'entry.mdx'
    );

    // 确保目录存在
    ensureDirectoryExists(path.dirname(outputPath));

    // 写入文件
    fs.writeFileSync(outputPath, content, 'utf8');
    console.log(`✅ 已生成: ${outputPath}`);

    return true;
  } catch (error) {
    console.error(`❌ 生成失败 ${productType}/${platform}/${locale}:`, error.message);
    return false;
  }
}

/**
 * 生成所有entry文档
 */
function generateAllEntries() {
  console.log('🚀 开始生成entry文档...\n');

  const combinations = getAllProductPlatforms();
  let successCount = 0;
  let failCount = 0;

  combinations.forEach(({ productType, platform, locale, routeBasePath }) => {
    const success = generateSingleEntry(productType, platform, locale, routeBasePath);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
  });

  console.log(`\n📊 生成汇总:`);
  console.log(`✅ 成功: ${successCount}`);
  console.log(`❌ 失败: ${failCount}`);
  console.log(`📁  总计: ${combinations.length}`);

  if (failCount === 0) {
    console.log('\n🎉 所有entry文档生成成功!');
  } else {
    console.log('\n⚠️  部分文件生成失败，请检查上述错误信息。');
    process.exit(1);
  }
}

/**
 * 生成指定产品的entry文档
 */
function generateProductEntries(productType) {
  if (!PRODUCT_CONFIG[productType]) {
    console.error(`❌ 未知的产品类型: ${productType}`);
    console.log('可用产品:', Object.keys(PRODUCT_CONFIG).join(', '));
    process.exit(1);
  }

  console.log(`🚀 正在生成 ${productType} 的entry文档...\n`);

  const combinations = getAllProductPlatforms().filter(c => c.productType === productType);
  let successCount = 0;
  let failCount = 0;

  combinations.forEach(({ productType, platform, locale,routeBasePath }) => {
    const success = generateSingleEntry(productType, platform, locale, routeBasePath);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
  });

  console.log(`\n📊 ${productType} 生成汇总:`);
  console.log(`✅ 成功: ${successCount}`);
  console.log(`❌ 失败: ${failCount}`);
  console.log(`📁 总计: ${combinations.length}`);
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
📚 Entry Generator - 自动生成产品entry文档

用法:
  node index.js [command] [options]

命令:
  generate              生成所有产品的entry文档
  generate <product>    生成指定产品的entry文档
  list                  列出所有可用的产品
  help                  显示帮助信息

产品类型:
  real-time-voice-video      实时音视频
  real-time-voice           实时语音
  low-latency-live-streaming 超低延迟直播

示例:
  node index.js generate                           # 生成所有entry
  node index.js generate real-time-voice-video    # 只生成实时音视频的entry
  node index.js list                              # 列出所有产品
`);
}

/**
 * 列出所有产品
 */
function listProducts() {
  console.log('📋 可用产品:');
  Object.entries(PRODUCT_CONFIG).forEach(([key, config]) => {
    console.log(`  ${key.padEnd(30)} ${config.name}`);
  });
}

// 主程序
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'generate':
      if (args[1]) {
        generateProductEntries(args[1]);
      } else {
        generateAllEntries();
      }
      break;
    case 'list':
      listProducts();
      break;
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    default:
      if (!command) {
        generateAllEntries();
      } else {
        console.error(`❌ 未知命令: ${command}`);
        showHelp();
        process.exit(1);
      }
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = {
  generateSingleEntry,
  generateAllEntries,
  generateProductEntries
};
