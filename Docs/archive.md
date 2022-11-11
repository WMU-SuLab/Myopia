# 归档代码

- 一部分代码已经不再维护，但是仍然可以使用
- 一部分代码是管理员对于数据的操作，不在系统代码中体现

## 项目表数据更新范例

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