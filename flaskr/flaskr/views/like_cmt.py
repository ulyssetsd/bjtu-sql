# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime


mod = Blueprint('like_cmt', __name__, url_prefix='/like_cmt',)


@mod.route('/like/<int:cmt_id>', methods=['GET', 'POST'])
def like(cmt_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO like_cmt(cmt_id, user_id,c_time) VALUES(%s,%s,%s);", (cmt_id, user_id, c_time))
        conn.commit()
        cursor.execute("SELECT msg_id FROM comment WHERE cmt_id = %s", (cmt_id,))
        c = cursor.fetchone()
    return redirect(url_for('comment.show', msg_id=c['msg_id']))


@mod.route('/unlike/<int:cmt_id>', methods=['GET', 'POST'])
def unlike(cmt_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        cursor.execute("DELETE FROM like_cmt where cmt_id = %s AND user_id = %s;", (cmt_id, user_id))
        conn.commit()
        cursor.execute("SELECT msg_id FROM comment WHERE cmt_id = %s", (cmt_id,))
        c = cursor.fetchone()
    return redirect(url_for('comment.show', msg_id=c['msg_id']))