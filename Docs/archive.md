# 归档代码

- 一部分代码已经不再维护，但是仍然可以使用
- 一部分代码是管理员对于数据的操作，不在系统代码中体现

## 项目表数据更新范例

### 更新备注字段

```python
import pandas as pd

from Common.models.project import Project

df = pd.read_csv(r'D:\Coding\Python\Myopia\Libs\user\筛选-散光大于等于100.csv', encoding='utf-8', dtype={'学籍号': str})
students_number = df['学籍号'].tolist()

projects = Project.objects.filter(name__icontains='2022-温医大').prefetch_related('user', 'user__student_role')
for project in projects:
    new_remarks_json = {'popup': {'report_file_full': project.remarks_json.get('report_file_full', False)}}
    if project.user.student_role.student_number in students_number:
        new_remarks_json['popup']['astigmatism>=100'] = True
    project.remarks_json = new_remarks_json
    project.save()
```

### 更新项目表的名称

```python
from Common.models.project import Project

projects = Project.objects.filter(name__icontains='用户自采样')
for project in projects:
    project.name = '高度近视遗传风险评估采样'
Project.objects.bulk_update(projects, ['name'])
```

### 迁移文件到OSS示例

```python

from django.conf import settings

from Common.models.equipments import InformedConsent
from Common.models.project import Project
from Common.utils.alibabacloud.oss.obj import generate_obj_file_path

projects = Project.objects.filter(report_file_path__isnull=False)
for project in projects:
    obj_name_index = project.report_file_path.find(settings.RELATIVE_USER_PDF_DIR_PATH)
    project.report_file_url = generate_obj_file_path(project.report_file_path[obj_name_index:])
Project.objects.bulk_update(projects, ['report_file_url'])

informed_consents = InformedConsent.objects.filter(file_path__isnull=False)
for informed_consent in informed_consents:
    obj_name_index = informed_consent.file_path.find(settings.RELATIVE_INFORMED_CONSENT_DIR_PATH)
    informed_consent.file_url = generate_obj_file_path(informed_consent.file_path[obj_name_index:])
InformedConsent.objects.bulk_update(informed_consents, ['file_url'])
```

## 顺丰API

### 面单打印

- 目前没有这个需求，记录一下测试代码（同步版本）

```python
import base64
import json
import time
import uuid
from hashlib import md5
from urllib import parse

import requests

req_url = 'https://sfapi-sbox.sf-express.com/std/service'
partner_id = 'PXYXJUX9BKhO'
checkword = 'QH5F5FF7UyQKakYfGvgX7A6nRk34FZUJ'
# 生成uuid
request_id = uuid.uuid1()
# 获取时间戳
timestamp = str(int(time.time()))

service_code = 'COM_RECE_CLOUD_PRINT_WAYBILLS',
msg_data = {
    'templateCode': 'fm_150_standard_PXYXJUX9BKhO',
    'documents': [{
        'masterWaybillNo': 'SF7444460351755'
    }],
    'sync': True,
    'version': '2.0'
}

msg_data = json.dumps(msg_data)
text = parse.quote_plus(msg_data + timestamp + checkword)
# 先md5加密然后base64加密
m = md5()
m.update(text.encode('utf-8'))
md5_str = m.digest()
msg_digest = base64.b64encode(md5_str).decode('utf-8')
data = {
    "partnerID": partner_id,
    "requestID": request_id,
    "serviceCode": service_code,
    "timestamp": timestamp,
    "msgDigest": msg_digest,
    "msgData": msg_data}
# 发送post请求
res = requests.post(req_url, data=data, headers={
    "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"
})
res_data = json.loads(res.text)
res_data['apiResultData'] = json.loads(res_data.get('apiResultData', '{}'))

print(res_data)
file_data = res_data['apiResultData']['obj']['files'][0]
download_url = file_data['url']
token = file_data['token']

file_res = requests.get(download_url, headers={
    'X-Auth-token': token
})
with open('test.pdf', 'wb') as f:
    f.write(file_res.content)
```