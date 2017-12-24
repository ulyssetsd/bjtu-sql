# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
	url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime
from requete import searchGetUserResults, relationByFollowingIdAndFollowerId


mod = Blueprint('search', __name__, url_prefix='/search',)

@mod.route('/', methods=['GET', 'POST'])
def new_search():
	if not session.get('logged_in'):
		return redirect(url_for('users.login'))
	if request.method == 'POST':
		search_request = request.form['search'].strip().lower()
		if search_request == '':
			flash("You can't do an empty search", 'danger')
			return redirect(redirect_url())
		return redirect(url_for('search.results', search_request=search_request))
	return redirect(url_for('show_entries'))


@mod.route('/<string:search_request>', methods=['GET', 'POST'])
def results(search_request):
	if not session.get('logged_in'):
		return redirect(url_for('users.login'))
	search = '%' + search_request + '%'
	users = searchGetUserResults(search, session['logged_id'])
	tmp_users = []
	for u in users:
		u = dict(u.items())
		u['is_followed'] = relationByFollowingIdAndFollowerId(u['user_id'], session['logged_id']) is not None
		tmp_users.append(u)
	users = tmp_users
	return render_template('relation/search.html', users=users, search=search_request)