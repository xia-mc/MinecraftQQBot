***Minecraft QQ Bot***


 - *它能做什么*

通过读取游戏日志捕获游戏内聊天信息

通过go-cqhttp转发到QQ群/聊天


 - *如何配置它*

配置go-cqhttp，然后将它先于本程序启动。

本程序第一次启动后，将会生成一个config.ini文件，你需要在这个文件里调整所有设置。

在配置好config.ini后，启动程序。


 - *config.ini的格式*

```ini
[Minecraft]  # 我的世界板块
# 游戏日志存放位置
logpath = D:\PCL\.minecraft\versions\MoXingTing\logs\latest.log
# 可供匹配游戏日志中聊天信息的正则表达式
chatmatch = \[\d\d:\d\d:\d\d] \[Render thread/INFO]: \[CHAT]
# 有效聊天信息开始的位置（从0开始数）
chatstartindex = 40

[QQBot]  # QQ机器人板块
# 转发消息的目标类型（group=群，private=人）
targettype = group
# 转发消息的目标ID（群号或QQ号）
targetqid = 123456789
# 反刷屏模块开关
antispam = True
# 反刷屏间隔时间
antispaminterval = 1.0
# 反刷屏模式 （normal, extra）
antispammode = normal

[go-cqhttp]  # go-cqhttp板块（仍在开发中）
# go-cqhttp的文件夹路径
path = ./go-cqhttp/
# 自动启动go-cqhttp
autostart = False
```
