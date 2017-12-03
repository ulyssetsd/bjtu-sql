import os
import flaskr
import unittest
import tempfile
import sys
from datetime import datetime

# import flaskr.database
# from flaskr.flaskr2 import db_getEntries2
from requete import *


class FlaskrTestCase(unittest.TestCase):

	debug = True
	emailGeneral = "toto@fleur.com"
	idGeneral = -69

	def setUp(self):
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		flaskr.app.testing = True
		self.app = flaskr.app.test_client()
		with flaskr.app.app_context():
			self.ptrMessageGetAll = messageGetAll
			self.ptrUserGetAll = userGetAll
			self.ptrMessageCount = messageCount
			self.ptrUserByEmail = userByEmail
			self.ptrUserCreate = userCreate
			self.ptrUserDelete = userDelete
			self.ptrUserIdByEmailPassword = userIdByEmailPassword
			self.ptrUserUpdateNicknameByEmail = userUpdateNicknameByEmail
			self.ptrUserUpdatePasswordByEmail = userUpdatePasswordByEmail
			self.ptrMessageCreate = messageCreate
			self.ptrMessageDeleteByUserId = messageDeleteByUserId
			self.ptrMessageGetAllFromUserId = messageGetAllFromUserId
			self.ptrMessageById = messageById
			self.ptrMessageUpdateContentById = messageUpdateContentById
			self.ptrMessageDeleteById = messageDeleteById
			self.ptrMessageGetAllFromUserIdOrder = messageGetAllFromUserIdOrder
			self.ptrLikeMsgCreate = likeMsgCreate
			self.ptrLikeMsgCount = likeMsgCount
			self.ptrLikeMsgGetAll = likeMsgGetAll
			self.ptrLikeMsgDelete = likeMsgDelete
			self.ptrCommentCreate = commentCreate
			self.ptrCommentCount = commentCount
			self.ptrCommentDeleteById = commentDeleteById
			self.ptrCommentUpdateById = commentUpdateById
			self.ptrLikeCommentCreate = likeCommentCreate
			self.ptrLikeCommentDelete = likeCommentDelete
			self.ptrLikeCommentCount = likeCommentCount
			self.ptrLikeMsgGetAll = likeMsgGetAll
			self.ptrLikeMsgCreate = likeMsgCreate
			self.ptrLikeMsgDelete = likeMsgDelete
			self.ptrLikeMsgCount = likeMsgCount
			self.ptrFollowUser = followUser
			self.ptrUnfollowUser = unfollowUser

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_messageGetAll(self):
		self.display('test_messageGetAll', self.ptrMessageGetAll())

	def test_usersGetAll(self):
		self.display('test_userGetAll', self.ptrUserGetAll())

	def test_likeMsgGetAll(self):
		self.display('test_likeMsgGetAll', self.ptrLikeMsgGetAll())

	def test_messageCount(self):
		u = self.ptrMessageCount()
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		self.ptrMessageDeleteByUserId(self.idGeneral)
		if u == (u1 - 1):
			self.display('test_messageCount', "")
			return ""
		self.display('test_messageCount', 'Error no message founded', 1)

	def test_userByEmail(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			# User NONE
			self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
			# User exist
			u = self.ptrUserByEmail(emailTest)
			if u is None:
				self.display('test_userByEmail', 'Error not able to find the user', 1)
				return ''
		self.display('test_userByEmail', "")
		userDelete(emailTest)

	def test_userCreate(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is not None:
			userDelete(emailTest)
		# User NONE
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		# User exist
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			self.display('test_userCreate', 'Error not able to create the user', 1)
			return ''
		self.display('test_userCreate', "")
		userDelete(emailTest)

	def test_userDelete(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			# User NONE
			self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
			# User exist
		u = self.ptrUserByEmail(emailTest)
		if u is not None:
			self.ptrUserDelete(emailTest)
			u = self.ptrUserByEmail(emailTest)
			if u is None:
				self.display('test_userDelete', "")
				return ""
		self.display('test_userDelete', 'Error not able to delete the user', 1)
	
	def test_userIdByEmailPassword(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		userSave = self.ptrUserByEmail(emailTest)
		user = self.ptrUserIdByEmailPassword(emailTest, "pierrePaul")
		if user['user_id'] == userSave['user_id']:
			self.display('test_userIdByEmailPassword', "")
			return ""
		self.display('test_userIdByEmailPassword', 'Error no ID matched', 1)

	def test_userUpdateNicknameByEmail(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		userSave = self.ptrUserByEmail(emailTest)
		self.ptrUserUpdateNicknameByEmail('thomas', emailTest)
		userSave2 = self.ptrUserByEmail(emailTest)
		if userSave2[1] == userSave[1]:
			self.display('test_userUpdateNicknameByEmail', "")
			return ""
		self.display('test_userUpdateNicknameByEmail', 'Erreur not able to update user nickname', 1)

	def test_userUpdatePasswordByEmail(self):
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		userSave = self.ptrUserByEmail(emailTest)
		self.ptrUserUpdatePasswordByEmail("monNewMdp", emailTest)
		userSave2 = self.ptrUserByEmail(emailTest)
		#print(userSave, userSave2)
		if userSave2[2] != userSave[2]:
			self.display('test_userUpdatePasswordByEmail', "")
			return ""
		self.display('test_userUpdatePasswordByEmail', 'Error not able to update user password', 1)

	def test_messageCreate(self):
		u = self.ptrMessageCount()
		self.ptrMessageCreate(self.idGeneral, 'test foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		if u < u1:
			self.display('test_messageCreate', "")
			self.ptrMessageDeleteByUserId(self.idGeneral)
			return ""
		self.display('test_messageCreate', 'Error not able to create a message', 1)

	def test_messageDeleteByUserId(self):
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrMessageDeleteByUserId(self.idGeneral)
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		if len(mess) > 0:
			self.display('test_messageDeleteByUserId', 'Error not able to delete user message', 1)
			return ""
		self.display('test_messageDeleteByUserId', "")

	def test_messageGetAllFromUserId(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		if len(mess) == 0:
			self.display('test_messageGetAllFromUserId', 'Error not able to fetchall messages from users', 1)
			return ""
		self.display('test_messageGetAllFromUserId', "")

	def test_messageById(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		idMess = mess[0][0]
		newMess = self.ptrMessageById(idMess)
		if newMess[2] == mess[0][2]:
			self.display('test_messageById', "")
			return ""
		self.display('test_messageById', 'Error not able to create message by a id', 1)

	def test_messageUpdateContentById(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		idMess = mess[0][0]
		self.ptrMessageUpdateContentById("New Content", idMess)
		mess2 = self.ptrMessageGetAllFromUserId(self.idGeneral)
		#print(mess2)
		if mess[0][2] != mess2[0][2]:
			self.display('test_messageUpdateContentById', "")
			return ""
		self.display('test_messageUpdateContentById', 'Error not able to update the user message content', 1)

	def test_messageDeleteById(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrMessageDeleteById(self.idGeneral)
		m = self.ptrMessageById(self.idGeneral)

		if m is not None:
			self.display('test_messageDeleteById', 'Error not able to delete message by id', 1)
			return ""
		self.display('test_messageDeleteById1111', "")

	def test_messageGetAllFromUserIdOrder(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserIdOrder(self.idGeneral)
		if len(mess) == 0:
			self.display('test_messageGetAllFromUserIdOrder', 'Error not able to get all message by id', 1)
			return ""
		self.display('test_messageGetAllFromUserIdOrder', "")

	def test_likeMsgCount(self):
		a1 = self.ptrLikeMsgCount()
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		a2 = self.ptrLikeMsgCount()
		if a1 == (a2 - 1):
			self.display('test_likeMsgCount', "")
			return ""
		self.display('test_likeMsgCount', 'Error not able to count messages liked', 1)

	def test_likeMsgDelete(self):
		a1 = self.ptrLikeMsgCount()
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrLikeMsgDelete(self.idGeneral, self.idGeneral)
		a2 = self.ptrLikeMsgCount()
		if a1 != a2:
			self.display('test_likeMsgDelete', "")
			return ""
		self.display('test_likeMsgDelete', 'Error not able to delete liked messages', 1)

	def test_likeMsgCreate(self):
		a1 = self.ptrLikeMsgCount()
		#print(a1)
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		a2 = self.ptrLikeMsgCount()
		#print(a2)
		if a1 == (a2 - 1):
			self.display('test_likeMsgCreate', "")
			return ""
		self.display('test_likeMsgCreate', 'Error not able to like a message', 1)

	def test_commentCreate(self):
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		if u < u1:
			if n < n1:
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				self.display('test_commentCreate', "")
				return ""
			return ""
		self.display('test_messageCreate', 'Error not able to comment a message', 1)

	def test_commentDelete(self):
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		if u < u1:
			if n < n1:
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				self.display('test_commentDelete', "")
				return ""
			return ""
		self.display('test_commentDelete', 'Error not able to delete a comment', 1)

	def test_commentUpdateById(self):
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		self.ptrCommentUpdateById('update', self.idGeneral)
		self.display('test_commentUpdateById', "")
		if u < u1:
			if n < n1:
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				return ""
			return ""
		self.display('test_commentUpdateById', 'Error not able to update a comment by id', 1)

	def test_commentCount(self):
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		a2 = self.ptrLikeMsgCount()
		if n == (n1 - 1):
			self.display('test_commentCount', "")
			return ""
		self.display('test_commentCount', 'Error not able to count comment', 1)
		if u < u1:
			if n < n1:
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				return ""
			return ""

	def test_likeCmtCreateDel(self):
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrLikeCommentCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		if u < u1:
			if n < n1:
				self.ptrLikeCommentDelete(self.idGeneral, self.idGeneral)
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				self.display('test_likeCmtCreateDel', "")
				return ""
			return ""
		self.display('test_likeCmtCreateDel', 'Error not able to like and delete a liked comment', 1)

	def test_likeMsgCount(self):
		a1 = self.ptrLikeCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrLikeCommentCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		a2 = self.ptrLikeCommentCount()
		if a1 == (a2 - 1):
			self.display('test_likeMsgCount', "")
			return ""
		self.display('test_likeMsgCount', 'Error not able to count messages liked', 1)

	def test_followUser(self):
		nickname =  "jean"
		password = "pierrePaul"
		emailTest = self.emailGeneral
		following_id = -69
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is not None:
			userDelete(emailTest)
		# User NONE
		self.ptrUserCreate(emailTest, nickname, password, c_time)
		# User exist
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			self.display('test_followUser', 'Error not able to create the user to follow', 1)
			return ''
		self.display('test_followUser', "")
		cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (emailTest, password,))
		u = cursor.fetchone()
		if u is None:
			return None
			print(u)
		follower_id = u['user_id']
		followUser(following_id, follower_id)
		userDelete(emailTest)

	def test_unfollowUser(self):
		nickname =  "jean"
		password = "pierrePaul"
		emailTest = self.emailGeneral
		following_id = -69
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is not None:
			userDelete(emailTest)
		# User NONE
		self.ptrUserCreate(emailTest, nickname, password, c_time)
		# User exist
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			self.display('test_followUser', 'Error not able to create the user to follow', 1)
			return ''
		self.display('test_followUser', "")
		cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (emailTest, password,))
		u = cursor.fetchone()
		if u is None:
			return None
			print(u)
		follower_id = u['user_id']
		followUser(following_id, follower_id)
		unfollowUser(following_id, follower_id)
		userDelete(emailTest)

	def test_zDrop(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.cleanEmail(self.emailGeneral)
		self.ptrLikeMsgDelete(self.idGeneral, self.idGeneral)
		self.display('test_zDrop', "   Drop all test")

	def cleanEmail(self, email):
		u = self.ptrUserByEmail(email)
		if u is not None:
			self.ptrUserDelete(email)
			self.cleanEmail(email)

	def display(self, name, value, error = 0):
		sys.stdout.write('\033[32m-------------------------------------\033[0m\n')
		if error == 1:
			sys.stdout.write(" \033[30;41m ")
			sys.stdout.write(name)
			sys.stdout.write(" \033[0m \n")
		else:
			sys.stdout.write(" \033[30;42m ")
			sys.stdout.write(name)
			sys.stdout.write(" \033[0m \n")
		if self.debug != False:
			if len(value) > 0:
				print(value)
		sys.stdout.write(' \033[31m-------------------------------------\033[0m\n')
if __name__ == '__main__':
	unittest.main()


#JVIENS DE FINI LE LIKE MSG IL FAUT FAIRE LE LIKE CMT & COMMENT