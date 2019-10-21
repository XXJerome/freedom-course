## 基于 Flask 框架的论坛

**主要功能**

技术栈：Python + Flask + MySQL + Linux/Ubuntu + Redis + Nginx + Gunicorn
1.实现了注册登录，密码找回，话题发布和评论回复，板块管理，用户信息更改，论坛私信和邮件发送等功能
2.实现了基于 MySQL 和 SQLAlchemy 常见操作封装定制 ORM 框架，便于快速开发
3.使用 Jinja2 模板继承减少重复性网页布置，JavaScript 实现 Markdown
4.使用 Nginx 反向代理，提升访问速度，配置 Gunicorn 多 worker 和 gevent 达到多进程负载均衡，Supervisor 管理进程
5.使用 Redis 解决多进程数据共享问题
6.针对 XSRF 和 XSS 攻击分别采取 CSRF token 和转义的防御措施

**运行**

1. cd /var/www
2. git clone git@github.com:XXJerome/bbs.git
4. cd /var/www/bbs
3. bash deploy.sh

**注意事项**

- 自行添加 secret.py(database_password,secret_key,mail_password) 
- 修改 config.py

## 演示
**站内信**

![](https://github.com/XXJerome/http-server-and-MVC-web-frame/blob/master/images/message.gif)

**个人信息**

![](https://github.com/XXJerome/http-server-and-MVC-web-frame/blob/master/images/personal_message.gif)

**帖子模块**

![](https://github.com/XXJerome/http-server-and-MVC-web-frame/blob/master/images/topic.gif)

