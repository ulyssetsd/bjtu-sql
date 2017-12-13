# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime
from requete import relationCreate, relationDelete, relationByFollowingIdAndFollowerId, relationGetFollowerUserByFollowingId, relationGetFollowingUserByFollowerId, userByUserId

mod = Blueprint('relation', __name__, url_prefix='/relation',)

@mod.route('/me')
def show_me():
    return redirect(url_for('relation.show', user_id=session['logged_id']))

@mod.route('/<int:user_id>')
def show(user_id):
    followers = relationGetFollowerUserByFollowingId(user_id)
    followings = relationGetFollowingUserByFollowerId(user_id)
    followings = add_informations(followings, session['logged_id'])
    followers = add_informations(followers, session['logged_id'])
    return render_template('relation/show.html', followings=followings, followers=followers)

@mod.route('/follow/<int:following_id>')
def follow(following_id):
    follower_id = session['logged_id']
    r = relationByFollowingIdAndFollowerId(following_id, follower_id)
    if r is not None:
        flash("Your already following this user", 'warning')
    elif following_id == follower_id:
        flash("Your can't follow yourself", 'warning')
    else:
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        relationCreate(following_id, follower_id, c_time)
        flash('You followed %s !' % userByUserId(following_id)['nickname'], 'success')
    return redirect(redirect_url())

@mod.route('/unfollow/<int:following_id>')
def unfollow(following_id):
    follower_id = session['logged_id']
    relationDelete(following_id, follower_id)
    flash('You unfollowed %s !' % userByUserId(following_id)['nickname'], 'success')
    return redirect(redirect_url())

def add_informations(follows, user_id):
    tmp_follows = []
    for f in follows:
        f = dict(f.items())
        f['is_followed'] = relationByFollowingIdAndFollowerId(f['user_id'], user_id) is not None
        f['is_me'] = f['user_id'] == user_id
        tmp_follows.append(f)
    return tmp_follows
