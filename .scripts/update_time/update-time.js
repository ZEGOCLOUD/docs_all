#! /usr/bin/env bun
/**
 * 获取当前时间，并更新到 mdx 文件的 frontmatter 中
 */

const fs = require('fs');

/**
 * 更新 mdx 文件 frontmatter 中的日期
 * @param {string[]} filePaths pr 变更的 mdx 文件路径列表
 */
function updateTime(filePaths) {
  if(!filePaths || filePaths.length === 0) {
    console.warn('没有变更的文件');
    return;
  }
  const now = new Date();
  const updatedDate = now.getFullYear() + '-' + (now.getMonth() + 1).toString().padStart(2, '0') + '-' + now.getDate().toString().padStart(2, '0');

  for (const filePath of filePaths) {
    if(!filePath.endsWith('.mdx')) {
      continue;
    }

    let content = '';
    try{
      content = fs.readFileSync(filePath, 'utf-8');
    }catch(error){
      console.error(`读取 ${filePath} 失败: ${error.message}`);
      continue;
    }

    // 只匹配文件开头的 frontmatter（必须以 --- 开头）
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

    let newContent = '';

    if(!frontmatterMatch) {
      console.warn(`${filePath} 没有有效的 frontmatter（必须以 --- 开头）`);
      // 没有 frontmatter，新增一个
      newContent = `---\ndate: "${updatedDate}"\n---\n${content}`;
    } else {
      const frontmatterStr = frontmatterMatch[1];
      const otherContent = content.slice(frontmatterMatch[0].length);

      // 用正则匹配并替换 date 字段，支持 date: value / date: 'value' / date: "value"
      if (/^date:/m.test(frontmatterStr)) {
        const updated = frontmatterStr.replace(/^date:.*$/m, `date: "${updatedDate}"`);
        newContent = `---\n${updated}\n---${otherContent}`;
      } else {
        // frontmatter 中没有 date 字段，在末尾添加
        newContent = `---\n${frontmatterStr}\ndate: "${updatedDate}"\n---${otherContent}`;
      }
    }

    try {
      fs.writeFileSync(filePath, newContent);
      console.log(`${filePath} 的更新日期为 ${updatedDate}`);
    } catch(error) {
      console.error(`写入 ${filePath} 失败: ${error.message}`);
    }
  }
}

// updateTime(['test/test.mdx','test/work.mdx','test/index.md',"core_products/zim/zh/docs_zim_android_zh/Send and receive messages.mdx"]);
// 处理传入的文件路径中包含空格的情况
console.log(process.argv.slice(2));
updateTime(process.argv.slice(2)[0].split('\n').filter(Boolean));