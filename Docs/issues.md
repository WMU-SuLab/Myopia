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
    - 注意poetry安装weasyprint 的52.5版本似乎又有问题，依赖一堆报错，但是使用pip安装虽然报错但是最后能用
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

## 服务器

### Supervisor

- 务必使用绝对路径
    - 如果使用相对路径，只有在相对路径下的文件夹下启动supervisor的时候有效，而更新、重载是无效的
    - 而且多个配置文件如果使用相同的相对路径，会全部定向到一个日志文件，这是错误的
- BACKOFF Exited too quickly (process log may have details)
    - 根目录出错
    - 日志文件目录不存在
- 无法使用source等终端命令：使用bash -c "command"
- 不断exit status 0; not expected
    - supervisor无法处理不在前台的程序，如nohup、gunicorn设置了守护进程等
    - 多次出现是因为没有监测到前台程序不断重启

### NGINX

- **巨坑**：配置文件不能使用`;`作为注释，一定要是`#`

## 数据库

### MySQL

- <span id="mysql-tzinfo">时区问题</span>
    - 出现问题：`Database returned an invalid datetime value. Are time zone definitions for your database installed`
    - 解决方法参考：https://blog.csdn.net/kq1983/article/details/109767343
        - 使用`mysql_tzinfo_to_sql`命令
            - `mysql_tzinfo_to_sql tz_dir`
                - 常用：`mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p密码 mysql`
            - `mysql_tzinfo_to_sql tz_file tz_name`
                - 常用：`mysql_tzinfo_to_sql tz_file tz_name | mysql -u root -p密码 mysql`
            - `mysql_tzinfo_to_sql --leap tz_file`
                - 常用：`mysql_tzinfo_to_sql --leap tz_file | mysql -u root -p密码 mysql`
        - 没有`mysql_tzinfo_to_sql`命令，如轻量级应用服务器安装等，直接使用sql文件
            - 下载地址：<https://dev.mysql.com/downloads/timezones.html>
                - 请注意下载与数据库对应的版本
            - 导入：`mysql -u root -p密码 mysql < 文件名称`
            - 或者使用Navicat等工具导入，非常简单
        - 最后可能需要刷新一下:`mysql -u root -p -e "flush tables;" mysql`
        - 或者重启一下：`sudo service mysql restart`