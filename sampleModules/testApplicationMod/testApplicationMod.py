##
# @file testApplicationMod.py
#
# @date 26.07.2013
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
# @brief This is a tiny demo application module.
#
# <pre>
# required functions:
# 	__init__(self, parent, name):
# 		settingModuleClass.__init__(self, parent, name)
# 
# 	initGUI(self)
# 
# optional functions:
# 	initPreSettings(self)
# 	initModule(self)
# 	initGui(self)
# 	onClose(self)
# 	onActive(self)
# 
# - You can load other module handles by _getModuleArray()
# - You can get other files by getIncludes()
# - You can get global progress bar by _getProgressBar()
#
# If you need other modules you have to add this module to a global variable as list like:
# dependencies = ["testSettingMod"]
# </pre>

from PyQt4.QtCore import SIGNAL
from abstractModuleClass import applicationModuleClass


##
# @brief application module for PyGUI
class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
	# end __init__

	def __onPushButton(self):
		self.label.setText("push button were pressed")
	# end __onPushButton

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		pass
	#end _initModule

	def initGUI(self):
		self.connect(self.pushButton, SIGNAL("clicked()"), self.__onPushButton)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
