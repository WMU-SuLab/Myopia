# 运维文档

- 项目根文件夹使用**ProjectRoot**代替

## 环境

### 环境安装

- 基础环境（基础环境安装请自行搜索，不同操作系统有不同安装方法）
    - Python(3.9+)或者Conda(4.10+)
        - 本项目有部分命令使用了conda，可以替换为相应激活环境和安装包的方式
    - NGINX(1.20+)
    - MySQL(8.0+)
    - Supervisor(3.1+)
        - supervisor在不同的服务器的最新版本不同，但是使用Python安装的一定是最新的
    - Redis(4.0+)
    - Memcached(1.5+)
- 环境依赖文件位置
    - pipenv:`ProjectRoot/Pipfile`
    - conda
        - `ProjectRoot/Dependencies/conda.yaml`
        - `ProjectRoot/Dependencies/requirements-conda.txt`
    - pip:`ProjectRoot/Dependencies/requirements-pip.txt`
- 首先需要进入项目文件夹：`cd ProjectRoot`
- 提供了以下几种环境安装方法
    - pipenv(推荐)
        - 安装pipenv：`pip install pipenv`
        - 安装依赖：`pipenv install`
    - conda
        - 使用导出的环境文件重建虚拟环境：`conda env create -f Dependencies/conda.yaml`
        - 单独创建
            - 创建虚拟环境：`conda create -n django python=3.10`
            - 激活虚拟环境：`conda activate django`
            - 安装依赖：`pip install -r requirements-conda.txt`
                - 此处也可以直接使用`Dependencies/requirements-pip.txt`安装依赖
    - 原生虚拟环境
        - 创建虚拟环境：`virtualenv -p python3.10 venv`
        - 激活虚拟环境：`source venv/bin/activate`
        - 安装依赖：`pip install -r Dependencies/requirements-pip.txt`

### 环境导出

- 导出conda环境
    - `conda env export > conda.yaml`
    - `conda list -e > requirements-conda.txt`
- 导出pip环境：`pip freeze > requirements-pip.txt`

## 项目启动（需要先激活虚拟环境）

- 推荐先进入项目文件夹`cd /.../ProjectRoot`
- 配置环境变量
    - `ProjectRoot/System`文件夹下创建`.env`文件
    - 配置`DJANGO_ENV`:`develop`或者`product`
    - 配置`SECRET_KEY`:任意值
    - 配置`HASHID_FIELD_SALT`:任意值
    - 配置数据库密码字段
        - DATABASE_DEFAULT_PASSWORD
        - DATABASE_SILENCER_ATLAS_PASSWORD
        - DATABASE_MYOPIA_PASSWORD
- 配置NGINX
    - 先收集静态文件:`python manage.py collectstatic`
    - 修改`nginx.conf`
        - 修改端口号
        - 修改域名或者ip地址
        - 修改用户名相关部分
        - 修改静态资源文件目录
        - 修改日志路径
        - 修改django服务器相关部分
        - 修改ssl相关配置
    - 全部修改完成后将配置链接到nginx的配置文件:`sudo ln -s /.../ProjectRoot/System/nginx.conf /etc/nginx/conf.d/myopia.conf`
    - 启动NGINX：`sudo systemctl start nginx`
        - 或者`sudo service nginx start`
        - 如果已经启动，则重载配置：`sudo nginx -s reload`
- 配置MySQL(需要先启动并设置好用户名和密码)
    - 进入MySQL：`mysql -u root -p`
    - 创建数据库：django对于除了sqlite的数据库都要求提前建好库
        - `CREATE DATABASE DjangoAuth;`
        - `CREATE DATABASE SilencerAtlas;`
        - 其余步骤自己查，或者用数据库管理工具建表，更加方便快速
        - ☆☆☆☆☆***一定要使用utf8mb4编码和utf8mb4_0900_as_cs排序规则，否则字段内容大小写不敏感，导致插入内容插插进去***☆☆☆☆☆
    - 配置`System/Manage/settings/product.py`
        - 修改`DATABASES`数据库用户和密码
    - 迁移数据库
        - `python manage.py makemigrations`
        - 创建表：`python manage.py migrate`
        - 创建DjangoAuth数据库表：`python manage.py migrate --database=DjangoAuth`
        - 创建SilencerAtlas数据库表：`python manage.py migrate --database=SilencerAtlas`
    - 创建django-admin的超级用户：`python manage.py createsuperuser`
