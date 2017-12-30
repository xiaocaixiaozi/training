FTP README

Welcome to FTP!

功能:
    提供FTP服务器、客户端之间使用命令、传输文件，目前支持命令:[cd、dir、get、put、help、del、bye]，
    可以自定义添加，在bin\server.py中修改comm_dict即可
    如果客户端使用没有定义的命令，则提示"Invalid command."
    客户端在登录后，不可切换目录到家目录之外，否则会提示"Can not change directory."
    现有账号：user01:user01  [ 账号密码相同 ]

结构：
    ├─bin       # 程序入口
    │      client_run.py
    │      server_run.py
    ├─conf      # 主配置文件和密码文件
    │      config.ini   # 配置文件
    │      shadow       # 密码文件
    ├─core      # 核心代码
    │     client.py     # 客户端主程序
    │     create_account.py     # 创建FTP账户，同时生成用户家目录，如果用户存在，则指修改密码
    │     FTP.png
    │     ftp_tools.py      # 提供FTP程序使用的工具
    │     read_config.py    # 读取配置，FTP程序启动时调用
    │     server.py         # 服务器端主程序
    │     __init__.py
    ├─dirs      # 用户基目录
    │  └─user01     # 用户目录
    │          user01.md     # 创建用户时产生的欢迎文件
    └─logs      # 日志目录
            ftp.log
    注释：
        bin\client_run.py为客户端入口，通过 python client_run.py -h 查看使用帮助，如下：
            usage: FTP [-h] [-s SERVER] [-p PORT] [-u USER]

            FTP Server

            optional arguments:
              -h, --help            show this help message and exit
              -s SERVER, --server SERVER
                                    服务器地址，默认为localhost
              -p PORT, --port PORT  服务器端口，默认为9999
              -u USER, --user USER  用户名，默认为anonymous

        bin\server_run.py为服务器端入口，通过 python server_run.py -h 查看使用帮助，如下：
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

        conf\config.ini 为配置文件，bin\server_run.py启动时调用，内容样例：
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

使用：
    服务器端启动: python bin\server_run.py -l [-s address] [-p port]
    创建账户：  python bin\server_run.py -c user_name
    客户端启动:  python bin\client_run.py [-s address] [-p port] [-u user]
    注：客户端启动后，会提示输入密码，认证失败则退出客户端程序。

