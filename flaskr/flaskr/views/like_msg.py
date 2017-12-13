# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, render_template, redirect, request,\
	url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime
from requete import likeMsgCreate, likeMsgDelete

app = Flask(__name__)
mod = Blueprint('like_msg', __name__, url_prefix='/message',)

@mod.route('/like/<int:msg_id>', methods=['GET', 'POST'])
def like(msg_id):
	c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	likeMsgCreate(msg_id, session['logged_id'], c_time)
	return redirect(redirect_url())


@mod.route('/unlike/<int:msg_id>', methods=['GET', 'POST'])
def unlike(msg_id):
	likeMsgDelete(msg_id, session['logged_id'])
	return redirect(redirect_url())
