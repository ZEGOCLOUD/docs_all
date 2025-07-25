## 1 获取标签列表

通过获取标签列表，可以知道歌曲资源的标签列表、标签分组名称、标签 ID、标签名称等信息。

<div class="mk-hint">

相比原有 [歌单](#15438) 接口，本接口歌曲资源更丰富，且支持动态更新。因此，ZEGO 推荐开发者使用本接口获得歌曲列表相关内容。

</div>


#### 请求参数

**command 参数**

`"/tag/list"`     // 扩展请求类型，字符串

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
  </tr>
</tbody></table>


**params 示例**

```json
{
    "vendor_id": 0
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>groups</td>
<td>Array of Object</td>
<td>标签分组列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>group_id</td>
<td>String</td>
<td>标签分组 ID。开发者可以通过 group_id，获取版权方 vendor_id 为 0（默认）、1、2 时的短分片高潮片段资源，详情请参考 <a href="!KTV_Live_Chorus_Program_down-Songs_resources_and_lyrics_interface_description#1_4">获取短分片高潮片段资源</a>。</td>
</tr>
<tr data-row-level="5-1-2">
<td>group_name</td>
<td>String</td>
<td>标签分组名称。</td>
</tr>
<tr data-row-level="5-1-3" data-row-child="true">
<td>tags</td>
<td>Array of Object</td>
<td>标签列表。</td>
</tr>
<tr data-row-level="5-1-3-1">
<td>tag_id</td>
<td>String</td>
<td>标签 ID，具备唯一性。</td>
</tr>
<tr data-row-level="5-1-3-2">
<td>tag_name</td>
<td>String</td>
<td>标签名称。​</td>
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


## 2 根据标签获取歌曲

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
  </tr>
  <tr>
    <td>tag_id</td>
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
    "vendor_id": 0,
    "tag_id": "string",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="20%">
    <col width="50%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>songs</td>
<td>Array of Object</td>
<td>歌曲列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>song_name</td>
<td>String</td>
<td>歌曲名。</td>
</tr>
<tr data-row-level="5-1-3">
<td>singer_name</td>
<td>String</td>
<td>歌手名。</td>
</tr>
<tr data-row-level="5-1-4">
<td>singer_img</td>
<td>String</td>
<td>歌手头像。</td>
</tr>
<tr data-row-level="5-1-5">
<td>album_name</td>
<td>String</td>
<td>歌曲所属专辑名。</td>
</tr>
<tr data-row-level="5-1-6">
<td>album_img</td>
<td>String</td>
<td>专辑封面。</td>
</tr>
<tr data-row-level="5-1-7">
<td>album_img_mini</td>
<td>String</td>
<td>专辑封面 100px 左右。</td>
</tr>
<tr data-row-level="5-1-8">
<td>album_img_small</td>
<td>String</td>
<td>专辑封面 300px 左右。</td>
</tr>
<tr data-row-level="5-1-9">
<td>album_img_medium</td>
<td>String</td>
<td>专辑封面 500px 左右。</td>
</tr>
<tr data-row-level="5-1-10">
<td>duration</td>
<td>Int</td>
<td>歌曲时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-11">
<td>has_clip</td>
<td>Int</td>
<td>是否具有长分片高潮片段资源。<ul><li>0：否</li><li>1：是</li></ul><p><b>vendor_id 为 2 时，不会返回此字段。</b></p</td>
</tr>
<tr data-row-level="5-1-12">
<td>vendor_id</td>
<td>Int</td>
<td>歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
</tr>
<tr data-row-level="5-1-13">
<td>pitch_ability</td>
<td>Int</td>
<td><p>是否具有音高线。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-14" data-row-child="true">
<td>copyright</td>
<td>Object</td>
<td>版权信息。</td>
</tr>
<tr data-row-level="5-1-14-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-14-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-14-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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
                "duration": 0,                   // 歌曲时长，单位：毫秒
                "has_clip": 1,                 // 是否有高潮片段，0：否；1：是
                "vendor_id": 2, // 歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询
                "pitch_ability": 1, //仅当 vendor_id 为 2 时，才会返回此字段
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


## 3 批量查询歌曲信息

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "songs_id": ["abc", "edf"]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>songs</td>
<td>Array of Object</td>
<td>歌曲列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>song_name</td>
<td>String</td>
<td>歌曲名。</td>
</tr>
<tr data-row-level="5-1-3">
<td>singer_id</td>
<td>String</td>
<td>歌手 ID。</td>
</tr>
<tr data-row-level="5-1-4">
<td>singer_name</td>
<td>String</td>
<td>歌手名。</td>
</tr>
<tr data-row-level="5-1-5">
<td>singer_img</td>
<td>String</td>
<td>歌手头像。</td>
</tr>
<tr data-row-level="5-1-6">
<td>album_id</td>
<td>String</td>
<td>歌曲所属专辑 ID。</td>
</tr>
<tr data-row-level="5-1-7">
<td>album_name</td>
<td>String</td>
<td>歌曲所属专辑名。</td>
</tr>
<tr data-row-level="5-1-8">
<td>album_img</td>
<td>String</td>
<td>专辑封面。</td>
</tr>
<tr data-row-level="5-1-9">
<td>album_img_mini</td>
<td>String</td>
<td>专辑封面 100px 左右。</td>
</tr>
<tr data-row-level="5-1-10">
<td>album_img_small</td>
<td>String</td>
<td>专辑封面 300px 左右。</td>
</tr>
<tr data-row-level="5-1-11">
<td>album_img_medium</td>
<td>String</td>
<td>专辑封面 500px 左右。</td>
</tr>
<tr data-row-level="5-1-12">
<td>duration</td>
<td>Int</td>
<td>歌曲时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-13">
<td>accompany_duration</td>
<td>Int</td>
<td>伴奏时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-14">
<td>vendor_id</td>
<td>Int</td>
<td>歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
</tr>
<tr data-row-level="5-1-15">
<td>pitch_ability</td>
<td>Int</td>
<td><p>是否具有音高线。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-16">
<td>has_short_segment</td>
<td>Int</td>
<td><p>是否具有短分片高潮片段资源。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-17" data-row-child="true">
<td>copyright</td>
<td>Object</td>
<td>版权信息。</td>
</tr>
<tr data-row-level="5-1-17-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-17-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-17-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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
                "duration": 248000,
                "accompany_duration": 248000,
                "vendor_id": 2, // 歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询
                "pitch_ability": 1, //仅当 vendor_id 为 2 时，才会返回此字段
                "has_short_segment": 1, //仅当 vendor_id 为 2 时，才会返回此字段
                "copyright": {
                    "song_lyric": 0,
                    "recording": 1,
                    "channel": 0
            }
        ]
    }
}
```

## 4 搜索提示

根据您输入的关键词内容，在搜索框下方实时展示包含该关键词最符合的提示词，您可以选择对应的提示词进行搜索。

<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）”、“1” 或 “2” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "keyword": "string"
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1">
<td>tips</td>
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

## 5 搜索歌曲

通过输入关键词，搜索指定版权方的歌曲资源，可获取包含歌曲信息、歌手信息、歌曲所属专辑信息、版权信息、以及是否有伴奏等。

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "keyword": "string",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>songs</td>
<td>Array of Object</td>
<td>歌曲列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>song_name</td>
<td>String</td>
<td>歌曲名。</td>
</tr>
<tr data-row-level="5-1-3">
<td>singer_id</td>
<td>String</td>
<td>歌手 ID。</td>
</tr>
<tr data-row-level="5-1-4">
<td>singer_name</td>
<td>String</td>
<td>歌手名。</td>
</tr>
<tr data-row-level="5-1-5">
<td>singer_img</td>
<td>String</td>
<td>歌手头像。</td>
</tr>
<tr data-row-level="5-1-6">
<td>album_id</td>
<td>String</td>
<td>歌曲所属专辑 ID。</td>
</tr>
<tr data-row-level="5-1-7">
<td>album_name</td>
<td>String</td>
<td>歌曲所属专辑名。</td>
</tr>
<tr data-row-level="5-1-8">
<td>album_img</td>
<td>String</td>
<td>专辑封面。</td>
</tr>
<tr data-row-level="5-1-9">
<td>album_img_mini</td>
<td>String</td>
<td>专辑封面 100px 左右。</td>
</tr>
<tr data-row-level="5-1-10">
<td>album_img_small</td>
<td>String</td>
<td>专辑封面 300px 左右。</td>
</tr>
<tr data-row-level="5-1-11">
<td>album_img_medium</td>
<td>String</td>
<td>专辑封面 500px 左右。</td>
</tr>
<tr data-row-level="5-1-12">
<td>duration</td>
<td>Int</td>
<td>歌曲时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-13">
<td>vendor_id</td>
<td>Int</td>
<td>歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
</tr>
<tr data-row-level="5-1-14">
<td>pitch_ability</td>
<td>Int</td>
<td><p>是否具有音高线。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-15">
<td>has_short_segment</td>
<td>Int</td>
<td><p>是否具有短分片高潮片段资源。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-16" data-row-child="true">
<td>copyright</td>
<td>Object</td>
<td>版权信息。</td>
</tr>
<tr data-row-level="5-1-16-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-16-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-16-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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
                "duration": 0,
                "vendor_id": 2, // 歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询
                "pitch_ability": 1, //仅当 vendor_id 为 2 时，才会返回此字段
                "has_short_segment": 1, //仅当 vendor_id 为 2 时，才会返回此字段
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

## 6 搜索多版权方的歌曲

通过输入关键词搜索歌曲，同时在多家版权方曲库中搜索查询，支持对搜索结果筛选、排序、自定义展示等。搜索结果包含歌曲信息、歌手信息、歌曲所属专辑信息、版权信息、以及是否有伴奏等。


#### 请求参数

**command 参数**

`"/search/plus"`     // 扩展请求类型，字符串

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
    <td><p>过滤选项。</p><ul><li>1：过滤不包含词曲权限的歌曲</li><li>2：过滤歌名带“纯音乐”的歌曲</li><li>3：过滤没有歌词的歌曲</li><li>4：过滤没有音高线的歌曲，仅在 vendor_id 为 0（默认）或 1 时支持该取值。</li></ul></td>
  </tr>
  <tr>
    <td>vendors_id</td>
    <td>Array of Int</td>
    <td>否</td>
    <td>需要进行搜索的版权方 ID 列表。<b>默认支持搜索所有的版权方。</b><br/>版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
  </tr>
  <tr>
    <td>keep_vendor</td>
    <td>Int</td>
    <td>否</td>
    <td>同一歌曲在多个版权方都存在资源时，在搜索结果中指定保留的版权方 ID。<br/>版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
  </tr>
  <tr>
    <td>items</td>
    <td>Array of Int</td>
    <td>否</td>
    <td>版权方条目，对应 vendors_id 参数中的各个版权方的展示条目，<b>默认每个版权方各取一条展示。</b></td>
  </tr>
</tbody></table>

<div class="mk-warning">

如果您填写了 vendors_id 和 items 参数（不使用默认配置），请注意确保 vendors_id 中的版权方和 items 中的版权方条目是一一对应的，否则调用本接口将会出错。
</div>

**params 示例**

```json
{
    "keyword": "string",
    "page": 1,
    "filter": [1],
    "vendors_id": [1, 2],
    "keep_vendor": 1,
    "items": [1,2]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>songs</td>
<td>Array of Object</td>
<td>歌曲列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>song_name</td>
<td>String</td>
<td>歌曲名。</td>
</tr>
<tr data-row-level="5-1-3">
<td>singer_id</td>
<td>String</td>
<td>歌手 ID。</td>
</tr>
<tr data-row-level="5-1-4">
<td>singer_name</td>
<td>String</td>
<td>歌手名。</td>
</tr>
<tr data-row-level="5-1-5">
<td>singer_img</td>
<td>String</td>
<td>歌手头像。</td>
</tr>
<tr data-row-level="5-1-6">
<td>album_id</td>
<td>String</td>
<td>歌曲所属专辑 ID。</td>
</tr>
<tr data-row-level="5-1-7">
<td>album_name</td>
<td>String</td>
<td>歌曲所属专辑名。</td>
</tr>
<tr data-row-level="5-1-8">
<td>album_img</td>
<td>String</td>
<td>专辑封面。</td>
</tr>
<tr data-row-level="5-1-9">
<td>album_img_mini</td>
<td>String</td>
<td>专辑封面 100px 左右。</td>
</tr>
<tr data-row-level="5-1-10">
<td>album_img_small</td>
<td>String</td>
<td>专辑封面 300px 左右。</td>
</tr>
<tr data-row-level="5-1-11">
<td>album_img_medium</td>
<td>String</td>
<td>专辑封面 500px 左右。</td>
</tr>
<tr data-row-level="5-1-12">
<td>duration</td>
<td>Int</td>
<td>歌曲时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-13">
<td>vendor_id</td>
<td>Int</td>
<td>歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
</tr>
<tr data-row-level="5-1-14">
<td>pitch_ability</td>
<td>Int</td>
<td><p>是否具有音高线。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-15">
<td>has_short_segment</td>
<td>Int</td>
<td><p>是否具有短分片高潮片段资源。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr>
<tr data-row-level="5-1-16" data-row-child="true">
<td>copyright</td>
<td>Object</td>
<td>版权信息。</td>
</tr>
<tr data-row-level="5-1-16-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-16-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-16-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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
                "duration": 0,
                "vendor_id": 2, // 歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询
                "pitch_ability": 1, //仅当 vendor_id 为 2 时，才会返回此字段
                "has_short_segment": 1, //仅当 vendor_id 为 2 时，才会返回此字段
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

## 7 获取榜单歌曲

通过榜单 ID 获取榜单歌曲，包含歌曲信息、歌手信息、歌曲所属专辑信息、版权信息、以及是否有伴奏等。

<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）”、“1” 或 “2” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
  </tr>
  <tr>
    <td>top_id</td>
    <td>String</td>
    <td>是</td>
    <td><p>榜单 ID。</p><ul><li>版权方 VendorId 为 “0（默认）” 或 “1” 时，对应榜单 ID 如下：<ul><li>6666：最新飙升</li><li>8888：热歌推荐</li><li>23784：网络红歌</li><li>24971：动感 DJ</li></ul></li><li>版权方 VendorId 为 “2” 时，对应榜单 ID 如下：<ul><li>22004：大众流行（K 歌场景）</li><li>22005：经典金曲（K 歌场景）</li><li>22006：甜蜜情歌（通用场景）</li><li>22007：甜蜜情歌（K 歌场景）</li><li>22008：甜蜜情歌（听歌场景）</li><li>22009：伤感情歌（通用场景）</li><li>22010：伤感情歌（K 歌场景）</li><li>22011：伤感情歌（听歌场景）</li><li>22015：90&00 后（通用场景）</li><li>22016：90&00 后（K 歌场景）</li><li>22017：90&00 后（听歌场景）</li><li>22018：70&80 后（通用场景）</li><li>22019：70&80 后（K 歌场景）</li><li>22020：70&80 后（听歌场景）</li><li>22026：情歌对唱（K 歌场景）</li></ul></li></ul></td>
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
    "vendor_id": 0,
    "top_id": "8888",
    "page": 1,
    "filter": [1]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>songs</td>
<td>Array of Object</td>
<td>歌曲列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>song_name</td>
<td>String</td>
<td>歌曲名。</td>
</tr>
<tr data-row-level="5-1-3">
<td>singer_id</td>
<td>String</td>
<td>歌手 ID。</td>
</tr>
<tr data-row-level="5-1-4">
<td>singer_name</td>
<td>String</td>
<td>歌手名。</td>
</tr>
<tr data-row-level="5-1-5">
<td>singer_img</td>
<td>String</td>
<td>歌手头像。</td>
</tr>
<tr data-row-level="5-1-6">
<td>album_id</td>
<td>String</td>
<td>歌曲所属专辑 ID。</td>
</tr>
<tr data-row-level="5-1-7">
<td>album_name</td>
<td>String</td>
<td>歌曲所属专辑名。</td>
</tr>
<tr data-row-level="5-1-8">
<td>album_img</td>
<td>String</td>
<td>专辑封面。</td>
</tr>
<tr data-row-level="5-1-9">
<td>album_img_mini</td>
<td>String</td>
<td>专辑封面 100px 左右。</td>
</tr>
<tr data-row-level="5-1-10">
<td>album_img_small</td>
<td>String</td>
<td>专辑封面 300px 左右。</td>
</tr>
<tr data-row-level="5-1-11">
<td>album_img_medium</td>
<td>String</td>
<td>专辑封面 500px 左右。</td>
</tr>
<tr data-row-level="5-1-12">
<td>duration</td>
<td>Int</td>
<td>歌曲时长，单位：毫秒。</td>
</tr>
<tr data-row-level="5-1-13">
<td>vendor_id</td>
<td>Int</td>
<td>歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
</tr>
<tr data-row-level="5-1-14">
<td>pitch_ability</td>
<td>Int</td>
<td><p>是否具有音高线。</p><ul><li>1：有。</li><li>2：没有。</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-1-15" data-row-child="true">
<td>copyright</td>
<td>Object</td>
<td>版权信息。</td>
</tr>
<tr data-row-level="5-1-15-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-15-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-15-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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
                "duration": int,
                "vendor_id": 2, // 歌曲的版权方。版权方的详细信息，请联系 ZEGO 商务人员咨询
                "pitch_ability": 1, //仅当 vendor_id 为 2 时，才会返回此字段
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

## 8 查询歌曲的版权信息

查询歌曲的版权信息，包含词曲伴奏版权、录音版权、及歌曲渠道。
 
<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）” 或 “1” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "songs_id": [
        "28466292",
        "287915293",
        "257333192"
    ]
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>copyright</td>
<td>Array of JSON</td>
<td>版权列表。</td>
</tr>
<tr data-row-level="5-1-1">
<td>song_id</td>
<td>String</td>
<td>歌曲 ID。</td>
</tr>
<tr data-row-level="5-1-2">
<td>right</td>
<td>Int</td>
<td>总版权，子版权任意一个有版权则为 1。<ul><li>0：无</li><li>1：有</li></ul></td>
</tr>
<tr data-row-level="5-1-3" data-row-child="true">
<td>subright</td>
<td>Object</td>
<td>子版权。</td>
</tr>
<tr data-row-level="5-1-3-1">
<td>song_lyric</td>
<td>Int</td>
<td>是否有词曲伴奏版权，可以通过 requestAccompaniment 拿到伴奏资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-3-2">
<td>recording</td>
<td>Int</td>
<td>是否有歌曲录音版权，可以通过 requestSong 拿到歌曲资源。<ul><li>0：否</li><li>1：是</li></ul></td>
</tr>
<tr data-row-level="5-1-3-3">
<td>channel</td>
<td>Int</td>
<td>歌曲渠道。<ul><li>若 channel 为 其他值，表示其他渠道歌曲。</li><li>若 channel 为 0，需要在 UI 界面展示 logo 标志。开发者可通过 <a href="https://artifact-sdk.zego.im/sdk-doc/doc/files/external/Yinsuda_logo.zip">本链接</a> 下载相关 logo 资源。UI 界面示例如下：<br><img src="/Pics/CopyrightedMusic/Chart_songs.png"></li></ul></td>
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

## 9 获取歌词分片

当多人合唱一首歌曲时，将一首歌中的歌词打上标签（如增加颜色区分），分成不同的歌词片段。因为每段歌词对应着相应的歌曲/伴奏片段，所以每个人可以选择不同的歌词片段进行演唱。

<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）” 或 “1” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "song_id": "28466292"
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1" data-row-child="true">
<td>tags</td>
<td>Array of Object</td>
<td>第 N 个人唱或多个人唱。</td>
</tr>
<tr data-row-level="5-1-1">
<td>end</td>
<td>Int</td>
<td>结束时间，单位为毫秒，以完整歌曲开始播放的时间为准。</td>
</tr>
<tr data-row-level="5-1-2">
<td>start</td>
<td>Int</td>
<td>开始时间，单位为毫秒，以完整歌曲开始播放的时间为准。</td>
</tr>
<tr data-row-level="5-1-3">
<td>tags</td>
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


## 10 获取伴奏高潮时间点

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "song_id": "28466292"
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1">
<td>segment_begin</td>
<td>Int</td>
<td><p>高潮开始时间，单位：毫秒。</p><p><b>仅当 vendor_id 为 0 或 1 时，此字段的返回值才有实际意义。</b></p></td>
</tr>
<tr data-row-level="5-2">
<td>segment_end</td>
<td>Int</td>
<td><p>高潮结束时间，单位：毫秒。</p><p><b>仅当 vendor_id 为 0 或 1 时，此字段的返回值才有实际意义。</b></p></td>
</tr>
<tr data-row-level="5-3">
<td>short_segment_begin</td>
<td>Int</td>
<td><p>高潮片段资源短分片的开始时间，单位：毫秒。</p><p><b>仅当 vendor_id 为 2 时，此字段的返回值才有实际意义。</b></p></td>
</tr>
<tr data-row-level="5-4">
<td>short_segment_end</td>
<td>Int</td>
<td><p>高潮片段资源短分片的结束时间，单位：毫秒。</p><p><b>仅当 vendor_id 为 2 时，此字段的返回值才有实际意义。</b></p></td>
</tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "8857e1e1-63c3-4dc4-837a-90919cbbf91e",
    "data": {
        "segment_begin": 0,
        "segment_end": 0,
        "short_segment_begin": 77059,
        "short_segment_end": 103955
    }
}
```


## 11 判断是否存在伴奏高潮片段

通过判断是否存在伴奏高潮片段，可以知道该伴奏是否具有高潮片段资源。

<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）”、“1” 或 “2” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "song_id": "28466292"
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1">
<td>has_clip_url</td>
<td>Int</td>
<td>是否具有长分片高潮片段资源。<ul><li>0：否</li><li>1：是</li></ul><p><b>vendor_id 为 2 时，不会返回此字段。</b></p></td>
</tr>
<tr data-row-level="5-2">
<td>has_short_segment_url</td>
<td>Int</td>
<td>是否具有短分片高潮片段资源。<ul><li>0：没有</li><li>1：有</li></ul><p><b>仅当 vendor_id 为 2 时，才会返回此字段。</b></p></td>
</tr>
</tbody></table>

**回调示例**

```json
{
    "code": 0,
    "message": "succeed",
    "request_id": "16e5b05a-a189-49e6-9bc9-805dee58af79",
    "data": {
        "has_clip_url": 1,
        "has_short_segment_url": 1
    }
}
```



## 12 获取歌曲附加信息

通过获取歌曲附加信息，可以知道该歌曲的节拍数、节拍类型、以及所属流派信息。

<div class="mk-warning">

仅当传入的版权方 vendor_id 为 “0（默认）” 或 “1” 时，才能使用本扩展请求；其余版权方不支持。版权方的详细信息，请联系 ZEGO 商务人员咨询。

</div>

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
    "song_id": "28466292"
}
```

#### 回调结果

<table class="collapsible-table" >
  <colgroup>
    <col width="30%">
    <col width="30%">
    <col width="40%">
  </colgroup>
<tbody><tr data-row-level="1">
<th>参数</th>
<th>类型</th>
<th>描述</th>
</tr>
<tr data-row-level="2">
<td>code</td>
<td>Int</td>
<td>返回码，具体请参见 <a target="_blank" href="15070#18">错误码</a>，如查询不到可联系 ZEGO 技术支持。</td>
</tr>
<tr data-row-level="3">
<td>message</td>
<td>String</td>
<td>操作结果描述。</td>
</tr>
<tr data-row-level="4">
<td>request_id</td>
<td>String</td>
<td>请求 ID。</td>
</tr>
<tr data-row-level="5" data-row-child="true">
<td>data</td>
<td>Object</td>
<td>响应数据。</td>
</tr>
<tr data-row-level="5-1">
<td>bpm</td>
<td>Int</td>
<td>歌曲节拍数。</td>
</tr>
<tr data-row-level="5-2">
<td>bpm_type</td>
<td>String</td>
<td>节拍类型。<ul><li>0：未知</li><li>1：慢</li><li>2：中</li><li>3：快</li></ul></td>
</tr>
<tr data-row-level="5-3">
<td>genres</td>
<td>Array of Int</td>
<td>歌曲流派，一首歌曲可能属于多个流派。<ul><li>1：ACG</li><li>2：DJ</li><li>3：R&amp;B</li><li>4：世界音乐</li><li>5：中国特色音乐</li><li>6：乡村音乐</li><li>7：儿童</li><li>8：其他</li><li>9：古典音乐</li><li>10：另类/独立</li><li>11：嘻哈</li><li>12：国风音乐</li><li>13：实验音乐</li><li>14：工业&amp;哥特</li><li>15：布鲁斯</li><li>16：拉丁</li><li>17：摇滚</li><li>18：朋克</li><li>19：民谣</li><li>20：流行</li><li>21：爵士乐</li><li>22：电子</li><li>23：纯音乐</li><li>24：舞曲</li><li>25：金属</li><li>26：雷鬼</li><li>27：潮玩</li></ul></td>
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

## 13 获取伴奏的前奏结束时间

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
    <td>vendor_id</td>
    <td>Int</td>
    <td>否</td>
    <td>版权方 ID。版权方的详细信息，请联系 ZEGO 商务人员咨询。</td>
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
    "vendor_id": 0,
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
    <td>Int</td>
    <td>伴奏的前奏结束时间(单位 ms)。</td>
  </tr>
</tbody></table>

**回调示例**

```json
{
    "prelude_end_time": 0
}
```



















