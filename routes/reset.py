# import json
import uuid

import redis
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from config import (
    admin_mail,
    ip,
    domain_name,
)
from models.user import User
from models.message import send_mail
from routes import csrf_tokens

from utils import log

main = Blueprint('reset', __name__)


@main.route('/send', methods=['POST'])
def send():
    form = request.form.to_dict()
    # log('send_form', form)
    n = form['username']
    # log('reset_send', n)
    u = User.one(username=n)
    token = str(uuid.uuid4())
    csrf_tokens.set(token, u.id)
    # csrf_tokens[token] = u.id
    # log('csrf_tokens', csrf_tokens)
    send_mail(
        subject='找回密码',
        author=admin_mail,
        to=u.email,
        content='站内信通知：\n点击找回密码链接：http://www.{}/reset/view?token={}'.format(domain_name, token),
    )
    log('http://{}/reset/view?token={}'.format(domain_name, token))
    return redirect(url_for('index.index'))


@main.route('/view')
def view():
    token = request.args.get('token')
    if csrf_tokens.exists(token):
        return render_template('reset.html', token=token)
    else:
        abort(404)


@main.route('/update', methods=['POST'])
def update():
    form = request.form.to_dict()
    token = form.get('token')
    log('reset_update', csrf_tokens.keys())
    if csrf_tokens.exists(token):
        uid = csrf_tokens.get(token)
        # log('csrf_tokens_uid', uid)
        # ts = json.loads(uid)
        new_pass = form['new_pass']
        # uid = csrf_tokens[token]
        password = User.salted_password(new_pass)
        # 更改密码
        User.update(id=uid, password=password)
        # token失效（一次性）
        csrf_tokens.delete(token)
        return redirect(url_for('index.index'))
    else:
        abort(404)



