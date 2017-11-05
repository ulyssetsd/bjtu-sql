# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime

mod = Blueprint('comment', __name__, url_prefix='/comment',)


@mod.route('/show/<int:msg_id>', methods=['GET', 'POST'])
def show(msg_id):
    if request.method == 'GET':
        sql = "SELECT * FROM message where msg_id = %d;" % (msg_id)
        cursor.execute(sql)
        m = cursor.fetchone()
        sql = "SELECT * FROM comment where msg_id = %d;" % (msg_id)
        cursor.execute(sql)
        cs = cursor.fetchall()
        if cs is None:
            cs = ()
    return render_template('comment/show.html', m=m, cs=cs)


@mod.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        msg_id = int(request.form['msg_id'])
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO comment(msg_id,user_id,content,c_time) " + \
                "VALUES(%d,%d,'%s','%s');" % (msg_id, user_id, content, c_time)
        cursor.execute(sql)
        conn.commit()
    return redirect(url_for('comment.show', msg_id=msg_id))


@mod.route('/edit/<int:cmt_id>', methods=['GET', 'POST'])
def edit(cmt_id):
    m = None
    if request.method == 'GET':
        sql = "SELECT * FROM comment where cmt_id = %d;" % (cmt_id)
        cursor.execute(sql)
        m = cursor.fetchone()
        return render_template('comment/edit.html', m=m, cmt_id=cmt_id)

    if request.method == 'POST':
        content = request.form['content']
        sql = "UPDATE comment SET content = '%s' where cmt_id = '%d';" \
            % (content, cmt_id)
        cursor.execute(sql)
        conn.commit()
        sql = "SELECT msg_id FROM comment where cmt_id = %d;" % (cmt_id)
        cursor.execute(sql)
        m = cursor.fetchone()
        flash('Edit Success!')
        return redirect(url_for('comment.show', msg_id=m[0]))

    return render_template('comment/edit.html', m=m, cmt_id=cmt_id)


@mod.route('/delete/<int:cmt_id>', methods=['GET', 'POST'])
def delete(cmt_id):
    if request.method == 'GET':
        sql = "SELECT msg_id FROM comment where cmt_id = %d;" % (cmt_id)
        cursor.execute(sql)
        m = cursor.fetchone()
        sql = "DELETE FROM comment where cmt_id = '%d';" % (cmt_id)
        cursor.execute(sql)
        conn.commit()
        flash('Delete Success!')
    return redirect(url_for('comment.show', msg_id=m[0]))