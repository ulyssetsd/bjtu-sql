# -*- coding: utf-8 -*-
from database import conn, cursor

sql = "CREATE TABLE message ( " + \
      "msg_id serial primary key not null, " + \
      "user_id int not null, " + \
      "content text , " + \
      "c_time timestamp );"

sql = "CREATE TABLE comment ( " + \
      "cmt_id serial primary key not null, " + \
      "msg_id int not null, " + \
      "user_id int not null, " + \
      "content text , " + \
      "c_time timestamp );"

sql = "CREATE TABLE like_msg ( " + \
      "like_msg_id serial primary key not null, " + \
      "msg_id int not null, " + \
      "user_id int not null, " + \
      "c_time timestamp, " + \
      "state int default 1 );"
cursor.execute(sql)
conn.commit()