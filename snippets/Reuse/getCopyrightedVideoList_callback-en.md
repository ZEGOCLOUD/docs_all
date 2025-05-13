### 回调结果
错误码，具体请参见 [常见错误码](!Common_error_codes)，如查询不到可联系 ZEGO 技术支持。

| 参数 | 类型 | 描述 |
| --- | ---- | --- |
| total_count| Int | 符合条件命中的查询结果总数。 |
| └ videos | Array of Object | 视频列表。 |
| &nbsp;&nbsp;└ actors | String | 演员（多个以逗号分隔）。 |
| &nbsp;&nbsp;└ country | String | 国家或地区（多个以逗号分隔）。 |
| &nbsp;&nbsp;└ directors | String | 导演（多个以逗号分隔）。 |
| &nbsp;&nbsp;└ duration | Int | 播放时长，单位（秒）。 |
| &nbsp;&nbsp;└ ep_num | Int | 单集序号。视频为剧集（单集）类型时，存在有效值。 |
| &nbsp;&nbsp;└ first_classify | Int | 视频一级分类，电视剧、电影、动画等。如 1000：电影。 |
| &nbsp;&nbsp;└ genre | String | 内容类型。根据主题、剧情划分的作品类型，如爱情、动作、悬疑等（多个以逗号分隔）。 |
| &nbsp;&nbsp;└ https_img_path_v | String | 图片 URL（HTTPS），竖图。 |
| &nbsp;&nbsp;└ https_img_path_h | String | 图片 URL（HTTPS），横图。 |
| &nbsp;&nbsp;└ img_path_v | String | 图片 URL（HTTP），竖图。 |
| &nbsp;&nbsp;└ img_path_h | String | 图片 URL（HTTP），横图。 |
| &nbsp;&nbsp;└ name | String | 视频名称。 |
| &nbsp;&nbsp;└ num_of_episodes | Int | 剧集集数。视频为剧集（整部）类型时，存在有效值。 |
| &nbsp;&nbsp;└ release_year | Int | 上映年份。 |
| &nbsp;&nbsp;└ score | String | 评分。 |
| &nbsp;&nbsp;└ type | Int | 1：剧集（整部）； </br> 2：剧集（单集）； </br> 3：非剧集。 |
| &nbsp;&nbsp;└ id | String | 视频 ID。 |
| &nbsp;&nbsp;└ episodes | Array of Object | 剧集子集。视频为剧集（整部）类型时，存在有效值。 |
| &nbsp;&nbsp;&nbsp;└ video_id | string |  视频 ID。 |
| &nbsp;&nbsp;&nbsp;└ ep_num | Int | 单集序号。视频为剧集（单集）类型时，存在有效值。 |

### 回调示例

