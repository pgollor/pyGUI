##
# @file abstractModuleClass.py

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


from PyQt4.QtGui import QWidget, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox
import xml.dom.minidom as dom
from xmlHelper import *
import guiLogger.client as logClient
from delete import delete
import logging


LOGLEVEL = logging.DEBUG


## @brief abstract module class
# 
class abstractModuleClass(QWidget):
	## class types
	enumClassType = {"setting" : 1, "application" : 2, "hidden" : 3}

	# ---------- Private ----------
	
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	def __init__(self, parent):
		QWidget.__init__(self, parent)
		
		self.__initVars()
		
		self.__p_parent = parent
		self._p_loggerClient = logClient.clientLogger()
	#end __init__
	
	## @brief class del function
	# @param self The object pointer.
	def __del__(self):
		if (self._p_loggerClient != False):
			delete(self._p_loggerClient)
			self._p_loggerClient = False
		# end if

		self.__initVars()
	# end __del__
	
	## @brief initialize class variables
	# @param self The object pointer.	
	def __initVars(self):
		## python logger object
		self._p_logger = False
		
		## logger client object
		self._p_loggerClient = False
		
		## custom module settings list
		self._l_customSettings = []
		
		## GUI modules list
		self.__l_modules = list()
		
		## module path
		self.__v_modulePath = ""
		
		## path from main.py
		self.__v_parentPath = ""
		
		## module class name
		self.__v_className = ""
		
		## @brief module class type
		# @see enumClassType
		self.__v_classType = 0
		
		## module display name
		self.__v_displayName = "foo"
		
		## dom settings handle
		self.__p_settingsHandle = False
		
		## parent object
		self.__p_parent = False
		
		## module includes as dict
		self.__d_includes = dict()
		
		## module settings as dict
		self.__d_settings = dict()
		
		## module setting xml list
		self.__l_settingXml = []
		
		## debug
		self.__v_debug = False
		
		## progressbar object
		self.__p_progressBar = False
		
		## progressbar thread object
		self.__p_progressBarThread = False
	# end __initVars
	
	## @brief create xml for custom module settings
	# @param self The object pointer.
	# @retval boolean
	def __createCustomSettings(self):
		if (self._l_customSettings == []):
			return False
		# end if
		
		custom = self.__p_settingsHandle.getElementsByTagName("custom")
		if (len(custom) > 0):
			custom = custom[0]
			custom.unlink()
		else:
			custom = self.__p_settingsHandle.createElement("custom")
		# end if
		
		# create xml string from dict list
		
		if (not writeXMLRec(self.__p_settingsHandle, custom, self._l_customSettings)):
			self._p_logger.critical("can't save custom settings");
			return False
		# end if
		
		return True
	# end __createCustomSettings
	
	## @brief load custom module settings from xml
	# @param self The object pointer.
	# @retval boolean
	def __loadCustomSettings(self):
		custom = self.__p_settingsHandle.getElementsByTagName("custom")
		if (len(custom) == 0):
			self._l_customSettings = []
			return False
		# end if
		
		self._l_customSettings = readXMLRec(custom[0])
		
		return True
	# end __loadCustomSettings
	
	# ---------- Private ----------


	# ---------- Protected ----------
	
	## @brief interface: set class Type
	# @param self The object pointer.
	# @param classType class type
	# @see enumClassType
	def _setClassType(self, classType):
		if (classType in self.enumClassType):
			self.__v_classType = self.enumClassType[classType]
		else:
			self.__error("Can not set class type to: " + str(classType))
		# end if
	# end _setClassType

	## @brief interface: set module name
	# @param self The object pointer.
	# @param name module name
	def _setName(self, name):
		self.__v_className = name
	# end setName

	## @brief interface: get GUI module handle(s)
	# @param self The object pointer.
	# @param name return only one module handle
	def _getModuleArray(self, name = ""):
		if (name == ""):
			return self.__l_modules
		# end if
		
		if (name in self.__l_modules and self.__l_modules[name]['handle'] != False):
			return self.__l_modules[name]
		else:
			return False
		# end if
	# end getModuleArray

	## @brief interface: return parent object
	# @param self The object pointer.
	# @retval object parent object
	def _getParent(self):
		return self.__p_parent
	# end _getParent
	
	## @brief interface: return progressbar object
	# @param self The object pointer.
	# @retval object progressbar object
	def _getProgressBar(self):
		return self.__p_progressBar
	# end getProgressBar
	
	## @brief interface: set settings
	# @param self The object pointer.
	def _setSettings(self, settings):
		self.__d_settings = settings
	# end

	# ---------- Protected ----------


	# ---------- Public ----------
	
	## @brief virtual function: initialize function before settings were loaded
	# @param self The object pointer.
	def initPreSettings(self):
		"virtual"
	# end initPreSettings

	## @brief virtual function: initialize the module 
	# @param self The object pointer.
	def initModule(self):
		"virtual"
	# end initModule

	## @brief virtual function: initialize the module GUI
	# @param self The object pointer.
	def initGUI(self):
		"virtual"
	# end initGUI

	## @brief virtual function: execute this function before module closed
	# @param self The object pointer.
	def onClose(self):
		"virtual"
	# end onClose
	
	## @brief virtual function: execute this function before settings save
	# @param self The object pointer.
	def onPreClose(self):
		"virtual"
	# end onPreClose

	## @brief virtual function: execute if this module is the current module
	# @param self The object pointer.
	def onActive(self):
		"virtual"
	# end onActive

	## @brief set module array from mainWindow
	# @param self The object pointer.
	# @param array module array as list
	def setModuleArray(self, array):
		self.__l_modules = array
	# end setModuleArray

	## @brief set module path from mainWindow
	# @param self The object pointer.
	# @param modulePath module path
	# @param parentPath parent path
	def setModulePath(self, modulePath, parentPath):
		self.__v_modulePath = modulePath
		self.__v_parentPath = parentPath
	# end _setModulePath

	## @brief get module path
	# @param self The object pointer.
	# @param absolute true: return absolute module path
	# @retval path module path
	def getModulePath(self, absolute = False):
		path = self.__v_modulePath
		
		if (absolute):
			path = self.__v_parentPath + "/" + path
		# end if
		
		return path
	# end getModulePath

	## @brief set includes from mainWindow
	# @param self The object pointer.
	def setIncludes(self, includes):
		self.__d_includes = includes
	# end setIncludes
	
	## @brief set progressbar object
	# @param self The object pointer.
	def setProgressBar(self, pBar):
		self.__p_progressBar = pBar
	# end setProgressBar
	
	## @brief set progressbar thread object
	# @param self The object pointer.
	def setProgressBarThread(self, pBar):
		self.__p_progressBarThread = pBar
	# end setProgressBarThread
	
	## @brief interface: return progressbar thread object
	# @param self The object pointer.
	# @retval object progressbar thread object
	def _getProgressBarThread(self):
		return self.__p_progressBarThread
	# end getProgressBarThread

	## @brief get module includes
	# @param self The object pointer.
	# @retval dict includes
	def getIncludes(self):
		return self.__d_includes
	# end getIncludes
	
	## @brief interface: for global file management module
	# @param self The object pointer.
	def getFileManagement(self):
		pass
	# end getFileManagement
	
	## @brief save modle settings
	# @param self The object pointer.
	def saveSettings(self):
		self.__createCustomSettings()
		
		# get settings handler
		settings = self.__p_settingsHandle.getElementsByTagName("settings")[0]
		
		# delete all old elements
		settings.unlink()

		defaultXmlList = self.__l_settingXml['module']['items'][0]['default_settings']['items'][0]
		xmlList = self.__l_settingXml['module']['items'][0]['settings']['items'][0]
		
		# search for difference between default and real current settings
		for elemType in defaultXmlList:
			if (elemType not in xmlList):
				xmlList[elemType] = defaultXmlList[elemType]
				continue
			# end if
			
			for item in defaultXmlList[elemType]['items']:
				# search item in current settings
				found = False
				
				for currentItem in xmlList[elemType]['items']:
					if (item['name'] == currentItem['name']):
						found = True
						break
					# end if
				# end for

				if (not found):
					xmlList[elemType]['items'].append(item)
				# end if
			# end for
		# end for

		loadGuiChange(xmlList, self)

		if (not writeXMLRec(self.__p_settingsHandle, settings, xmlList)):
			self._p_logger.critical("Can't save settings!!!");
			return False
		# end if

		writer = open(self.__v_modulePath + "/" + self.__v_className + ".xml", "w", encoding='utf-8')
		self.__p_settingsHandle.writexml(writer, encoding='utf-8')
		writer.close()
	# end _saveSettings

	## @brief load module settings
	# @param self The object pointer.
	def loadSettings(self):
		self.loadDefaultSettings()
		self.__loadCustomSettings()

		setGuiSettings(self.__l_settingXml['module']['items'][0]['settings']['items'][0], self)
	# end _loadSettings
	
	## @brief load default module settings
	# @param self The object pointer.
	def loadDefaultSettings(self):
		self.__p_settingsHandle = dom.parse(self.__v_modulePath + "/" + self.__v_className + ".xml")
		self.__l_settingXml = readXMLRec(self.__p_settingsHandle)

		# get display name
		displayName = ''
		if ('displayname' not in self.__l_settingXml['module']['items'][0]['main']['items'][0]):
			self._p_logger.critical("No Attribute displayname was found in xml file!!!")
			return False
		else:
			displayName = self.__l_settingXml['module']['items'][0]['main']['items'][0]['displayname']['content']
		# end if
		self.__v_displayName = displayName

		# save settings from gui elements
		setGuiSettings(self.__l_settingXml['module']['items'][0]['default_settings']['items'][0], self)
	# end _loadDefaultSettings

	## @brief get module class type
	# @param self The object pointer.
	# @retval classType class type as integer
	# @see enumClassType
	def getClassType(self):
		for k,v in self.enumClassType.items():
			if (v == self.__v_classType):
				return k
			# end if
		# end for
	# end getClassType

	## @brief get module name
	# @param self The object pointer.
	# @retval name class name
	def getName(self):
		return self.__v_className
	# end getName
	
	## @brief set display name from mainWindow
	# @param self The object pointer.
	# @param name GUI module name
	def setDisplayName(self, name):
		self.__v_displayName = name
	# end setDisplayName

	## @brief get display name
	# @param self The object pointer.
	# @retval name display name
	def getDisplayName(self):
		return self.__v_displayName
	# end getDisplayName
	
	## @brief get GUI field values
	# @param self The object pointer.
	# @param parents parent objects as list
	# @retval fieldValues filed values as list
	#
	# <pre>
	# valid parent objects are:
	# - QLineEdit
	# - QCheckBox
	# - QComboBox
	# - QRadioButton
	# - QGroupBox
	# </pre>
	def getFieldValues(self, parents = False):
		if not parents:
			return False
		# end if

		fieldValues = {}
		for parent in parents:
			widgets = parent.findChildren((QLineEdit, QCheckBox, QComboBox, QRadioButton, QGroupBox))
			
			for widget in widgets:
				name = widget.objectName()
				if type(widget) == QLineEdit:
					name = name[8::]
					value = widget.text()
				elif type(widget) == QCheckBox:
					name = name[8::]
					value = widget.isChecked()
				elif type(widget) == QComboBox:
					name = name[8::]
					value = widget.currentText()
				elif type(widget) == QGroupBox:
					if widget.isCheckable():
						name = name[8::]
						value = widget.isChecked()
					else:
						continue
				elif type(widget) == QRadioButton:
					name = name[11::]
					value = widget.isChecked()
				# end if
				
				#print(name,":",value, type(value))
				fieldValues[name] = value
			# end for
		#end for

		return fieldValues
	# end getFieldValues

	## @brief set GUI values
	# @param self The object pointer.
	# @param values values as list
	def setValues(self, values):
		for name, value in values.items():
			self.setValue(name, value)
		# end for
	# end setValues
	
	## @brief get values
	# @param self The object pointer.
	# @retval values values list
	def getValues(self):
		values = dict()
		for key, __value in self.__d_settings.items():
			values[key] = self.getValue(key)
		#end for

		return values
	#end getValues

	## @brief set value
	# @param self The object pointer.
	# @param name object name
	# @param value object value
	def setValue(self, name, value):
		if name in self.__d_settings:
			if value == "":
				self._p_logger.warn("Parameter \"" + name + "\" has empty value")
				#print("Parameter \"" + name + "\" has empty value")
				return
			# end if
			Type = self.__d_settings[name]["Type"]
			if Type == "float":
				val = float(value)
				if val > self.__d_settings[name]["maxValue"]:
					val = self.__d_settings[name]["maxValue"]
				# end if
				if val < self.__d_settings[name]["minValue"]:
					val = self.__d_settings[name]["minValue"]
				#end if
				self.__d_settings[name]["value"] = val
			elif Type == "int":
				val = int(value)
				if val > self.__d_settings[name]["maxValue"]:
					val = self.__d_settings[name]["maxValue"]
				# end if
				if val < self.__d_settings[name]["minValue"]:
					val = self.__d_settings[name]["minValue"]
				#end if
				self.__d_settings[name]["value"] = val
			elif Type == "string":
				self.__d_settings[name]["value"] = value
			elif Type == "bool":
				self.__d_settings[name]["value"] = bool(value)
			else:
				self._p_logger.warn("Type \"" + Type + "\" is not supported")
				#print("Type \"" + Type + "\" is not supported")
		else:
			self._p_logger.warn("Parameter \"" + name + "\" is not available")
			#print("Parameter \"" + name + "\" is not available")
		# end if
	# end setValue

	## @brief get value
	# @param self The object pointer.
	# @param name object value
	# @retval value object value
	def getValue(self, name):
		if name in self.__d_settings:
			return self.__d_settings[name]["value"]
	# end getValue
	
	# ---------- Public ----------

