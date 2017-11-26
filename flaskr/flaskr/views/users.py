# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template, redirect, request,\
    url_for, session, flash
from datetime import datetime
from helpers import conn, cursor
from views import comment, like_msg
from requete import userByEmail, userIdByEmailPassword, userCreate, userUpdateNicknameByEmail, userUpdatePasswordByEmail
import re

app = Flask(__name__)
mod = Blueprint('users', __name__, url_prefix='/users',)

@mod.route('/me')
def show_me():
    return redirect(url_for('users.show', user_id=session['logged_id']))

@mod.route('/<int:user_id>', methods=['GET', 'POST'])
def show(user_id):
    cursor.execute("SELECT * FROM users where user_id = %s;", (user_id,))
    u = cursor.fetchone()
    u = dict(u.items())
    cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (u['user_id'], session['logged_id']))
    u['is_followed'] = cursor.fetchone() is not None
    u['is_me'] = u['user_id'] == session['logged_id']
    cursor.execute("SELECT * FROM message where user_id = %s ORDER BY c_time DESC;", (user_id,))
    ms = cursor.fetchall()
    entries = []
    for m in ms:
        m = dict(m.items())
        cursor.execute("SELECT nickname FROM users where user_id = %s", (m['user_id'],))
        m['nickname'] = cursor.fetchone()['nickname']
        cursor.execute("SELECT * FROM like_msg where msg_id = %s AND user_id = %s", (m['msg_id'], session['logged_id']))
        m['like_flag'] = cursor.fetchone() is not None
        m['is_mine'] = m['user_id'] == session['logged_id']
        m['like_num'] = like_msg.countlike(m['msg_id'])
        m['cmt_num'] = comment.countcmt(m['msg_id'])
        entries.append(m)
    ms=entries
    return render_template('users/show.html', u=u, ms=ms)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        nickname = request.form['nickname'].strip()
        password = request.form['password'].strip()
        password2 = request.form['password2'].strip()
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        email = email.lower()

        u = userByEmail(email)

        if email == "" or nickname == "" or password == "" or password2 == "":
            flash('Please input all the information', 'danger')
        elif not re.match(r'^[0-9a-zA-Z_]{0,19}@' +
                          '[0-9a-zA-Z]{1,15}\.[0-9a-zA-Z]{2,4}', email):
            flash('Please input the right email', 'danger')
        elif u is not None:
            flash('The email has already exist', 'danger')
        elif password2 != password:
            flash('The password is not repeated correctly', 'danger')
        elif len(password) < 6:
            flash('The password has at least 6 characters', 'danger')
        else:
            userCreate(email, nickname, password, c_time)
            flash('Register Success!', 'success')
            return redirect(url_for('users.login'))

    return render_template('users/register.html')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if session.get('logged_in'):
        return redirect(url_for('show_entries'))
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        email = email.lower()
        u = userByEmail(email)

        if u is None:
            flash("The user doesn\'t exsit.Please register first.", 'danger')

        else:
            u = userIdByEmailPassword(email, password)
            if u is None:
                flash("Your password is wrong.Try it again.", 'danger')
            else:
                session['logged_in'] = True
                session['logged_email'] = email
                session['logged_id'] = u['user_id']
                return redirect(url_for('show_entries'))

    return render_template('users/login.html', email=email)


@mod.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('users.login'))


@mod.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        userUpdateNicknameByEmail(request.form['nickname'], session['logged_email'])
        flash('Edit Nickname Success!', 'success')
    u = userByEmail(session['logged_email'])
    return render_template('users/edit.html', u=u)


@mod.route('/editPwd', methods=['GET', 'POST'])
def editPwd():
    if request.method == 'POST':
        oldPassword = request.form['oldPassword'].strip()
        newPassword = request.form['newPassword'].strip()
        newPassword2 = request.form['newPassword2'].strip()
        u = userIdByEmailPassword(session['logged_email'], oldPassword)

        if u is None:
            flash("Your old password is not right.", 'danger')
        elif newPassword != newPassword2:
            flash('The password is not repeated correctly', 'danger')
        elif len(newPassword) < 6:
            flash('The password has at least 6 characters', 'danger')
        else:
            password = newPassword
            userUpdatePasswordByEmail(password, session['logged_email'])
            flash('Edit Password Success!', 'success')
    u = userByEmail(session['logged_email'])
    return render_template('users/edit.html', u=u)
