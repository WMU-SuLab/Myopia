# 后端说明文档

- 本文档主要是架构设计、模块使用等相关内容。

## 开始开发

- **先看一遍文档**
- 暂时代码中注释很少，得靠自己的领悟
- 自己开发完一个功能，如果确定要提交，**记得写文档！！！**

### git设置

- `git config core.ignorecase false`，这样才能使git区分大小写

## 文件结构说明

- 根目录
    - Dependencies: 各种依赖环境配置文件
    - Docs: 文档
    - Libs: 资源文件
    - System: 系统主文件夹
        - Config: 系统配置部分
        - Common: 公共程序
        - data: 数据文件
        - logs: 日志文件
        - Sample: 谱希基因采样应用
        - Screening: 高度近视筛查应用
        - .env: 系统环境变量
        - gunicorn.py: gunicorn配置文件
        - manage.py: 主程序入口
        - test.py: 测试程序文件
        - nginx.conf: nginx配置文件
        - nginx-test.conf: nginx测试服务器配置文件
        - supervisor.ini: supervisor配置文件
        - uwsgi.ini: uwsgi配置文件
    - .gitignore: git 会的忽略文件或文件夹的配置文件
    - LICENSE: 许可证
    - README.md: 主说明文档
    - Pipfile: pipenv 环境配置文件
    - Pipfile.lock: pipenv 模块锁定文件
    - pyproject.toml: poetry 环境配置文件
    - poetry.lock: poetry 模块锁定文件

# Django应用

## Common

### admin:后台管理模型

- 放对于django自带的后台管理的配置和操作

### libs:公用资源库

### management:管理程序

#### commands:自定义命令

- 初始化学生数据:`python manage.py init_data -S -f 文件路径`

### models:数据库模型

### serializers:数据库序列化部分

- 基于 drf 的 serializers 模块构建
- 大多数是关于 models 中 数据库模型的序列化部分，少部分是自定义的，所以和数据库模型同级别

### static:通用静态文件目录

- 生产环境部署到`System/static`，方便NGINX调用

### templates:通用模板

### viewModels:视图-数据库结构

- 常放置对于数据库模型的通用操作

### utils:通用工具(重点看这个)

- **其他的APP的utils基本遵照Common的结构**

#### algorithm_handler:算法处理器

#### alibabacloud:阿里云接口

- oss:对象存储
- sms:短信

#### auth:认证相关

- permissions:根据数据库自己设计的权限验证类
- views:整合了各种权限的自定义类视图函数
    - authentication:身份验证
    - permission:权限验证
    - throttle:限流(节流)
- authentication:自定义验证机制
- backends:重写django用户登录验证机制
- verification:验证码底层接口

#### email:邮件处理

- 封装了django发送邮件的函数
- 发送验证码

#### file_handler:文件处理

#### forms:表单验证

- 基于django的forms模块构建
- 注意
    - **和数据库模型没有必然联系，所以是utils模块中的子模块，而不是和models模块同级**
    - 在基于JSON数据传输的今天，可能表单都不怎么使用了，但是依留存这个模块，便于前后端不分离的情况下使用
- validators:通用的验证器

#### http

- throtting:自定义限流规则
- exceptions:自定义异常
- renderer:重写JSON数据相关处理规则，统一各个框架下的异常处理，保证返回JSON数据格式一致性
- response:自定义JSON返回格式及其处理
- sf_express:顺丰快递API
- successes:自定义成功返回
- url:url处理相关工具
- wechat:微信一键登录

#### schemes:数据验证

- 注意
    - 这并不是django rest framework的Schemes
    - 和form部分不同的是，本部分基于 pydantic 模块构建
    - **虽然和数据库序列化很相似，但是实际上和数据库模型的字段没有必然关系，和form部分是一样的功效**
- 完全服务于JSON形式的数据验证，可以更好的提高数据安全性和超高的解析速度

#### text_handler:文本处理

### viewModels:通用视图-数据库工具

- cache:封装django缓存功能

### views:通用视图

- 用户管理，基于Token
    - 同一个API可能能够适用于多种使用场景
    - 基于用户名
        - register_by_username
    - 基于手机号
        - register_by_phone_number：手机号+密码+验证码注册
        - login：手机号+密码登录
        - user_register_by_phone_number_and_verification_code：手机号+验证码注册
        - user_reset_password_by_phone_number_and_verification_code：手机号+验证码重置密码
        - user_register_and_login：手机号+验证码注册并登录
    - 基于邮箱
        - user_register_by_email_and_verification_code：邮箱+密码+验证码注册
        - user_reset_password_by_email_and_verification_code：邮箱+验证码重置密码
    - 基于微信
        - wechat_register_and_login：微信一键注册并登录
    - 通用操作
        - logout:退出登录
        - refresh:输入refresh token刷新access token
        - verify:获得token解析的信息
        - reset_password_by_login:重置密码
- 可公开使用的信息
    - 地区信息
    - 身份相关信息
- 文件和图片处理

## Screening

### 管理员Web端，基于Session

- 页面：views/manage
- api：views/api/manage

### 高度近视筛查小程序:views/api/mina

### 高度近视筛查用户报告小程序:views/api/report

- report_data:获得报告
- report_file:获得报告文件

## Sample

### 管理员Web端，基于Session

- 页面：views/manage
- api：views/api/manage

### 采样小程序

- 高度近视遗传风险评估:views/api/mina/high_myopia
- TGFBI角膜营养不良基因检测：views/api/mina/tgfbi
- 单基因遗传性眼病检测：views/api/mina/single_gene
- 眼全科疾病辅助诊断：views/api/mina/eye_disease
