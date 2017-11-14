# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
	url_for, session, flash
from database import conn, cursor
from datetime import datetime


mod = Blueprint('search', __name__, url_prefix='/search',)

@mod.route('/', methods=['GET', 'POST'])
def results():
	user_id = session['logged_id']
	users = {}
	search_request = ''
	if request.method == 'POST':
		search_request = request.form['search'].strip().lower()
	search = '%' + search_request + '%'
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
	return render_template('relation/search.html', users=users, search=search_request)