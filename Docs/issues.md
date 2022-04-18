# 问题文档

记录一些比较重要的问题

## Python模块

### weasyprint

- 52.5以上的版本需要pango 1.44+以上的版本，而centos8最高1.42，需要注意安装特定版本
    - 查看pango版本：`pango-view --version`
    - 注意poetry安装weasyprint似乎有问题，使用pip安装是正常的
