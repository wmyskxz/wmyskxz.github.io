---
title: DNS是什么？它是如何运作的？
cover: https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612775267339-image.png
categories: [网络]
tags: [网络]
date: 2021/02/18 08:47:12
references:
  - '[What Is A Domain Name System (DNS) & How Does It Work?](https://phoenixnap.com/kb/what-is-domain-name-system-works)'
  - '[域名报告](https://www.verisign.com/assets/domain-name-report-Q32020.pdf)'
  - '[根域名服务器只有 13 台？](https://zhuanlan.zhihu.com/p/107492241)'
  - '[30张图解：当键入网址后，到网页显示，其间发生了什么？](https://zhuanlan.zhihu.com/p/113702574)'
  - '[美国如果把根域名服务器封了，中国会从网络上消失？](https://segmentfault.com/a/1190000023696737)'
---


![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612775267339-image.png)

# 前言

我们在[上一篇](https://www.wmyskxz.com/network/how-to-link)说到，IP 地址的发明把我们纷乱复杂的网络设备整齐划一地统一在了**同一个网络**中。

但是类似于 `192.168.1.0` 这样的地址并不便于人类记忆，于是发明了 **域名(Domain Name)** 来帮助解决这样的问题。

对应的，我们也需要一个系统来帮助"翻译"：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-2/1612232538793-image.png)

# Part 1. DNS 是什么？

DNS *（Domain Name System 的缩写）* 的作用非常简单，就是根据域名查出对应的 IP 地址，你可以把它想象成一本**巨大的电话本**。

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-2/1612235242990-image.png)

换句话说，DNS 是将域名映射到响应 IP 地址的服务。

# Part 2. DNS 是如何工作的？

DNS 是我们今天使用 Internet 的核心。

[最新报告](https://www.verisign.com/assets/domain-name-report-Q32020.pdf)显示，2020 年第三季度有 `3.71` 亿个域名，如果没有 DNS 将其对应解析成对应的 IP 地址，我们将会在网络世界中迷路。

当宁想要使用手机打电话给某人，宁几乎不太可能背出确切的电话号码，而是直接使用此人的名字进行搜索和拨号。

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-2/1612237425402-image.png)

当宁想要加载网站时，DNS 会执行类似的操作。

解析域名或者主机名需要经历几个不同的阶段。

在某些情况下，DNS 解析是一个一步就完成的过程，而某些情况下，则需要联系多个 DNS 服务器。

下图就展示了这一过程**必要的步骤**，并且没有考虑浏览器缓存：

![DNS 如何工作的示例](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-2/1612249392326-image.png)

过程可能有些复杂，为了便于理解，我们在进一步说明之前需要先说明两点：**「DNS 服务器和域名的分级」** 以及 **「DNS 缓存」**。

# Part 3. 域名和 DNS 服务器的分级

## 域名的分级

我们日常上网输入的网址，比如：`https://www.google.com`，其实可以拆成几个部分看待：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-5/1612518999165-image.png)

默认支持的服务类型（HTTP/ HTTPS）、主机名（www）、端口号（80）、默认文档（index.html）是可以省略的，所以以上网址可以省略为：`google.com`。

严格来说，`google.com` 才被称为**域名（全球唯一）**，`www` 是主机名，对应着一种服务，`google.com` 域名下不同的主机服务器，可以提供很多不同的服务：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612748244033-image.png)

`www`、`blog` 等很多服务可以部署在同一台服务器上，而一台服务器独占着一个 IP 地址，可见，**域名和 IP 地址的对应关系**可以是**多对一**的，或者**一对多**（负载均衡），也可以**一对一**。

所有的域名都有一个**根**的概念，所以整个互联网的域名空间看起来会是这样：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612754653538-image.png)

## DNS 分级

把全世界所有的电话号码存储在同一个通讯录里面既不现实也效率低下。

DNS 也是类似，对应域名空间，DNS 也有类似的结构：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612755294400-image.png)

整个域名系统采取**分布式存储**。

全世界**根域名服务器**总共有 13 个，其中 10 个在美国，英国瑞典各 1 个，日本 1 个：

![来源：https://root-servers.org/](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612756134103-image.png)

这是逻辑上的数量，这 13 个根域名器服务器背后其实还是有很多台物理的服务器在工作。

根域名服务器只负责管理**顶级域名服务器**（Top Level Domain，简称 TLD），记录所有 TLD 的位置。

而 TLD 则对应管理着所有注册在当前顶级域名下的所有**权限服务器**，也就是真实提供服务的服务器的真实 IP 地址。

这有点儿类似于我们真实的通讯录，比如我们想要给 *香克斯* 打电话：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612766626972-2021-02-08%2014.42.56.gif)

可以这样想象：全世界的域名被**根域名服务器**逻辑的统一在一个通讯录中，而根域名服务器就像右边的导航一样，存储着不同标识对应列表的位置信息；

