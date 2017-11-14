# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from helpers import conn, cursor


user_id = 5
cursor.execute('SELECT * FROM message where user_id = %s ORDER BY c_time DESC', (user_id,))
m = cursor.fetchall()
messages = list(m)
for i, message in enumerate(messages):
    message = list(message)
    message.append("nickname")
    messages[i] = message
    print (message)

print (messages)