# end class abstractModuleClass


## @brief setting module class
# @param self The object pointer.
class settingModuleClass(abstractModuleClass):
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	# @param name module name
	# 
	# set current module name and class type
	# create client logger object
	def __init__(self, parent, name):
		abstractModuleClass.__init__(self, parent)
		self._setName(name)
		self._setClassType("setting")
		
		# init logger
		self._p_loggerClient.init(name, LOGLEVEL)
		self._p_logger = self._p_loggerClient.getLogger()
	# end __init__

# end class settingModuleClass


## @brief application module class
# @param self The object pointer.
class applicationModuleClass(abstractModuleClass):
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	# @param name module name
	# 
	# set current module name and class type
	# create client logger object
	def __init__(self, parent, name):
		abstractModuleClass.__init__(self, parent)
		self._setName(name)
		self._setClassType("application")
		
		# init logger
		self._p_loggerClient.init(name, LOGLEVEL)
		self._p_logger = self._p_loggerClient.getLogger()
	# end __init__

# end class applicationModuleClass


## @brief hidden module class
# @param self The object pointer.
class hiddenModuleClass(abstractModuleClass):
	
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	# @param name module name
	# 
	# set current module name and class type
	# create client logger object
	def __init__(self, parent, name):
		abstractModuleClass.__init__(self, parent)
		self._setName(name)
		self._setClassType("hidden")
		
		# init logger
		self._p_loggerClient.init(name, LOGLEVEL)
		self._p_logger = self._p_loggerClient.getLogger()
	# end __init__

# end class hiddenModuleClass
