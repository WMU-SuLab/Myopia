# 需求文档

- 这是根据所需要的功能自己编写的文档

## Common

- [x] 初始化所有文档
    - [ ] 完善文档
    - [ ] 完善代码注释
- [x] 用户身份管理
    - [x] 登录注册部分
        - [x] 登录
        - [x] 注册
        - [x] 退出
        - [x] 重置密码
    - [x 用户身份认证的backend
        - [x] 完善对于验证码的支持
        - [x] 完善对于微信用户登录的支持
- [x] 节流
- [x] 响应类定义和继续划分模块
- [x] 了解微信如何认证用户
- [x] 配置服务器
    - [x] 域名
    - [x] SSL
    - [x] NGINX
    - [x] Supervisor
- [x] 研究PDM和Poetry安装环境
- [x] 导出数据脚本
- [ ] 完善导入数据脚本
- [ ] admin部分
    - [x] 用户部分
    - [ ] 其他部分

## Sample

### 谱希基因采样小程序

- [x]高度近视遗传风险评估采样小程序
- [x]TGFBI角膜营养不良基因检测采样小程序

## Screening

### 管理员Web端

- 查询
    - [ ] 输入学生学号等关键词获取各项检查数据
    - [ ] 单个样本（病案管理）：籍贯，年龄，ID号，各项指标数据（临床测量，知情同意，人遗，电子版扫描件），测序数据，分析报告，疾病标签；随访多条记录分别展示
    - [ ] 分类别查询：单位，科室，用户（区分权限），项目--样本统计信息以及单个样本数据
    - [ ] 条件查询：年龄段，性别，各类指标依次筛选排序
- 数据统计
    - 总体
        - [ ] 人数统计展示：总人数、高度近视人数、眼病人数、测序人数
    - 细化
        - [ ] 依据年龄分组，统计不同阶段近视人数、眼病人数

### 高度近视筛查小程序

- [x] 筛查相关接口

### 高度近视用户报告小程序

- [x] 弱视条件
- [x] 散光条件
- [x] 建议去的科室等
- [x] 学生身份证和班级
- [x] 报告下载
    - [x] 合并依未科技的PDF报告
    - [x] 上传OSS服务器
    - [x] 测试本地服务器发送，如果网速可以就不传OSS
    - [x] 调整相关接口逻辑
- [x] 增加知情同意书

# 搁置计划

- 筛查小程序管理员端搁置