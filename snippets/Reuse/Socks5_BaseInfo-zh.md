# 本地代理

- - -

## 功能简介

本地代理（原“客户端代理”）指开发者可以设置 socks5 代理服务器作为 SDK 数据的中转站，启用本地代理后，SDK 所有网络数据的收发，都会经过所设置的 socks5 代理服务器。

## 适用场景

当开发者的本地网络使用 socks5 代理服务器访问外网时，将无法通过直连的方式访问 ZEGO 服务，那么此时可以使用本地代理功能来访问 ZEGO 服务。

## 架构说明

![架构图](https://doc-media.zego.im/sdk-doc/Pics/Express/iOS_Client_Framework.png)

## 使用流程

### 1 配置代理服务器

请确保您的代理服务器和代理，支持标准 socks5 协议代理服务器。

<div class="mk-warning">


若无法支持标准 socks5 协议代理服务器，请联系 ZEGO 技术支持进行配置。  
</div>

socks5 代理服务器推荐使用 3proxy 及 Dante（ubuntu）。
- 3proxy 安装配置，示例如下，详细配置请参考 [3proxy 安装配置教程](https://3proxy.org/doc/howtoe.html)。
    ```
    #!/usr/local/bin/3proxy
    #3proxy 内部超时时间
    timeouts 1 5 30 60 180 1800 15 60 
    #新增用户名和密码
    users hyz:CL:12345678 hyz1:CL:123456789 
    
    #log 保存地址
    log /root/3proxy/3proxy.log D 
    #log 保存格式
    logformat "- +_L%t.%.  %N.%p %E %U %C:%c %R:%r %O %I %h %T" 
    #轮换的 log 数量
    rotate 30 

    #代理服务器的地址
    internal 192.168.200.55 
    
    #开启鉴权
    auth strong 
    flush
    #允许访问的用户名
    allow hyz,hyz1 
    #指定 socks 5 的端口
    socks -p1080 

    #socks5 支持的最大连接数 
    #ZEGO 配置需要根据客户端数量和推拉流数量计算，1 个客户端 1 路推流加 1 路拉流至少需要 3+1+1=5 条连接 
    #例如：10 个客户端，每个客户端有 10 个推流和 10 个拉流，那么总共至少需要 10*(3+10*1+10*1)=230 条连接，建议适当增加冗余，将 maxconn 配置为 300
    **maxconn** **300** 
    ```
    
- Dante 安装配置，请参考 [Dante 安装配置教程](http://wiki.kartbuilding.net/Dante_Socks_Server)。




























