### 回调结果

错误码，具体请参见 [常见错误码](!Common_error_codes)，如查询不到可联系 ZEGO 技术支持。

| 参数 | 类型 | 描述 |
| --- | ---- | --- |
| videos | Array of Object | 视频列表。 |
| └ actors | String | 演员（多个以逗号分隔）。 |
| └ country | String | 国家或地区（多个以逗号分隔）。 |
| └ detail | String | 视频描述 |
| └ directors | String | 导演（多个以逗号分隔）。 |
| └ duration | Int | 播放时长，单位（秒）。 |
| └ ep_num | Int | 单集序号。视频为剧集（单集）类型时，存在有效值。 |
| └ first_classify | Int | 视频一级分类，电视剧、电影、动画等。如 1000：电影。 |
| └ genre | String | 内容类型。根据主题、剧情划分的作品类型，如爱情、动作、悬疑等（多个以逗号分隔）。 |
| └ https_img_path_v | String | 图片 URL（HTTPS），竖图。 |
| └ https_img_path_h | String | 图片 URL（HTTPS），横图。 |
| └ img_path_v | String | 图片 URL（HTTP），竖图。 |
| └ img_path_h | String | 图片 URL（HTTP），横图。 |
| └ name | String | 视频名称。 |
| └ num_of_episodes | Int | 剧集集数。视频为剧集（整部）类型时，存在有效值。 |
| └ release_year | Int | 上映年份。 |
| └ score | String | 评分。 |
| └ type | Int | 1：剧集（整部）； </br> 2：剧集（单集）； </br> 3：非剧集。 |
| └ id | String | 视频 ID。 |
| └ episodes | Array of Object | 剧集子集。视频为剧集（整部）类型时，存在有效值。 |
| &nbsp;&nbsp;└ video_id | string |  视频 ID。 |
| &nbsp;&nbsp;└ ep_num | Int | 单集序号。视频为剧集（单集）类型时，存在有效值。 |

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
