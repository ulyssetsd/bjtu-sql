# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template, redirect, request,\
    url_for, session, flash
from datetime import datetime
from helpers import conn, cursor
from views import comment, like_msg
from requete import userByEmail, userByNickname, userIdByEmailPassword, userCreate, userUpdateNicknameByEmail, userUpdatePasswordByEmail, userByUserId, messageGetAllFromUserIdOrder, CommentCountCmt, likeMsgCountLike, relationByFollowingIdAndFollowerId, likeMsgGetOne
import re

app = Flask(__name__)
mod = Blueprint('users', __name__, url_prefix='/users',)

@mod.route('/me')
def show_me():
    return redirect(url_for('users.show', user_id=session['logged_id']))

@mod.route('/<int:user_id>', methods=['GET', 'POST'])
def show(user_id):
    u = userByUserId(user_id)
    u = dict(u.items())
    u['is_followed'] = relationByFollowingIdAndFollowerId(u['user_id'], session['logged_id']) is not None
    u['is_me'] = u['user_id'] == session['logged_id']
    ms = messageGetAllFromUserIdOrder(user_id)
    entries = []
    for m in ms:
        m = dict(m.items())
        m['nickname'] = userByUserId(m['user_id'])['nickname']
        m['like_flag'] = likeMsgGetOne(m['msg_id'], session['logged_id']) is not None
        m['is_mine'] = m['user_id'] == session['logged_id']
        m['like_num'] = likeMsgCountLike(m['msg_id'])
        m['cmt_num'] = CommentCountCmt(m['msg_id'])
        entries.append(m)
    ms=entries
    return render_template('users/show.html', u=u, ms=ms)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        nickname = request.form['nickname'].strip()
        password = request.form['password'].strip()
        password2 = request.form['password2'].strip()
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        uByEmail = userByEmail(email)
        uByNickname = userByNickname(nickname)

        ret = registerRequest(email, nickname, password, password2, uByEmail, uByNickname)
        if ret != 'Register Success!':
            flash(ret, 'danger')
        else:
            userCreate(email, nickname, password, c_time)
            flash('Register Success!', 'success')
            return redirect(url_for('users.login'))

        # if email == "" or nickname == "" or password == "" or password2 == "":
        #     flash('Please input all the information', 'danger')
        # elif not re.match(r'^[0-9a-zA-Z_]{0,19}@' +
        #                   '[0-9a-zA-Z]{1,15}\.[0-9a-zA-Z]{2,4}', email):
        #     flash('Please input the right email', 'danger')
        # elif uByEmail is not None:
        #     flash('The email already exist', 'danger')
        # elif uByNickname is not None:
        #     flash('The nickname already exist', 'danger')
        # elif password2 != password:
        #     flash('The password is not repeated correctly', 'danger')
        # elif len(password) < 6:
        #     flash('The password should be at least 6 characters', 'danger')
        # else:
        #     userCreate(email, nickname, password, c_time)
        #     flash('Register Success!', 'success')
        #     return redirect(url_for('users.login'))


    return render_template('users/register.html')

@mod.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if session.get('logged_in'):
        return redirect(url_for('show_entries'))
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        if email == "" or password == "":
            flash('Please input all the information', 'danger')
        else:
            rep = loginRequest(email, password)
            if rep != "Login Success!":
                flash(rep, 'danger')
            else:
                u = userIdByEmailPassword(email, password)
                session['logged_in'] = True
                session['logged_email'] = email
                session['logged_id'] = u['user_id']
                return redirect(url_for('show_entries'))

        # u = userByEmail(email)

        # if u is None:
        #     flash("The user doesn\'t exsit.Please register first.", 'danger')

        # else:
        #     u = userIdByEmailPassword(email, password)
        #     if u is None:
        #         flash("Your password is wrong.Try it again.", 'danger')
        #     else:
        #         session['logged_in'] = True
        #         session['logged_email'] = email
        #         session['logged_id'] = u['user_id']
        #         return redirect(url_for('show_entries'))

    return render_template('users/login.html', email=email)


@mod.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('users.login'))


@mod.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        newNickname = request.form['nickname']
        uByNickname = userByNickname(request.form['nickname'])
        rep = editNicknameRequest(uByNickname, newNickname)
        if rep != "Edit Nickname Success!":
            flash(rep, "danger")
        else:
            userUpdateNicknameByEmail(request.form['nickname'], session['logged_email'])
            flash('Edit Nickname Success!', 'success')
        # if newNickname == "":
        #     flash('The nickname can not be null', 'danger')
        # elif uByNickname is not None:
        #     flash('The nickname already exist', 'danger')
        # else:
        #     userUpdateNicknameByEmail(request.form['nickname'], session['logged_email'])
        #     flash('Edit Nickname Success!', 'success')
    u = userByEmail(session['logged_email'])
    return render_template('users/edit.html', u=u)


@mod.route('/editPwd', methods=['GET', 'POST'])
def editPwd():
    if request.method == 'POST':
        oldPassword = request.form['oldPassword'].strip()
        newPassword = request.form['newPassword'].strip()
        newPassword2 = request.form['newPassword2'].strip()
        u = userIdByEmailPassword(session['logged_email'], oldPassword)

        rep = editPasswordRequest(u, newPassword, newPassword2)
        if rep != "Edit Password Success!":
            flash(rep, "danger")
        else:
            password = newPassword
            userUpdatePasswordByEmail(password, session['logged_email'])
            flash('Edit Password Success!', 'success')

        # if u is None:
        #     flash("Your old password is not right.", 'danger')
        # elif newPassword != newPassword2:
        #     flash('The password is not repeated correctly', 'danger')
        # elif len(newPassword) < 6:
        #     flash('The password should be at least 6 characters', 'danger')
        # else:
        #     password = newPassword
        #     userUpdatePasswordByEmail(password, session['logged_email'])
        #     flash('Edit Password Success!', 'success')

    u = userByEmail(session['logged_email'])
    return render_template('users/edit.html', u=u)

def editNicknameRequest(uByNickname, newNickname):
    if newNickname == "":
        return 'The nickname can not be null'
    elif uByNickname is not None:
        return 'The nickname already exist'
    else:
        return 'Edit Nickname Success!'

def editPasswordRequest(u, newPassword, newPassword2):
    if u is None:
        return "Your old password is not right."
    elif newPassword != newPassword2:
        return 'The password is not repeated correctly'
    elif len(newPassword) < 6:
        return 'The password should be at least 6 characters'
    else:
        return "Edit Password Success!"


def loginRequest(email, password):
    u = userByEmail(email)

    if u is None:
        return "The user doesn\'t exist. Please register first."
    else:
        u = userIdByEmailPassword(email, password)
        if u is None:
            return "Your password is wrong. Try it again."
        else:
            return "Login Success!"

def registerRequest(email, nickname, password, password2, uByEmail, uByNickname):
    if email == "" or nickname == "" or password == "" or password2 == "":
        return 'Please input all the information'
    elif not re.match(r'^[0-9a-zA-Z_]{0,19}@' + '[0-9a-zA-Z]{1,15}\.[0-9a-zA-Z]{2,4}', email):
        return 'Please input the right email'
    elif uByEmail is not None:
        return 'The email already exist'
    elif uByNickname is not None:
        return 'The nickname already exist'
    elif password2 != password:
        return "The password is not repeated correctly"
    elif len(password) < 6:
        return 'The password should be at least 6 characters'
    else:
        return "Register Success!"

