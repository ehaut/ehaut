## SB-Srun3k-python 版

<s>因为学校全面禁止了路由器，使用路由器会导致五分钟一断线，于是就诞生了 python 版本</s>

由于已经修复掉线的BUG，现已不用向服务器发送心跳包了

Python 版实现了

- 自动保存输入的用户名和密码（需要更改登录账户，直接删除 config.ini 配置文件即可重新输入，或者直接在 config.ini 处直接更改）

- 掉线自动重连（每秒检测一下登录状态，实现掉线一秒自动重连）

- <s>后台向服务器发送 UDP 心跳包</s>



## 网页版(HTML) 已更新，修复了校园网频繁掉线的问题

https://github.com/noisky/srun3k-sb-client/tree/master

