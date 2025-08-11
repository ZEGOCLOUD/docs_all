### 1.1 获取标签列表

通过获取标签列表，可以知道歌曲资源的标签列表、标签分组名称、标签 ID、标签名称等信息。

<div class="mk-hint">

相比原有 [歌单](#15438) 接口，[标签](!copyright_music_agreement/copyright_music_agreement#0_1) 接口歌曲资源更丰富，且支持动态更新。因此，ZEGO 推荐开发者使用 [标签](!copyright_music_agreement/copyright_music_agreement#0_1) 接口获得歌曲列表相关内容。

</div>


#### 请求参数

**command 参数**

`"/tag/list"`     // 扩展请求类型，字符串

**params 参数**

<div class="mk-warning">


该业务不需要额外的参数，开发者传 "{}" 字符串即可。
</div>


**params 示例**

```json
{
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ groups</td>
    <td> Array of Object</td>
    <td>标签分组列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ group_id</td>
    <td>String</td>
    <td>标签分组 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ group_name</td>
    <td>String</td>
    <td>标签分组名称。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ tags</td>
    <td>Array of Object</td>
    <td>标签列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ tag_id</td>
    <td>String</td>
    <td>标签 ID，具备唯一性。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ tag_name</td>
    <td>String</td>
    <td>标签名称。​</td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "6669156f-11b3-4e71-9413-b3aa57ab2da3",
    "data": {
        "groups": [
            {
                "group_id": "5",
                "group_name": "场景",
                "tags": [
                    {
                        "tag_id": "587",
                        "tag_name": "学习"
                    }
                ]
            }
        ]
    }
}
```


### 1.2 根据标签获取歌曲

需通过 [获取标签列表](!copyright_music_agreement/copyright_music_agreement#0_1) 中的标签 ID，可获取对应的歌曲 ID、歌曲名、歌曲专辑、以及版权相关信息等。

#### 请求参数

**command 参数**

`"/tag/song"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td> tag_id </td>
    <td>String</td>
    <td>是</td>
    <td>标签 ID，通过 <a href="#0_1">获取标签列表</a> 接口获取。</td>
  </tr>
  <tr>
    <td>page</td>
    <td>Int</td>
    <td>是</td>
    <td>第几页，从 1 开始。</td>
  </tr>
  <tr>
    <td>filter</td>
    <td>Array of Int</td>
    <td>否</td>
    <td>过滤选项。<ul><li>1：过滤不包含词曲权限的歌曲</li><li>3：过滤没有歌词的歌曲</li><li>4：过滤没有音高线的歌曲</li></ul></td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "tag_id": "string",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="20%">
    <col width="50%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ songs</td>
    <td>Array of Object</td>
    <td>歌曲列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_id</td>
    <td>String</td>
    <td>歌曲 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_name</td>
    <td>String</td>
    <td>歌曲名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_name</td>
    <td>String</td>
    <td>歌手名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_img</td>
    <td>String</td>
    <td>歌手头像。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_name</td>
    <td>String</td>
    <td>歌曲所属专辑名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img</td>
    <td>String</td>
    <td>专辑封面。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_mini</td>
    <td>String</td>
    <td>专辑封面 100px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_small</td>
    <td>String</td>
    <td>专辑封面 300px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_medium</td>
    <td>String</td>
    <td>专辑封面 500px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ has_accompany</td>
    <td>Int</td>
    <td>是否有伴奏。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ duration </td>
    <td> Int </td>
    <td>歌曲时长，单位：毫秒。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ has_clip </td>
    <td> Int </td>
    <td>是否有高潮片段。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ copyright</td>
    <td>Object</td>
    <td>版权信息。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ song_lyric</td>
    <td>Int</td>
    <td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ recording</td>
    <td>Int</td>
    <td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ channel</td>
    <td>Int</td>
    <td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲，UI 界面无需展示“音速达” logo 标志。</li><li>若 channel 为 0，表示音速达渠道主推歌曲，需在 UI 界面展示“音速达” logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。<br>UI 界面示例如下：<br><img src="https://doc-media.zego.im/sdk-doc/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "string",
    "request_id": "string",
    "data": {
         "songs": [
            {
                "song_id": "string",          // 歌曲 id
                "song_name": "string",          // 歌曲名
                "singer_name": "string",      // 歌手名
                "singer_img": "string",              // 歌手头像
                "album_name": "string",          // 歌曲所属专辑名
                "album_img": "string",            // 专辑封面
                "album_img_mini": "string",       // 专辑封面 100px 左右
                "album_img_small": "string",      // 专辑封面 300px 左右
                "album_img_medium": "string",     // 专辑封面 500px 左右
                "has_accompany": int,             // 是否有伴奏，0：否；1：是
                "duration": int,                   // 歌曲时长，单位：毫秒
                "has_clip": int,                 // 是否有高潮片段，0：否；1：是
                "copyright": {                    // 版权信息
                    "song_lyric": 0,              // 词曲伴奏版权 非 0 表示有版权
                    "recording": 0,              // 歌曲录音版权 非 0 表示有版权
                    "channel": 0              // 歌曲渠道 非 0 表示其他渠道歌曲
                }
            }
        ]
    }
}
```


### 1.3 批量查询歌曲信息

通过歌曲 ID 列表批量查询歌曲信息，可获取包含歌曲信息、歌手信息、歌曲所属专辑信息、歌曲时长、以及是否有伴奏等。

#### 请求参数

**command 参数**

`"/song/infos"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>songs_id</td>
    <td>Array of String</td>
    <td>是</td>
    <td>歌曲 ID 数组。最多只支持查询 30 首歌曲信息。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "songs_id": ["abc", "edf"]
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ songs</td>
    <td>Array of Object</td>
    <td>歌曲列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_id</td>
    <td>String</td>
    <td>歌曲 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_name</td>
    <td>String</td>
    <td>歌曲名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_id</td>
    <td>String</td>
    <td>歌手 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_name</td>
    <td>String</td>
    <td>歌手名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_img</td>
    <td>String</td>
    <td>歌手头像。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_id</td>
    <td>String</td>
    <td>歌曲所属专辑 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_name</td>
    <td>String</td>
    <td>歌曲所属专辑名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img</td>
    <td>String</td>
    <td>专辑封面。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_mini</td>
    <td>String</td>
    <td>专辑封面 100px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_small</td>
    <td>String</td>
    <td>专辑封面 300px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_medium</td>
    <td>String</td>
    <td>专辑封面 500px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ has_accompany</td>
    <td>Int</td>
    <td>是否有伴奏。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ duration</td>
    <td>Int</td>
    <td>歌曲时长，单位：毫秒。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ copyright</td>
    <td>Object</td>
    <td>版权信息。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ song_lyric</td>
    <td>Int</td>
    <td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ recording</td>
    <td>Int</td>
    <td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ channel</td>
    <td>Int</td>
    <td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲，UI 界面无需展示“音速达” logo 标志。</li><li>若 channel 为 0，表示音速达渠道主推歌曲，需在 UI 界面展示“音速达” logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。<br>UI 界面示例如下：<br><img src="https://doc-media.zego.im/sdk-doc/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
  </tr>
</tbody></table>


**回调示例**

```json
{
    "code": 0,
    "message": "string",
    "request_id": "string",
    "data": {
        "songs": [
            {
                "song_id": "string",
                "song_name": "string",
                "singer_id": "string",
                "singer_name": "string",
                "singer_img": "string",
                "album_id": "string",
                "album_name": "string",
                "album_img": "string",
                "album_img_mini": "string",
                "album_img_small": "string",
                "album_img_medium": "string",
                "has_accompany": 1,
                "duration": 0
                "copyright": {
                    "song_lyric": 0,
                    "recording": 1,
                    "channel": 0
            }
        ]
    }
}
```

### 1.4 搜索提示

根据您输入的关键词内容，在搜索框下方实时展示包含该关键词最符合的提示词，您可以选择对应的提示词进行搜索。

#### 请求参数

**command 参数**

`"/search/tips"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>keyword</td>
    <td>String</td>
    <td>是</td>
    <td>搜索关键字。</td>
  </tr>
</tbody></table>

**params 示例**

```json
{
    "keyword": "string"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ tips</td>
    <td>Array of String</td>
    <td>搜索提示 tip 列表。</td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "string",
    "request_id": "string",
    "data": {
        "tips": [	// 提示列表
            "string"
        ]
    }
}
```

### 1.5 搜索歌曲

通过输入关键词搜索歌曲，可获取包含歌曲信息、歌手信息、歌曲所属专辑信息、版权信息、以及是否有伴奏等。

#### 请求参数

**command 参数**

`"/search/song"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>keyword</td>
    <td>String</td>
    <td>是</td>
    <td>搜索关键字。</td>
  </tr>
  <tr>
    <td>page</td>
    <td>Int</td>
    <td>是</td>
    <td>第几页，从 1 开始。</td>
  </tr>
  <tr>
    <td>filter</td>
    <td>Array of Int</td>
    <td>否</td>
    <td>过滤选项。<ul><li>1：过滤不包含词曲权限的歌曲</li><li>2：过滤歌名带“纯音乐”的歌曲</li><li>3：过滤没有歌词的歌曲</li><li>4：过滤没有音高线的歌曲</li></ul></td>
  </tr>
</tbody></table>

**params 示例**

```json
{
    "keyword": "string",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ songs</td>
    <td>Array of Object</td>
    <td>歌曲列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_id</td>
    <td>String</td>
    <td>歌曲 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_name</td>
    <td>String</td>
    <td>歌曲名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_id</td>
    <td>String</td>
    <td>歌手 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_name</td>
    <td>String</td>
    <td>歌手名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_img</td>
    <td>String</td>
    <td>歌手头像。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_id</td>
    <td>String</td>
    <td>歌曲所属专辑 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_name</td>
    <td>String</td>
    <td>歌曲所属专辑名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img</td>
    <td>String</td>
    <td>专辑封面。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_mini</td>
    <td>String</td>
    <td>专辑封面 100px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_small</td>
    <td>String</td>
    <td>专辑封面 300px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_medium</td>
    <td>String</td>
    <td>专辑封面 500px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ has_accompany</td>
    <td>Int</td>
    <td>是否有伴奏。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ duration</td>
    <td>Int</td>
    <td>歌曲时长，单位：毫秒。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ copyright</td>
    <td>Object</td>
    <td>版权信息。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ song_lyric</td>
    <td>Int</td>
    <td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ recording</td>
    <td>Int</td>
    <td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ channel</td>
    <td>Int</td>
    <td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲，UI 界面无需展示“音速达” logo 标志。</li><li>若 channel 为 0，表示音速达渠道主推歌曲，需在 UI 界面展示“音速达” logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。<br>UI 界面示例如下：<br><img src="https://doc-media.zego.im/sdk-doc/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
  </tr>
</tbody></table>


**回调示例**

```json
{
    "code": 0,
    "message": "string",
    "request_id": "string",
    "data": {
        "songs": [
            {
                "song_id": "string",
                "song_name": "string",
                "singer_id": "string",
                "singer_name": "string",
                "singer_img": "string",
                "album_id": "string",
                "album_name": "string",
                "album_img": "string",
                "album_img_mini": "string",
                "album_img_small": "string",
                "album_img_medium": "string",
                "has_accompany": 1,
                "duration": int
                "copyright": {
                    "song_lyric": 0,
                    "recording": 1,
                    "channel": 0
                }
            }
        ]
    }
}
```

### 1.6 榜单歌曲

通过榜单 ID 获取榜单歌曲，包含歌曲信息、歌手信息、歌曲所属专辑信息、版权信息、以及是否有伴奏等。


#### 请求参数

**command 参数**

`"/top/song"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>top_id</td>
    <td>String</td>
    <td>是</td>
    <td>榜单 ID。<ul><li>热歌推荐：8888</li><li>网络红歌：23784</li><li>动感 DJ：24971</li><li>最新飙升：6666</li></ul></td>
  </tr>
  <tr>
    <td>page</td>
    <td>Int</td>
    <td>是</td>
    <td>第几页，从 1 开始。</td>
  </tr>
  <tr>
    <td>filter</td>
    <td>Array of Int</td>
    <td>否</td>
    <td>过滤选项。<ul><li>1：过滤不包含词曲权限的歌曲</li><li>3：过滤没有歌词的歌曲</li><li>4：过滤没有音高线的歌曲</li></ul></td>
  </tr>
</tbody></table>

**params 示例**

```json
{
    "top_id": "8888",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ songs</td>
    <td>Array of Object</td>
    <td>歌曲列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_id</td>
    <td>String</td>
    <td>歌曲 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_name</td>
    <td>String</td>
    <td>歌曲名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_id</td>
    <td>String</td>
    <td>歌手 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_name</td>
    <td>String</td>
    <td>歌手名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ singer_img</td>
    <td>String</td>
    <td>歌手头像。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_id</td>
    <td>String</td>
    <td>歌曲所属专辑 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_name</td>
    <td>String</td>
    <td>歌曲所属专辑名。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img</td>
    <td>String</td>
    <td>专辑封面。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_mini</td>
    <td>String</td>
    <td>专辑封面 100px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_small</td>
    <td>String</td>
    <td>专辑封面 300px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ album_img_medium</td>
    <td>String</td>
    <td>专辑封面 500px 左右。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ has_accompany</td>
    <td>Int</td>
    <td>是否有伴奏。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└duration</td>
    <td>Int</td>
    <td>歌曲时长，单位：毫秒。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ copyright</td>
    <td>Object</td>
    <td>版权信息。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ song_lyric</td>
    <td>Int</td>
    <td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ recording</td>
    <td>Int</td>
    <td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ channel</td>
    <td>Int</td>
    <td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲，UI 界面无需展示“音速达” logo 标志。</li><li>若 channel 为 0，表示音速达渠道主推歌曲，需在 UI 界面展示“音速达” logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。<br>UI 界面示例如下：<br><img src="https://doc-media.zego.im/sdk-doc/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
  </tr>
</tbody></table>


**回调示例**

```json
{
    "code": 0,
    "message": "string",
    "request_id": "string",
    "data": {
        "songs": [
            {
                "song_id": "string",
                "song_name": "string",
                "singer_id": "string",
                "singer_name": "string",
                "singer_img": "string",
                "album_id": "string",
                "album_name": "string",
                "album_img": "string",
                "album_img_mini": "string",
                "album_img_small": "string",
                "album_img_medium": "string",
                "has_accompany": 0,
                "duration": int
                "copyright": {
                    "song_lyric": 0,
                    "recording": 0,
                    "channel": 0
                }
            }
        ]
    }
}
```

### 1.7 查询版权信息

查询歌曲的版权信息，包含词曲伴奏版权、录音版权、及歌曲渠道。
 
#### 请求参数

**command 参数**

`"/song/copyright"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>songs_id[]</td>
    <td>Array of String</td>
    <td>是</td>
    <td>歌曲 ID 列表，最多支持 20 个。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "songs_id": [
        "28466292",
        "287915293",
        "257333192"
    ]
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ copyright</td>
    <td>Array of JSON</td>
    <td>版权列表。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ song_id</td>
    <td>String</td>
    <td>歌曲 ID。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ right</td>
    <td>Int</td>
    <td>总版权，子版权任意一个有版权则为 1。<ul><li>0：无</li><li>1：有</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ subright</td>
    <td>Object</td>
    <td>子版权。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ song_lyric</td>
    <td>Int</td>
    <td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ recording</td>
    <td>Int</td>
    <td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;└ channel</td>
    <td>Int</td>
    <td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲，UI 界面无需展示“音速达” logo 标志。</li><li>若 channel 为 0，表示音速达渠道主推歌曲，需在 UI 界面展示“音速达” logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。<br>UI 界面示例如下：<br><img src="https://doc-media.zego.im/sdk-doc/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
  </tr>
</tbody></table>


**回调示例**

```json
{
  "code": 0,
  "message": "string",
  "request_id": "string",
  "data": {
    "copyright": [
      {
        "right": 1,
        "song_id": "string",
        "subright": {
          "song_lyric": 0,
          "recording": 1,
          "channel": 0
        }
      },
      {
        "right": 1,
        "song_id": "string",
        "subright": {
          "song_lyric": 1,
          "recording": 1,
          "channel": 0
        }
      },
      {
        "right": 1,
        "song_id": "string",
        "subright": {
          "song_lyric": 1,
          "recording": 1,
          "channel": 0
        }
      }
    ]
  }
}
```

### 1.8 获取歌词分片

当多人合唱一首歌曲时，将一首歌中的歌词打上标签（如增加颜色区分），分成不同的歌词片段。因为每段歌词对应着相应的歌曲/伴奏片段，所以每个人可以选择不同的歌词片段进行演唱。

#### 请求参数

**command 参数**

`"/song/accompany/krc/segment"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>song_id</td>
    <td>String</td>
    <td>是</td>
    <td>歌曲 ID。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "song_id": "28466292"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ tags</td>
    <td>Array of Object</td>
    <td>第 N 个人唱或多个人唱。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ end</td>
    <td>Int</td>
    <td>结束时间，单位为毫秒，以完整歌曲开始播放的时间为准。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ start</td>
    <td>Int</td>
    <td>开始时间，单位为毫秒，以完整歌曲开始播放的时间为准。</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;└ tags</td>
    <td>Array of String</td>
    <td>标签。</td>
  </tr>
</tbody></table>


**回调示例**

```json
{
  "code": 0,
  "message": "succeed",
  "request_id": "6f92edae-5cfa-4caa-9dd1-584c613671d3",
  "data": {
    "tags": [
      {
        "end": 21660,
        "start": 510,
        "tags": [
          "1"
        ]
      },
      {
        "end": 32600,
        "start": 21660,
        "tags": [
          "2"
        ]
      },
      {
        "end": 43730,
        "start": 32600,
        "tags": [
          "1"
        ]
      },
      {
        "end": 54210,
        "start": 43730,
        "tags": [
          "2"
        ]
      }
    ]
  }
}
```


### 1.9 获取伴奏高潮时间点

通过获取伴奏高潮时间点，可以标示出一首伴奏中高潮片段的时间节点。

#### 请求参数

**command 参数**

`"/song/accompany/clip_info"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>song_id</td>
    <td>String</td>
    <td>是</td>
    <td>歌曲 ID。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "song_id": "28466292"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ segment_begin</td>
    <td>Int</td>
    <td>高潮开始时间。</td>
  </tr>
  <tr>
    <td>└ segment_end</td>
    <td>Int</td>
    <td>高潮结束时间。</td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "8857e1e1-63c3-4dc4-837a-90919cbbf91e",
    "data": {
        "segment_begin": 43737,
        "segment_end": 67290
    }
}
```


### 1.10 判断是否存在伴奏高潮片段

通过判断是否存在伴奏高潮片段，可以知道该伴奏是否具有高潮片段资源。

#### 请求参数

**command 参数**

`"/song/accompany/clip_url/status"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>song_id</td>
    <td>String</td>
    <td>是</td>
    <td>歌曲 ID。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "song_id": "28466292"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ has_clip_url</td>
    <td>Number</td>
    <td>是否有高潮片段。<ul><li>0：否</li><li>1：是</li></ul></td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "16e5b05a-a189-49e6-9bc9-805dee58af79",
    "data": {
        "has_clip_url": 1
    }
}
```



### 1.11 获取歌曲附加信息

通过获取歌曲附加信息，可以知道该歌曲的节拍数、节拍类型、以及所属流派信息。

#### 请求参数

**command 参数**

`"/song/extra"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>song_id</td>
    <td>String</td>
    <td>是</td>
    <td>歌曲 ID。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "song_id": "28466292"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>操作结果描述。</td>
  </tr>
  <tr>
    <td>request_id</td>
    <td>String</td>
    <td>请求 ID。</td>
  </tr>
  <tr>
    <td>data</td>
    <td>Object</td>
    <td>响应数据。</td>
  </tr>
  <tr>
    <td>└ bpm</td>
    <td>Number</td>
    <td>歌曲节拍数。</td>
  </tr>
  <tr>
    <td>└ bpm_type</td>
    <td>String</td>
    <td>节拍类型。<ul><li>0：未知</li><li>1：慢</li><li>2：中</li><li>3：快</li></ul></td>
  </tr>
  <tr>
    <td>└ genres</td>
    <td>Array of Number</td>
    <td>歌曲流派，一首歌曲可能属于多个流派。<ul><li>1：ACG</li><li>2：DJ</li><li>3：R&B</li><li>4：世界音乐</li><li>5：中国特色音乐</li><li>6：乡村音乐</li><li>7：儿童</li><li>8：其他</li><li>9：古典音乐</li><li>10：另类/独立</li><li>11：嘻哈</li><li>12：国风音乐</li><li>13：实验音乐</li><li>14：工业&哥特</li><li>15：布鲁斯</li><li>16：拉丁</li><li>17：摇滚</li><li>18：朋克</li><li>19：民谣</li><li>20：流行</li><li>21：爵士乐</li><li>22：电子</li><li>23：纯音乐</li><li>24：舞曲</li><li>25：金属</li><li>26：雷鬼</li><li>27：潮玩</li></ul></td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "3d0409a2-6462-4bd1-9b4e-b2180c3e2209",
    "data": {
        "bpm": 130,
        "bpm_type": "3",
        "genres": [
            5
        ]
    }
}
```

### 1.12 获取伴奏的前奏结束时间

获取伴奏的前奏结束时间，用户可获取该时间跳过前奏。

<div class="mk-warning">

需在获取伴奏资源**成功**且获取音高线**成功**后，再调用此扩展协议。
</div>

#### 请求参数

**command 参数**

`"/api/get_prelude_end_time"`     // 扩展请求类型，字符串

**params 参数**

<table>
  <colgroup>
    <col width="20%">
    <col width="20%">
    <col width="20%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>是否必须</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>resource_id</td>
    <td>String</td>
    <td>是</td>
    <td>资源 ID。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "resource_id": "z_28466292_2"
}
```

#### 回调结果

<table>
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
  <tbody><tr>
    <th>参数</th>
    <th>类型</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>prelude_end_time</td>
    <td>Number</td>
    <td>伴奏的前奏结束时间(单位 ms)。</td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "prelude_end_time": 0
}
```












