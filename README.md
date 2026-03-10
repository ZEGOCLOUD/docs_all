# 使用说明

详细指南：https://zegocloud.feishu.cn/wiki/G3stwqUPYinrVEkkWkFctzdTnwb

## 本地预览

```
./run.sh
```


如果本地遇到了问题或者文档系统有更新，请运行以下命令：
```bash
docuo clear & ./run.sh
```

## 文档内容组件
支持的组件请参考：https://docuo-docs.vercel.app/editing-docs/components

## 更新搜索数据

登录以下网址触发重新爬取数据。

https://dashboard.algolia.com/

## 更新 AI 数据

请参考 [更新AI数据说明](.scripts/ai_data/README.md)

## 产品上架迁移

请参考 [产品上架迁移说明](https://zegocloud.feishu.cn/wiki/NwKuwv5jYi7YBRkGthzcAxjBn6b)

## 更新 API 文档

从[API 管理平台](http://api-mgr.zego.cloud/)下载对应SDK原始文件，解压至.scripts/api/raw_data目录下。

修改.scripts/api/config.json文件以更新生成映射关系。

执行以下命令更新 API 文档：

```bash
python3 .scripts/api/generate_api_mdx.py --config
```