# 后端说明文档

- 本文档主要是架构设计、模块使用等相关内容。

## 开始开发

- **先看一遍文档**
- 暂时代码中注释很少，得靠自己的领悟
- 自己开发完一个功能，如果确定要提交，**记得写文档！！！**

## 文件结构说明

- 根目录
    - Dependencies: 各种依赖环境配置文件
    - Docs: 文档
    - System: 系统主文件夹
        - Config: 系统配置部分
        - Common: 公共程序
        - Screening: 采样程序
        - UserService: 用户服务程序
        - .env: 系统环境变量
        - gunicorn.py: gunicorn配置文件
        - manage.py: 主程序入口
        - nginx.conf: nginx配置文件
        - supervisor.ini: supervisor配置文件
        - test.py: 测试程序文件
        - uwsgi.ini: uwsgi配置文件
    - .gitignore: git 会的忽略文件或文件夹的配置文件
    - LICENSE: 许可证
    - README.md: 主说明文档
    - Pipfile: pipenv 环境配置文件
    - Pipfile.lock: pipenv 模块锁定文件
    - pyproject.toml: poetry 环境配置文件
    - poetry.lock: poetry 模块锁定文件

# Common

## models:数据库模型

## serializers:数据库序列化部分

- 基于 drf 的 serializers 模块构建
- 大多数是关于 models 中 数据库模型的序列化部分，少部分是自定义的，所以和数据库模型同级别

## viewModel:视图-数据库结构

- 常放置对于数据库模型的通用操作

## admin:后台管理模型

- 放对于django自带的后台管理的配置和操作

## utils:通用工具(重点看这个)

- **其他的APP的utils基本遵照Common的结构**

### auth:认证相关

### http:http相关

### forms:表单验证

- 基于django的forms模块构建
- 注意
    - **和数据库模型没有必然联系，所以是utils模块中的子模块，而不是和models模块同级**
    - 在基于JSON数据传输的今天，可能表单都不怎么使用了，但是依留存这个模块，便于前后端不分离的情况下使用

### schemes:数据验证

- 注意
    - 这并不是django rest framework的Schemes
    - 和form部分不同的是，本部分基于 pydantic 模块构建
    - **虽然和数据库序列化很相似，但是实际上和数据库模型的字段没有必然关系，和form部分是一样的功效**
- 完全服务于JSON形式的数据验证，可以更好的提高数据安全性和超高的解析速度

### throttles:限流(节流)

## templates:通用模板

## static_dev:通用静态文件

## management:管理程序

# Screening

## views/manage:管理员Web端，基于Session

## views/api/mina:小程序采样端API，基于Token

# UserService

## views/api/:MAGIC队列用户服务API

### 报告（临时）

- report:获得报告

### 用户管理，基于Token

- register: 用户注册
- login:输入验证信息，获得access和refresh token
- logout:退出登录
- refresh:输入refresh token刷新access token
- verify:获得token解析的信息

