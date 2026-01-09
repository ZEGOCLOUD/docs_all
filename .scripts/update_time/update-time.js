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
  console.log(`更新日期为 ${updatedDate}`);
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
    // 使用正则获取 frontmatter，以 --- 开头，第2个 --- 前的内容，用yaml解析
    const frontmatter = content.match(/---[\s\S]*?---/)?.[0];
    const otherContent = content.replace(frontmatter, '');

    let frontmatterObj = {};
    if(!frontmatter) {
      console.warn(`${filePath} 没有 frontmatter`);
      frontmatterObj = {date:updatedDate};
    }else{
      frontmatterObj = {
        ...yaml.load(frontmatter.replace(/---/g, '')),
        date:updatedDate,
      }
    }
    const newContent = `---\n${yaml.dump(frontmatterObj)}---${otherContent}`;
    fs.writeFileSync(filePath, newContent);
    console.log(`${filePath} 的更新日期为 ${updatedDate}`);
  }

}

// updateTime(['test/test.mdx','test/work.mdx','test/index.md',"core_products/zim/zh/docs_zim_android_zh/Send and receive messages.mdx"]);
// 处理传入的文件路径中包含空格的情况
console.log(process.argv.slice(2));
updateTime(process.argv.slice(2)[0].split('\n').filter(Boolean));