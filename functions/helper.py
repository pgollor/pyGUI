##
# @file helper.py
# 
# @date 10.02.2015
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



from PyQt4.QtGui import QLabel, QTextEdit, QCheckBox, QRadioButton, QGroupBox,\
	QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QSlider, QPlainTextEdit
from functions.betterSlider import betterSlider
from PyQt4.QtCore import SIGNAL, QObject
from functools import partial
from functions.customGuiElements import abstractCustomLineEdit


## @brief check if checkClass in compareClassList
def classEqual(checkClass, compareClassList):
	if (type(compareClassList) == list and checkClass in compareClassList):
		return True
	# end if
	
	# convert classes to string
	checkClass = str(checkClass)
	compareClassList = str(compareClassList)
	
	# remove some sub strings
	checkClass = checkClass.replace('<class \'', '')
	
	if (compareClassList.find(checkClass) >= 0):
		
		return True
	# end if
	
	return False
# end if


## @brief convert string in True or False
# @param v string to convert
#
# supported strings for True
# - yes
# - true
# - t
# - 1
def str2bool(v):
	v = str(v)

	return v.lower() in ("yes", "true", "t", "1")
# end str2bool


## @brief class settings handler
#
class settingsHandler(QObject):
	supportedQtElements = (QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox, QSpinBox, QDoubleSpinBox, QSlider, QTextEdit, QPlainTextEdit)
	
	def __init__(self, module, savedSettings):
		QObject.__init__(self)
		# init variables
		self.__p_module = module
		self.__d_savedSettings = savedSettings
		self.__d_internalSettings = dict()
		self.__d_moduleSettings = dict()
		

		# get default settings from module
		defaultSettings = module.getDefaultSettings()
		if (defaultSettings == None):
			defaultSettings = dict()
		# end if
		
		# create internal settings struct
		self.__initInternalSettings(defaultSettings)
		
		# search for GUI elements
		self.__addGUIpointer()

		# set GUI values		
		self.__restoreGUIElements()
		
		# create settings dict als interface for the module
		self.__createModuleSettings()
		
		# connect all signals check for gui changes
		self.__connectGUIelementSignals()
	# end __init__
	
	## @brief Qt slot for combo box changes
	# @param self The object pointer.
	# @param elemName element name
	# @param elem Qt element pointer
	# @param index current index
	def __onComboBoxValidChange(self, elemName, elem, index):
		self.__d_moduleSettings[elemName] = elem.currentText()
		self.__d_internalSettings[elemName]['value'] = elem.currentText()
	# end
	
	## @brief Qt slot for spin box changes
	# @param self The object pointer.
	# @param elemName element name
	# @param elem Qt element pointer
	# @param index current index
	def __onSpinBoxValidChange(self, elemName, elem, index):
		self.__d_moduleSettings[elemName] = elem.value()
		self.__d_internalSettings[elemName]['value'] = elem.value()
	# end
	
	## @brief Qt slot for some GUI element changes.
	# @param self The object pointer.
	# @param elemName element name
	# @param elemValue element value
	def __onValidChange(self, elemName, elemValue):
		self.__d_moduleSettings[elemName] = elemValue
		self.__d_internalSettings[elemName]['value'] = elemValue
	# end __onValidChange
	
	## @brief Qt slot for text edit changes.
	# @param self The object pointer.
	# @param elemName element name
	# @param elemHandle element handle
	def __onTextEditChanged(self, elemName, elemHandle):
		# debug putput
		#print('========== SIGNAL ==========')
		#print(elemName)
		#print(elemHandle)
		#print(elemHandle.metaObject().className())
		#print(elemHandle.toPlainText())
		#print(elemHandle.toHtml())
		#print('========== SIGNAL ==========')

		self.__d_moduleSettings[elemName] = elemHandle.toPlainText()
		self.__d_internalSettings[elemName]['value'] = elemHandle.toPlainText()
	# end __onTextEditChanged
	
	## @brief
	# @param self The object pointer.
	def __createModuleSettings(self):
		self.__d_moduleSettings = dict()
		
		for elemName, elemDict in self.__d_internalSettings.items():
			self.__d_moduleSettings[elemName] = elemDict['value']
		# end for
	# end __createSettingsDict
	
	## @brief
	# @param self The object pointer.
	def __connectGUIelementSignals(self):
		for elemName, elemDict in self.__d_internalSettings.items():
			if ('qElem' not in elemDict or elemDict['qElem'] == None):
				continue
			# end if
			
			elem = elemDict['qElem']
			elemClass = type(elem)
			
			if (issubclass(elemClass, QLineEdit)):
				if (issubclass(elemClass, abstractCustomLineEdit)):
					sig = SIGNAL('validChange(PyQt_PyObject, PyQt_PyObject)')
					dest = self.__onValidChange
				else:
					sig = SIGNAL('textChanged(QString)')
					dest = partial(self.__onValidChange, elemName)
				# end if
			elif (issubclass(elemClass, QTextEdit)):
				sig = SIGNAL('textChanged()')
				dest = partial(self.__onTextEditChanged, elemName, elem)
			elif (issubclass(elemClass, QCheckBox) or issubclass(elemClass, QGroupBox) ):
				sig = SIGNAL('clicked(bool)')
				dest = partial(self.__onValidChange, elemName)
			elif (issubclass(elemClass, QRadioButton)):
				sig = SIGNAL('toggled(bool)')
				dest = partial(self.__onValidChange, elemName)
			elif (issubclass(elemClass, QComboBox)):
				sig = SIGNAL('currentIndexChanged(int)')
				dest = partial(self.__onComboBoxValidChange, elemName, elem)
			elif (issubclass(elemClass, QSpinBox)):
				sig = SIGNAL("valueChanged(int)")
				dest = partial(self.__onSpinBoxValidChange, elemName, elem)
			elif (issubclass(elemClass, QDoubleSpinBox)):
				sig = SIGNAL("valueChanged(double)")
				dest = partial(self.__onSpinBoxValidChange, elemName, elem)
			elif (issubclass(elemClass, QSlider)):
			#elif (classEqual(elemClass, betterSlider)):
				sig = SIGNAL('changed(PyQt_PyObject)')
				dest = partial(self.__onValidChange, elemName)
			else:
				continue
			# end if
		
			self.disconnect(elem, sig, dest)
			self.connect(elem, sig, dest)
		# end for
	# end __connectGUIelementSignals
	
	## @brief add GUI pointer to internal settings dict
	# @param self The object pointer.
	def __addGUIpointer(self):
		for elemName, elemDict in self.__d_internalSettings.items():
			if ('qName' not in elemDict):
				continue
			# end if

			qName = elemDict['qName']
			
			# Wenn qname = None handelt es sich um ein Modul eigene Einstellung ohne Qt Bindung.
			if (qName == None):
				continue
			# end if
			
			# finde GUI Elemente zu den settings
			elem = self.__p_module.findChild(settingsHandler.supportedQtElements, qName)
			
			if (elem == None):
				continue
			# end if

			# add qt pointer
			self.__d_internalSettings[elemName]['qElem'] = elem
		# end for
	# end __addGUIpointer
	
	## @brief initialize internal settings dict
	# @param self The object pointer.
	def __initInternalSettings(self, defaultSettings):
		if (len(self.__d_internalSettings.keys()) == 0):
			intSettings = dict()
		else:
			intSettings = self.__d_internalSettings
		# end if
		
		for elemName, elemDict in defaultSettings.items():
		# Nur default settings benutzen, wenn keine user eigenen Einstellungen existieren.
			if (elemName in self.__d_savedSettings):
				intSettings[elemName] = self.__d_savedSettings[elemName]
			else:
				intSettings[elemName] = elemDict
			# end if
		# end for
		
		self.__d_internalSettings = intSettings
	# end __initInternalSettings

	## @brief restore GUI values with settings from self.__d_internalSettings
	# @param self The object pointer.
	def __restoreGUIElements(self):
		for elemDict in self.__d_internalSettings.values():
			if ('qElem' not in elemDict):
				continue
			# end if
			
			# Falls das Qt Element nicht unterstuetzt wird, soll es nicht behandelt werden.
			elem = elemDict['qElem']
			if (elem == None):
				continue
			# end if
			
			elemClass = type(elem)
			value = elemDict['value']
			
			# special handling for custom line edits
			if (issubclass(elemClass, QLineEdit)):
				elemFunctions = dir(elem)
				
				if ('maxVal' in elemDict and 'minVal' in elemDict and 'setMinMax' in elemFunctions):
					elem.setMinMax(elemDict['minVal'], elemDict['maxVal'])
				# end if
				
				if ('list' in elemDict and 'setList' in elemFunctions):
					elem.setList(elemDict['list'])
				# end if

				#if (classEqual(elemClass, customListLineEdit)):
				#	
				# end if
			# end if
	
			# get values from qt elements
			if (issubclass(elemClass, QLineEdit) or issubclass(elemClass, QLabel)):
				elem.setText(value)
			elif (issubclass(elemClass, QTextEdit)):
				elem.setPlainText(value)
			elif (issubclass(elemClass, QCheckBox) or issubclass(elemClass, QRadioButton) or issubclass(elemClass, QGroupBox) ):
				elem.setChecked(value)
			elif (issubclass(elemClass, QComboBox)):
				index = elem.findText(str(value))

				if (index < 0):
					index = 0;
				# end if
				
				elem.setCurrentIndex(index)
			elif (issubclass(elemClass, QSpinBox) or issubclass(elemClass, QDoubleSpinBox)):
				if ('step' in elemDict):
					elem.setSingleStep(elemDict['step'])
				# end if
				
				if ('minVal' in elemDict):
					elem.setMinimum(elemDict['minVal'])
				# end if
				
				if ('maxVal' in elemDict):
					elem.setMaximum(elemDict['maxVal'])
				# end if
				
				elem.setValue(value)
			#elif (issubclass(elemClass, QSlider)):
			#	print("slider")
			#elif (issubclass(elemClass, betterSlider)):
			elif (classEqual(elemClass, betterSlider)):
				# own better slider class
				# supported elements for betterSlider class:
				# type: integer, double, logarithm
				# value: current value
				# minVal: minimum value
				# maxVal: maximum value
				# step: step size for normal change (optional not for logarithm)
				# pageStep: step size for page change (optional not for logarithm)
				# connectedLabels: list for connected labels separated by , (optional)
				# connectedLineEdits: list for connected line edits separated by , (optional)
				
				if ('type' not in elemDict or 'value' not in elemDict or 'maxVal' not in elemDict or 'minVal' not in elemDict):
					continue
				# end if
				
				# set step size to default if not available
				if ('step' not in elemDict):
					elemDict['step'] = 1
				# end if
				
				# set page step to default if not available
				if ('pageStep' not in elemDict):
					elemDict['pageStep'] = 10
				# end if

				# init betterSlider with type and values
				try:
					if (elemDict['type'] == 'integer'):
						elem.initInteger(int(elemDict['minVal']), int(elemDict['maxVal']), int(elemDict['step']))
						elem.setPageStep(int(elemDict['pageStep']))
						elem.setEditedValue(int(value))
					elif (elemDict['type'] == 'double'):
						elem.initDouble(float(elemDict['minVal']), float(elemDict['maxVal']), float(elemDict['step']))
						elem.setPageStep(float(elemDict['pageStep']))
						elem.setEditedValue(float(value))
					elif (elemDict['type'] == 'logarithm'):
						elem.initLogarithm(float(elemDict['minVal']), float(elemDict['maxVal']))
						elem.setEditedValue(float(value))
					else:
						continue
					# end if
				except:
					continue
				# end try
				
				# add conected items
				if ('connectedLabels' in elemDict):
					connectedLabels = elemDict['connectedLabels']
					for labelName in connectedLabels:
						label = self.__p_module.findChild((QLabel), labelName)
						
						if (label != None):
							elem.connectLabel(label)
						# end if
					# end for
				# end if

				if ('connectedLineEdits' in elemDict):
					connectedLineEdits = elemDict['connectedLineEdits']
					for lineeditName in connectedLineEdits:
						lineedit = self.__p_module.findChild((QLineEdit), lineeditName)
						
						if (lineedit != None):
							elem.connectLineEdit(lineedit)
						# end if
					# end for
				# end if
			# end if
		# end for
	# end restoreGUIelements
	
	## @brief return settings dict for modules
	# @param self The object pointer.
	def getModuleSettings(self):
		return self.__d_moduleSettings
	# end getModuleSettings
	
	def setModuleSettings(self, key, value):
		self.__d_moduleSettings[key] = value
		self.__d_internalSettings[key]['value'] = value
		
		return self.__d_moduleSettings[key]
	# end setModuleSettings
	
	## @brief return settings struct for saving
	def getSaveSettings(self):
		settings = dict()
		
		for key in self.__d_internalSettings:
			settings[key] = self.__d_internalSettings[key].copy()
			if ('qElem' in settings[key] and settings[key]['qElem'] != None):
				settings[key].pop('qElem')
			# end if
		# end for
		
		return settings
	# end getSettings
	
	## @brief load default settings 
	# @param self The object pointer.
	def loadDefault(self):
		defaultSettings = self.__p_module.getDefaultSettings()
		
		# load default settings and store this into internal settings
		for key, val in defaultSettings.items():
			if (key not in self.__d_internalSettings):
				self.__d_internalSettings[key] = dict()
			# end if
			
			for subKey in val:
				self.__d_internalSettings[key][subKey] = defaultSettings[key][subKey]
			# end for
		# end for
		
		self.__restoreGUIElements()
		self.__createModuleSettings()
	# end loadDefault
	
	def load(self, savedSettings):
		self.__d_savedSettings = savedSettings
		
		# load settings and store this into internal settings
		for key, val in savedSettings.items():
			for subKey in val:
				#if (subKey != "qName" and key in self.__d_internalSettings):
				if (key in self.__d_internalSettings):
					self.__d_internalSettings[key][subKey] = savedSettings[key][subKey]
				# end if
			# end for
		# end for
		
		self.__restoreGUIElements()
		self.__createModuleSettings()
	# end load
	
	def delete(self):
		self.__d_savedSettings = dict()
		self.__d_internalSettings = dict()
		self.__d_moduleSettings = dict()
	# end delete
	
# end class setttingsHandler

