# -*- coding: utf-8 -*-
from database import conn, cursor

sql = "CREATE TABLE users ( " + \
      "user_id serial primary key not null, " + \
      "email text, " + \
      "password text, " + \
      "nickname text, " + \
      "c_time timestamp );"
cursor.execute(sql)
conn.commit()

sql = "CREATE TABLE message ( " + \
      "msg_id serial primary key not null, " + \
      "user_id int not null, " + \
      "content text , " + \
      "c_time timestamp , " + \
      "status integer );"
cursor.execute(sql)
conn.commit()

sql = "CREATE TABLE comment ( " + \
      "cmt_id serial primary key not null, " + \
      "msg_id int not null, " + \
      "user_id int not null, " + \
      "content text , " + \
      "c_time timestamp );"
cursor.execute(sql)
conn.commit()

sql = "CREATE TABLE like_msg ( " + \
      "like_msg_id serial primary key not null, " + \
      "msg_id int not null, " + \
      "user_id int not null, " + \
      "c_time timestamp);"
cursor.execute(sql)
conn.commit()

sql = "CREATE TABLE like_cmt ( " + \
      "like_cmt_id serial primary key not null, " + \
      "cmt_id int not null, " + \
      "user_id int not null, " + \
      "c_time timestamp);"
cursor.execute(sql)
conn.commit()
print('database updated!')