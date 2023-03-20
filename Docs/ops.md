# 运维文档

**注意，本文档请从头到尾全部看完，不要跳过任何部分，很多错误也许是跳步骤做导致的！！！**
**注意，本文档请从头到尾全部看完，不要跳过任何部分，很多错误也许是跳步骤做导致的！！！**
**注意，本文档请从头到尾全部看完，不要跳过任何部分，很多错误也许是跳步骤做导致的！！！**

- 项目根文件夹使用**ProjectRoot**代替
- 文档不会面面俱到，事无巨细，建议学习过相关知识后再使用
- 所有的软连接推荐使用绝对路径，如果实在想用相对路径，要使用`ln -rs`

## 环境

### 环境安装

- 基础环境
    - 基础环境安装请自行搜索，不同操作系统有不同安装方法
    - 开发环境
        - Python(3.9+)或者Conda(4.10+)
            - 本项目有部分命令使用了conda，可以替换为相应激活环境和安装包的方式
            - 如果不是使用conda**创建**的虚拟环境，可能需要安装sqlite相关的包
        - Redis(4.0+)
        - MySQL(8.0+)可选
    - 测试和生产环境
        - NGINX(1.20+)
        - MySQL(8.0+)
        - Supervisor(3.1+)
            - supervisor在不同的服务器的最新版本不同，但是使用Pip安装的一定是最新的
            - 如：`dnf install supervisor`安装的是`4.2.2`版本
        - Memcached(1.5+)
        - pango(1.40+)/gtk3(3.24.31+)
            - pango是Unix/Linux/MacOS环境
            - gtk3是Windows环境，直接官网下载安装即可
            - 用于Python的 weasyprint 模块
                - 需要根据自己的系统和 pango 版本手动使用 pip 指定版本进行安装，详见[issue文档](issues.md)
        - python-devel
            - 只有Linux操作系统需要安装
            - 用于安装阿里云 OSS Python SDK
            - 详见[阿里云 OSS Python SDK 安装](https://help.aliyun.com/document_detail/85288.html)
                - 对于CentOS、RHEL、Fedora系统:`yum install python-devel`
                    - 有可能找不到，可以试试：`yum install python36-devel`
                - 对于Debian，Ubuntu系统:`apt-get install python-dev`
- Python虚拟环境
    - Python环境依赖文件位置
        - poetry:`ProjectRoot/pyproject.toml`
        - pipenv:`ProjectRoot/Pipfile`
        - conda
            - `ProjectRoot/Dependencies/conda.yaml`
            - `ProjectRoot/Dependencies/requirements-conda.txt`
        - pip:`ProjectRoot/Dependencies/requirements-pip.txt`
    - 提供了以下几种Python环境安装方法
        - 首先需要进入项目文件夹：`cd ProjectRoot`
        - poetry(推荐)
            - 安装 poetry：`pip install poetry`
            - 安装依赖：`poetry install`
            - 可在conda环境下使用
        - pipenv(推荐)
            - 安装 pipenv：`pip install pipenv`
            - 安装依赖：`pipenv install`
            - **不可在conda环境下使用**
        - conda
            - 使用导出的环境文件重建虚拟环境：`conda env create -f Dependencies/conda.yaml`
            - 单独创建
                - 创建虚拟环境：`conda create -n django python=3.10 -y`
                - 激活虚拟环境：`conda activate django`
                - 安装依赖：`pip install -r requirements-conda.txt`
                    - 此处也可以直接使用`Dependencies/requirements-pip.txt`安装依赖
            - 以上方法安装基本都会遇到各种各样的问题而失败，不如直接对照`Pipfile`文件一个一个手动安装
        - 原生虚拟环境
            - 创建虚拟环境：`virtualenv -p python3.10 venv`
            - 激活虚拟环境：`source venv/bin/activate`
            - 安装依赖：`pip install -r Dependencies/requirements-pip.txt`
    - 一些难以使用poetry和pdm安装的包（但是pipenv一定可以），具体可以查看[issue文档](issues.md#python)
        - [weasyprint](issues.md#weasyprint)
        - [PEP 440](https://python-poetry.org/docs/master/faq/#why-is-poetry-telling-me-that-the-current-projects-python-requirement-is-not-compatible-with-one-or-more-packages-python-requirements):
          主要原因是这些包只支持到某个版本，不保证向后兼容，而poetry他们很坑的地方在于自动设置的Python版本是^3.x，要求项目内所有包需要保证能够一直向后兼容到4.0，导致了冲突，不给安装，文档写的不是很明确，坑了很多人。
            - scanpy
            - numba
            - scipy
    - [阿里云OSS相关安装过程](https://help.aliyun.com/document_detail/85288.html)
        - 主要保证python-devel安装成功

### Python环境导出

- 导出conda环境
    - `conda env export > conda.yaml`
    - 或者`conda list -e > requirements-conda.txt`
- 导出pip环境：`pip freeze > requirements-pip.txt`
    - 如果使用conda管理环境，导出的pip文件是可能有问题的，需要使用`pip list --format=freeze > requirements-pip.txt`
    - 但是需要手动删除一些基础包
- pipenv, poetry, pdm 环境管理不需要导出，会自动写入配置文件

### 服务器端口

- 打开NGINX端口:80和443
    - 根据情况也可以是别的端口
- 数据库端口
    - 根据服务器环境可以更换端口，或者禁止外部访问
    - 打开MySQL端口:3306
    - 打开Redis端口:6379
    - 打开Memcached端口:11211
- 打开邮件通信端口:25或者465或者587(根据自己服务器的情况)

## 项目启动（需要先激活虚拟环境）

- 推荐先进入项目文件夹`cd /.../ProjectRoot`
- 配置环境变量
    - `ProjectRoot/System`文件夹下创建`.env`文件
    - 配置`DJANGO_ENV`:`develop`或者`test`或者`product`
    - 配置加密
        - 配置`SECRET_KEY`
        - 配置`CRYPTOGRAPHY_SECRET_KEY`
        - 配置`HASHID_FIELD_SALT`
    - 配置邮箱
    - 配置数据库
        - MySQL
            - 根据是否使用多数据库添加其他数据库相应字段
        - Redis
        - Memcached

```dotenv
# .env文件示例
# 详见Config.settings.base和Config.settings.project模块对应的生成方法
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

# Redis
REDIS_URL='redis://127.0.0.1:6379'

# 小程序应用配置
# 谱希基因采样小程序应用配置
SAMPLE_APP_ID=''
SAMPLE_APP_SECRET=''

# 高度近视筛查小程序应用配置
SCREENING_APP_ID=''
SCREENING_APP_SECRET=''

# 高度近视报告小程序应用配置
SCREENING_REPORT_APP_ID=''
SCREENING_REPORT_APP_SECRET=''

# 阿里云API配置
ALIBABACLOUD_SMS_ACCESS_KEY_ID=''
ALIBABACLOUD_SMS_ACCESS_KEY_SECRET=''
ALIBABACLOUD_OSS_ACCESS_KEY_ID=''
ALIBABACLOUD_OSS_ACCESS_KEY_SECRET=''
# 域名前面要加上https://，否则微信小程序禁止访问
ALIBABACLOUD_OSS_ENDPOINT=''
ALIBABACLOUD_OSS_ENDPOINT_TEST=''
ALIBABACLOUD_OSS_BUCKET_NAME=''
ALIBABACLOUD_OSS_BUCKET_NAME_TEST=''
ALIBABACLOUD_OSS_BUCKET_DOMAIN=''
ALIBABACLOUD_OSS_BUCKET_DOMAIN_TEST=''

# 短信过期时间
SMS_EXPIRED_TIME='600'

# 验证码长度
VERIFICATION_CODE_LENGTH=4

# 顺丰快递API配置
SF_EXPRESS_URL='https://bspgw.sf-express.com/std/service'
SF_EXPRESS_URL_TEST='https://sfapi-sbox.sf-express.com/std/service'
SF_EXPRESS_URL_HK='https://sfapi-hk.sf-express.com/std/service'

# 采样小程序顺丰快递API配置
SF_EXPRESS_SAMPLE_APP_PARTNER_ID=''
SF_EXPRESS_SAMPLE_APP_CHECKWORD=''
SF_EXPRESS_SAMPLE_APP_CHECKWORD_TEST=''

# 谱希基因额外配置
SAMPLE_APP_LIMS_TGFBI_URL='https://lims.psi-gene.com:8088/rest/RestfulService/pushOrderInfoToCrm'

```

- 初始化项目
    - 拷贝数据文件到服务器
    - `python3 /.../ProjectRoot/System/manage.py init_data -i`
        - 请详细看完代码之后再使用，根据当前的情况，可能需要修改命令参数，比如不需要创建用户、文件夹等等
- 创建日志文件夹
    - 使用`mkdir -p 路径`
        - django:`/.../ProjectRoot/System/logs/django`
    - 使用`python /.../ProjectRoot/System/manage.py init_data -d`代替
        - gunicorn:`/.../ProjectRoot/System/logs/gunicorn`
        - supervisor:`/.../ProjectRoot/System/logs/supervisor`
        - NGINX:`/var/log/nginx`
    - 不需要创建对应的文件，配置文件里写好后这些都会自动创建文件
- 配置用户数据文件夹
    - 使用软连接：`ln -s /.../ProjectRoot/System/data/user 某个存放用户数据的文件夹`
        - 因为用户有很多数据无法存入数据库
        - 有可能数据很大，需要保存在另一个有很大空间的磁盘中
- 配置NGINX
    - 先收集静态文件:`python /.../ProjectRoot/System/manage.py collectstatic`
    - 修改`nginx.conf`，如果是测试服需要使用`nginx-test.conf`
        - 修改端口号
        - 修改域名或者ip地址
        - 修改用户名相关部分
        - 修改静态资源文件目录
        - 修改日志文件路径
        - 修改django服务器相关部分
        - 修改ssl相关配置，拷贝证书到对应目录下
    -
  全部修改完成后将配置链接到nginx的配置文件:`sudo ln -s /.../ProjectRoot/System/nginx.conf /etc/nginx/conf.d/myopia.conf`
    - 启动NGINX：`sudo systemctl start nginx`
        - 或者`sudo service nginx start`
        - 如果已经启动，则重载配置：`sudo nginx -s reload`
- 配置MySQL(需要先启动并设置好用户名和密码)
    - 进入MySQL：`mysql -u root -p`
    - 创建数据库：django对于除了sqlite的数据库都要求提前建好库
        - `CREATE DATABASE Myopia;`
        - `CREATE DATABASE MyopiaTest;`
        - 其余步骤自己查，或者用数据库管理工具建表，更加方便快速
        - ☆☆☆☆☆***一定要使用utf8mb4编码和utf8mb4_0900_as_cs排序规则，否则字段内容大小写不敏感，导致插入内容插不进去***
          ☆☆☆☆☆
    - 启用时区，具体参考[问题文档](issues.md#mysql)
    - 配置`System/Manage/settings/product.py`
        - 修改`DATABASES`数据库用户和密码
    - 迁移数据库(此迁移非从一个服务器向另一个服务器迁移，是ORM模型对于数据库表结构的迁移)
        - `python /.../ProjectRoot/System/manage.py makemigrations`
        - 创建表：`python /.../ProjectRoot/System/manage.py migrate`
        - 创建数据库表：`python /.../ProjectRoot/System/manage.py migrate`
    - 数据库初始化
        - 初始化权限、组、用户:`python /.../ProjectRoot/System/manage.py init_data -i`
        - [其他APP需要初始化的数据](backend.md)
- 启动Memcached:`service memcached start`
    - `memcached -d -u root -l 127.0.0.1 -p 11211 -m 128`
- 启动Redis:`service redis start`
- 配置gunicorn
    - 可以修改`System/gunicorn.py`文件中的端口等内容，默认不需要进行修改
    - 测试能否启动：`gunicorn Config.wsgi -c gunicorn.py`
        - 能够启动即可，确认能够运行后关闭，后续会使用supervisor来管理
        - 如果不准备使用supervisor可以将gunicorn改为后台运行
- 配置supervisor
    - **配置项目文件夹和启动命令**
        - 根据自己的服务器情况更换文件路径、虚拟环境路径、启动命令
    - 你可以选择使用默认的`/etc/supervisord.conf`和`/etc/supervisord.d`文件夹，或者像下面这样进行配置
        - supervisor自带这两个文件了，如果需要重新配置，最好删除，否则容易引起冲突
        - 创建supervisor配置文件夹
            - `mkdir -p /etc/supervisor`
            - `mkdir -p /etc/supervisor/supervisord.d`
        - 以下操作都使用**创建supervisor配置文件夹**的形式配置，如果不需要，请删除路径中的`supervisor`文件夹
            - 备份supervisor配置文件：`echo_supervisord_conf > /etc/supervisor/supervisord.conf`
            - 修改supervisord.conf文件最后的include部分为：`files = /etc/supervisor/supervisord.d/*.ini`
                - 请注意`[include]`和`files`前面的`;`要删除，这是注释
            -
          链接本项目的supervisor配置文件：`sudo ln -s /.../ProjectRoot/System/supervisor.ini /etc/supervisor/supervisord.d/myopia.ini`
            - 启动服务：`supervisord -c /etc/supervisor/supervisord.conf`
- 配置阿里云OSS
    - 购买，获得AccessKeyId和AccessKeySecret
    - 创建bucket
    - **创建文件夹**，这很重要，一定要提前创建好文件夹，否则502

### 维护

- 项目复杂之后的不停止服务、零延时切换到新代码的方法
    - 在以往项目简单，访问人数少的时候，直接重启即可解决
    - 人数多一些，但是业务量还不大的时候，可以通过在夜间重启服务器解决
    - 但是当项目、业务更加复杂，使用人数越来越多的时候，重启的方法终究会遇到瓶颈
    - 根据查询大量的资料，现在研究出了如下方法
        - 启动一个新的服务，如果是不涉及数据库的修改，只需要修改端口号，如果涉及数据库，那需要修改更多的配置
        - 在nginx配置文件中，把端口号重新修改为这个新的端口号的服务
        - 使用`nginx reload`方法进行重载，具体为什么可以查看后面的NGINX相关说明
    - 如果没有使用NGINX，那只能另寻他法了

## 数据库

### SQL

- 创建django-admin的超级用户：`python /.../ProjectRoot/System/manage.py createsuperuser`

### MySQL

- 常用命令
    - 启动：service mysqld start
    - 停止：service mysqld stop
    - 重启：service mysqld restart
    - 登录：mysql -uroot -p

### Redis

- 常用命令
    - 启动：service redis start
    - 停止：service redis stop
    - 重启：service redis restart
    - 登录：redis-cli
    - 退出：quit 或者 exit

### Memcached

## 服务器

### 上传文件

- 推荐使用filezilla等软件使用 SFTP 上传
- 上传文件之前请一定要注意磁盘空间是否足够，否则会导致上传失败
- 使用密钥(.pem)文件
    - 上传文件：`scp -i 密钥文件 文件路径 root@wmu-bio-data.top:目标文件夹`
    - 上传整个目录：`scp -i 密钥文件 -r 目录 root@wmubio-data.top:目标文件夹`

### uWSGI

- 常用命令
    - 启动：uwsgi --ini uwsgi.ini
    - 查看uwsgi的pid号：cat uwsgi/uwsgi.pid
    - 查看一下uwsgi的进程：ps aux | grep uwsgi
    - 重启uwsgi：uwsgi --reload uwsgi/uwsgi.pid
    - 停止uwsgi：uwsgi --stop uwsgi/uwsgi.pid
    - 查看uwsgi的版本：uwsgi --version

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
        - nginx -c /path/to/nginx.conf
    - 快速停止或关闭：nginx -s stop
    - 正常停止或关闭：nginx -s quit
    - 重启：service nginx restart
    - 重载：nginx -s reload
- 当不知道NGINX配置文件位置的时候
    - 通过测试配置文件查看NGINX配置文件位置：nginx -t
        - 可以测试配置文件是否有语法错误
    - 其余配置文件需要查看主配置文件最后有`include`语句的那一行
- nginx reload
    - 运行"service nginx reload"或者"/etc/init.d/nginx reload"将会热重载配置从而消除停机时间
    - 如果还有等待的请求，只要连接还没有断开，nginx进程就会接着处理这些连接
    - 因此这是一个非常优雅地重载配置的方式
    - 来源于"Nginx config reload without downtime"on ServerFault

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
- 更新配置文件
    - 当更新ini配置文件后，**即使重启，也不会自动加载新配置文件**
    - 查看配置文件是否更新：sudo supervisorctl reread
    - 重载配置文件：sudo supervisorctl update
    - 重新启动服务

### ossutil

- 安装:<https://help.aliyun.com/document_detail/120075.htm?spm=a2c4g.11186623.0.0.52613e06vcHGQ1#concept-303829>
- 配置
    - 修改文件执行权限:`chmod 755 ossutil64`
    - 使用交互式配置生成配置文件:`ossutil64 config`
- 上传
    - 简单上传
        - 文件:`ossutil64 cp 本地文件路径 oss://bucket_name/文件路径`
            - 通过设置上传路径可以重命名文件
        - 文件夹：`ossutil64 cp -r 本地文件夹路径 oss://bucket_name/文件夹路径`
            - 通过设置上传路径可以重命名文件夹
- 下载
    - 简单下载
        - 文件:`ossutil64 cp oss://bucket_name/文件路径 本地文件路径`
- 删除
    - 一般建议使用客户端或者网页删除
