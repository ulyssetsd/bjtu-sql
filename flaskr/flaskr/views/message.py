# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime
from requete import messageById, messageCreate, messageDeleteById, messageUpdateContentById, commentByMsgIdOrder, userByUserId, likeCmtGetOne, likeCmtCountLike

mod = Blueprint('message', __name__, url_prefix='/message',)


@mod.route('/<int:msg_id>', methods=['GET', 'POST'])
def show(msg_id):
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        m = messageById(msg_id)
        cs = commentByMsgIdOrder(msg_id)
        final_cs = []
        for c in cs:
            c = dict(c.items())
            c['nickname'] = userByUserId(c['user_id'])['nickname']
            c['like_flag'] = likeCmtGetOne(c['cmt_id'], session['logged_id']) is not None
            c['like_num'] = likeCmtCountLike(c['cmt_id'])
            final_cs.append(c)
    return render_template('message/show.html', m=m, cs=final_cs, user_id=session['logged_id'])

@mod.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    if request.method == 'POST':
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if content == "":
            flash('Do not send null ', 'warning')
        else:
            messageCreate(user_id, content, c_time)
    return redirect(url_for('show_entries'))


@mod.route('/edit/<int:msg_id>', methods=['GET', 'POST'])
def edit(msg_id):
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    m = messageById(msg_id)
    if request.method == 'POST':
        if m['user_id'] == session['logged_id']:
            content = request.form['content']
            messageUpdateContentById(content, msg_id)
            flash('Edit Success!', 'success')
        else:
            flash("You are not the owner of this message! You can't edit it.", 'warning')
        return redirect(url_for('show_entries'))

    return render_template('message/edit.html', m=m, msg_id=msg_id)


@mod.route('/delete/<int:msg_id>', methods=['GET', 'POST'])
def delete(msg_id):
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    m = messageById(msg_id)
    if request.method == 'GET':
        if m['user_id'] == session['logged_id']:
            messageDeleteById(msg_id)
            flash('Delete Success!', 'success')
        else:
            flash("You are not the owner of this message! You can't delete it.", 'warning')
    return redirect(url_for('show_entries'))
