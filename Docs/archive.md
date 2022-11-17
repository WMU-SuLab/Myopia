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