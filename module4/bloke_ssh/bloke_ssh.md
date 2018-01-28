---
## 项目名称: bloke_ssh
###### 模仿Ansible编写简单的ssh批量执行客户端
---

* ### 功能
    > * 批量执行Shell命令
    > * 批量上传文件
    > * 批量下载文件

---
* ### 实现原理
    > * 用户配置主机信息到配置文件，yaml格式
    > * 读取配置文件，使用paramiko模块连接指定的主机
    > * 使用threading实现多并发执行

---
* ### 执行

>> ###### `python run.py --help`

```shell
usage: run.py <host-pattern> options

类Ansible工具

positional arguments:
  hosts                 指定要运行的主机或主机组

optional arguments:
  -h, --help            show this help message and exit
  -m {exec,put,get}, --module {exec,put,get}
                        { exec: 远程执行命令; put: 上传文件; get: 下载文件}, 默认为exec
  -a ARGS, --args ARGS  参数
  -l, --list            列出指定主机组的主机
```

> ##### Demo 1: 列出指定主机组的主机成员，all代表所有主机

>> ###### `python run.py all --list`

```shell
other
      gateway
      varnish
mongo
      mongo-1
      mongo-2
      mongo-3
```

> ##### Demo 2: 批量获取主机名

>> ###### `python run.py other -m exec -a "hostname -f"`

```shell

***********************************gateway 结果***********************************
gateway

***********************************varnish 结果***********************************
varnish
```

> ##### Demo 3: 下载文件

>> ###### `python run.py mongo -m get -a "src=/var/log/messages dest=message"`

```shell
***********************************mongo-1 结果***********************************
Done
***********************************mongo-2 结果***********************************
Done
***********************************mongo-3 结果***********************************
Done
```
> ***注：在下载文件时，会在程序根目录的tmp目录下，为每台主机以主机名为名创建目录，并将文件分别保存到各自目录下，例如:***

```shell
# tree /F tmp

├─mongo-1
│      message
│
├─mongo-2
│      message
│
└─mongo-3
        message
```

> ##### Demo 4: 上传文件

>> ###### `python run.py all -m put -a "src=C:\\test.txt dest=/home/test"`

---

* ### 目录结构

```shell
│  bloke_ssh.md
│  bloke_ssh.png        # 流程图
│  __init__.py
│  问题
│  需求
│
├─bin                   # 可执行文件
│      run.py           # 程序入口
│      __init__.py
│
├─conf                  # 配置文件目录
│      conf.yml         # 主机资源文件，yaml语法格式
│
├─main                  # 主程序目录
│  │  bloke_ssh.py      # ssh连接
│  │  yaml_tools.py     # 读取配置文件
│  │  __init__.py│
│
├─tmp                   # 文件下载存放目录
```

---

**[![Blog](https://www.cnblogs.com/images/logo_small.gif)](http://www.cnblogs.com/bloke/)**

***http://www.cnblogs.com/bloke/***

---

