package com.example.digitalhumanquickstartdemo.model

import com.google.gson.annotations.SerializedName

/**
 * 播报列表响应
 */
data class BroadcastListResponse(
    @SerializedName("broadcastList")
    val broadcastList: Map<String, BroadcastInfo>
)
