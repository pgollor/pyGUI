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
# @brief This is a tiny demo module.


from abstractModuleClass import applicationModuleClass


##
# @brief application module for PyGUI
class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
	# end __init__
	
	def __onPushButton(self):
		print(self._getSettings())
	# end if

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
