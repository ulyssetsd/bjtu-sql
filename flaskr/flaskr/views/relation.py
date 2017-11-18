# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime

mod = Blueprint('relation', __name__, url_prefix='/relation',)

def add_informations(follows, user_id):
    tmp_follows = []
    for f in follows:
        f = dict(f.items())
        cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (f['user_id'], user_id))
        f['is_followed'] = cursor.fetchone() is not None
        f['is_me'] = f['user_id'] == user_id
        tmp_follows.append(f)
    return tmp_follows

@mod.route('/me')
def show_me():
    return redirect(url_for('relation.show', user_id=session['logged_id']))

@mod.route('/<int:user_id>')
def show(user_id):
    cursor.execute("SELECT * FROM relation, users WHERE user_id = follower_id AND following_id = %s;", (user_id,))
    followers = cursor.fetchall()
    cursor.execute("SELECT * FROM relation, users WHERE user_id = following_id AND follower_id = %s;", (user_id,))
    followings = cursor.fetchall()
    followings = add_informations(followings, session['logged_id'])
    followers = add_informations(followers, session['logged_id'])
    return render_template('relation/show.html', followings=followings, followers=followers)

@mod.route('/follow/<int:following_id>')
def follow(following_id):
    follower_id = session['logged_id']
    cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (following_id, follower_id))
    if cursor.fetchone() is None and following_id != follower_id:
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO relation(following_id, follower_id, c_time) VALUES(%s,%s,%s);", (following_id, follower_id, c_time))
        conn.commit()
        cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
        flash('You followed %s !' % cursor.fetchone()['nickname'], 'success')
    return redirect(redirect_url())

@mod.route('/unfollow/<int:following_id>')
def unfollow(following_id):
    follower_id = session['logged_id']
    cursor.execute("DELETE FROM relation where following_id = %s AND follower_id = %s;", (following_id, follower_id))
    conn.commit()
    cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
    flash('You unfollowed %s !' % cursor.fetchone()['nickname'], 'success')
    return redirect(redirect_url())