```
{
    "total_count" = 9;
    videos =     (
                {
            actors = "张晋,甄子丹,熊黛林,谭耀文";
            country = "中国大陆,中国香港";
            directors = "叶伟信";
            duration = 6288;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "动作,剧情,传记,历史";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/224/202111161357_482185_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/224/202111161357_802132_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/224/202111161357_482185_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/224/202111161357_802132_V34_1080.webp";
            name = "叶问3";
            "num_of_episodes" = 0;
            "release_year" = 2015;
            score = "8.9";
            type = 3;
            "video_id" = 730276746;
        },
                {
            actors = "黑妹,蓝天";
            country = "中国大陆";
            directors = "齐为民";
            duration = 5980;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "剧情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/140/149/202202231848_241801_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/140/149/202202231848_314391_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/140/149/202202231848_241801_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/140/149/202202231848_314391_V34_1080.webp";
            name = "少年林祥谦";
            "num_of_episodes" = 0;
            "release_year" = 2012;
            score = "6.1";
            type = 3;
            "video_id" = 730276977;
        },
                {
            actors = "武斌,乔卫东,苏婷婷,诸燕,南光,王文林";
            country = "中国大陆";
            directors = "吴志国";
            duration = 6491;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "剧情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5500/660/160/202203031054_140171_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5500/660/160/202203031054_730261_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5500/660/160/202203031054_140171_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5500/660/160/202203031054_730261_V34_1080.webp";
            name = "笑神穷不怕";
            "num_of_episodes" = 0;
            "release_year" = 2018;
            score = 6;
            type = 3;
            "video_id" = 730277352;
        },
                {
            actors = "张洋,叶芳";
            country = "中国大陆";
            directors = "谢宝锐";
            duration = 4860;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "动画,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/228/202203241642_357542_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/228/202203241642_798684_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/228/202203241642_357542_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/228/202203241642_798684_V34_1080.webp";
            name = "牧野传奇";
            "num_of_episodes" = 0;
            "release_year" = 2017;
            score = "7.3";
            type = 3;
            "video_id" = 730277571;
        },
                {
            actors = "德姬,班玛才格尔,诺敏达莱,王劲松,赵宁,苟晓娟";
            country = "中国大陆";
            directors = "柯克";
            duration = 5421;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "剧情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/134/952/202204151112_872285_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/134/952/202204151112_161146_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/134/952/202204151112_872285_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/134/952/202204151112_161146_V34_1080.webp";
            name = "八万里";
            "num_of_episodes" = 0;
            "release_year" = 2017;
            score = "7.8";
            type = 3;
            "video_id" = 730277621;
        },
                {
            actors = "赵贶,李凤绪,杨小米,李金哲,陈瑞加";
            country = "中国大陆";
            directors = "占俊科";
            duration = 5595;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "剧情,战争,爱情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/869/202204250958_102957_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/135/869/202204250958_482156_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/869/202204250958_102957_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/135/869/202204250958_482156_V34_1080.webp";
            name = "雏鸟的天空";
            "num_of_episodes" = 0;
            "release_year" = 2016;
            score = "7.7";
            type = 3;
            "video_id" = 730277735;
        },
                {
            actors = "冯绍峰,王志文,郝蕾,朱亚文,汤唯,黄轩,袁泉,袁文康,王千源,田沅,丁嘉丽";
            country = "中国大陆,中国香港";
            directors = "许鞍华";
            duration = 10429;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "爱情,剧情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/133/343/202207311556_224776_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/133/343/202207311556_801357_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/133/343/202207311556_224776_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/133/343/202207311556_801357_V34_1080.webp";
            name = "黄金时代";
            "num_of_episodes" = 0;
            "release_year" = 2014;
            score = "8.800000000000001";
            type = 3;
            "video_id" = 730277848;
        },
                {
            actors = "乌尔里奇·图克尔,史蒂夫·布西密,丹尼尔·布鲁尔,张静初,安妮·康斯金尼,达格玛·曼泽尔,香川照之,柄本明";
            country = "中国大陆,德国,法国";
            directors = "佛罗瑞·加仑伯格";
            duration = 7588;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "战争,历史,剧情,传记";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5500/233/195/202111031131_681376_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5500/233/195/202111031131_832855_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5500/233/195/202111031131_681376_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5500/233/195/202111031131_832855_V34_1080.webp";
            name = "拉贝日记";
            "num_of_episodes" = 0;
            "release_year" = 2009;
            score = "8.9";
            type = 3;
            "video_id" = 730277968;
        },
                {
            actors = "魏鹤龄,二林,季虹,李保罗";
            country = "中国大陆";
            directors = "孙瑜";
            duration = 4837;
            "ep_num" = 1;
            "first_classify" = 1000;
            genre = "动作,传记,剧情";
            "https_img_path_h" = "https://img.cmvideo.cn/publish/poms/image//image/5501/247/315/202110290940_255580_H169_1080.webp";
            "https_img_path_v" = "https://img.cmvideo.cn/publish/poms/image//image/5501/247/315/202110290940_486262_V34_1080.webp";
            "img_path_h" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/247/315/202110290940_255580_H169_1080.webp";
            "img_path_v" = "http://wapx.cmvideo.cn:8080/publish/poms/image//image/5501/247/315/202110290940_486262_V34_1080.webp";
            name = "鲁班的传说";
            "num_of_episodes" = 0;
            "release_year" = 1958;
            score = "7.8";
            type = 3;
            "video_id" = 730278291;
        }
    );
}
```
