/**
 * 获取当前时间，并更新到 mdx 文件的 frontmatter 中
 */

const fs = require('fs');
const yaml = require('js-yaml');

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
  // console.log(`更新日期为 ${updatedDate}`);

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
    // ^--- 确保从文件开头匹配，[\s\S]*? 匹配任意内容（非贪婪），\n--- 匹配结束标记
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

    let frontmatterObj = {};
    let otherContent = '';

    if(!frontmatterMatch) {
      console.warn(`${filePath} 没有有效的 frontmatter（必须以 --- 开头）`);
      frontmatterObj = {date: updatedDate};
      otherContent = '\n'+content;// 添加换行符避免 frontmatter 和内容之间没有换行符
    } else {
      const frontmatterContent = frontmatterMatch[1];
      // 获取 frontmatter 之后的内容
      otherContent = content.slice(frontmatterMatch[0].length);

      try {
        // 解析 YAML frontmatter
        const parsedFrontmatter = yaml.load(frontmatterContent);
        frontmatterObj = {
          ...(parsedFrontmatter || {}),
          date: updatedDate,
        };
      } catch(error) {
        console.error(`${filePath} 的 frontmatter YAML 解析失败: ${error.message}`);
        continue;
      }
    }

    // 生成新内容
    const newContent = `---\n${yaml.dump(frontmatterObj)}---${otherContent}`;

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