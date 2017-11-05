# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime

mod = Blueprint('message', __name__, url_prefix='/message',)


@mod.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = session['logged_id']
        content = request.form['content']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO message(user_id,content,c_time) " + \
                "VALUES(%d,'%s','%s');" % (user_id, content, c_time)
        cursor.execute(sql)
        conn.commit()
    return redirect(url_for('show_entries'))


@mod.route('/edit/<int:msg_id>', methods=['GET', 'POST'])
def edit(msg_id):
    m = None
    if request.method == 'GET':
        sql = "SELECT * FROM message where msg_id = %d;" % (msg_id)
        cursor.execute(sql)
        m = cursor.fetchone()
        return render_template('message/edit.html', m=m, msg_id=msg_id)

    if request.method == 'POST':
        content = request.form['content']
        sql = "UPDATE message SET content = '%s' where msg_id = '%d';" \
            % (content, msg_id)
        cursor.execute(sql)
        conn.commit()
        flash('Edit Success!')
        return redirect(url_for('show_entries'))

    return render_template('message/edit.html', m=m, msg_id=msg_id)


@mod.route('/delete/<int:msg_id>', methods=['GET', 'POST'])
def delete(msg_id):
    if request.method == 'GET':
        sql = "DELETE FROM message where msg_id = '%d';" % (msg_id)
        cursor.execute(sql)
        conn.commit()
        flash('Delete Success!')
    return redirect(url_for('show_entries'))


@mod.route('/test', methods=['GET', 'POST'])
def test():
    user_id = session['logged_id']
    sql = 'SELECT * FROM message where user_id = %d ORDER BY c_time DESC' \
        % (user_id)
    cursor.execute(sql)
    m = cursor.fetchall()
    print(m)