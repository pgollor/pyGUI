## @file testProgressBar.py
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
# @brief This is a demo module to demonstrate the global progressbar functionality. 


from PyQt4.QtCore import SIGNAL
from abstractModuleClass import applicationModuleClass


class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
	# end __init__

	def __onPushButtonInit(self):
		pb = self._getProgressBar()
		pb.init(self, printModuleName = True)
	# end __onPushButtonInit
	
	def __onPushButtonSet(self):
		pb = self._getProgressBar()
		val = int(self.lineEditValue.text())
		pb.setValue(val)
	# end __onPushButtonSet
	
	def __onPushButtonClear(self):
		pb = self._getProgressBar()
		pb.clear()
	# end __onPushButtonClear
	
	def __onPushButtonDisable(self):
		pb = self._getProgressBar()
		pb.disable()
	# end __onPushButtonDisable

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		pass
	#end _initModule

	def initGUI(self):
		self.connect(self.pushButtonInit, SIGNAL("clicked()"), self.__onPushButtonInit)
		self.connect(self.pushButtonSet, SIGNAL("clicked()"), self.__onPushButtonSet)
		self.connect(self.pushButtonClear, SIGNAL("clicked()"), self.__onPushButtonClear)
		self.connect(self.pushButtonDisable, SIGNAL("clicked()"), self.__onPushButtonDisable)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
