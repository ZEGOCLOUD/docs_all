// generate_static_faq.mjs
//
// 为「curl 取数据」场景预生成静态 JSON：每个 instance.id 一个文件，
// 内容是该实例命中的 FAQ [{href, title}]。
//
//   curl https://doc-zh.zego.im/faq-instance/zh/real_time_video_ios_oc_zh.json
//   → [{"href":"/faq/express-reconnect","title":"..."}, ...]
//
// 为什么需要它：docuo 是 SSG，?instance= 过滤只在浏览器端跑，curl 拿到的是全量 HTML。
// 所以把结果预生成成静态文件，放进 docuo 的 static/ 目录（会被原样 serve 到根路径）。
//
// 按 lang 分目录（faq-instance/zh、faq-instance/en）：static/ 是两套站点共享的同一目录，
// 中英文 id 将来可能撞车，分目录隔离。zh/en 虽是不同域名，但共用 static/，故仍需 lang 子目录。
//
// 维护：改了 docuo.config / overview 后重跑本脚本（run.sh 已自动调用），提交即可；
//       docuo 生产构建会打包已提交的 static/ 文件。
// 注意：dev 模式下 docuo 在启动时一次性拷贝 static/，新增/改动文件需重启 docuo dev 才能在本地 curl 到。

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const OUT_DIR = path.join(ROOT, 'static', 'faq-instance');

// 复用各语言已生成好的维度 + 匹配逻辑（与浏览器同一份，保证零漂移）
async function loadLang(lang) {
  const dir = path.join(ROOT, 'general', lang, 'faq');
  const dims = await import(pathToFileURL(path.join(dir, 'faqDimensions.js')).href);
  const { matchFaq } = await import(pathToFileURL(path.join(dir, 'faqMatch.js')).href);
  return { dir, ...dims, matchFaq };
}

// 静态解析 overview.mdx 的所有 <FilteredLink>
function parseLinks(mdx) {
  const A = (a, k) => (a.match(new RegExp(k + '="([^"]*)"')) || [, ''])[1];
  const clean = (s) => s.replace(/\s+/g, ' ').trim();
  return [...mdx.matchAll(/<FilteredLink\b([^>]*)>([\s\S]*?)<\/FilteredLink>/g)].map((x) => ({
    product: A(x[1], 'product'),
    platform: A(x[1], 'platform'),
    href: A(x[1], 'href'),
    title: clean(x[2]),
  }));
}

// 重建输出目录（幂等：删旧文件，避免 config 删掉的 id 残留）
fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

let fileCount = 0;

for (const lang of ['zh', 'en']) {
  const langDir = path.join(OUT_DIR, lang);
  fs.mkdirSync(langDir, { recursive: true });

  const { dir, instanceMap, allProducts, allPlatforms, matchFaq } = await loadLang(lang);
  const links = parseLinks(fs.readFileSync(path.join(dir, 'overview.mdx'), 'utf8'));

  const index = []; // 本语言的 [{id, product, platform}]
  for (const [id, sel] of Object.entries(instanceMap)) {
    const hit = links
      .filter((l) => matchFaq(l, sel, allProducts, allPlatforms))
      .map(({ href, title }) => ({ href, title }));
    fs.writeFileSync(path.join(langDir, `${id}.json`), JSON.stringify(hit, null, 2), 'utf8');
    index.push({ id, product: sel.product, platform: sel.platform });
    fileCount++;
  }
  // 每语言一个索引，方便消费端发现该语言合法 id
  fs.writeFileSync(path.join(langDir, 'index.json'), JSON.stringify(index, null, 2), 'utf8');
  console.log(`✓ ${lang}: ${Object.keys(instanceMap).length} instances + index → static/faq-instance/${lang}/`);
}

console.log(`\nDone. ${fileCount} instance JSON + 2 index written to static/faq-instance/{zh,en}/`);
console.log(`curl 示例: curl https://doc-zh.zego.im/faq-instance/zh/real_time_video_ios_oc_zh.json`);
