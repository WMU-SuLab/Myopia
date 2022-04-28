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
    - pango(1.40+)
        - Python的 weasyprint 模块需要根据自己的系统和 pango 版本手动使用 pip 进行安装
- 环境依赖文件位置
    - pipenv:`ProjectRoot/Pipfile`
    - conda
        - `ProjectRoot/Dependencies/conda.yaml`
        - `ProjectRoot/Dependencies/requirements-conda.txt`
    - pip:`ProjectRoot/Dependencies/requirements-pip.txt`
- 首先需要进入项目文件夹：`cd ProjectRoot`
- 提供了以下几种环境安装方法
    - poetry(推荐)
        - 安装 poetry：`pip install poetry`
        - 安装依赖：`poetry install`
    - pipenv(推荐)
        - 安装 pipenv：`pip install pipenv`
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
    - 或者`conda list -e > requirements-conda.txt`
- 导出pip环境：`pip freeze > requirements-pip.txt`
    - 如果使用conda管理环境，导出的pip文件是有问题的，不能使用
    - 可以使用`pip list --format=freeze > requirements-pip.txt`
        - 但是需要手动删除一些基础包，也不好用
- pipenv, poetry, pdm 环境管理不需要导出，会自动写入配置文件

### 服务器端口

- 打开NGINX端口:80和443
    - 根据情况也可以是别的端口
- 数据库端口
    - 打开MySQL端口:3306
        - 便于开发调试
    - 打开Redis端口:6379
        - 便于开发调试
    - 打开Memcached端口:11211
        - 便于开发调试
- 打开邮件通信端口:25或者465或者587(根据自己服务器的情况)

## 项目启动（需要先激活虚拟环境）

- 推荐先进入项目文件夹`cd /.../ProjectRoot`
- 配置环境变量
    - `ProjectRoot/System`文件夹下创建`.env`文件
    - 配置`DJANGO_ENV`:`develop`或者`product`
    - 配置加密
        - 配置`SECRET_KEY`
        - 配置`HASHID_FIELD_SALT`
    - 配置邮箱
    - 配置数据库
        - MySQL
            - 根据是否使用多数据库添加其他数据库相应字段
        - Redis
        - Memcached
    - 配置小程序

```dotenv
# .env文件示例
SECRET_KEY=''
CRYPTOGRAPHY_SECRET_KEY=''
HASHID_FIELD_SALT=''

EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

DJANGO_ENV='develop'
#DJANGO_ENV='product'
#DJANGO_ENV='test'

SERVER_DOMAIN='localhost'
SERVER_PORT='8000'

# Database
# MySQL
DATABASE_DEFAULT_DOMAIN_DEV=''
DATABASE_DEFAULT_PORT_DEV=''
DATABASE_DEFAULT_NAME_DEV=''
TEST_DATABASE_DEFAULT_NAME_DEV=''
DATABASE_DEFAULT_USER_DEV=''
DATABASE_DEFAULT_PASSWORD_DEV=''

DATABASE_DEFAULT_DOMAIN_TEST=''
DATABASE_DEFAULT_PORT_TEST=''
DATABASE_DEFAULT_NAME_TEST=''
TEST_DATABASE_DEFAULT_NAME_TEST=''
DATABASE_DEFAULT_USER_TEST=''
DATABASE_DEFAULT_PASSWORD_TEST=''

DATABASE_DEFAULT_DOMAIN=''
DATABASE_DEFAULT_PORT=''
DATABASE_DEFAULT_NAME=''
TEST_DATABASE_DEFAULT_NAME=''
DATABASE_DEFAULT_USER=''
DATABASE_DEFAULT_PASSWORD=''

#Redis
REDIS_URL='redis://127.0.0.1:6379'

#MINA
MINA_SCREENING_APPID=''
MINA_SCREENING_APP_SECRET=''
MINA_USER_SERVICE_APPID=''
MINA_USER_SERVICE_APP_SECRET=''

```

- 创建资源文件夹
    - 使用`mkdir -p`创建多级目录
    - `ProjectRoot/System/Common/libs`
        - `ProjectRoot/System/Common/libs/pdf`
- 创建日志文件夹，使用`mkdir`命令
    - django
        - 只需要创建文件夹：`ProjectRoot/System/Common/logs/django`
    - gunicorn
        - 创建gunicorn的日志文件夹，路径为：`ProjectRoot/System/Common/logs/gunicorn`
        - 创建日志文件
            - `touch ProjectRoot/System/Common/logs/gunicorn/access.log`
            - `touch ProjectRoot/System/Common/logs/gunicorn/error.log`
    - supervisor
        - 创建supervisor的日志文件夹，路径为：`ProjectRoot/System/Common/logs/supervisor`
        - 创建日志文件
            - `touch ProjectRoot/System/Common/logs/supervisor/access.log`
            - `touch ProjectRoot/System/Common/logs/supervisor/error.log`
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
        - 创建数据库表：`python manage.py migrate`
    - 创建django-admin的超级用户：`python manage.py createsuperuser`
- 启动Memcached:`service memcached start`
    - `memcached -d -u root -l 127.0.0.1 -p 11211 -m 128`
- 启动Redis:``
- 配置gunicorn
    - 可以修改`System/gunicorn.py`文件中的端口等内容，默认不需要进行修改
    - 启动：`gunicorn Config.wsgi -c gunicorn.py`
        - 如果不准备使用supervisor可以将gunicorn改为后台运行
- 配置supervisor
    - **配置项目文件夹和启动命令**
        - 根据自己的服务器情况更换文件路径即可
    - 你可以选择使用默认的`/etc/supervisord.conf`和`/etc/supervisord.d`文件夹，或者像下面这样进行配置
        - 创建supervisor配置文件夹
            - `mkdir -p /etc/supervisor`
            - `mkdir -p /etc/supervisor/supervisord.d`
        - 以下操作都使用**创建supervisor配置文件夹**的形式配置，如果不需要，请删除路径中的`supervisor`文件夹
            - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
            - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisord.d/*.ini`
            -
          链接本项目的supervisor配置文件：`sudo ln -s /.../ProjectRoot/System/supervisor.ini /etc/supervisor/supervisord.d/myopia.ini`
            - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`

## 数据库

### MySQL

- 常用命令
    - 启动：service mysqld start
    - 停止：service mysqld stop
    - 重启：service mysqld restart
    - 登录：mysql -uroot -p

### Redis

### Memcached

## 服务器

### 上传文件

- 推荐使用filezilla等软件使用 SFTP 上传
- 上传文件之前请一定要注意磁盘空间是否足够，否则会导致上传失败
- 使用密钥(.pem)文件
    - 上传文件：`scp -i 密钥文件 文件路径 root@wmu-bio-data.top:目标文件夹`
    - 上传整个目录：`scp -i 密钥文件 -r 目录 root@wmubio-data.top:目标文件夹`

### Gunicorn

- 常用命令
    - 启动：`gunicorn Config.wsgi -c gunicorn.py`
    - 获取进程：`ps -ef|grep gunicorn`
    - 获取进程树：`pstree -ap|grep gunicorn`
    - 关闭：`kill -9 进程号`
    - 重启：`kill -HUP 进程号`

### NGINX

- 常用命令
    - 启动：service nginx start
    - 快速停止或关闭：nginx -s stop
    - 正常停止或关闭：nginx -s quit
    - 重启：service nginx restart
    - 重载：nginx -s reload
    - 查看NGINX安装位置和配置文件位置：nginx -t

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