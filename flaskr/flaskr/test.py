# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request,\
    url_for, session, flash
from database import conn, cursor


user_id = 5
sql = 'SELECT * FROM message where user_id = %d ORDER BY c_time DESC' \
    % (user_id)
cursor.execute(sql)
m = cursor.fetchall()
messages = list(m)
for i, message in enumerate(messages):
    message = list(message)
    message.append("nickname")
    messages[i] = message
    print (message)

print (messages)