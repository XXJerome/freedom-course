#!/usr/bin/env python3
import time

from flask import Flask

import secret
import config
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.reset import main as reset_routes
from routes.setting import main as setting_routes
from routes.message import main as mail_routes

from utils import log


def count(input):
    return len(input)


def format_time(unix_timestamp):
    # enum Year():
    #     2013
    #     13
    # f = Year.2013
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    # print('fotmat_time', value)
    formatted = time.strftime(f, value)
    return formatted


def passed_time(updated_time):
    time1 = time.localtime(time.time())
    time2 = time.localtime(updated_time)
    t = dict(
        年=time1.tm_year - time2.tm_year,
        月=time1.tm_mon - time2.tm_mon,
        天=time1.tm_mday - time2.tm_mday,
        小时=time1.tm_hour - time2.tm_hour,
        分钟=time1.tm_min - time2.tm_min,
        秒=time1.tm_sec - time2.tm_sec,
    )
    # print('passed_time', t)
    for i, j in t.items():
        if j > 0:
            return '{} {}前'.format(j, i)


# XSS 防御——标签失效
def remove_script(content):
    c = str(content)
    c = c.replace('>', '&gt')
    c = c.replace('<', '&lt')
    return c


def configured_app():
    # web framework
    # web application
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # app.secret_key = secret.secret_key
    # log('configured_app', app.secret_key)

    uri = 'mysql+pymysql://root:{}@localhost/bbs?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    # 注册蓝图
    # url_prefix 可以用来给蓝图中的每个路由加一个前缀

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(reset_routes, url_prefix='/reset')
    app.register_blueprint(setting_routes, url_prefix='/setting')
    app.register_blueprint(mail_routes, url_prefix='/mail')

    app.template_filter()(count)
    app.template_filter()(format_time)
    app.template_filter()(passed_time)
    app.template_filter()(remove_script)


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
