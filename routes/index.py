import os
import uuid
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory,
)
from werkzeug.datastructures import FileStorage
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, session
import redis
import json
from utils import log

main = Blueprint('index', __name__)

cache = redis.StrictRedis()

@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register/view")
def register_view():
    return render_template("register.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


# @main.route("/login/view")
# def register_view():
#     return render_template("login_view.html")


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        # session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        # session.permanent = True
        # 转到 topic.index 页面
        session_id = str(uuid.uuid4())
        # log('login_index', session_id)
        session.set(session_id, u.id)
        r = redirect(url_for('topic.index'))
        make_response(r).set_cookie('session_id', session_id)
        return r


def created_topic(user_id):
    # O(n)
    # ts = Topic.all(user_id=user_id)
    # return ts

    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    # O(k)+O(m*n)
    # rs = Reply.all(user_id=user_id)
    # ts = []
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     ts.append(t)
    # return ts

    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.one(id=r.topic_id)
            ts.append(t)

        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)

        return ts


# def created_topic(user_id):
#     created = Topic.all(user_id=user_id)
#     created.sort(key=lambda k: k.created_time, reverse=True)
#     return created
#
#
# def replied_topic(user_id):
#     replied = []
#     for r in Reply.all(user_id=user_id):
#         t = Topic.one(id=r.topic_id)
#         if t not in replied and t is not None:
#             replied.append(t)
#     replied.sort(key=lambda k: k.updated_time, reverse=True)
#     return replied


# def newest_reply(topics):
#     r = []
#     for i in topics:
#         replies = i.replies()
#         replies.sort(key=lambda k: k.created_time, reverse=True)
#         # 选择最新的回复
#         r.append(replies[0])
#     return r


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        abort(404)
    else:
        return redirect(url_for('.user_detail', id=u.id))


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        return redirect(url_for('.index'))
    else:
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'profile.html',
            user=u,
            created_topic=created,
            replied_topic=replied,
        )


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    # filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 直接拼接路由不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)


# @main.route('/reset/view')
# def reset_send():
#     if



