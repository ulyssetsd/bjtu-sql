# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from helpers import conn, cursor, redirect_url
from datetime import datetime
from requete import likeCmtCreate, likeCmtDelete

mod = Blueprint('like_cmt', __name__, url_prefix='/like_cmt',)


@mod.route('/like/<int:cmt_id>', methods=['GET', 'POST'])
def like(cmt_id):
    if request.method == 'GET':
        c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        likeCmtCreate(cmt_id, session['logged_id'], c_time)
    return redirect(redirect_url())


@mod.route('/unlike/<int:cmt_id>', methods=['GET', 'POST'])
def unlike(cmt_id):
    if request.method == 'GET':
        likeCmtDelete(cmt_id, session['logged_id'])
    return redirect(redirect_url())
