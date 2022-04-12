# API文档

## API 规范

### 编写接口

- 基本参考Restful API规范
    - 不同的地方
        - 主要在于不完全遵守资源的操作规范
        - 因为嫌麻烦，不带有API版本号
- response
    - 推荐`from rest_framework.response import Response`配合响应类
    - 完全自己定义，参考：*Common.utils.http.response.JsonResponse*
- 响应类在*Common.utils.http.exceptions*中定义
    - 返回的json规范详见*Common.utils.http.response.BaseHTTPJSONResponse*
    - 继承成功和失败两个类编写自己的响应类
    - 定义的响应类应在[code定义文档](code.md)中进行详细说明

### 编写文档

- **如果嫌写文档麻烦可以跳过**
- 本架构使用 [drf_spectacular](https://github.com/tfranzel/drf-spectacular) 来生成文档
- 主要使用`from drf_spectacular.utils import extend_schema`来编写接口
    - 参数
        - operation_id：⼀个唯⼀标识ID，基本⽤不到
        - parameters：添加到列表中的附加或替换参数去⾃动发现字段
        - responses：替换Serializer
            - Serializer类
            - 序列化实例，⽐如：Serializer(many=True)
            - OpenApiTypes的基本类型或者实例
            - OpenApiResponse类
            - PolymorphicProxySerializer类
            - 1个字典，以状态码作为键， 以上其中⼀项作为值(是最常⽤的，格式{200, None})
            - 1个字典，以状态码作为键，以media_type作为值
        - request：替换序列化，接受各种输⼊
            - Serializer 类或者实例
            - OpenApiTypes基本类型或者实例
            - PolymorphicProxySerializer类
            - 1个字典，以media_type作为键，以上其中⼀项作为值
        - auth：⽤auth⽅法的显式列表替换发现的auth
        - description：替换发现的⽂档字符串
        - summary：⼀个可选的短的总结描述
        - deprecated：将操作标记为已弃⽤
        - tags：覆盖默认标记列表
        - exclude：设置为True以从schema中排除操作
        - operation：⼿动覆盖⾃动发现将⽣成的内容，你必须提供⼀个兼容OpenAPI3的字典，该字典可以直接翻译成YAML
        - methods：检查extend_schema中特殊的⽅法，默认匹配所有
        - versions：检查extend_schema中特殊的API版本，默认匹配所有
        - example：将请求/响应⽰例附加到操作中
        - extensions：规范扩展
    - 示例：todo，待完善
        - 函数式
        - 类视图

### 查看文档

- `api/schema/`:下载接口文档配置文件
- `/api//schema/swagger-ui/`:swagger工具
- `/api/schema/redoc/`:查看接口文档说明

## API 接口说明

### 身份认证

- JWT介绍
    - Token
        - Access Token: 用户访问令牌
        - Refresh Token:刷新Access Token
        - Sliding Token:同时具备Access Token和Refresh Token的功能，本项目不使用，故**后续文档中不进行相关内容的编写**
    - 视图：在`Common.utils.auth.views`中定义
        - TokenObtainPairView:用户认证成功后，得到Access Token和Refresh Token
        - TokenRefreshView:使用Refresh Token刷新Access Token
        - TokenVerifyView:验证Access Token是否正确合法
        - TokenBlacklistView:禁用Token，常用于用户退出登录
- 使用
    - 开启JWT认证：`'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',)`
        - 现在默认关闭
    - simplejwt的身份认证方式为：在请求的Headers里面里面添加设置参数，名称为：Authorization, 值是一个固定组成的字符串： Bearer +空格 + access_token
        - 未添加的时候，会显示：`Authentication credentials were not provided.`，即身份认证信息为提供
    - 跳过认证
        - `permission_classes`中设置`[AllowAny]`
            - 根据**视图类型**使用装饰器或者类属性进行定义

### 接口结构（目前不够完善）

- /
    - api/
    - screening/
        -  /:用户页面（比如介绍筛查项目，暂时用不到）
            - api/
            - mina/:筛查小程序使用的接口
            - manage/:管理员后台使用的接口
        - manage/:管理员后台页面
    - user_service/
        - /:用户页面（暂时用不到）
        - api/:用户服务小程序使用的接口
    - admin/:超级管理员