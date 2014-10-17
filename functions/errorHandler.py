##
# @file errorHandler.py
#
# @date unknown
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
# 
# @brief error and log handler

from PyQt4.QtCore import Qt, QObject
from PyQt4.QtGui import QListWidgetItem, QBrush


class errorHandler(QObject):
	enumErrorFlag = {"crit" : 1, "warn" : 2, "info" : 3, "debug" : 4, "devdebug": 5}

	def __init__(self, parent = None):
		QObject.__init__(self, parent)
		
		self.__initVars()
	# end __init__

	def __initVars(self):
		self.__v_logLevel = 5
		self.__p_outputWidget = False
	# end __initVars

	def printError(self, displayName, msg, flag = 1):
		if (self.__p_outputWidget == False):
			return False
		# end if

		if (flag in self.enumErrorFlag):
			# alias
			if (flag == "error"):
				flag = "crit"
			# end if

			if (flag == "devd"):
				flag = "devdebug"
			# end if

			flag = self.enumErrorFlag[flag]
		# end if

		if (flag > self.__v_logLevel):
			return False
		# end if

		errMsg = str(displayName) + ": "
		if (flag == self.enumErrorFlag["crit"]):
			errMsg += "[ERROR]: " + str(msg) + "!!!"
		elif (flag == self.enumErrorFlag["warn"]):
			errMsg += "[WARN]: " + str(msg) + "."
		elif (flag == self.enumErrorFlag["info"]):
			errMsg += "[INFO]: " + str(msg)
		elif (flag == self.enumErrorFlag["debug"]):
			errMsg += "[DEBUG]: " + str(msg)
		elif (flag == self.enumErrorFlag["devdebug"]):
			errMsg += "[DEV DEBUG]: " + str(msg)
		# end if

		item = QListWidgetItem(errMsg)

		if (flag == self.enumErrorFlag["crit"]):
			item.setForeground(QBrush(Qt.red))
		elif (flag == self.enumErrorFlag["warn"]):
			item.setForeground(QBrush(Qt.blue))
		elif (flag == self.enumErrorFlag["debug"]):
			item.setForeground(QBrush(Qt.gray))
		elif (flag == self.enumErrorFlag["devdebug"]):
			item.setForeground(QBrush(Qt.yellow))
		# end if

		self.__p_outputWidget.addItem(item)
		self.__p_outputWidget.scrollToItem(item)

		return True
	# end printError

	def setErrorWidget(self, widget):
		self.__p_outputWidget = widget
	# end setErrorWidget

	def setLogLevel(self, logLevel):
		self.__v_logLevel = logLevel
	# end setLogLevel

	def logLevel(self):
		return self.__v_logLevel
	# end logLevel

# end class errorHandler