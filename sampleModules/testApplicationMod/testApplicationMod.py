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
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
# 
#
# @defgroup testApplicationMod
# 
# @brief This is a tiny sample application module.
# 
# @section app-mod Application Module
#
# @subsection req-func Required functions:
# -	<pre>__init__(self, parent, name):
#  applicationModuleClass.__init__(self, parent, name)
#
#  self.setDisplayName('testApplication')</pre>
# 
# @subsection opt-func Optional functions:
# - initPreSettings(self)
# - initModule(self)
# - initGui(self)
# - onClose(self)
# - onActive(self)
# - onInactive(self)
# - onInactive(self)
# - getDefaultSettings(self)
#
# @subsection add-infos Additional information: 
# - You can load other module handles by self._getModuleArray()
# - You can get other files by self.getIncludes()
# - You can get global progress bar by self._getProgressBar()
# - You can get values from GUI elements. The GUI elements have to be located in xml file. self._getSettings([name])
#
# If you need other modules you have to add this module to a global list like:
# dependencies = ["testSettingMod"]
#
# @subsection mod-icon Module icon:
# Specify the icon for menu button by using the following line in initModule function:
# - Icon from GUI icon folder: <pre>self._setIconPath('usb.svg', True)</pre>
# - Icon from Module folder: <pre>self._setIconPath('usb.svg')</pre>
#
# @{

from abstractModuleClass import applicationModuleClass


##
# @brief application module for PyGUI
class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
		
		self.setDisplayName('testApplication')
	# end __init__

	## @brief Qt slot which is connected to pushButton.
	# @param self The object pointer.
	# 
	# This function generates some logger output to show how to use the python logger.
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
	
	## @brief Have to return default settings.
	# @param self The object pointer.
	# @return settings dict
	def getDefaultSettings(self):
		d = {"label": {"qName": "label", "value": "default text from ini"}}
		
		return d
	# end getDefaultSettings
	
	## @brief Initialize Module function.
	# @param self The object pointer.
	#
	# This function is called before initGUI.
	# You can set a custom icon path or so. 
	def initModule(self):
		self._setIconPath('usb.svg', True)
		
		applicationModuleClass.initModule(self)
	# end initModule

	## @brief Function to initialize the GUI
	# @param self The object pointer.
	# 
	# In this function you have to connect all Qt elements and so on.
	def initGUI(self):
		self.pushButton.clicked.connect(self.__onPushButton)
		
		applicationModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module

## @}