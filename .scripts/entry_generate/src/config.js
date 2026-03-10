// 产品配置
const PRODUCT_CONFIG = {
  "real-time-voice-video": {
    name: "实时音视频",
    icon: "https://doc-media.zego.im/sdk-doc/Pics/DeveloperCenter/homePage/product_img/icon_shishiyinshipin.png",
    description: "支持全球超低延迟多人视频、音频互动，为开发者提供便捷接入、高可靠、多平台互通的音视频服务。",
    apiPaths: {
      client: "/client-sdk/api-reference/function-list",
      server: "/real-time-video-server/api-reference/overview"
    },
    hasVideoCapability: true,
    quickStartPath: "implementing-video-call"
  },
  "real-time-voice": {
    name: "实时语音", 
    icon: "https://doc-media.zego.im/sdk-doc/Pics/DeveloperCenter/homePage/product_img/icon_shishiyuyin.png",
    description: "支持全球超低延迟、超高音质的音频通话，为开发者提供便捷接入、高可靠、多平台互通的音视频服务。",
    apiPaths: {
      client: "/client-sdk/api-reference/function-list", 
      server: "/real-time-voice-server/api-reference/overview"
    },
    hasVideoCapability: false,
    quickStartPath: "implementing-voice-call"
  },
  "low-latency-live-streaming": {
    name: "超低延迟直播",
    icon: "https://zego-public-develop-center.oss-cn-shanghai.aliyuncs.com/homePageData/image/ico_live_streaming.png", 
    description: "为高质量体验而生，直播分发产品中的\"六边形战士\"，打造超低延迟、超强同步、抗极端弱网、超低卡顿、超清画质、首帧秒开的极致体验。",
    apiPaths: {
      client: "/client-sdk/api-reference/function-list",
      server: "/live-streaming-server/api-reference/overview"  
    },
    hasVideoCapability: true,
    quickStartPath: "implementing-live-streaming",
    stepOrder: ["产品介绍", "快速开始", "直播能力", "通信能力", "房间能力", "音频能力", "视频能力", "其他能力", "最佳实践", "参考文档"]
  }
};

// Step图标配置
const STEP_ICONS = {
  "产品介绍": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_jianjie.png",
  "快速开始": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_kuaisukaishi.png", 
  "通信能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_tongxun.png",
  "房间能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_fangjian.png",
  "音频能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_yinpin.png", 
  "视频能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_shipin.png",
  "直播能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_zhibo.png",
  "其他能力": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_xiaoxi_2.png",
  "最佳实践": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_zuijiashijian.png",
  "参考文档": "https://doc-media.zego.im/sdk-doc/Pics/Express/overview_catalog/icon_documentation_cankaowendang.png"
};

// 默认Step顺序
const DEFAULT_STEP_ORDER = [
  "产品介绍", "快速开始", "通信能力", "房间能力", "音频能力", 
  "视频能力", "直播能力", "其他能力", "最佳实践", "参考文档"
];

// Sidebar category到Step的映射
const SIDEBAR_TO_STEP_MAPPING = {
  "产品简介": "产品介绍",
  "快速开始": "快速开始",
  "通信能力": "通信能力", 
  "房间能力": "房间能力",
  "音频能力": "音频能力",
  "视频能力": "视频能力",
  "直播能力": "直播能力",
  "其他能力": "其他能力",
  "最佳实践": "最佳实践",
  "API 参考文档": "参考文档"
};

// 标签颜色映射
const TAG_COLOR_MAPPING = {
  "Hot": "red",
  "New": "blue",
  "特色": "red"
};

module.exports = {
  PRODUCT_CONFIG,
  STEP_ICONS,
  DEFAULT_STEP_ORDER,
  SIDEBAR_TO_STEP_MAPPING,
  TAG_COLOR_MAPPING
};
