# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from helpers import conn, cursor
from datetime import datetime
from views import like_cmt

mod = Blueprint('message', __name__, url_prefix='/message',)


@mod.route('/<int:msg_id>', methods=['GET', 'POST'])
def show(msg_id):
    user_id = session['logged_id']
    if request.method == 'GET':
        cursor.execute("SELECT * FROM message where msg_id = %s;", (msg_id,))
        m = cursor.fetchone()
        cursor.execute("SELECT * FROM comment where msg_id = %s ORDER BY c_time ASC;", (msg_id,))
        cs = cursor.fetchall()
        final_cs = []
        for c in cs:
            c = dict(c.items())
            cursor.execute("SELECT nickname FROM users where user_id = %s", (c['user_id'],))
            u = cursor.fetchone()
            c['nickname'] = u['nickname']
            cursor.execute("SELECT * FROM like_cmt where cmt_id = %s AND user_id = %s", (c['cmt_id'], user_id))
            like = cursor.fetchone()
            if like is not None:
                like_flag = 1
            else:
                like_flag = 0
            c['like_flag'] = like_flag
            c['like_num'] = like_cmt.countlike(c['cmt_id'])
            final_cs.append(c)
    return render_template('message/show.html', m=m, cs=final_cs, user_id=user_id)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if content == "":
            flash('Do not send null ', 'warning')
        else:
            cursor.execute("INSERT INTO message(user_id,content,c_time) VALUES(%s,%s,%s);", (user_id, content, c_time))
            conn.commit()
    return redirect(url_for('show_entries'))


@mod.route('/edit/<int:msg_id>', methods=['GET', 'POST'])
def edit(msg_id):
    m = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM message where msg_id = %s;", (msg_id,))
        m = cursor.fetchone()
        return render_template('message/edit.html', m=m, msg_id=msg_id)

    if request.method == 'POST':
        cursor.execute("SELECT user_id FROM message where msg_id = %s;", (msg_id,))
        if cursor.fetchone()['user_id'] == session['logged_id']:
            content = request.form['content']
            cursor.execute("UPDATE message SET content = %s where msg_id = %s;", (content, msg_id))
            conn.commit()
            flash('Edit Success!', 'success')
        else:
            flash("You are not the owner of this message! You can't edit it.", 'warning')
        return redirect(url_for('show_entries'))

    return render_template('message/edit.html', m=m, msg_id=msg_id)


@mod.route('/delete/<int:msg_id>', methods=['GET', 'POST'])
def delete(msg_id):
    if request.method == 'GET':
        cursor.execute("SELECT user_id FROM message where msg_id = %s;", (msg_id,))
        if cursor.fetchone()['user_id'] == session['logged_id']:
            cursor.execute("DELETE FROM message where msg_id = %s;", (msg_id,))
            conn.commit()
            flash('Delete Success!', 'success')
        else:
            flash("You are not the owner of this message! You can't delete it.", 'warning')
    return redirect(url_for('show_entries'))


@mod.route('/test', methods=['GET', 'POST'])
def test():
    user_id = session['logged_id']
    cursor.execute('SELECT * FROM message where user_id = %s ORDER BY c_time DESC', (user_id,))
    m = cursor.fetchall()
    print(m)