# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime

def redirect_url(): # function for going to the previous page (didn't work with POST page)
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

app = Flask(__name__)
mod = Blueprint('like_msg', __name__, url_prefix='/message',)

@mod.route('/like/<int:msg_id>', methods=['GET', 'POST'])
def like(msg_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO like_msg(msg_id, user_id, c_time) VALUES(%s,%s,%s);", (msg_id, user_id, c_time))
        conn.commit()
    return redirect(redirect_url())


@mod.route('/unlike/<int:msg_id>', methods=['GET', 'POST'])
def unlike(msg_id):
    if request.method == 'GET':
        user_id = session['logged_id']
        cursor.execute("DELETE FROM like_msg where msg_id = %s AND user_id = %s;", (msg_id, user_id))
        conn.commit()
    return redirect(redirect_url())


def countlike(msg_id):
    cursor.execute("SELECT COUNT(*) FROM like_msg where msg_id = %s;", (msg_id,))
    like_num = cursor.fetchone()
    return like_num[0]
