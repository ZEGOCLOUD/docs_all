// generate_faq_dimensions.mjs
//
// 从 docuo.config.{zh,en}.json 的 themeConfig.instanceGroups 派生 FAQ 维度数据。
// 这是 FAQ 过滤系统的「唯一真相」入口：config 是唯一维护点，本脚本可随时重跑（幂等）。
//
// 产物：general/{zh,en}/faq/faqDimensions.js，导出：
//   - allProducts / allPlatforms : 「全部」通配哨兵值（zh: 全部/全部平台, en: All/All Platforms）
//   - productData  : { <分类>: [<产品名>, ...] }，仅取 category[0] === '产品'/'Products' 的 group，按 category[1] 分组
//   - platformData : [<归一化平台>, ...]，从产品实例的 platform 归一化去重
//   - instanceMap  : { <instance.id>: { product, platform } }，零手写
//
// 用法：node .scripts/faq/generate_faq_dimensions.mjs
// 维护：改了 docuo.config.*.json 后重跑本脚本即可，faqDimensions.js 全量重建，无需手改映射。

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');

const LANGS = [
  { lang: 'zh', cat0: '产品', config: 'docuo.config.zh.json' },
  { lang: 'en', cat0: 'Products', config: 'docuo.config.en.json' },
];

// 下拉里展示的平台顺序（归一化后的值）。未列出的平台追加到末尾。
const PLATFORM_ORDER = [
  'iOS', 'Android', 'macOS', 'Windows', 'Linux', 'Web',
  'Flutter', 'Electron', 'ReactNative', 'uni-app', 'Unity3D',
  'HarmonyOS', '小程序', 'Mini Program',
];

// 归一化：把 config 里的 '平台: 语言' 形式压成下拉/标注共用的短名。
// Server/文档/服务端 API/All/Docs/版本类/引擎类 等「非客户端平台」→ ''（在 instanceMap 层转成 allPlatforms 哨兵）。
function normalizePlatform(raw) {
  const s = String(raw || '').trim();
  if (!s) return '';
  const lower = s.toLowerCase();
  if (lower.startsWith('ios')) return 'iOS';
  if (lower.startsWith('android')) return 'Android';
  if (lower.startsWith('macos')) return 'macOS';
  if (lower.startsWith('windows')) return 'Windows';
  if (lower.startsWith('linux')) return 'Linux';
  if (lower.startsWith('web')) return 'Web';
  if (lower.startsWith('flutter')) return 'Flutter';
  if (lower.startsWith('electron')) return 'Electron';
  if (lower.startsWith('react native')) return 'ReactNative';
  if (lower.startsWith('uni-app')) return 'uni-app';
  if (lower.startsWith('unity')) return 'Unity3D';
  if (lower.startsWith('harmonyos')) return 'HarmonyOS';
  if (s.startsWith('小程序')) return '小程序';
  if (lower.startsWith('mini program')) return 'Mini Program';
  return '';
}

const sortByPreferred = (arr) =>
  arr.sort((a, b) => {
    const ia = PLATFORM_ORDER.indexOf(a);
    const ib = PLATFORM_ORDER.indexOf(b);
    if (ia !== -1 && ib !== -1) return ia - ib;
    if (ia !== -1) return -1;
    if (ib !== -1) return 1;
    return a.localeCompare(b);
  });

function build(langCfg) {
  const { lang, cat0, config } = langCfg;
  const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, config), 'utf8'));
  const groups = cfg?.themeConfig?.instanceGroups || [];

  const allProducts = lang === 'en' ? 'All' : '全部';
  const allPlatforms = lang === 'en' ? 'All Platforms' : '全部平台';

  // productData：仅「产品」类 group，按 category[1] 分组（保留 config 出现顺序）
  const productData = {};
  const platformSet = new Set();
  const instanceMap = {};

  for (const g of groups) {
    const category = g.category || [];
    const isProduct = category[0] === cat0;
    const sub = category[1] || (lang === 'en' ? 'Other' : '其他');
    if (isProduct) {
      (productData[sub] = productData[sub] || []).push(g.name);
    }
    for (const inst of g.instances || []) {
      const norm = normalizePlatform(inst.platform);
      if (isProduct && norm) platformSet.add(norm);
      // instanceMap：每个实例都记录它所属产品（group.name）+ 归一化平台。
      // 非客户端平台（Server/文档…）→ 用 allPlatforms 哨兵，表示该实例不按平台过滤。
      instanceMap[inst.id] = {
        product: g.name,
        platform: norm || allPlatforms,
      };
    }
  }

  const platformData = sortByPreferred([...platformSet]);

  return { allProducts, allPlatforms, productData, platformData, instanceMap };
}

// 以注释头 + ESM export 形式写出，便于人工核对。
function serialize(lang, d) {
  const header = `// ⚠️ 本文件由 .scripts/faq/generate_faq_dimensions.mjs 自动生成，请勿手改。
//   数据源：docuo.config.${lang}.json → themeConfig.instanceGroups
//   维护：改 config 后重跑生成脚本（node .scripts/faq/generate_faq_dimensions.mjs）。
//   实例数：${Object.keys(d.instanceMap).length}，产品分类：${Object.keys(d.productData).length}，平台：${d.platformData.length}。`;
  return `${header}
export const allProducts = ${JSON.stringify(d.allProducts)};
export const allPlatforms = ${JSON.stringify(d.allPlatforms)};

export const productData = ${JSON.stringify(d.productData, null, 2)};

export const platformData = ${JSON.stringify(d.platformData, null, 2)};

export const instanceMap = ${JSON.stringify(d.instanceMap, null, 2)};
`;
}

let touched = 0;
for (const langCfg of LANGS) {
  const d = build(langCfg);
  const outPath = path.join(ROOT, 'general', langCfg.lang, 'faq', 'faqDimensions.js');
  fs.writeFileSync(outPath, serialize(langCfg.lang, d), 'utf8');
  touched++;
  console.log(`✓ ${langCfg.lang}: ${Object.keys(d.instanceMap).length} instances → ${outPath}`);
  console.log(`    product groups: ${Object.keys(d.productData).map(k => `${k}(${d.productData[k].length})`).join(', ')}`);
  console.log(`    platforms: ${d.platformData.join(', ')}`);
}
console.log(`\nDone. ${touched} file(s) regenerated from config.`);
