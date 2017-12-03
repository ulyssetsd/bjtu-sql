from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

from helpers import conn, cursor
from datetime import datetime

def userGetAll():
	cursor.execute("SELECT * FROM users")
	users = cursor.fetchall()
	return users

def userIdByEmailPassword(email, password):
	cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (email, password,))
	u = cursor.fetchone()
	if u is None:
		return None
	return u

def userByEmail(email):
	cursor.execute("SELECT * FROM users where email = %s;", (email,))
	u = cursor.fetchone()
	return u

def userByNickname(nickname):
	cursor.execute("SELECT * FROM users where nickname = %s;", (nickname,))
	u = cursor.fetchone()
	return u

def userCreate(email, nickname, password, c_time):
	cursor.execute("INSERT INTO users(email,nickname,password,c_time) VALUES(%s,%s,crypt(%s, gen_salt('bf', 8)), %s);", (email, nickname, password, c_time))
	conn.commit()

def userDelete(email):
	cursor.execute("DELETE FROM users WHERE email = %s;", (email,))
	conn.commit()

def userUpdateNicknameByEmail(nickname, email):
	cursor.execute("UPDATE users SET nickname = %s where email = %s", (nickname, email,))
	conn.commit()

def userUpdatePasswordByEmail(password, email):
	cursor.execute("UPDATE users SET password = crypt(%s, gen_salt('bf', 8)) where email = %s", (password, email,))
	conn.commit()




def messageGetAll():
	cursor.execute('SELECT * FROM message')
	message = cursor.fetchall()
	return message

def messageCreate(user_id, content, c_time):
	cursor.execute("INSERT INTO message(user_id,content,c_time) VALUES(%s,%s,%s);", (user_id, content, c_time,))
	conn.commit()

def messageDeleteByUserId(user_id):
	cursor.execute("DELETE FROM message where user_id = %s;", (user_id,))
	conn.commit()

def messageGetAllFromUserIdOrder(user_id):
	cursor.execute('SELECT * FROM message where user_id = %s ORDER BY c_time DESC', (user_id,))
	m = cursor.fetchall()
	return m

def messageDeleteById(msg_id):
	cursor.execute("DELETE FROM message where msg_id = %s;", (msg_id,))
	conn.commit()

def messageById(msg_id):
	cursor.execute("SELECT * FROM message where msg_id = %s;", (msg_id,))
	m = cursor.fetchone()
	return m

def messageGetAllFromUserId(user_id):
	cursor.execute('SELECT * FROM message WHERE user_id = %s;', (user_id,))
	message = cursor.fetchall()
	return message

def messageUpdateContentById(content, msg_id):
	cursor.execute("UPDATE message SET content = %s where msg_id = %s;", (content, msg_id,))
	conn.commit()

def messageCount():
	cursor.execute("SELECT COUNT(*) AS count FROM message")
	nb = cursor.fetchone()
	if nb is None:
		return 0
	return nb['count']




def commentCreate(msg_id, user_id, content, c_time):
	cursor.execute("INSERT INTO comment(msg_id,user_id,content,c_time) VALUES(%s,%s,%s,%s);", (msg_id, user_id, content, c_time))
	conn.commit()

def commentUpdateById(content, cmt_id):
	cursor.execute("UPDATE comment SET content = %s where cmt_id = %s;", (content, cmt_id))
	conn.commit()

def commentDeleteById(cmt_id):
	cursor.execute("DELETE FROM comment where cmt_id = %s;", (cmt_id,))
	conn.commit()

def commentCount():
	cursor.execute("SELECT COUNT(*) AS count FROM comment")
	nb = cursor.fetchone()
	if nb is None:
		return 0
	return nb['count']




def likeCommentCreate(cmt_id, user_id, c_time):
	cursor.execute("INSERT INTO like_cmt(cmt_id, user_id,c_time) VALUES(%s,%s,%s);", (cmt_id, user_id, c_time))
	conn.commit()

def likeCommentDelete(cmt_id, user_id):
	cursor.execute("DELETE FROM like_cmt where cmt_id = %s AND user_id = %s;", (cmt_id, user_id))
	conn.commit()

def likeCommentCount():
	cursor.execute("SELECT COUNT(*) AS count FROM like_cmt")
	nb = cursor.fetchone()
	if nb is None:
		return 0
	return nb['count']

def likeMsgGetAll():
	cursor.execute('SELECT * FROM like_msg')
	message = cursor.fetchall()
	return message

def likeMsgCreate(msg_id, user_id, c_time):
	cursor.execute("INSERT INTO like_msg(msg_id, user_id,c_time) VALUES(%s,%s,%s);", (msg_id, user_id, c_time,))
	conn.commit()

def likeMsgDelete(msg_id, user_id):
	cursor.execute("DELETE FROM like_msg where msg_id = %s AND user_id = %s;", (msg_id, user_id,))
	conn.commit()

def likeMsgCount():
	cursor.execute("SELECT COUNT(*) AS count FROM like_msg")
	nb = cursor.fetchone()
	if nb is None:
		return 0
	return nb['count']

def followUser(following_id, follower_id):
	cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (following_id, follower_id))
	if cursor.fetchone() is None and following_id != follower_id:
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		cursor.execute("INSERT INTO relation(following_id, follower_id, c_time) VALUES(%s,%s,%s);", (following_id, follower_id, c_time))
		conn.commit()
		cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
	return ""

def unfollowUser(following_id, follower_id):
	cursor.execute("DELETE FROM relation where following_id = %s AND follower_id = %s;", (following_id, follower_id))
	conn.commit()
	cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
	return ""