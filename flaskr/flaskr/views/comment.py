# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime

mod = Blueprint('comment', __name__, url_prefix='/comment',)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        msg_id = int(request.form['msg_id'])
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO comment(msg_id,user_id,content,c_time) VALUES(%s,%s,%s,%s);", (msg_id, user_id, content, c_time))
        conn.commit()
    return redirect(url_for('message.show', msg_id=msg_id))


@mod.route('/edit/<int:cmt_id>', methods=['GET', 'POST'])
def edit(cmt_id):
    m = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM comment where cmt_id = %s ORDER BY c_time ASC;", (cmt_id,))
        m = cursor.fetchone()
        return render_template('comment/edit.html', m=m, cmt_id=cmt_id)

    if request.method == 'POST':
        cursor.execute("SELECT user_id FROM comment where cmt_id = %s;", (cmt_id,))
        if cursor.fetchone()['user_id'] == session['logged_id']:
            content = request.form['content']
            cursor.execute("UPDATE comment SET content = %s where cmt_id = %s;", (content, cmt_id))
            conn.commit()
            flash('Edit Success!', 'success')
        else:
            flash("You are not the owner of this comment! You can't edit it.", 'warning')
        cursor.execute("SELECT msg_id FROM comment where cmt_id = %s;", (cmt_id,))
        m = cursor.fetchone()
        return redirect(url_for('message.show', msg_id=m['msg_id']))

    return render_template('comment/edit.html', m=m, cmt_id=cmt_id)


@mod.route('/delete/<int:cmt_id>', methods=['GET', 'POST'])
def delete(cmt_id):
    if request.method == 'GET':
        cursor.execute("SELECT msg_id, user_id FROM comment where cmt_id = %s;", (cmt_id,))
        m = cursor.fetchone()
        if m['user_id'] == session['logged_id']:
            cursor.execute("DELETE FROM comment where cmt_id = %s;", (cmt_id,))
            conn.commit()
            flash('Delete Success!', 'success')
        else:
            flash("You are not the owner of this comment! You can't delete it.", 'warning')
    return redirect(url_for('message.show', msg_id=m['msg_id']))


def countcmt(msg_id):
    cursor.execute("SELECT COUNT(*) FROM comment where msg_id = %s;", (msg_id,))
    like_num = cursor.fetchone()
    return like_num[0]