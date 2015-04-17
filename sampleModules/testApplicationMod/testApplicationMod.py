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
# 	onInactive(self)
# 
# - You can load other module handles by self._getModuleArray()
# - You can get other files by self.getIncludes()
# - You can get global progress bar by self.p_progressBar
# - You can get values from GUI elements. The GUI elements have to be located in xml file. self._getSettings([name])
#
# If you need other modules you have to add this module to a global variable as list like:
# dependencies = ["testSettingMod"]
#
# Module icon:
# specify the icon for menu button by using the following line in initGui function:
# self.getMenuButton().setIcon(QIcon(self.getModulePath(True) + '/joystick8.svg'))
# Or you can add <icon>relative path</icon> to the main node from modulename.xml
# </pre>

from abstractModuleClass import applicationModuleClass


##
# @brief application module for PyGUI
class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
	# end __init__

	def __onPushButton(self):
		self._p_logger.debug('debug test')
		self._p_logger.info('info test')
		self._p_logger.warning('warning test')
		self._p_logger.error('error test')
		self._p_logger.critical('critial test')
		self.label.setText("push button were pressed")
	# end __onPushButton

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		applicationModuleClass.initModule(self)
	#end _initModule

	def initGUI(self):
		self.pushButton.clicked.connect(self.__onPushButton)
		
		applicationModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
