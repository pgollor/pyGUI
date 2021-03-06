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
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
# 
# @brief This is a demo module to demonstrate the global progressbar functionality. 


from abstractModuleClass import applicationModuleClass


class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
		
		self.setDisplayName('testProgressBar')
	# end __init__

	def __onPushButtonInit(self):
		self.p_progressBar.init(self, printModuleName = True)
		
		self.lineEditPbValue.setEnabled(True)
	# end __onPushButtonInit
	
	def __onPushButtonSet(self):
		self.p_progressBar.setValue(self._getSettings('PbValue'))
	# end __onPushButtonSet
	
	def __onPushButtonClear(self):
		self.p_progressBar.clear()
		self.lineEditPbValue.setText(0);
	# end __onPushButtonClear
	
	def __onPushButtonDisable(self):
		self.p_progressBar.disable()
		
		self.lineEditPbValue.setEnabled(False)
	# end __onPushButtonDisable

	# ---------- Private ----------


	# ---------- overrided functions ----------
	
	## @brief return default settings
	# @param self The object pointer.
	# @return settings dict
	def getDefaultSettings(self):
		d = {'PbValue': {'qName': 'lineEditPbValue', 'value': 0, 'minVal': 0, 'maxVal': 100}}
		
		return d;
	# end getDefaultSettings

	def initModule(self):
		applicationModuleClass.initModule(self)
	#end _initModule

	def initGUI(self):
		self.lineEditPbValue.setEnabled(False)
		self.lineEditPbValue.setText(0);
		
		self.pushButtonInit.clicked.connect(self.__onPushButtonInit)
		self.pushButtonSet.clicked.connect(self.__onPushButtonSet)
		self.pushButtonClear.clicked.connect(self.__onPushButtonClear)
		self.pushButtonDisable.clicked.connect(self.__onPushButtonDisable)
		
		# Update progress bar if enter in lien edit pressed.
		self.lineEditPbValue.returnPressed.connect(self.__onPushButtonSet)
		
		applicationModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