- 启动Memcached:`service memcached start`
    - `memcached -d -u root -l 127.0.0.1 -p 11211 -m 128`
- 配置gunicorn
    - 可以修改`System/gunicorn.py`文件中的端口等内容，默认不需要进行修改
        - 如果不准备使用supervisor可以将gunicorn改为后台运行
    - 创建gunicorn的日志文件夹，路径为：`ProjectRoot/System/Common/logs/gunicorn`
    - 创建日志文件
        - `touch ProjectRoot/System/Common/logs/gunicorn/access.log`
        - `touch ProjectRoot/System/Common/logs/gunicorn/error.log`
    - 启动：`gunicorn Config.wsgi -c gunicorn.py`
- 配置supervisor
    - 创建supervisor的日志文件夹，路径为：`ProjectRoot/System/Common/logs/supervisor`
    - 创建日志文件
        - `touch ProjectRoot/System/Common/logs/supervisor/access.log`
        - `touch ProjectRoot/System/Common/logs/supervisor/error.log`
    - 你可以选择使用默认的`/etc/supervisord.conf`和`/etc/supervisord.d`文件夹，或者像下面这样进行配置
        - 创建supervisor配置文件夹
            - `mkdir -p /etc/supervisor`
            - `mkdir -p /etc/supervisor/supervisord.d`
        - 以下操作都使用**创建supervisor配置文件夹**的形式配置，如果不需要，请删除路径中的`supervisor`文件夹
          - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
          - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisord.d/*.ini`
          - 链接本项目的supervisor配置文件：`sudo ln -s /.../ProjectRoot/System/supervisor.ini /etc/supervisor/supervisord.d/myopia.ini`
          - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`
              - 问题
                  - BACKOFF Exited too quickly (process log may have details)
                      - 根目录出错
                      - 日志文件或者其目录不存在
                  - 无法使用source等终端命令：使用bash -c "command"
                  - 不断exit status 0; not expected
                      - supervisor无法处理不在前台的程序，如nohup、gunicorn设置了守护进程等
                      - 多次出现是因为没有监测到前台程序不断重启

## 数据库

### MySQL

- 常用命令
    - 启动：service mysqld start
    - 停止：service mysqld stop
    - 重启：service mysqld restart
    - 登录：mysql -uroot -p

### Redis

## 服务器

### 上传文件

- 推荐使用filezilla等软件上传
- 上传文件之前请一定要注意磁盘空间是否足够，否则会导致上传失败
- 使用密钥(.pem)文件
    - 上传文件：`scp -i 密钥文件 文件路径 root@wmu-bio-data.top:目标文件夹`
    - 上传整个目录：`scp -i 密钥文件 -r 目录 root@wmubio-data.top:目标文件夹`

### Gunicorn

### NGINX

- 常用命令
    - 启动：service nginx start
    - 快速停止或关闭：nginx -s stop
    - 正常停止或关闭：nginx -s quit
    - 重启：service nginx restart
    - 重载：nginx -s reload

### Supervisor

- 常用命令
    - 启动Supervisor：supervisord -c /etc/supervisord.conf
        - 配置文件需要根据你设置的位置进行调整
    - 关闭supervisor：supervisorctl shutdown
    - 查看所有进程的状态：supervisorctl status
    - 启动服务：supervisorctl start 服务名
    - 停止服务：supervisorctl stop 服务名
    - 重启服务：supervisorctl restart 服务名
    - 重载配置：supervisorctl update
    - 重新启动配置中的所有程序：supervisorctl reload
    - 清空进程日志：supervisorctl clear 服务名
    - 服务名可以使用all代替所有服务
    - 启动supervisor并加载默认配置文件：systemctl start supervisord.service
    - 将supervisor加入开机启动项：systemctl enable supervisord.service