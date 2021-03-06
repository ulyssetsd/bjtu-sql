# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from helpers import conn, cursor
from datetime import datetime
from requete import commentCreate, commentByCmtId, commentUpdateById, commentDeleteById

mod = Blueprint('comment', __name__, url_prefix='/comment',)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    if request.method == 'POST':
        msg_id = int(request.form['msg_id'])
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if content == "":
            flash('Do not send null ', 'warning')
        else:
            commentCreate(msg_id, user_id, content, c_time)
    return redirect(url_for('message.show', msg_id=msg_id))


@mod.route('/edit/<int:cmt_id>', methods=['GET', 'POST'])
def edit(cmt_id):
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    m = None
    if request.method == 'GET':
        m = commentByCmtId(cmt_id)
        return render_template('comment/edit.html', m=m, cmt_id=cmt_id)

    if request.method == 'POST':
        m = commentByCmtId(cmt_id)
        if m['user_id'] == session['logged_id']:
            content = request.form['content']
            commentUpdateById(content, cmt_id)
            flash('Edit Success!', 'success')
        else:
            flash("You are not the owner of this comment! You can't edit it.", 'warning')
        return redirect(url_for('message.show', msg_id=m['msg_id']))

    return render_template('comment/edit.html', m=m, cmt_id=cmt_id)


@mod.route('/delete/<int:cmt_id>', methods=['GET', 'POST'])
def delete(cmt_id):
    if not session.get('logged_in'):
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        m = commentByCmtId(cmt_id)
        if m['user_id'] == session['logged_id']:
            commentDeleteById(cmt_id)
            flash('Delete Success!', 'success')
        else:
            flash("You are not the owner of this comment! You can't delete it.", 'warning')
    return redirect(url_for('message.show', msg_id=m['msg_id']))


def countcmt(msg_id):
    cursor.execute("SELECT COUNT(*) FROM comment where msg_id = %s;", (msg_id,))
    like_num = cursor.fetchone()
    return like_num[0]