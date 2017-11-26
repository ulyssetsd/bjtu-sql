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
		self.display('test_messageCount', 'Erreur perso...', 1)

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
				self.display('test_userByEmail', 'Erreur perso...', 1)
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
			self.display('test_userCreate', 'Erreur perso...', 1)
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
		self.display('test_userDelete', 'Erreur perso...', 1)
	
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
		self.display('test_userIdByEmailPassword', 'Erreur perso...', 1)

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
		self.display('test_userUpdateNicknameByEmail', 'Erreur perso...', 1)

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
		self.display('test_userUpdatePasswordByEmail', 'Erreur perso...', 1)

	def test_messageCreate(self):
		u = self.ptrMessageCount()
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		if u < u1:
			self.display('test_messageCreate', "")
			self.ptrMessageDeleteByUserId(self.idGeneral)
			return ""
		self.display('test_messageCreate', 'Erreur perso...', 1)

	def test_messageDeleteByUserId(self):
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrMessageDeleteByUserId(self.idGeneral)
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		if len(mess) > 0:
			self.display('test_messageDeleteByUserId', 'Erreur perso...2', 1)
			return ""
		self.display('test_messageDeleteByUserId', "")

	def test_messageGetAllFromUserId(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		if len(mess) == 0:
			self.display('test_messageGetAllFromUserId', 'Erreur perso...2', 1)
			return ""
		self.display('test_messageGetAllFromUserId', "")

	def test_messageById(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		idMess = mess[0][0]
		newMess = self.ptrMessageById(idMess)
		if newMess[2] == mess[0][2]:
			self.display('test_messageById', "")
			return ""
		self.display('test_messageById', 'Erreur perso...', 1)

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
		self.display('test_messageUpdateContentById', 'Erreur perso...', 1)

	def test_messageDeleteById(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrMessageDeleteById(self.idGeneral)
		m = self.ptrMessageById(self.idGeneral)
		#print(m)
		if m is not None:
			self.display('test_messageDeleteById', 'Erreur perso...', 1)
			return ""
		self.display('test_messageDeleteById', "")

	def test_messageGetAllFromUserIdOrder(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		mess = self.ptrMessageGetAllFromUserIdOrder(self.idGeneral)
		if len(mess) == 0:
			self.display('test_messageGetAllFromUserIdOrder', 'Erreur perso...2', 1)
			return ""
		self.display('test_messageGetAllFromUserIdOrder', "")

	def test_likeMsgCount(self):
		a1 = self.ptrLikeMsgCount()
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		a2 = self.ptrLikeMsgCount()
		if a1 == (a2 - 1):
			self.display('test_likeMsgCount', "")
			return ""
		self.display('test_likeMsgCount', 'Erreur perso...', 1)

	def test_likeMsgDelete(self):
		a1 = self.ptrLikeMsgCount()
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrLikeMsgDelete(self.idGeneral, self.idGeneral)
		a2 = self.ptrLikeMsgCount()
		if a1 != a2:
			self.display('test_likeMsgDelete', "")
			return ""
		self.display('test_likeMsgDelete', 'Erreur perso...', 1)

	def test_likeMsgCreate(self):
		a1 = self.ptrLikeMsgCount()
		#print(a1)
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		a2 = self.ptrLikeMsgCount()
		#print(a2)
		if a1 == (a2 - 1):
			self.display('test_likeMsgCreate', "")
			return ""
		self.display('test_likeMsgCreate', 'Erreur perso...', 1)

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