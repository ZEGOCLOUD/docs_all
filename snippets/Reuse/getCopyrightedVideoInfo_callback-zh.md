### 回调结果

错误码，具体请参见 [精准同步播放器 - 常见错误码](!ZegoAccurateSyncMediaPlayerSDK-Common_error_codes)，如查询不到可联系 ZEGO 技术支持。

<table class="collapsible-table" >
  <colgroup>
    <col width="15%">
    <col width="20%">
    <col width="65%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="3" data-row-child="true">
<td>videos</td>
<td>Array of Object</td>
<td>视频列表。</td>
</tr>
<tr data-row-level="3-1">
<td>actors</td>
<td>String</td>
<td>演员（多个以逗号分隔）。</td>
</tr>
<tr data-row-level="3-2">
<td>country</td>
<td>String</td>
<td>国家或地区（多个以逗号分隔）。</td>
</tr>
<tr data-row-level="3-4">
<td>detail</td>
<td>String</td>
<td>视频描述</td>
</tr>
<tr data-row-level="3-5">
<td>directors</td>
<td>String</td>
<td>&nbsp;导演（多个以逗号分隔）。</td>
</tr>
<tr data-row-level="3-6">
<td>duration</td>
<td>Int</td>
<td>播放时长，单位（秒）。&nbsp;</td>
</tr>
<tr data-row-level="3-7">
<td>ep_num</td>
<td>Int</td>
<td>单集序号。视频为剧集（单集）类型时，存在有效值。</td>
</tr>
<tr data-row-level="3-8">
<td>first_classify</td>
<td>Int</td>
<td>视频一级分类，电视剧、电影、动画等。如 1000：电影。&nbsp;</td>
</tr>
<tr data-row-level="3-9">
<td>genre</td>
<td>String</td>
<td>内容类型。根据主题、剧情划分的作品类型，如爱情、动作、悬疑等（多个以逗号分隔）。</td>
</tr>
<tr data-row-level="3-10">
<td>https_img_path_v</td>
<td>String</td>
<td>图片 URL（HTTPS），竖图。</td>
</tr>
<tr data-row-level="3-11">
<td>https_img_path_h</td>
<td>String</td>
<td>图片 URL（HTTPS），横图。</td>
</tr>
<tr data-row-level="3-12">
<td>img_path_v</td>
<td>String</td>
<td>图片 URL（HTTP），竖图。</td>
</tr>
<tr data-row-level="3-13">
<td>img_path_h</td>
<td>String</td>
<td>图片 URL（HTTP），横图。&nbsp;</td>
</tr>
<tr data-row-level="3-15">
<td>name</td>
<td>String</td>
<td>视频名称。</td>
</tr>
<tr data-row-level="3-16">
<td>num_of_episodes</td>
<td>Int</td>
<td>剧集集数。视频为剧集（整部）类型时，存在有效值。</td>
</tr>
<tr data-row-level="3-17">
<td>release_year</td>
<td>Int</td>
<td>上映年份。&nbsp;</td>
</tr>
<tr data-row-level="3-18">
<td>score</td>
<td>String</td>
<td>评分。</td>
</tr>
<tr data-row-level="3-19">
<td>type</td>
<td>Int</td>
<td>1：剧集（整部）； <br> 2：剧集（单集）； <br> 3：非剧集。</td>
</tr>
<tr data-row-level="3-20">
<td>video_id</td>
<td>String</td>
<td>视频 ID。</td>
</tr>
<tr data-row-level="3-21" data-row-child="true">
<td>episodes</td>
<td>Array of Object</td>
<td>剧集子集。视频为剧集（整部）类型时，存在有效值。</td>
</tr>
<tr data-row-level="3-21-1">
<td>video_id</td>
<td>string</td>
<td>视频 ID。</td>
</tr>
<tr data-row-level="3-21-2">
<td>ep_num</td>
<td>Int</td>
<td>单集序号。视频为剧集（单集）类型时，存在有效值。</td>
</tr>
</tbody></table>

### 回调示例

```
{
    videos =     (
                {
            actors = "利亚姆·坎宁安,布莱丹·格里森,露丝·布莱德利,欧文·沃尔";
            country = "爱尔兰";
            detail = "格萝妮娅是作恶多端的黑帮老大的女儿，被父亲安排进入娱乐圈当明星，无奈星路失败，过着行尸走肉般的生活。父亲为了在激烈的帮派斗争中巩固自己的黑帮地位，自作主张将女儿嫁给自己最大的威胁对象菲奥纳，不料女儿却有一个疯狂的计划。";
            directors = "Paul,Mercier";
            duration = 5720;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "动作,犯罪,爱情";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/667/202111121605_202008131023591450460_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/667/202111121605_2_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/667/202111121605_202008131023591450460_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/667/202111121605_2_V34_1080.webp";
            name = "追击(2017年)";
            "num_of_episodes" = 0;
            "release_year" = 2017;
            score = "7.5";
            type = 3;
            "video_id" = 730276738;
        }
    );
}
```









