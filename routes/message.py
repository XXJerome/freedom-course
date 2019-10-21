from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages

main = Blueprint('mail', __name__)


@main.route('/')
def index():
    u = current_user()

    send = Messages.all(sender_id=u.id)
    received = Messages.all(receiver_id=u.id)

    t = render_template(
        'mail/index.html',
        send=send,
        received=received,
    )
    return t


@main.route('/detail/<int:id>')
def detail(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [message.receiver_id, message.sender_id]:
        return render_template('mail/detail.html', message=message, user=u)
    else:
        return redirect(url_for('.index'))


@main.route('/received_mail')
def view():
    u = current_user()
    messages = Messages.all(receiver_id=u.id)
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    # if u.id in [message.receiver_id, message.sender_id]:
    return render_template('mail/receive_mail.html', messages=messages, user=u)
    # else:
    #     return redirect(url_for('.index'))


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    log('message_add', form, request.form)
    u = current_user()
    receiver_id = int(form['receiver_id'])
    # 发邮件
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver_id
    )

    return redirect(url_for('.index'))


@main.route("/delete", methods=["POST"])
def delete():
    # 批量删除
    ms_id = request.form.getlist('id')
    log('mail form_delete', ms_id)
    for m_id in ms_id:
        m_id = int(m_id)
        Messages.delete(id=m_id)
    return redirect(url_for('.view'))
