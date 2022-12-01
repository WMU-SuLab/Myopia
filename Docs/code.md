# 各种code的含义

## HTTP Response Code

### 常用接口格式规范

- 注意，这是 typescript 的定义，名称使用了小驼峰命名法，根据使用规范的不同，可以使用其他命名，但是基本格式类似这样

```typescript
interface ErrorInfoStructure {
    success: boolean; // if request is success
    data?: any; // response data
    errorCode?: string; // code for errorType
    errorMessage?: string; // message display to user
    showType?: number; // error display type： 0 silent; 1 message.warn; 2 message.error; 4 notification; 9 page
    traceId?: string; // Convenient for back-end Troubleshooting: unique request ID
    host?: string; // Convenient for backend Troubleshooting: host of current access server
}
```

### HTTP 常用状态码(Status Code)

- 参考:<https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>
- 100:应该继续发送请求
- 200:查询成功
- 201:创建、更新成功
- 202:Accepted（已接受），但服务器尚未处理
- 204:删除成功
    - 但是 code=204 的话，即使后端返回了数据，前端也一样不会接受到，因为规范规定了 204 就是什么都没有，所以可以改为 202
- 301:重定向
- 302:临时性重定向
    - 表示请求的资源被分配了新的 URL，希望本次访问使用新的 URL
    - 301 与 302 的区别：前者是永久移动，后者是临时移动（之后可能还会更改 URL）
- 303:表示请求的资源被分配了新的 URL，应使用 GET 方法定向获取请求的资源；
    - 302 与 303 的区别：后者明确表示客户端应当采用 GET 方式获取资源
- 400:参数错误
- 401:未授权
- 403:禁止访问
- 404:没有找到资源
- 405:Method Not Allowed
- 407:代理认证请求 — 客户机首先必须使用代理认证自身。
- 415:介质类型不受支持 — 服务器拒绝服务请求，因为不支持请求实体的格式。
- 428:Precondition Required (要求先决条件)
- 429:Too Many Requests (太多请求)
- 431:Request Header Fields Too Large (请求头字段太大)
- 500:服务器产生未知错误
- 503:服务器由于在维护或已经超载而无法响应

### code 说明

- 999 以下表示成功
- 1000 以上表示错误
- 因为错误状态千奇百怪，而成功的状态种类不会很多
- todo：定义具体的错误代码

#### Success

- 0:通用无错误，成功

##### 数据库操作:10-20

- 10:查询成功
- 11:创建成功
- 12:更新成功
- 13:删除成功

##### 用户操作:100-199

- 100:通用用户操作成功
    - 110:注册成功
        - 111:验证成功
    - 120:登录成功
        - 121:获取新 token 成功
        - 122:延长登录时间成功
    - 130:登出成功
    - 140:修改信息成功
        - 141:修改密码成功
        - 142:修改绑定信息成功
        - 143:修改个人基础信息成功

##### 服务器操作:201-300

#### Error/Failure

- 1000:通用错误，未知错误

##### 数据库操作:1001-2000

##### 用户操作:2001-3000

##### 服务器操作:3001-4000

## Database Code

### 通用

- status
    - 1:正常使用，可查询
    - 0:在回收站
    - -1:从回收站删除
        - 一般不会真的删除

### 用户

- gender/sex
    - -:未知
    - male:男
    - female:女
- is_active
    - true:可使用
    - false:停用/禁用
- is_authenticated
    - true:已验证
    - false:未验证
- is_staff
    - true:可以访问管理站点
    - false:不可以访问管理站点
- is_superuser
    - true:是超级管理员
    - false:不是超级管理员