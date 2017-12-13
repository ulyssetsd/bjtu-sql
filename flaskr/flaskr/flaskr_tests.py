import os
import flaskr
import unittest
import tempfile
import sys
from datetime import datetime

# import flaskr.database
# from flaskr.flaskr2 import db_getEntries2
from requete import *
from views.users import registerRequest, loginRequest, editPasswordRequest, editNicknameRequest

class FlaskrTestCase(unittest.TestCase):

	debug = True
	emailGeneral = "toto@fleur.com"
	idGeneral = -69
	debugTxt = ""
	retourLine = "\n"

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
			self.ptrUserDeleteAll = userDeleteAll
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
			self.ptrLikeCmtCreate = likeCmtCreate
			self.ptrLikeCmtDelete = likeCmtDelete
			self.ptrLikeCmtCount = likeCmtCount
			self.ptrLikeMsgGetAll = likeMsgGetAll
			self.ptrLikeMsgCreate = likeMsgCreate
			self.ptrLikeMsgDelete = likeMsgDelete
			self.ptrLikeMsgCount = likeMsgCount
			self.ptrLikeDeleteAll = likeDeleteAll
			self.ptrMessageDeleteAll = messageDeleteAll
			self.ptrCommentDeleteAll = commentDeleteAll
			self.ptrLikeMsgDeleteAll = likeMsgDeleteAll
			self.ptrCommentGetAll = commentGetAll
			self.ptrUserFollow = userFollow
			self.ptrUserUnfollow = userUnfollow

			self.ptrRegisterRequest = registerRequest
			self.ptrLoginRequest = loginRequest
			self.ptrEditPasswordRequest = editPasswordRequest
			self.ptrEditNicknameRequest = editNicknameRequest
			

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_aDropTable(self):
		self.ptrUserDeleteAll()
		self.ptrLikeDeleteAll()
		self.ptrMessageDeleteAll()
		self.ptrCommentDeleteAll()
		self.ptrLikeMsgDeleteAll()

	def test_messageGetAll(self):
		self.display('test_messageGetAll', self.ptrMessageGetAll())

	def test_usersGetAll(self):
		self.display('test_userGetAll', self.ptrUserGetAll())

	def test_likeMsgGetAll(self):
		self.display('test_likeMsgGetAll', self.ptrLikeMsgGetAll())

	def test_commentGetAll(self):
		self.display('test_commentGetAll', self.ptrCommentGetAll())

	def test_userByEmail(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		if u is None:
			# User NONE
			self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
			self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
			# User exist
			self.debugTxt += "Creer user: " + emailTest + self.retourLine
			u = self.ptrUserByEmail(emailTest)
			self.debugTxt += "Recupere user: " + emailTest + self.retourLine
			if u is None:
				self.debugTxt += "L'user: " + emailTest +" n'a pas ete trouve " + self.retourLine
				self.display('test_userByEmail', 'Error not able to find the user', 1)
				return ''
		self.debugTxt += "L'user: " + emailTest +" a ete trouve " + self.retourLine
		self.display('test_userByEmail', "")
		userDelete(emailTest)

	def test_userCreate(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
		if u is not None:
			userDelete(emailTest)
		# User NONE
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		# User exist
		self.debugTxt += "Creer user: " + emailTest + self.retourLine
		u = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Recupere user: " + emailTest + self.retourLine
		if u is None:
			self.debugTxt += "L'user: " + emailTest +" n'a pas ete trouve " + self.retourLine
			self.display('test_userCreate', 'Error not able to create the user', 1)
			return ''
		self.debugTxt += "L'user: " + emailTest +" a ete trouve " + self.retourLine
		self.display('test_userCreate', "")
		userDelete(emailTest)

	def test_userDelete(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		u = self.ptrUserByEmail(emailTest)
		self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
		if u is None:
			# User NONE
			self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
			self.debugTxt += "Creer user: " + emailTest + self.retourLine
			# User exist
		u = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Recupere user: " + emailTest + self.retourLine
		if u is not None:
			self.ptrUserDelete(emailTest)
			self.debugTxt += "Delete user: " + emailTest + self.retourLine
			u = self.ptrUserByEmail(emailTest)
			self.debugTxt += "Recupere user: " + emailTest + self.retourLine
			if u is None:
				self.debugTxt += "L'user: " + emailTest +" n'a pas ete trouve " + self.retourLine
				self.display('test_userDelete', "")
				return ""
		self.debugTxt += "L'user: " + emailTest +" a ete trouve " + self.retourLine
		self.display('test_userDelete', 'Error not able to delete the user', 1)
	
	def test_userIdByEmailPassword(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		self.debugTxt += "Creer user: " + emailTest + self.retourLine
		userSave = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Recupere user: " + emailTest +" par email "+ self.retourLine
		user = self.ptrUserIdByEmailPassword(emailTest, "pierrePaul")
		self.debugTxt += "Recupere user: " + emailTest +" par email & password"+ self.retourLine
		if user['user_id'] == userSave['user_id']:
			self.debugTxt += "Les users sont les memes "+ self.retourLine
			self.display('test_userIdByEmailPassword', "")
			return ""
		self.debugTxt += "Les users ne sont pas les memes "+ self.retourLine
		self.display('test_userIdByEmailPassword', 'Error no ID matched', 1)

	def test_userUpdateNicknameByEmail(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		self.debugTxt += "Creer user: " + emailTest + self.retourLine
		userSave = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Get user: " + emailTest +" par email "+ self.retourLine
		self.ptrUserUpdateNicknameByEmail('thomas', emailTest)
		self.debugTxt += "Mise a jour nom de l'user pour Thomas" + self.retourLine
		userSave2 = self.ptrUserByEmail(emailTest)
		if userSave2[1] == userSave[1] and userSave2[3] == "thomas" :
			self.debugTxt += "L'user se nomme desormais : " + userSave2[3] + self.retourLine
			self.display('test_userUpdateNicknameByEmail', "")
			return ""
		self.debugTxt += "L'user ne se nomme pas thomas ! " + self.retourLine
		self.display('test_userUpdateNicknameByEmail', 'Erreur not able to update user nickname', 1)

	def test_userUpdatePasswordByEmail(self):
		self.debugTxt = ""
		emailTest = self.emailGeneral
		c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.cleanEmail(emailTest)
		self.debugTxt += "L'user "+emailTest+" n'existe pas" + self.retourLine
		self.ptrUserCreate(emailTest, "jean", "pierrePaul", c_time)
		self.debugTxt += "Creer user: " + emailTest + self.retourLine
		userSave = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Get user: " + emailTest +" par email "+ self.retourLine
		self.ptrUserUpdatePasswordByEmail("monNewMdp", emailTest)
		self.debugTxt += "Mise a jour du password de l'user " + self.retourLine
		userSave2 = self.ptrUserByEmail(emailTest)
		self.debugTxt += "Get user: " + emailTest +" par email "+ self.retourLine
		#print(userSave, userSave2)
		if userSave2[2] != userSave[2]:
			self.debugTxt += "L'user a desormais un nouveau mot de passe : "  + self.retourLine
			self.display('test_userUpdatePasswordByEmail', "")
			return ""
		self.debugTxt += "L'user n'a pas de nouveau mot de passe : " + self.retourLine
		self.display('test_userUpdatePasswordByEmail', 'Error not able to update user password', 1)

	def test_messageCount(self):
		self.debugTxt = ""
		u = self.ptrMessageCount()
		self.debugTxt += "Nombre message: " + str(u) + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		u1 = self.ptrMessageCount()
		self.debugTxt += "Nombre message 2: " + str(u1) + self.retourLine
		self.ptrMessageDeleteByUserId(self.idGeneral)
		if u == (u1 - 1):
			self.display('test_messageCount', "")
			return ""
		self.display('test_messageCount', 'Error no message founded', 1)

	def test_messageCreate(self):
		self.debugTxt = ""
		u = self.ptrMessageCount()
		self.debugTxt += "Nombre message: " + str(u) + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'test foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		u1 = self.ptrMessageCount()
		self.debugTxt += "Nombre message 2: " + str(u1) + self.retourLine
		if u < u1:
			self.display('test_messageCreate', "")
			self.ptrMessageDeleteByUserId(self.idGeneral)
			return ""
		self.display('test_messageCreate', 'Error not able to create a message', 1)

	def test_messageDeleteByUserId(self):
		self.debugTxt = ""
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		if len(mess) > 0:
			self.debugTxt += "Le message est toujours la" + self.retourLine
			self.display('test_messageDeleteByUserId', 'Error not able to delete user message', 1)
			return ""
		self.debugTxt += "Le message n'est plus la" + self.retourLine
		self.display('test_messageDeleteByUserId', "")

	def test_messageGetAllFromUserId(self):
		self.debugTxt = ""
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		if len(mess) == 0:
			self.debugTxt += "Il n'y a pas de message" + self.retourLine
			self.display('test_messageGetAllFromUserId', 'Error not able to fetchall messages from users', 1)
			return ""
		self.debugTxt += "Il y a un ou des messages" + self.retourLine
		self.display('test_messageGetAllFromUserId', "")

	def test_messageById(self):
		self.debugTxt = ""
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'foobar', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		idMess = mess[0][0]
		newMess = self.ptrMessageById(idMess)
		self.debugTxt += "Recuperation d'un messages par messageId" + self.retourLine
		if newMess[2] == mess[0][2]:
			self.debugTxt += "Le message est le meme" + self.retourLine
			self.display('test_messageById', "")
			return ""
		self.debugTxt += "Le message n'est pas le meme" + self.retourLine
		self.display('test_messageById', 'Error not able to create message by a id', 1)

	def test_messageUpdateContentById(self):
		self.debugTxt = ""
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		mess = self.ptrMessageGetAllFromUserId(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		idMess = mess[0][0]
		self.ptrMessageUpdateContentById("New Content", idMess)
		self.debugTxt += "Mise a jour du message par messageId" + self.retourLine
		mess2 = self.ptrMessageGetAllFromUserId(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		if mess[0][2] != mess2[0][2]:
			self.debugTxt += "Le message n'est pas le meme" + self.retourLine
			self.display('test_messageUpdateContentById', "")
			return ""
		self.debugTxt += "Le message est le meme" + self.retourLine
		self.display('test_messageUpdateContentById', 'Error not able to update the user message content', 1)

	def test_messageDeleteById(self):
		self.debugTxt = ""
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		self.ptrMessageDeleteById(self.idGeneral)
		self.debugTxt += "Suppression des messages par messageId" + self.retourLine
		m = self.ptrMessageById(self.idGeneral)
		self.debugTxt += "Recuperation d'un message par messageId" + self.retourLine
		if m is not None:
			self.debugTxt += "Il y a un message" + self.retourLine
			self.display('test_messageDeleteById', 'Error not able to delete message by id', 1)
			return ""
		self.debugTxt += "Il n'y pas de message" + self.retourLine
		self.display('test_messageDeleteById', "")

	def test_messageGetAllFromUserIdOrder(self):
		self.debugTxt = ""
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Suppression des messages par userId" + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'Bite', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un message" + self.retourLine
		mess = self.ptrMessageGetAllFromUserIdOrder(self.idGeneral)
		self.debugTxt += "Recuperation des messages par userId" + self.retourLine
		if len(mess) == 0:
			self.debugTxt += "Il n'y a pas de message" + self.retourLine
			self.display('test_messageGetAllFromUserIdOrder', 'Error not able to get all message by id', 1)
			return ""
		self.debugTxt += "Le/Les messages sont la" + self.retourLine
		self.display('test_messageGetAllFromUserIdOrder', "")

	def test_likeMsgCount(self):
		self.debugTxt = ""
		a1 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like: " + str(a1) + self.retourLine
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un like" + self.retourLine
		a2 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like2: " + str(a2) + self.retourLine
		if a1 == (a2 - 1):
			self.display('test_likeMsgCount', "")
			return ""
		self.display('test_likeMsgCount', 'Error not able to count messages liked', 1)

	def test_likeMsgDelete(self):
		self.debugTxt = ""
		self.ptrLikeMsgDeleteAll()
		a1 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like: " + str(a1) + self.retourLine
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un like" + self.retourLine
		self.ptrLikeMsgDelete(self.idGeneral, self.idGeneral)
		self.debugTxt += "Delete le like" + self.retourLine
		a2 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like: " + str(a2) + self.retourLine
		if a1 == a2:
			self.debugTxt += "Le nombre de like est le meme "+ self.retourLine
			self.display('test_likeMsgDelete', "")
			return ""
		self.debugTxt += "Il y a bien un like de plus "+ self.retourLine
		self.display('test_likeMsgDelete', 'Error not able to delete liked messages', 1)

	def test_likeMsgCreate(self):
		self.debugTxt = ""
		a1 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like: " + str(a1) + self.retourLine
		self.ptrLikeMsgCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un like" + self.retourLine
		a2 = self.ptrLikeMsgCount()
		self.debugTxt += "Nombre like: " + str(a2) + self.retourLine
		if a1 == (a2 - 1):
			self.debugTxt += "Il y a bien un like de plus "+ self.retourLine
			self.display('test_likeMsgCreate', "")
			return ""
		self.debugTxt += "Le nombre de like est le meme "+ self.retourLine
		self.display('test_likeMsgCreate', 'Error not able to like a message', 1)

	def test_commentCreate(self):
		self.debugTxt = ""
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n) + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un commentaire" + self.retourLine
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n1) + self.retourLine
		if u < u1:
			if n < n1:
				self.debugTxt += "Le commentaire a bien ete creer" + self.retourLine
				self.ptrCommentDeleteById(self.idGeneral)
				self.display('test_commentCreate', "")
				return ""
			return ""
		self.display('test_messageCreate', 'Error not able to comment a message', 1)

	def test_commentDelete(self):
		self.debugTxt = ""
		self.ptrMessageDeleteAll()
		self.ptrCommentDeleteAll()
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n) + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un commentaire" + self.retourLine
		
		n3 = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n3) + self.retourLine
		
		comment = self.ptrCommentGetAll()
		idComm = comment[0][0]
		self.ptrCommentDeleteById(idComm)
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.debugTxt += "Delete le commentaire" + self.retourLine	
		
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n1) + self.retourLine
		if u <= u1:
			if n == n1:
				self.display('test_commentDelete', "")
				return ""
			self.display('test_commentDelete', 'Error not able to delete a comment', 1)
			return ""
		self.display('test_commentDelete', 'Error not able to delete a comment', 1)

	def test_commentUpdateById(self):
		self.debugTxt = ""
		self.ptrCommentDeleteAll()
		n = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n) + self.retourLine
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un commentaire" + self.retourLine
		
		n3 = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n3) + self.retourLine
		
		comment = self.ptrCommentGetAll()
		idComm = comment[0][0]
		txtComm = comment[0][3]
		self.debugTxt += "Le commentaire est : " + txtComm + self.retourLine

		self.ptrCommentUpdateById("new comme", idComm)
		self.debugTxt += "Mise a jour du message par commentaireId" + self.retourLine
		

		comment2 = self.ptrCommentGetAll()
		idComm2 = comment2[0][0]
		txtComm2 = comment2[0][3]
		self.debugTxt += "Le commentaire 2 est : " + txtComm2 + self.retourLine


		if idComm == idComm2 and txtComm != txtComm2:
			self.debugTxt += "Le commentaire est desormais : " + txtComm2 + self.retourLine
			self.ptrCommentDeleteById(idComm)
			self.debugTxt += "Delete le commentaire" + self.retourLine	
			self.display('test_commentUpdateById', "")
			return "";
		self.ptrCommentDeleteById(idComm)
		self.debugTxt += "Delete le commentaire" + self.retourLine	
		self.debugTxt += "Le commentaire est le meme" + self.retourLine
		self.display('test_commentUpdateById', 'Error not able to update the user message content', 1)

	def test_commentCount(self):
		self.debugTxt = ""
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n) + self.retourLine
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.debugTxt += "Ajoute un commentaire" + self.retourLine
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		self.debugTxt += "Nombre commentaire: " + str(n1) + self.retourLine
		if n == (n1 - 1):
			self.debugTxt += "Il y a un commentaire un plus" + self.retourLine
			self.display('test_commentCount', "")
			return ""
		self.display('test_commentCount', 'Error not able to count comment', 1)
		if u < u1:
			if n < n1:
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				return ""
			return ""

	def test_zz_registrationRequest(self):
		self.debugTxt = "Envoi de data vide" + self.retourLine
		a = self.ptrRegisterRequest("","","","", "","")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input all the information":
			self.debugTxt += "Creation refuse" + self.retourLine
			self.display('test_registrationRequest_emptyData', "")
		else:
			self.display('test_registrationRequest_emptyData', "", 1)

	def test_zz_registrationRequest0(self):
		fakeEmail = ""
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass2", "ube","ubn")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input all the information":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_wrongEmail', "")
		else:
			self.display('test_registrationRequest_wrongEmail', "", 1)


	def test_zz_registrationRequest01(self):
		fakeEmail = "a"
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass2", "ube","ubn")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input the right email":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_wrongEmail', "")
		else:
			self.display('test_registrationRequest_wrongEmail', "", 1)

	def test_zz_registrationRequest02(self):
		fakeEmail = "pierrePaulJaques.com"
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass2", "ube","ubn")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input the right email":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_wrongEmail', "")
		else:
			self.display('test_registrationRequest_wrongEmail', "", 1)

	def test_zz_registrationRequest03(self):
		fakeEmail = "a@a.a"
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass2", "ube","ubn")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input the right email":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_wrongEmail', "")
		else:
			self.display('test_registrationRequest_wrongEmail', "", 1)

	def test_zz_registrationRequest04(self):
		fakeEmail = "bonjoursJeSuisUnTrooooolllEtJeFaisDesMegaEmail@free.fr"
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass2", "ube","ubn")
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Please input the right email":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_wrongEmail', "")
		else:
			self.display('test_registrationRequest_wrongEmail', "", 1)

	def test_zz_registrationRequest05(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		self.debugTxt += "Suppression de tous les users" + self.retourLine
		u = self.ptrUserByEmail("romain@free.com")
		if u is not None:
			self.debugTxt += " exist deja " + self.retourLine
		fakeEmail = "romain@free.com"
		self.debugTxt += "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","passpass","passpass", u, None)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Register Success!":
			self.debugTxt += "Creation ok"  + self.retourLine
			self.ptrUserCreate(fakeEmail, "nickn", "passpass", None)
			self.display('test_registrationRequest_Email', "")
		else:
			self.display('test_registrationRequest_Email', "", 1)

	def test_zz_registrationRequest06(self):
		self.debugTxt = ""
		u = self.ptrUserByEmail("romain@free.com")
		if u is not None:
			self.debugTxt += " exist deja " + self.retourLine
		fakeEmail = "romain@free.com"
		self.debugTxt = "Test avec Email: " + fakeEmail + self.retourLine
		a = self.ptrRegisterRequest(fakeEmail,"nickn","passpass","passpass", u, None)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The email already exist":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_EmailRepeat', "")
		else:
			self.display('test_registrationRequest_EmailRepeat', "", 1)

	def test_zz_registrationRequest07(self):
		self.debugTxt = ""
		fakeEmail = "romain2@free.com"
		fakeNick = "nickn"

		self.debugTxt += "Test avec Nickname: " + fakeNick + " : "
				
		u = self.ptrUserByEmail(fakeEmail)
		uByNickname = userByNickname(fakeNick)
		if u is not None:
			self.debugTxt += "Email deja existant " + self.retourLine
		if uByNickname is not None:
			self.debugTxt += "Nickname deja existant " + self.retourLine

		a = self.ptrRegisterRequest(fakeEmail,"nickn","passpass","passpass", u, uByNickname)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The nickname already exist":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_NicknameRepeat', "")
		else:
			self.display('test_registrationRequest_NicknameRepeat', "", 1)

	def test_zz_registrationRequest08(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakeNick = "nickn"

		u = self.ptrUserByEmail(fakeEmail)
		uByNickname = userByNickname(fakeNick)
		a = self.ptrRegisterRequest(fakeEmail,"nickn","passpass","passpass2", u, uByNickname)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The password is not repeated correctly":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_PasswordReapeatWrong', "")
		else:
			self.display('test_registrationRequest_PasswordReapeatWrong', "", 1)

	def test_zz_registrationRequest09(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakeNick = "nickn"

		u = self.ptrUserByEmail(fakeEmail)
		uByNickname = userByNickname(fakeNick)
		a = self.ptrRegisterRequest(fakeEmail,"nickn","passpass","passpass", u, uByNickname)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Register Success!":
			self.debugTxt += "Creation Ok"  + self.retourLine
			self.display('test_registrationRequest_PasswordReapeatOk', "")
		else:
			self.display('test_registrationRequest_PasswordReapeatOk', "", 1)

	def test_zz_registrationRequest10(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakeNick = "nickn"

		u = self.ptrUserByEmail(fakeEmail)
		uByNickname = userByNickname(fakeNick)
		a = self.ptrRegisterRequest(fakeEmail,"nickn","pass","pass", u, uByNickname)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The password should be at least 6 characters":
			self.debugTxt += "Creation refuse"  + self.retourLine
			self.display('test_registrationRequest_PasswordToSmall', "")
		else:
			self.display('test_registrationRequest_PasswordToSmall', "", 1)

	def test_zz_loginRequest(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		a = self.ptrLoginRequest(fakeEmail, fakePassword)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The user doesn't exist. Please register first.":
			self.debugTxt += "Login refuse"  + self.retourLine
			self.display('test_loginRequestNoUser', "")
		else:
			self.display('test_loginRequestNoUser', "", 1)

	def test_zz_loginRequest01(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		self.ptrUserCreate(fakeEmail, "nickn", "passpass", None)

		a = self.ptrLoginRequest(fakeEmail, fakePassword)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Your password is wrong. Try it again.":
			self.debugTxt += "Login refuse"  + self.retourLine
			self.display('test_loginRequestWrongPassword', "")
		else:
			self.display('test_loginRequestWrongPassword', "", 1)
			
	def test_zz_loginRequest02(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		a = self.ptrLoginRequest(fakeEmail, fakePassword)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Login Success!":
			self.debugTxt += "Login ok"  + self.retourLine
			self.display('test_loginRequestPasswordOk', "")
		else:
			self.display('test_loginRequestPasswordOk', "", 1)
	
	def test_zz_editPasswordRequest(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userIdByEmailPassword(fakeEmail, 'pass')

		a = self.ptrEditPasswordRequest(u, 'pass', 'pass')
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Your old password is not right.":
			self.debugTxt += "Changement password refuse"  + self.retourLine
			self.display('test_editPasswordRequestWrongOldPassword', "")
		else:
			self.display('test_editPasswordRequestWrongOldPassword', "", 1)
	
	def test_zz_editPasswordRequest01(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userIdByEmailPassword(fakeEmail, fakePassword)

		a = self.ptrEditPasswordRequest(u, fakePassword, 'pass')
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The password is not repeated correctly":
			self.debugTxt += "Changement password refuse"  + self.retourLine
			self.display('test_editPasswordRequestDifferentPassAndPass2', "")
		else:
			self.display('test_editPasswordRequestDifferentPassAndPass2', "", 1)
	
	def test_zz_editPasswordRequest02(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nickn"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userIdByEmailPassword(fakeEmail, fakePassword)

		a = self.ptrEditPasswordRequest(u, fakePassword, fakePassword)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The password should be at least 6 characters":
			self.debugTxt += "Changement password refuse"  + self.retourLine
			self.display('test_editPasswordRequestPasswordToSmall', "")
		else:
			self.display('test_editPasswordRequestPasswordToSmall', "", 1)

	def test_zz_editPasswordRequest03(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nicknazety"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userIdByEmailPassword(fakeEmail, fakePassword)

		a = self.ptrEditPasswordRequest(u, fakePassword, fakePassword)
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Edit Password Success!":
			self.debugTxt += "Changement password ok"  + self.retourLine
			self.display('test_editPasswordRequestPasswordOk', "")
		else:
			self.display('test_editPasswordRequestPasswordOk', "", 1)
		
	def test_zz_editNicknameRequest(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nicknazety"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)
		self.ptrUserCreate("fakeEmail@free.com", "nickkyyy", fakePassword, None)

		u = userByNickname('nickkyyy')

		a = self.ptrEditNicknameRequest(u, 'nickkyyy')
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The nickname already exist":
			self.debugTxt += "Changement nickname refuse"  + self.retourLine
			self.display('test_editNicknameRequestNicknameCopy', "")
		else:
			self.display('test_editNicknameRequestNicknameCopy', "", 1)
	
	def test_zz_editNicknameRequest01(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nicknazety"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userByNickname('')

		a = self.ptrEditNicknameRequest(u, '')
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "The nickname can not be null":
			self.debugTxt += "Changement nickname refuse"  + self.retourLine
			self.display('test_editNicknameRequestNicknameNull', "")
		else:
			self.display('test_editNicknameRequestNicknameNull', "", 1)
			
	def test_zz_editNicknameRequest02(self):
		self.debugTxt = ""
		self.ptrUserDeleteAll()
		fakeEmail = "romain2@free.com"
		fakePassword = "nicknazety"

		self.ptrUserCreate(fakeEmail, "nickn", fakePassword, None)

		u = userByNickname('jeanPaulDupuit')

		a = self.ptrEditNicknameRequest(u, 'jeanPaulDupuit')
		self.debugTxt += 'Reponse: ' + a + ' : '
		if a == "Edit Nickname Success!":
			self.debugTxt += "Changement nickname ok"  + self.retourLine
			self.display('test_editNicknameRequestNicknameOk', "")
		else:
			self.display('test_editNicknameRequestNicknameOk', "", 1)
			


	#ervin
	def test_likeCmtCreateDel(self):
		self.debugTxt = ""
		u = self.ptrMessageCount()
		n = self.ptrCommentCount()
		self.ptrMessageCreate(self.idGeneral, 'message to comment', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrCommentCreate(self.idGeneral, self.idGeneral, 'Comment the message', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.ptrLikeCmtCreate(self.idGeneral, self.idGeneral, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		u1 = self.ptrMessageCount()
		n1 = self.ptrCommentCount()
		if u < u1:
			if n < n1:
				self.ptrLikeCmtDelete(self.idGeneral, self.idGeneral)
				self.ptrCommentDeleteById(self.idGeneral)
				self.ptrMessageDeleteByUserId(self.idGeneral)
				self.display('test_likeCmtCreateDel', "")
				return ""
			return ""
		self.display('test_likeCmtCreateDel', 'Error not able to like and delete a liked comment', 1)


	# def test_userFollow(self):
	# 	nickname =  "jean"
	# 	password = "pierrePaul"
	# 	emailTest = self.emailGeneral
	# 	following_id = -69
	# 	c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	# 	self.cleanEmail(emailTest)
	# 	u = self.ptrUserByEmail(emailTest)
	# 	if u is not None:
	# 		userDelete(emailTest)
	# 	# User NONE
	# 	self.ptrUserCreate(emailTest, nickname, password, c_time)
	# 	# User exist
	# 	u = self.ptrUserByEmail(emailTest)
	# 	if u is None:
	# 		self.display('test_userFollow', 'Error not able to create the user to follow', 1)
	# 		return ''
	# 	self.ptrUserFollow(following_id, follower_id)
	# 	self.display('test_userFollow', "")
	# 	cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (emailTest, password,))
	# 	u = cursor.fetchone()
	# 	if u is None:
	# 		return None
	# 		print(u)
	# 	follower_id = u['user_id']
	# 	followUser(following_id, follower_id)
	# 	userDelete(emailTest)

	# def test_unfollowUser(self):
	# 	nickname =  "jean"
	# 	password = "pierrePaul"
	# 	emailTest = self.emailGeneral
	# 	following_id = -69
	# 	c_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	# 	self.cleanEmail(emailTest)
	# 	u = self.ptrUserByEmail(emailTest)
	# 	if u is not None:
	# 		userDelete(emailTest)
	# 	# User NONE
	# 	self.ptrUserCreate(emailTest, nickname, password, c_time)
	# 	# User exist
	# 	u = self.ptrUserByEmail(emailTest)
	# 	if u is None:
	# 		self.display('test_followUser', 'Error not able to create the user to follow', 1)
	# 		return ''
	# 	self.display('test_followUser', "")
	# 	cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = crypt(%s, password);", (emailTest, password,))
	# 	u = cursor.fetchone()
	# 	if u is None:
	# 		return None
	# 		print(u)
	# 	follower_id = u['user_id']
	# 	followUser(following_id, follower_id)
	# 	unfollowUser(following_id, follower_id)
	# 	userDelete(emailTest)

	def test_zDrop(self):
		self.ptrMessageDeleteByUserId(self.idGeneral)
		self.cleanEmail(self.emailGeneral)
		self.ptrLikeMsgDelete(self.idGeneral, self.idGeneral)
		self.ptrUserDeleteAll()
		self.ptrLikeDeleteAll()
		self.ptrMessageDeleteAll()
		self.ptrCommentDeleteAll()
		self.ptrLikeMsgDeleteAll()
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
			if len(self.debugTxt) > 0:
				print(self.debugTxt[:-1])
			if len(value) > 0:
				print(value)
		sys.stdout.write(' \033[31m-------------------------------------\033[0m\n')
if __name__ == '__main__':
	unittest.main()

#add les test deletes all



#userByUserId , ptrLikeCmtDelete