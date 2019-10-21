from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
)

from models.user import User
from routes.index import current_user
from utils import log

main = Blueprint('setting', __name__)


@main.route('/')
def setting():
    u = current_user()
    if u is None:
        redirect(url_for('index.index'))
    else:
        # token = new_csrf_token()
        # return render_template('setting.html', user=u, csrf=token)
        return render_template('setting.html', user=u)


@main.route("/update_message", methods=["POST"])
# @csrf_required
def update_message():
    form = request.form.to_dict()
    u = current_user()
    u.update(id=u.id, **form)
    return redirect(url_for('.setting'))


@main.route("/update_password", methods=["POST"])
def update_password():
    form = request.form.to_dict()
    # log('user_update', form)
    u = current_user()
    # 如果输入的当前密码正确，则更改密码
    p = User.salted_password(form['old_pass'])
    if p == u.password:
        salted_pass = User.salted_password(form['new_pass'])
        User.update(id=u.id, password=salted_pass)
    # log('user_update12312', u)
    return redirect(url_for('.setting'))
