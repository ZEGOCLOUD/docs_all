# Entry Generator 使用指南

## 📋 快速使用

### 1. 生成所有产品的entry文档

```bash
# 在项目根目录执行
.scripts/entry_generate/generate.sh
```

### 2. 生成指定产品的entry文档

```bash
# 生成实时音视频的所有平台entry
.scripts/entry_generate/generate.sh generate real-time-voice-video

# 生成实时语音的所有平台entry
.scripts/entry_generate/generate.sh generate real-time-voice

# 生成超低延迟直播的所有平台entry
.scripts/entry_generate/generate.sh generate low-latency-live-streaming
```

### 3. 查看支持的产品

```bash
.scripts/entry_generate/generate.sh list
```

### 4. 运行测试

```bash
.scripts/entry_generate/generate.sh test
```

### 5. 其他命令

```bash
# 列出所有支持的产品
node index.js list
npm run list

# 显示帮助信息
node index.js help
npm run help
```

## 📊 测试结果

✅ **所有测试通过！**
- 实时音视频: 生成21个平台的entry文档
- 实时语音: 支持所有平台
- 超低延迟直播: 支持所有平台

## 🔧 生成的文件

脚本会在以下位置生成entry.mdx文件：
```
core_products/{product}/{locale}/{platform}/introduction/entry.mdx
```

例如：
- `core_products/real-time-voice-video/zh/ios-oc/introduction/entry.mdx`
- `core_products/real-time-voice/zh/android-java/introduction/entry.mdx`
- `core_products/low-latency-live-streaming/zh/web/introduction/entry.mdx`

## ✨ 主要特性

1. **自动化生成**: 基于sidebars.json自动生成Steps组件
2. **配置驱动**: 根据docuo.config.json获取路由信息
3. **产品定制**: 支持不同产品的特殊需求（如实时语音无视频能力）
4. **一致性保证**: 所有平台使用统一的模板和结构
5. **批量处理**: 一次性生成所有或指定产品的entry文档

## 🎯 生成内容

每个entry.mdx文件包含：
- 产品标题和图标
- 产品描述
- 快捷操作按钮（下载SDK、快速开始、API文档）
- 基于sidebars.json的Steps组件：
  - 产品介绍
  - 快速开始
  - 通信能力
  - 房间能力
  - 音频能力
  - 视频能力（实时语音产品除外）
  - 直播能力
  - 其他能力
  - 最佳实践
  - 参考文档

## 🔄 维护说明

### 添加新产品
1. 在`.scripts/entry_generate/config.js`中添加产品配置
2. 确保docuo.config.json中有对应的实例配置
3. 确保有对应的sidebars.json文件
4. 运行生成脚本

### 修改现有产品
1. 更新sidebars.json文件
2. 重新运行生成脚本，entry文档会自动更新

### 自定义配置
- 修改`config.js`中的产品配置
- 调整Step顺序或图标
- 添加新的标签映射