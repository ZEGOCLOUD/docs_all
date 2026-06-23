// generate_instance_groups.mjs
//
// 把 docuo.config.{zh,en}.json 的 themeConfig.instanceGroups 单独抽出来，
// 写成静态 JSON，供 curl / 外部脚本读取。
//
//   curl https://doc-zh.zego.im/sys-config/zh/instance-groups.json
//   → [ { "id": "real_time_video_zh", "name": "实时音视频", "category": [...], "instances": [...] }, ... ]
//
// 为什么需要它：与 generate_static_faq.mjs 同理——docuo 是 SSG，curl 拿到的是渲染后的
// HTML，取不到运行时配置。所以把 instanceGroups 预生成成静态文件，放进 docuo 的 static/
// 目录（会被原样 serve 到根路径）。
//
// 按 lang 分目录（sys-config/zh、sys-config/en）：static/ 是两套站点共享的同一目录，
// 中英文将来可能撞车，分目录隔离（与 faq-instance 的约定一致）。
// 目录名用 sys-config 而非 config：/config 是部署链路的保留路径，会被网关拦截返回 404。
//
// 维护：改了 docuo.config.*.json 后重跑本脚本（pre-commit hook 已自动触发）；
//       docuo 生产构建会打包已提交的 static/ 文件。
// 注意：dev 模式下 docuo 在启动时一次性拷贝 static/，改动需重启 docuo dev 才能在本地 curl 到。

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const OUT_DIR = path.join(ROOT, 'static', 'sys-config');

// 重建输出目录（幂等：删旧文件，避免 config 删掉的 group 残留）
fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

let fileCount = 0;

for (const lang of ['zh', 'en']) {
  const configPath = path.join(ROOT, `docuo.config.${lang}.json`);
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const instanceGroups = config.themeConfig?.instanceGroups ?? [];

  const langDir = path.join(OUT_DIR, lang);
  fs.mkdirSync(langDir, { recursive: true });

  fs.writeFileSync(
    path.join(langDir, 'instance-groups.json'),
    JSON.stringify(instanceGroups, null, 2),
    'utf8',
  );
  fileCount++;
  console.log(`✓ ${lang}: ${instanceGroups.length} groups → static/sys-config/${lang}/instance-groups.json`);
}

console.log(`\nDone. ${fileCount} instance-groups.json written to static/sys-config/{zh,en}/`);
console.log(`curl 示例: curl https://doc-zh.zego.im/sys-config/zh/instance-groups.json`);
