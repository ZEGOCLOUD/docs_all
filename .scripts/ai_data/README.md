# 使用说明

## 设置环境变量
将.env.example文件复制为.env，并填写其中的环境变量。环境变量值找文档负责人获取

## AI数据更新脚本

运行 `./run_update_ai_data.sh` 以启动AI数据更新脚本
根据提示更新需要更新的实例即可

## 平时更新

1. 将更新发布至线上
2. 运行AI数据更新脚本，选择根据git变更更新(注意⚠️⚠️⚠️⚠️⚠️:数据更新脚本要跑两次，一次中文一次英文)
3. 选择最近一次提交或者之前提交（从哪个提交开始没更新AI数据就选哪个）
4. 将 data/ai_search_mapping.json 文件提交至仓库触发重新构建

## 新增实例
1. 将新实例发布上线
2. 在 docuo.config.en/zh.json 中，给同一个group.id的instance加一个askAi.quetions属性以便生成 ai 默认问题
3. 运行AI数据更新脚本，选择要更新的实例
4. 将 data/ai_search_mapping.json 文件提交至仓库触发重新构建
