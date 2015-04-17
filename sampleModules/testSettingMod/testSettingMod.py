## @file testSettingMod.py
# 
# @date 26.07.2013
# @author Stanislav Tereschenko
# @author Pascal Gollor (http://www.pgollor.de)
# 
# @copyright Dieses Projekt ist lizensiert als Inhalt der
# Creative Commons Namensnennung - Weitergabe unter gleichen Bedingungen 3.0 Unported-Lizenz.<br>
# Um eine Kopie der Lizenz zu sehen, besuchen Sie http://creativecommons.org/licenses/by-sa/3.0/.<br>
# -- englisch version --<br>
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
# 
# @brief This is a tiny demo settings module. 

from abstractModuleClass import settingModuleClass


## @brief settings module for PyGUI
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
# 	onInactive(elf)
# 
# - You can load other module handles by _getModuleArray()
# - You can get other files by getIncludes()
# - You can get global progress bar by _getProgressBar()
# </pre>
#
class module(settingModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		settingModuleClass.__init__(self, parent, name)
	# end __init__

	def __onPushButton(self):
		self.labelFoo.setText("push button were pressed")
	# end __onPushButton

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		settingModuleClass.initModule(self)
	# end _initModule

	def initGUI(self):
		self.pushButton.clicked.connect(self.__onPushButton)
		
		settingModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
