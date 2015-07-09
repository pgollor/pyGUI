##
# @file testCustomGuiElements.py
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
# @brief This is a tiny demo module hot how to use the custom GUI elements.


from abstractModuleClass import applicationModuleClass
from PyQt4.QtCore import pyqtSlot


class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
		
		self.setDisplayName("testCustomGuiElements")
	# end __init__
	
	## @brief Qt slot which is connected to pushButton.
	# @param self The object pointer.
	def __onPushButton(self):
		print('push Button pressed')
		
		print(self._getSettings())
		self._setSettings('foo', 465)
		print(self._getSettings('foo'))
	# end if

	# ---------- Private ----------


	# ---------- virtual functions ----------
	
	## @brief return default settings
	# @param self The object pointer.
	# @return settings dict
	def getDefaultSettings(self):
		d = {
				"foo": {"qName": None, "value": {123, "23243"}}, ## sample for user custom settings for none GUI objects
				"Integer": {"qName": "lineEditInteger", "value": 20, "minVal": 20, "maxVal": 50},
				"Normal": {"qName": "lineEditNormal", "value": "sdasda"},
				"List": {"qName": "lineEditList", "value": "foo", "list": ["foo", "bar"]},
				"TestCheck": {"qName": "checkBoxTestCheck", "value": False},
				"TestRadio": {"qName": "radioButtonTestRadio", "value": True},
				"TestGroup": {"qName": "groupBoxTestGroup", "value": True},
				"IntegerBox": {"qName": "comboBoxIntegerBox", "value": 99},
				"StringBox": {"qName": "comboBoxStringBox", "value": "sieben"},
				"Float": {"qName": "lineEditFloat", "value": 1, "minVal": 1.0, "maxVal": 2.0},
				"intSl": {
									"qName": "horizontalSliderInteger",
									"value": 4,
									"minVal": -10,
									"maxVal": 10,
									"step": 2,
									"pageStep": 2,
									"connectedLabels": ["labelIntegerSlider"],
									"connectedLineEdits": ["lineEditIntegerSlider"]
									},
				"floatSl": {
									"qName": "horizontalSliderFloat",
									"value": 1,
									"minVal": -2,
									"maxVal": 10,
									"step": 0.2,
									"pageStep": 2,
									"connectedLabels": ["labelFloatSlider"],
									"connectedLineEdits": ["lineEditFloatSlider"]
									},
				"logSl": {
									"qName": "horizontalSliderLogarithm",
									"value": 1,
									"minVal": 1,
									"maxVal": 100000,
									"pageStep": 100,
									"connectedLabels": ["labelLogarithmSlider"],
									"connectedLineEdits": ["lineEditLogarithmSlider"]
									},
				"SBD": {"qName": "doubleSpinBoxSBD", "value": 2, "minVal": 0, "maxVal": 10, "step": 0.1},
				"SBN": {"qName": "spinBoxSBN", "value": 2, "minVal": 0, "maxVal": 10, "step": 1}
			}

		return d
	# end getDefaultSettings
	
	@pyqtSlot(int)
	@pyqtSlot(float)
	def __onSliderChange(self, value):
		self._p_logger.info('Slider change to %s.', str(value))
	# end __onSliderChange
	
	@pyqtSlot(int)
	def __onIntegerSliderChange(self, value):
		self._p_logger.info('Integer slider change to %i.', value)
	# end __onFloatSliderChange
	
	@pyqtSlot(float)
	def __onFloatSliderChange(self, value):
		self._p_logger.info('Float slider change to %0.2f.', value)
	# end __onFloatSliderChange
	
	@pyqtSlot(int)
	def __onLogarithmSliderChange(self, value):
		self._p_logger.info('Logarithm slider change to %i.', value)
	# end __onFloatSliderChange

	## @brief Function to initialize the GUI
	# @param self The object pointer.
	# 
	# In this function you have to connect all Qt elements and so on.
	def initGUI(self):
		# connect signals
		self.pushButton.clicked.connect(self.__onPushButton)
		self.horizontalSliderInteger.sigChanged[int].connect(self.__onIntegerSliderChange)
		self.horizontalSliderInteger.sigChanged[int].connect(self.__onSliderChange)
		self.horizontalSliderFloat.sigChanged[float].connect(self.__onFloatSliderChange)
		self.horizontalSliderFloat.sigChanged[float].connect(self.__onSliderChange)
		self.horizontalSliderLogarithm.sigChanged[float].connect(self.__onLogarithmSliderChange)
		self.horizontalSliderLogarithm.sigChanged[float].connect(self.__onSliderChange)
		
		applicationModuleClass.initGUI(self)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
