# 使用说明

详细指南：https://zegocloud.feishu.cn/wiki/G3stwqUPYinrVEkkWkFctzdTnwb

## 本地预览

安装 Docuo CLI.



```
npm i -g @spreading/docuo
```

安装后执行以下命令启动预览。启动完成后会在浏览器打开一个页面显示文档网站预览。预览内容会根据文档内容变更实时同步渲染。

```
docuo dev
```

一般情况下，在运行一次 `docuo dev`后，文档网站会在本地缓存一份数据。缓存过后可以执行以下命令加快每次启动时间。
```
docuo dev --noinstall
```

如果本地遇到了问题或者文档系统有更新，请运行以下命令：
```bash
docuo clear & docuo dev
```

## 更新搜索数据

登录以下网址触发重新爬取数据。 

https://dashboard.algolia.com/

## 更新 AI 数据

请参考 [更新AI数据说明](.scripts/ai_data/README.md)