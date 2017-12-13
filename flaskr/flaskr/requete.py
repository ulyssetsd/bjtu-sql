from flask import Flask, request, session, g, redirect, url_for, abort, \
		render_template, flash

from helpers import conn, cursor
from datetime import datetime

def userGetAll():
	cursor.execute("SELECT * FROM users")
	users = cursor.fetchall()
	return users

def userDeleteAll():
	cursor.execute("truncate table users")

def userIdByEmailPassword(email, password):
	cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (email, password,))
	u = cursor.fetchone()
	if u is None:
		return None
	return u

def userByUserId(user_id):
	cursor.execute("SELECT * FROM users where user_id = %s;", (user_id,))
	u = cursor.fetchone()
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



def messageDeleteAll():
	cursor.execute("truncate table message")

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

def messageGetAllFromManyUserIdOrder(tuple_list_user_id):
	cursor.execute('SELECT * FROM message where user_id IN %s ORDER BY c_time DESC', (tuple_list_user_id,))
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


def commentGetAll():
	cursor.execute('SELECT * FROM comment')
	message = cursor.fetchall()
	return message

def commentByCmtId(cmt_id):
	cursor.execute("SELECT * FROM comment where cmt_id = %s;", (cmt_id,))
	cmt = cursor.fetchone()
	return cmt

def commentByMsgIdOrder(msg_id):
	cursor.execute("SELECT * FROM comment where msg_id = %s ORDER BY c_time ASC;", (msg_id,))
	cs = cursor.fetchall()
	return cs

def commentDeleteAll():
	cursor.execute("truncate table comment")

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

def CommentCountCmt(msg_id):
		cursor.execute("SELECT COUNT(*) AS count FROM comment where msg_id = %s;", (msg_id,))
		like_num = cursor.fetchone()
		return like_num['count']




def likeCmtDeleteAll():
	cursor.execute("truncate table like_cmt")

def likeCmtCreate(cmt_id, user_id, c_time):
	cursor.execute("INSERT INTO like_cmt(cmt_id, user_id,c_time) VALUES(%s,%s,%s);", (cmt_id, user_id, c_time))
	conn.commit()

def likeCmtDelete(cmt_id, user_id):
	cursor.execute("DELETE FROM like_cmt where cmt_id = %s AND user_id = %s;", (cmt_id, user_id))
	conn.commit()

def likeCmtGetOne(cmt_id, user_id):
	cursor.execute("SELECT * FROM like_cmt where cmt_id = %s AND user_id = %s", (cmt_id, user_id))
	like = cursor.fetchone()
	return like

def likeCmtCount():
	cursor.execute("SELECT COUNT(*) AS count FROM like_cmt")
	nb = cursor.fetchone()
	if nb is None:
		return 0
	return nb['count']

def likeCmtCountLike(cmt_id):
		cursor.execute("SELECT COUNT(*) AS count FROM like_cmt where cmt_id = %s;", (cmt_id,))
		like_num = cursor.fetchone()
		return like_num['count']





def likeMsgDeleteAll():
	cursor.execute("truncate table like_msg")

def likeMsgGetAll():
	cursor.execute('SELECT * FROM like_msg')
	message = cursor.fetchall()
	return message

def likeMsgGetOne(msg_id, user_id):
	cursor.execute("SELECT * FROM like_msg where msg_id = %s AND user_id = %s", (msg_id, user_id))
	like = cursor.fetchone()
	return like

def likeMsgCreate(msg_id, user_id, c_time):
	cursor.execute("INSERT INTO like_msg(msg_id, user_id, c_time) VALUES(%s,%s,%s);", (msg_id, user_id, c_time,))
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

def likeMsgCountLike(msg_id):
	cursor.execute("SELECT COUNT(*) AS count FROM like_msg where msg_id = %s;", (msg_id,))
	like_num = cursor.fetchone()
	return like_num['count']


def relationCreate(following_id, follower_id, c_time):
	cursor.execute("INSERT INTO relation(following_id, follower_id, c_time) VALUES(%s,%s,%s);", (following_id, follower_id, c_time))
	conn.commit()

def relationDelete(following_id, follower_id):
	cursor.execute("DELETE FROM relation where following_id = %s AND follower_id = %s;", (following_id, follower_id))
	conn.commit()

def relationByFollowingIdAndFollowerId(following_id, follower_id):
	cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (following_id, follower_id,))
	r = cursor.fetchone()
	return r

def relationByFollowerId(follower_id):
	cursor.execute('SELECT * FROM relation where follower_id = %s', (follower_id,))
	rs = cursor.fetchall()
	return rs

def relationGetFollowerUserByFollowingId(following_id):
	cursor.execute("SELECT * FROM relation, users WHERE user_id = follower_id AND following_id = %s;", (following_id,))
	followers = cursor.fetchall()
	return followers

def relationGetFollowingUserByFollowerId(follower_id):
	cursor.execute("SELECT * FROM relation, users WHERE user_id = following_id AND follower_id = %s;", (follower_id,))
	followings = cursor.fetchall()
	return followings


def searchGetUserResults(search, user_id):
	cursor.execute("SELECT * FROM users WHERE (nickname LIKE %s OR email LIKE %s) AND user_id != %s;", (search, search, user_id))
	users = cursor.fetchall()
	return users

# ervin
def userFollow(following_id, follower_id):
	cursor.execute('SELECT * FROM relation WHERE following_id = %s AND follower_id = %s', (following_id, follower_id))
	if cursor.fetchone() is None and following_id != follower_id:
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		cursor.execute("INSERT INTO relation(following_id, follower_id, c_time) VALUES(%s,%s,%s);", (following_id, follower_id, c_time))
		conn.commit()
		cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
	return ""

def userUnfollow(following_id, follower_id):
	cursor.execute("DELETE FROM relation where following_id = %s AND follower_id = %s;", (following_id, follower_id))
	conn.commit()
	cursor.execute("SELECT nickname FROM users WHERE user_id = %s;", (following_id,))
	return ""