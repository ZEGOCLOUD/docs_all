package com.example.digitalhumanquickstartdemo.model

/**
 * 播报信息
 */
data class BroadcastInfo(
    val roomId: String,
    val streamId: String,
    val clientInferencePackageUrl: String,  // 客户端素材包下载地址，用于生成 base64config
    val digitalHumanId: String,              // 数字人ID
    val isSupportSmallImageMode: Boolean     // 是否支持小图模式
)
