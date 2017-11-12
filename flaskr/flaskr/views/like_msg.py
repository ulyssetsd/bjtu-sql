# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime


mod = Blueprint('like_msg', __name__, url_prefix='/like_msg',)


@mod.route('/like/<int:msg_id>', methods=['GET', 'POST'])
def like(msg_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO like_msg(msg_id, user_id, c_time) VALUES(%s,%s,%s);", (msg_id, user_id, c_time))
        conn.commit()
    return redirect(url_for('show_entries'))


@mod.route('/unlike/<int:msg_id>', methods=['GET', 'POST'])
def unlike(msg_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        cursor.execute("DELETE FROM like_msg where msg_id = %s AND user_id = %s;", (msg_id, user_id))
        conn.commit()
    return redirect(url_for('show_entries'))
