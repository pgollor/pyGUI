##
# @file client.py
# 
# @date 03.03.2014
# @author Stanislav Tereschenko
# @author Pascal Gollor (http://www.pgollor.de)
# 
# @copyright Dieses Projekt ist lizensiert als Inhalt der
# Creative Commons Namensnennung - Weitergabe unter gleichen Bedingungen 3.0 Unported-Lizenz.<br>
# Um eine Kopie der Lizenz zu sehen, besuchen Sie http://creativecommons.org/licenses/by-sa/3.0/.<br>
# -- englisch version --<br>
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


import logging, logging.handlers


##
# @brief client logger class
# 
# Each client have to use these class for logging.
class clientLogger():
	def __init__(self, name = "", level = logging.DEBUG):
		self.__initVars()
		
		if (name != ""):
			self.init(name, level)
		# end if
	# end __init__
	
	def __initVars(self):
		self.__p_logger = False
		self.__p_socketHandler = False
	# end __initVars
	
	def init(self, name, level = logging.DEBUG):
		self.__p_logger = logging.getLogger(str(name))
		self.__p_logger.setLevel(level)
		self.__p_socketHandler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		
		self.__p_logger.addHandler(self.__p_socketHandler)
	# end init
	
	def __del__(self):
		if (self.__p_logger != False and self.__p_socketHandler != False):
			self.__p_logger.removeHandler(self.__p_socketHandler)
			self.__p_socketHandler.close()
			
			del(self.__p_socketHandler)
			del(self.__p_logger)

			self.__initVars()
		# end if
	# end __del__
	
	def getLogger(self):
		return self.__p_logger
	# end getLogger
	
# end class clientLogger