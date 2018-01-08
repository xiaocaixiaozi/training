FTP README
==========
Welcome to FTP!

*****
## 功能
    1、提供FTP服务器、客户端之间使用命令、传输文件，目前支持命令:[cd、dir、get、put、help、del、bye]，
    2、可以自定义添加，在bin\server.py中修改comm_dict即可，如果客户端使用没有定义的命令，则提示"Invalid command."
    3、客户端在登录后，不可切换目录到家目录之外，否则会提示"Can not change directory."
    4、对每个账户默认的磁盘配额设置为1M，在conf/config.ini文件中server项的quota字段，以MB为单位，也可单独对账户配置，
      修改conf/quota.ini 文件，格式为 [账户名] = [配额大小] ，单位为MB，此配置项会覆盖config.ini中的quota配置
    5、现有账号：user01:user01; user02:user02; user03:user03  [ 账号密码相同 ]

## 结构
    FTP
    ├─bin
    │      client_run.py    # 客户端启动脚本
    │      server_run.py    # 服务器端启动脚本
    │      __init__.py
    │
    ├─client    # 客户端目录
    │  │  ftp_client.py     # 客户端主程序文件
    │  │  __init__.py
    │
    ├─conf      # 配置文件目录
    │      config.ini       # 主配置文件，包括服务监听地址、端口，日志级别，磁盘配额
    │      quota.ini        # 对用户进行单独配置磁盘配额
    │      shadow           # 密码文件
    │
    ├─dirs          # 用户家目录
    │  ├─user01
    │  │
    │  ├─user02
    │  │
    │  └─user03
    │
    ├─docs
    ├─logs      # 日志目录
    │      ftp.log
    │
    └─server        # 服务器端主程序目录
        │  create_account.py    # 创建账户，修改密码
        │  ftp_server.py        # 服务器主程序
        │  ftp_tools.py         # 提供功能
        │  read_config.py       # 读取配置
        │  __init__.py


### 注释：
#### bin\client_run.py为客户端入口，通过 python client_run.py -h 查看使用帮助，如下：
            usage: FTP [-h] [-s SERVER] [-p PORT] [-u USER]

            FTP Server

            optional arguments:
              -h, --help            show this help message and exit
              -s SERVER, --server SERVER
                                    服务器地址，默认为localhost
              -p PORT, --port PORT  服务器端口，默认为9999
              -u USER, --user USER  用户名，默认为anonymous

#### bin\server_run.py为服务器端入口，通过 python server_run.py -h 查看使用帮助，如下：
            usage: FTP [-h] [-c ACCOUNT] [-l] [-s ADDRESS] [-p PORT]

            FTP Server

            optional arguments:
              -h, --help            show this help message and exit
              -c ACCOUNT, --account ACCOUNT
                                    创建账户并设置密码，如果账户存在，则修改密码
              -l, --listen          运行服务
              -s ADDRESS, --address ADDRESS
                                    服务监听地址，默认 localhost
              -p PORT, --port PORT  服务监听端口，默认9999

#### conf\config.ini 为配置文件，bin\server_run.py启动时调用，内容样例：
            [server]
            addr = 127.0.0.1    # 服务器监听地址
            port = 9999         # 服务器监听端口
            loglevel = 20       # 日志级别

            [account]
            shadow_file = shadow    # 密码文件名
            -----------------------------------
            # 日志级别对应表：
            CRITICAL    50
            ERROR       40
            WARNING     30
            INFO        20
            DEBUG       10
            NOTSET      0

## 启动：
##### 服务器端启动
    python bin\server_run.py -l [-s address] [-p port]
##### 创建账户
    python bin\server_run.py -c user_name
##### 客户端启动
    python bin\client_run.py [-s address] [-p port] [-u user]
##### 注：客户端启动后，会提示输入密码，认证失败则退出客户端程序。

