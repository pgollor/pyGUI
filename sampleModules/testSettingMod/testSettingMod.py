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
# @defgroup testSettingMod
# 
# @brief This is a tiny sample setting module.
# 
# @section set-mod Setting Module
# 
# @subsection req-func Required functions:
# -	<pre>__init__(self, parent, name):
#  settingModuleClass.__init__(self, parent, name)
#
#  self.setDisplayName('testSetting')</pre>
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
# @{

from abstractModuleClass import settingModuleClass


class module(settingModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		settingModuleClass.__init__(self, parent, name)
		
		self.setDisplayName('testSetting')
	# end __init__

	## @brief Qt slot which is connected to pushButton.
	# @param self The object pointer.
	def __onPushButton(self):
		self.lineEditFoo.setText("push button were pressed")
	# end __onPushButton

	# ---------- Private ----------


	# ---------- overrided functions ----------
	
	## @brief return default settings
	# @param self The object pointer.
	# @return settings dict
	def getDefaultSettings(self):
		d = {
			'Foo': {'qName': "lineEditFoo", 'value': "default text from ini"},
			'Test': {'qName': "checkBoxTest", 'value': True},
			'RB1': {'qName': "radioButtonRB1", 'value': True},
			'RB': {'qName': "radioButtonRB2", 'value': False}
		}
		
		return d
	# end getDefaultSettings

	## @brief Function to initialize the GUI
	# @param self The object pointer.
	# 
	# In this function you have to connect all Qt elements and so on.
	def initGUI(self):
		self.pushButton.clicked.connect(self.__onPushButton)
		
		settingModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module

## @}