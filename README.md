# Virtual Friend
#### nonebot-plugin-vf 
##### 基于Nonebot v2的虚拟朋友插件

#### 目前支持: 虚拟男友, 虚拟女友

[Project on PyPI](https://pypi.org/project/nonebot-plugin-vf/)

### 0.安装
1.(极力推荐)使用nb-cli安装,
```
nb plugin install nonebot-plugin-vf
```
安装完成后记得
```

```
2.使用pip安装
```
pip install nonebot-plugin-vf
```
3.(比较推荐)万能法
```
去PyPI官网下载项目的whl文件, 当成zip解压了, 把包含__init__.py文件的文件夹塞到你的插件目录
```

### 1.三分钟配置好
```
1.打开手机QQ, 给QQ小冰发消息, 如果不知道在哪里找QQ小冰, 可以建一个群, 然后在群机器人中添加小冰.
2.依次发送@小冰 创造男友, @小冰 创造女友, 点开小冰回复的链接, 注册并创建虚拟朋友, 然后将虚拟朋友添加为好友.
3.当虚拟朋友出现在消息列表时, 添加成功, 通过使用插件命令来体验吧.
```
### 2.使用

普通用户命令
```
原始命令:
vf connect <vf_name>  # 连接到虚拟朋友
vf disconnect # 从当前会话断开
vf list # 列出虚拟朋友使用情况
vf help # 查看帮助文档
中文命令:
虚拟朋友 连接 虚拟朋友名称
虚拟朋友 断开
虚拟朋友 列出
虚拟朋友 帮助
```
超级用户命令
```
原始命令:
vfs transfer <vf_name> <user_id>  # 将虚拟朋友转接到另一个用户
vfs release <vf_name> # 将虚拟朋友释放, 相当于强制断开
vfs release all # 释放所有虚拟朋友
vfs list  # 列出更加详细的虚拟朋友使用情况
中文命令:
虚拟管理 转接 虚拟朋友名称 用户id
虚拟管理 释放 虚拟朋友名称
虚拟管理 释放 所有
虚拟管理 列出
```


虚拟朋友名称目前支持:
```
虚拟男友, 虚拟女友, 小冰, BabyQ, 创造恋人
```
原始命令和中文命令参数可以混着来, 如:
```
vf 连接 <vf_name>
```
