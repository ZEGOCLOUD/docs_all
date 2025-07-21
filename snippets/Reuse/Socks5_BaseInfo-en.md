# 客户端代理

- - -

## 功能简介
客户端代理指开发者可以设置 socks5 代理服务器作为 SDK 数据的中转站，启用客户端代理后，SDK 所有网络数据的收发，都会经过所设置的 socks5 代理服务器。

## 适用场景

当开发者的本地网络使用 socks5 代理服务器访问外网时，将无法通过直连的方式访问 ZEGO 服务，那么此时可以使用客户端代理功能来访问 ZEGO 服务。

## 架构说明

![架构图](https://doc-media.zego.im/sdk-doc/Pics/Express/iOS_Client_Framework.png)

## 使用流程

### 1 配置代理服务器

请确保您的代理服务器和代理，支持标准 socks5 协议代理服务器。

<div class="mk-warning">


若无法支持标准 socks5 协议代理服务器，请联系 ZEGO 技术支持进行配置。  
</div>

socks5 代理服务器推荐使用 3proxy 及 Dante（ubuntu） 。
- 3proxy 安装配置，请参考 [3proxy 安装配置教程](https://3proxy.org/doc/howtoe.html)。
- Dante 安装配置，请参考 [Dante 安装配置教程](http://wiki.kartbuilding.net/Dante_Socks_Server)。

### 2 配置客户端

客户端需配置的代理信息如下
