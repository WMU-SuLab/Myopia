# 问题文档

记录一些比较重要的问题

## Python模块

### weasyprint

- windows安装
    - 需要安装GTK，[下载页面](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
- Linux安装
    - 需要安装pango
- 52.5以上的版本需要pango 1.44+以上的版本，而centos8最高1.42，需要注意安装特定版本
    - 查看pango版本：`pango-view --version`
- 注意poetry安装weasyprint似乎有问题，使用pip安装是正常的
  - 所以最后决定将weasyprint从poetry环境文件中删除
- 中文乱码问题
    - 原因：linux不存在对应的中文字体
    - 解决方法
        - 查看有的字体：`fc-list`
        - 查看有的中文字体：`fc-list :lang=zh`
            - 没有显示任何东西就是没有中文字体
        - 创建目录：`mkdir /usr/share/fonts/chinese`
        - 分配权限：`chmod -R 755 /usr/share/fonts/chinese`
        - 安装中文字体
            - 复制Windows系统中C:\Windows\Fonts下的字体到/usr/share/fonts/chinese下
            - 字体文件一般都是.TTF .TTC 后缀
        - 刷新缓存：`fc-cache`
        - 查看字体缓存：`fc-cache -fv`
        - 修改Linux字体配置文件：这一步不是必须的，当上面步骤走完但是没有用效果的时候可以尝试
            - 编辑字体配置文件：`vim /etc/fonts/fonts.conf`
            - 增加中文字体目录，就是刚刚创建的目录：`<dir>/usr/share/fonts/chinese</dir>`