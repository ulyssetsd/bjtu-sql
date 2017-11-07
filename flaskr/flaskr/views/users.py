# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template, redirect, request,\
    url_for, session, flash
#from models import Users
from database import conn, cursor
from flask_bcrypt import *
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
mod = Blueprint('users', __name__, url_prefix='/users',)


@mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        error = None
        email = request.form['email'].strip()
        nickname = request.form['nickname'].strip()
        password = request.form['password'].strip()
        password2 = request.form['password2'].strip()

        email = email.lower()

        if email == "" or nickname == "" or password == "" or password2 == "":
            error = 'Please input all the information'
        elif password2 != password:
            error = 'The password is not repeated correctly'
        elif len(password) < 6:
            error = 'The password has at least 6 characters'
        elif not re.match(r'^[0-9a-zA-Z_]{0,19}@' +
                          '[0-9a-zA-Z]{1,15}\.[com,cn,net]', email):
            error = 'Please input the right email'

        cursor.execute("SELECT * FROM users where email = %s;", (email,))
        u = cursor.fetchone()

        if u is not None:
            error = 'The email has already exsit'

        if error is not None:
            return render_template('register.html', error=error)
        else:
            password = bcrypt.generate_password_hash(password)
            cursor.execute("INSERT INTO users(email,nickname,password) VALUES(%s,%s,%s);", (email, nickname, password))
            conn.commit()
            flash('Register Success!')
            return redirect(url_for('users.login'))

    return render_template('register.html')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in'):
        return redirect(url_for('show_entries'))
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        email = email.lower()

        cursor.execute("SELECT password,user_id FROM users where email = %s;", (email,))
        u = cursor.fetchone()

        if u is None:
            error = "The user doesn\'t exsit.Please register first."
        elif bcrypt.check_password_hash(u[0], password):
            session['logged_in'] = True
            session['logged_email'] = email
            session['logged_id'] = u[1]
            return redirect(url_for('show_entries'))
        else:
            error = "Your password is wrong.Try it again."

    return render_template('login.html', error=error)


@mod.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('users.login'))


@mod.route('/edit', methods=['GET', 'POST'])
def edit():
    cursor.execute("SELECT * FROM users where email = %s;", (session['logged_email'],))
    u = cursor.fetchone()
    if request.method == 'POST':
        cursor.execute("UPDATE users SET nickname = %s where email = %s", (request.form['nickname'], session['logged_email']))
        cursor.execute("SELECT * FROM users where email = %s;", (session['logged_email'],))
        u = cursor.fetchone()
        conn.commit()
        flash('Edit Nickname Success!')
    return render_template('users/edit.html', u=u)


@mod.route('/editPwd', methods=['GET', 'POST'])
def editPwd():
    cursor.execute("SELECT password FROM users where email = %s;", (session['logged_email'],))
    u = cursor.fetchone()
    error = None
    if request.method == 'POST':
        oldPassword = request.form['oldPassword'].strip()
        newPassword = request.form['newPassword'].strip()
        newPassword2 = request.form['newPassword2'].strip()
        if not bcrypt.check_password_hash(u[0], oldPassword):
            error = 'Your old password is not right.'
        elif newPassword != newPassword2:
            error = 'The password is not repeated correctly'
        elif len(newPassword) < 6:
            error = 'The password has at least 6 characters'
        else:
            password = bcrypt.generate_password_hash(newPassword)
            cursor.execute("UPDATE users SET password = %s where email = %s" , (password, session['logged_email']))
            conn.commit()
            flash('Edit Password Success!')
    return render_template('users/edit.html', u=u, error=error)