而这些标识类似于**顶级域名服务器**，存储着注册其下所有的**权限服务器**（比如 `google.com` 对应的服务器）信息；

只有查询**权限服务器**，你才能拿到详细的 IP 地址（不考虑缓存的情况下）；

# Part 4. 为什么需要 DNS 缓存？

通过上面通讯录的例子，我们已经足够理解 DNS 查询的主要过程了：*（再来看一眼）*

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612768826974-image.png)

但实际上，真正访问 DNS 服务器之前，我们会在多个地方**缓存**域名与 IP 之间的对应关系：

1. 这样可以减少对 DNS 服务器的访问，减缓 DNS 服务器的访问压力；
2. 这样也能够加快域名解析的过程；

**涉及 DNS 的地方就会有缓存**，包括浏览器、操作系统、本地 DNS 服务器、路由器、ISP 提供的递归路由器、根域名服务器等，它们都会对 DNS 结果做一定程度的缓存。

但是，DNS 缓存也存在一些问题：

1. DNS 更改刷新需要时间来传播，这意味着每一台 DNS 服务器缓存更新到最新的 IP 需要一段时间；
2. DNS 缓存也是黑客潜在的攻击手段；

# Part 5. 一次请求的详细过程

这一次我们来跟踪一次详细的过程，例如我们在浏览器输入网址 `www.example.com` 并回车：

1. 查询**浏览器缓存**，有结果则返回；（如果你使用 Chrome 浏览器可以输入 `chrome://net-internals/#dns` 自行查看）
1. 查询**系统缓存**，通常存在于 host 文件中，有结果则返回；
   ](Mac：`/etc/hosts`
   ](Windows：`C:\Windows\System32\drivers\etc\hosts`
1. 向**本地 DNS 服务器**，通常是路由器，有结果则返回，否则向上查询直连 ISP 的递归 DNS 服务器；
    ![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612772452687-image.png)
1. 查询 ISP 提供的 **「递归 DNS 服务器」**，有缓存则返回，否则一直递归查询到 **「根服务器」**；
1. **「递归 DNS 服务器」** 向 **「根服务器」** 查询 **「`.com` 权威 DNS 服务器」** 的地址；
1. **「递归 DNS 服务器」** 向 **「`.com` 权威 DNS 服务器」** 查询 **「`example.com` 所使用权威 DNS 服务器」** 的地址；
1. **「递归 DNS 服务器」** 向 **「`example.com` 所使用权威 DNS 服务器」** 查询解析获得 DNS 记录并**缓存**；
1. **「递归 DNS 服务器」** 向浏览器返回结果；
1. 浏览器拿到 IP 地址并向 `www.example.com` 发送请求；（完毕）

结合上面的内容，我相信你已经对 DNS 如何工作不再陌生。

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612772963469-007hyfXLly1g1cyjwuqvhg301m01vdfp.gif)

# 相关问题

## 为什么根 DNS 只有 13 台？

**简而言之**：由于历史和技术原因，对于 IPv4 来说，根 DNS 只能有 13 个。

**不简而言之的简而言之**：

DNS 消息使用 UDP 协议进行传输，这规定了消息最大的长度在 512 字节（不包含 IP 头部、UDP 头部）。

有了最大长度限制之后，一个 UDP 协议传输的 DNS 响应能够返回的资源记录数量就是有限的。

**要让所有的根服务器数据能包含在一个 512 字节的 UDP 包中，根服务器只能限制在 13 个。**（事实上改进之后才能容纳 13 个，最开始也没有 13 个这么多）

（[扩展阅读(下3)](https://zhuanlan.zhihu.com/p/107492241)）

## 当键入网址后，到网页显示，其间发生了什么？

本文涉及输入网址访问，这是自然而然会联想到的问题。但本文只是详细说明了 DNS 查询域名背后 IP 的过程。

![来源：@小林coding](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-8/1612774979659-image.png)

该问题涉及浏览器原理、网络协议等细节问题，感兴趣可以[戳这里(下4)](https://zhuanlan.zhihu.com/p/113702574)

## 美国如果把根域名服务器封了，中国会从网络上消失吗？

美国拥有最多的根域名服务器，如果美国把根域名服务器封了，中国会从网络上消失吗？

**答案是：不会。** 因为虽然根不在我们手里，但是我们有镜像（备份）。

[扩展阅读(下5)](https://segmentfault.com/a/1190000023696737)

# 后记

这一篇文章我们又进一步揭开了一点网络关于 DNS 一角的神秘面纱：

![](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-1/1612146383742-image.png)

也是使用了 **PPT** 制作了动图帮助大家理解，希望大家能够有所收获。

后续也会继续跟大家一起学习计算机网络的基础知识，也会尝试着跟着[后端学习路线图](https://roadmap.sh/backend)的脚步跟着大家一起学习进阶。

![https://roadmap.sh/backend](https://cdn.jsdelivr.net/gh/wmyskxz/BlogImage02/2021-2-1/1612147071259-image.png)

（完）