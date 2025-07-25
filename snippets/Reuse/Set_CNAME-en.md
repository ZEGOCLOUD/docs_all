## 2 配置步骤

本文以在腾讯云、阿里云、百度云、DNSPod、万网、新网配置 CNAME 域名解析为例。操作步骤仅供参考，如与实际配置不符，请以各自 DNS 服务商的信息为准。

### 2.1 腾讯云配置方法

若 DNS 服务商为腾讯云，可根据如下步骤添加 CNAME 记录。
1. 登录“腾讯云域名服务控制台”。
2. 选择需要添加 CNAME 的域名，单击 “解析”。
3. 进入指定域名的域名解析页，单击 “添加记录”。
4. 在该新增列填写域名 CNAME 记录，具体填写内容如下所示：

 | 参数名 | 参数描述 | 配置方案 |
|---|-----|-----|
| 主机记录 | 子域名的前缀。 | <ul><li>若域名为 “play.roomkit.zego.im”，请选择：“play”。</li><li>若解析主域名zego.im，请选择：“@”。</li><li>若解析泛域名，请选择：“\*”。</li></ul> |
| 记录类型 | CNAME 类型。 | 将域名指向另一个域名，请选择：CNAME。 |
| 线路类型 | 用于 DNS 服务器在解析域名时，根据访问者的来源，返回对应的服务器 IP 地址。 | 默认。|
| 记录值 | 需指向的域名，填写ZEGO所提供的域名对应的 CNAME 值。 | - |
| TTL(秒) | 缓存的生存时间。 | 建议填写 600 秒（默认）。 |

5. 单击“保存”，配置 CNAME 完毕。
![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/Tencent_cname.png)

### 2.2 阿里云配置方法

若 DNS 服务商为阿里云，且已完成域名备案，可参考下述步骤进行 CNAME 设置。
1. 登录阿里云控制台，选择“云解析DNS > 域名解析”。
2. 选择需要添加 CNAME 的域名，单击“解析设置”。
3. 单击添加记录，添加 CNAME 记录。

  a. 记录类型：选择 “CNAME”。  
  b. 主机记录：域名的前缀。
 | 域名 | 主机记录 |
|---|---|
| roomkit.zego.im | roomkit |
| www.zego.im | www |
| zego.im | @ |
| *.zego.im | * |

  c. 解析路线：默认值。  
  d. 记录值：填写 ZEGO 提供的域名对应的 CNAME 值。  
  e. TTL：默认填写 10 分钟。
  ![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/AliCloud_cname.png)

### 2.3 百度云配置方法

若 DNS 服务商为百度云，可通过如下步骤添加 CNAME 记录。
1. 登录百度云控制台，选择“域名管理”，进入域名管理列表页。
2. 选择云直播添加的域名，在操作列单击“解析”进入 DNS 解析页面。
3. 添加解析记录，在该页面进行如下配置：

  a. 主机记录：填写子域名的前缀。若播放域名为 “play.roomkit.zego.im”，则添加 “play”；若需要直接解析主域名 “zego.im”，则输入 “@”；若需要解析泛域名，则输入 “\*”。  
  b. 记录类型：选择 “CNAME 记录”。  
  c. 解析路线：建议选择“默认”。  
  d. 记录值：填写 ZEGO 提供的域名对应的 CNAME 值。  
  e. TTL：建议填写 10 分钟。

4. 单击“确定”提交即可。
 ![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/BaiduCloud_cname.png)

### 2.4 DNSPod 配置方法

若 DNS 服务商为 DNSPod，可通过如下步骤添加 CNAME 记录。
1. 登录 DNSPod 域名服务控制台。
2. 在列表中，找到需要添加 CNAME 记录的域名所在行，单击对应域名名称，跳转至“添加记录”界面。
3. 通过如下步骤添加 CNAME 记录：

  a. 主机记录处填子域名（例如需要添加 “www.123.com” 的解析，只需要在主机记录处填写 “www” 即可。如果只是想添加 “123.com” 的解析，主机记录直接留空，系统会自动填一个 “@” 到输入框内，“@” 的 CNAME 会影响到 MX 记录的正常解析，添加时请慎重考虑）。  
  b. 记录类型为 “CNAME”。  
  c. 线路类型（默认为必填项，否则会导致部分用户无法解析。在上图中，默认的作用为：除了联通用户之外的所有用户，都会指向 “1.com”）。  
  d. 记录值为 CNAME 指向的域名，只可以填写域名，记录生成后会自动在域名后面补一个 “.”，这是正常现象。  
  e. MX 优先级不需要填写。  
  f. TTL 不需要填写，添加时系统会自动生成，默认为 600 秒（TTL 为缓存时间，数值越小，修改记录各地生效时间越快）。
 ![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/DNSPod_cname.png)
 
### 2.5 万网配置方法

若 DNS 服务商为万网，可通过如下步骤添加 CNAME 记录。
1. 登录万网会员中心。
2. 单击会员中心左侧导航栏中的“产品管理 > 我的云解析”进入万维网云解析列表页。
3. 单击要解析的域名，进入解析记录页。
4. 进入解析记录页后，单击“新增解析”，开始设置解析记录。
5. 若要设置 CNAME 解析记录，将记录类型选择为 “CNAME”。主机记录即域名前缀，可任意填写（如：www）。记录值填写为当前域名指向的另一个域名。解析线路，TTL 默认即可。
 ![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/Wan_cname.png)

6. 填写完成后，单击“保存”，完成解析设置。


### 2.6 新网配置方法

若您的 DNS 服务商为新网，可通过设置别名（CNAME 记录）添加 CNAME 记录。别名记录允许将多个名字映射到同一台计算机。通常用于同时提供 WWW 和 MAIL 服务的计算机。

例如，有一台计算机名为 “host.mydomain.com（A记录）”，它同时提供 WWW 和 MAIL 服务，为了便于用户访问服务。可以为该计算机设置两个别名（CNAME）：WWW 和 MAIL。如下图：

  ![](https://doc-media.zego.im/sdk-doc/Pics/Consle/Permissions/Xin_cname.png)

