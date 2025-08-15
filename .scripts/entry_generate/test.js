#!/usr/bin/env node

const { generateEntryContent } = require('./generator');
const { PRODUCT_CONFIG } = require('./config');

/**
 * 测试生成器功能
 */
function runTests() {
  console.log('🧪 Running Entry Generator Tests...\n');
  
  const testCases = [
    { productType: 'real-time-voice-video', platform: 'ios-oc', locale: 'zh' },
    { productType: 'real-time-voice', platform: 'ios-oc', locale: 'zh' },
    { productType: 'low-latency-live-streaming', platform: 'ios-oc', locale: 'zh' }
  ];
  
  let passCount = 0;
  let failCount = 0;
  
  testCases.forEach(({ productType, platform, locale }, index) => {
    console.log(`Test ${index + 1}: ${productType}/${platform}/${locale}`);
    
    try {
      const content = generateEntryContent(productType, platform, locale);
      
      // 基本验证
      const checks = [
        { name: 'Has frontmatter', test: content.includes('---\nshow_toc: false\n---') },
        { name: 'Has import statement', test: content.includes('import FeatureList') },
        { name: 'Has product title', test: content.includes(PRODUCT_CONFIG[productType].name) },
        { name: 'Has product description', test: content.includes(PRODUCT_CONFIG[productType].description) },
        { name: 'Has buttons', test: content.includes('<Button') },
        { name: 'Has Steps component', test: content.includes('<Steps') && content.includes('</Steps>') },
        { name: 'Has Step components', test: content.includes('<Step') && content.includes('</Step>') },
        { name: 'Has FeatureList components', test: content.includes('<FeatureList') }
      ];
      
      // 产品特定检查
      if (productType === 'real-time-voice') {
        checks.push({ name: 'No video capability (real-time-voice)', test: !content.includes('视频能力') });
      } else {
        checks.push({ name: 'Has video capability', test: content.includes('视频能力') });
      }
      
      const failedChecks = checks.filter(check => !check.test);
      
      if (failedChecks.length === 0) {
        console.log('  ✅ PASS - All checks passed');
        passCount++;
      } else {
        console.log('  ❌ FAIL - Failed checks:');
        failedChecks.forEach(check => {
          console.log(`    - ${check.name}`);
        });
        failCount++;
      }
      
      // 输出内容长度信息
      console.log(`  📏 Content length: ${content.length} characters`);
      console.log(`  📄 Lines: ${content.split('\n').length}`);
      
    } catch (error) {
      console.log(`  ❌ ERROR: ${error.message}`);
      failCount++;
    }
    
    console.log('');
  });
  
  console.log('📊 Test Summary:');
  console.log(`✅ Passed: ${passCount}`);
  console.log(`❌ Failed: ${failCount}`);
  console.log(`📁 Total: ${testCases.length}`);
  
  if (failCount === 0) {
    console.log('\n🎉 All tests passed!');
  } else {
    console.log('\n⚠️  Some tests failed. Please check the implementation.');
    process.exit(1);
  }
}

/**
 * 生成示例内容并输出到控制台
 */
function generateSample() {
  console.log('📝 Generating sample entry content...\n');
  
  try {
    const content = generateEntryContent('real-time-voice-video', 'ios-oc', 'zh');
    console.log('--- Sample Content Start ---');
    console.log(content);
    console.log('--- Sample Content End ---');
  } catch (error) {
    console.error('❌ Failed to generate sample:', error.message);
    process.exit(1);
  }
}

/**
 * 显示测试帮助
 */
function showTestHelp() {
  console.log(`
🧪 Entry Generator Test Suite

用法:
  node test.js [command]

命令:
  test      运行所有测试用例
  sample    生成示例内容并输出
  help      显示帮助信息

示例:
  node test.js test      # 运行测试
  node test.js sample    # 查看生成的示例内容
`);
}

// 主程序
function main() {
  const command = process.argv[2];
  
  switch (command) {
    case 'test':
    case undefined:
      runTests();
      break;
    case 'sample':
      generateSample();
      break;
    case 'help':
    case '--help':
    case '-h':
      showTestHelp();
      break;
    default:
      console.error(`❌ Unknown command: ${command}`);
      showTestHelp();
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  runTests,
  generateSample
};
