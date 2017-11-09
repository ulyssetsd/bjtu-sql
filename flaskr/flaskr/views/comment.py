# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime

mod = Blueprint('comment', __name__, url_prefix='/comment',)


@mod.route('/show/<int:msg_id>', methods=['GET', 'POST'])
def show(msg_id):
    user_id = session['logged_id']
    if request.method == 'GET':
        cursor.execute("SELECT * FROM message where msg_id = %s;", (msg_id,))
        m = cursor.fetchone()
        cursor.execute("SELECT * FROM comment where msg_id = %s ORDER BY c_time ASC;", (msg_id,))
        cs = cursor.fetchall()
        if cs is None:
            cs = ()
        cs = list(cs)
        for i, comment in enumerate(cs):
            comment = list(comment)
            cursor.execute("SELECT nickname FROM users where user_id = %s", (user_id,))
            u = cursor.fetchone()
            comment.append(u[0])
            cursor.execute("SELECT * FROM like_cmt where cmt_id = %s AND user_id = %s", (comment[0], user_id))
            like = cursor.fetchone()
            if like is not None:
                like_flag = 1
            else:
                like_flag = 0
            comment.append(like_flag)
            cs[i] = comment
    return render_template('comment/show.html', m=m, cs=cs)


@mod.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        msg_id = int(request.form['msg_id'])
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO comment(msg_id,user_id,content,c_time) VALUES(%s,%s,%s,%s);", (msg_id, user_id, content, c_time))
        conn.commit()
    return redirect(url_for('comment.show', msg_id=msg_id))


@mod.route('/edit/<int:cmt_id>', methods=['GET', 'POST'])
def edit(cmt_id):
    m = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM comment where cmt_id = %s ORDER BY c_time ASC;", (cmt_id,))
        m = cursor.fetchone()
        return render_template('comment/edit.html', m=m, cmt_id=cmt_id)

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("UPDATE comment SET content = %s where cmt_id = %s;", (content, cmt_id))
        conn.commit()
        cursor.execute("SELECT msg_id FROM comment where cmt_id = %s;", (cmt_id,))
        m = cursor.fetchone()
        flash('Edit Success!', 'success')
        return redirect(url_for('comment.show', msg_id=m[0]))

    return render_template('comment/edit.html', m=m, cmt_id=cmt_id)


@mod.route('/delete/<int:cmt_id>', methods=['GET', 'POST'])
def delete(cmt_id):
    if request.method == 'GET':
        cursor.execute("SELECT msg_id FROM comment where cmt_id = %s;", (cmt_id,))
        m = cursor.fetchone()
        cursor.execute("DELETE FROM comment where cmt_id = %s;", (cmt_id,))
        conn.commit()
        flash('Delete Success!', 'success')
    return redirect(url_for('comment.show', msg_id=m[0]))