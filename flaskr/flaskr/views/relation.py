# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor
from datetime import datetime


mod = Blueprint('relation', __name__, url_prefix='/relation',)

@mod.route('/')
def list():
    user_id = session['logged_id']
    cursor.execute("SELECT * FROM relation, users WHERE user_id = follower_id AND following_id = %s;", (user_id,))
    followers = cursor.fetchall()
    cursor.execute("SELECT * FROM relation, users WHERE user_id = following_id AND follower_id = %s;", (user_id,))
    followings = cursor.fetchall()
    tmp_followers = []
    for f in followers:
        f = dict(f.items())
        cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (f['user_id'], user_id))
        if cursor.fetchone() is None:
            f['is_followed'] = False
        else:
            f['is_followed'] = True
        tmp_followers.append(f)
    followers = tmp_followers
    return render_template('relation/show.html', followings=followings, followers=followers)

@mod.route('/search', methods=['GET', 'POST'])
def search():
    user_id = session['logged_id']
    users = {}
    if request.method == 'POST':
        search = '%' + request.form['search'].strip().lower() + '%'
        cursor.execute("SELECT * FROM users WHERE (nickname LIKE %s OR email LIKE %s) \
            AND user_id != %s;", (search, search, user_id))
        users = cursor.fetchall()
        tmp_users = []
        for u in users:
            u = dict(u.items())
            cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (u['user_id'], user_id))
            if cursor.fetchone() is None:
                u['is_followed'] = False
            else:
                u['is_followed'] = True
            tmp_users.append(u)
        users = tmp_users
    return render_template('relation/search.html', users=users)

@mod.route('/follow/<int:following_id>')
def like(following_id):
    follower_id = session['logged_id']
    cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (following_id, follower_id))
    if cursor.fetchone() is None and following_id != follower_id:
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO relation(following_id, follower_id, c_time) VALUES(%s,%s,%s);", (following_id, follower_id, c_time))
        conn.commit()
    return redirect(url_for('relation.list'))


@mod.route('/unfollow/<int:following_id>')
def unlike(following_id):
    follower_id = session['logged_id']
    cursor.execute("DELETE FROM relation where following_id = %s AND follower_id = %s;", (following_id, follower_id))
    conn.commit()
    return redirect(url_for('relation.list'))