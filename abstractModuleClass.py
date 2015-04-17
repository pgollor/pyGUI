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
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


import os, sys, logging
from PyQt4.QtCore import SIGNAL, QSize, pyqtSignal
from PyQt4.QtGui import QWidget, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QSlider,\
	QCloseEvent
import xml.dom.minidom as dom
from functions.xmlHelper import readXMLRec, writeXMLRec, loadGuiChange,	setGuiSettings
from functions.delete import delete
from functions.menu import applicationMenuButton
from functools import partial
# try to import plotengine
try:
	g_plotWindowSupport = True
	from functions.plotEngine import plotWindow
	from guiqwt.builder import make
except:
	g_plotWindowSupport = False
	sys.stderr.write('Plot engine can not be loaded. You can use this GUI only without plot engine support!\r\n')
# end try



## @brief abstract module class
# 
class abstractModuleClass(QWidget):
	global g_plotWindowSupport

	## static class types
	enumClassType = {"setting" : 1, "application" : 2, "hidden" : 3}
	d_plots = dict()
	p_progressBar = False
	p_progressBarThread = False
	d_modules = []
	plotWindowSupport = g_plotWindowSupport

	# ---------- Private ----------
	
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	def __init__(self, parent, name):
		QWidget.__init__(self, parent)
		
		self.__initVars()
		
		# set parent pointer
		self.__p_parent = parent
		
		# set class name
		self.__v_className = name
		
		# add and initialize logger
		self._p_logger = logging.getLogger(name)
		self._p_logger.setLevel(logging.DEBUG) # set log level to debug for all modules
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
		
		## module path
		self.__v_modulePath = ""
		
		## path from main.py
		self.__v_parentPath = ""
		
		## module class name
		self.__v_className = ""
		
		## @brief module class type
		# @see enumClassType
		self.__v_classType = 0
		
		## parent object
		self.__p_parent = False
		
		## module includes as dict
		self.__d_includes = dict()
		
		## debug
		self.__v_debug = False
	# end __initVars

	
	# ---------- Private ----------


	# ---------- Protected ----------
	
	## @brief generate new plot
	# @param name: plot name
	# @param x: x data vector
	# @param y: y data vektor
	# @return new curve plot
	def _plot(self, name, x, y, *args, **kwargs):
		if (not abstractModuleClass.plotWindowSupport):
			return False
		# end if

		# get new dialog
		window = self._newPlotWindow(name)
		
		curve = make.curve(x, y, color="b", linestyle="DashLine")
		plot = window.addCurvePlot(curves = curve, *args, **kwargs)

		# show plot
		window.show()
		
		return plot
	# end _plot
	
	def _newPlotWindow(self, name, autoReInit = True):
		if (not abstractModuleClass.plotWindowSupport):
			return False
		# end if

		plots = abstractModuleClass.d_plots

		if (name in plots):
			if (autoReInit):
				plots[name].reInit()
			# end if
			
			return plots[name]
		# end if

		window = plotWindow(parent = self.parentWidget())
		
		plots[name] = window

		return window
	# end _newPlotWindow
	
	def _getPlotWindow(self, name):
		plots = abstractModuleClass.d_plots
		
		if (name not in plots):
			#self._p_logger.error("There is no plot available with the given name.")
			return False
		# end if

		return plots[name]
	# end _getPlot
	
	#def closeEvent(self, *args, **kwargs):
	def closeEvent(self, event):
		self.emit(SIGNAL('onClose()'))
		self.emit(SIGNAL('onClose(PyQt_PyObject)'), self)
		
		#return QWidget.closeEvent(self, *args, **kwargs)
		return QWidget.closeEvent(self, event)
	# end closeEvent
	
	@staticmethod
	def getModuleByName(name):
		mods = abstractModuleClass.d_modules
		
		for mod in mods:
			if (mod == name):
				return mods[mod]
		# end for
		
		return False
	# end getModuleByName
	
	@staticmethod
	def deletePlotWindow(name):
		plots = abstractModuleClass.d_plots
		
		if (name not in plots):
			return False
		# end if

		w = plots.pop(name)

		if (w.isVisible()):
			w.close()
		# end if
		
		manager = w.getManager()
		del(manager)

		del(w)

		return True
	# end _deletePlotDialog
	
	@staticmethod
	def deleteAllPlots():
		keys = list(abstractModuleClass.d_plots.keys())
		for key in keys:
			abstractModuleClass.deletePlotWindow(key)
		# end for
	# deleteAllPlots
	
	def _closeAllPlots(self):
		plots = abstractModuleClass.d_plots
		
		for name in plots:
			plots[name].close()
		# end for
	# end _closeAllPlots
	
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

	## @brief interface: get GUI module handle(s)
	# @param self The object pointer.
	# @param name return only one module handle
	# @param sendError display error message if module does not exists
	def _getModuleArray(self, name = "", sendError = False):
		modules = abstractModuleClass.d_modules
		
		if (name == ""):
			#return self.__l_modules
			return modules
		# end if
		
		if (name in modules and modules[name]['handle'] != False):
			return modules[name]
		else:
			if (sendError):
				self._p_logger.critical('Can\'t find module ' + name + '!!!')
			# end if
			
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
		return abstractModuleClass.p_progressBar
	# end getProgressBar

	# ---------- Protected ----------


	# ---------- Public ----------

	## @brief virtual function: initialize the module 
	# @param self The object pointer.
	def initModule(self):
		"virtual"
	# end initModule

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
	
	## @brief virtual function: executes in previous module, after tab changing
	# @param self The object pointer.
	def onInactive(self):
		"virtual"
	# end onInactive

	## @brief set module array from mainWindow
	# @param self The object pointer.
	# @param array module array as list
	def setModuleArray(self, array):
		#self.__l_modules = array
		abstractModuleClass.d_modules = array
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
	
	## @brief get parent path
	# @param self The object pointer.
	# retval parent path
	def getParentPath(self):
		return self.__v_parentPath
	# end getParentPath

	## @brief set includes from mainWindow
	# @param self The object pointer.
	def setIncludes(self, includes):
		self.__d_includes = includes
	# end setIncludes
	
	## @brief set progressbar object
	# @param self The object pointer.
	def setProgressBar(self, pBar):
		#self.__p_progressBar = pBar
		abstractModuleClass.p_progressBar = pBar
	# end setProgressBar
	
	## @brief set progressbar thread object
	# @param self The object pointer.
	def setProgressBarThread(self, pBarThread):
		#self.__p_progressBarThread = pBarThread
		abstractModuleClass.p_progressBarThread = pBarThread
	# end setProgressBarThread
	
	## @brief interface: return progressbar thread object
	# @param self The object pointer.
	# @retval object progressbar thread object
	def _getProgressBarThread(self):
		#return self.__p_progressBarThread
		return abstractModuleClass.p_progressBarThread
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
		self._p_logger.info('getFileManagement function is not implemented.')
	# end getFileManagement

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
	
	# ---------- Public ----------

# end class abstractModuleClass


class abstractGuiModuleClass(abstractModuleClass):
	def __init__(self, *args, **kwargs):
		abstractModuleClass.__init__(self, *args, **kwargs)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		## custom module settings list
		self.__l_noneGuiSpecificSettings = []
		
		## module display name
		self.__v_displayName = "foo"
		
		## dom settings handle
		self.__p_settingsHandle = False
		
		## dom custom settings handle
		self.__p_userSettingsHandle = False
		
		## module settings as dict
		self.__d_settings = dict()
		
		## module setting xml list
		self.__l_settingXml = []
		
		## module user setting xml list
		self.__l_userSettingXml = []
		
		## absolute path to icon file
		self.__v_iconPath = False
	# end __initVars
	
	## @brief load none GUI specific settings from xml
	# @param self The object pointer.
	# @retval boolean
	def __loadNoneGuiSpecificSettings(self):
		custom = self.__p_userSettingsHandle.getElementsByTagName("custom")

		if (len(custom) == 0):
			self.__l_noneGuiSpecificSettings = []

			return False
		# end if
		
		self.__l_noneGuiSpecificSettings = readXMLRec(custom[0])
		
		return True
	# end __loadNoneGuiSpecificSettings
	
	## @brief create xml for custom module settings
	# @param self The object pointer.
	# @retval boolean
	def __createNoneGuiSpecificSettings(self):
		if (self.__l_noneGuiSpecificSettings == []):
			return False
		# end if
		
		custom = self.__p_userSettingsHandle.getElementsByTagName("custom")
		
		if (len(custom) > 0):
			custom = custom[0]
			custom.unlink()
		else:
			custom = self.__p_userSettingsHandle.createElement("custom")
		# end if
		
		# create xml string from dict list
		if (not writeXMLRec(self.__p_userSettingsHandle, custom, self.__l_noneGuiSpecificSettings)):
			self._p_logger.critical("can't save custom settings");
			return False
		# end if
		
		return True
	# end __createNoneGuiSpecificSettings
	
	def _getNoneGuiSpecificSettings(self):
		return self.__l_noneGuiSpecificSettings
	# end _getNoneGuiSpecificSettings
	
	def _setNoneGuiSpecificSettings(self, s):
		self.__l_noneGuiSpecificSettings = s
	# end _setNoneGuiSpecificSettings
	
	def _getCustomSettings(self):
		return self._getNoneGuiSpecificSettings()
	# end if
	
	def _setCustomSettings(self, s):
		self._setNoneGuiSpecificSettings(s)
	# end _setCustomSettings
		
	
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
	
	## @brief return absolute icon path
	def getIconPath(self):
		return self.__v_iconPath
	# end getIconPath
	
	## @brief get module settings from the gui elements which were given in xml file
	# @param self The object pointer.
	# @param key return settings from one specific element
	# @retval settings list
	def _getSettings(self, key = False):
		if (key != False and key in self.__d_settings):
			return self.__d_settings[key]
		# end if
			
		return self.__d_settings
	# end _getSettings
	
	## @brief save module settings
	# @param self The object pointer.
	def saveUserSettings(self):
		self.__createNoneGuiSpecificSettings()
		
		# get settings handler
		userSettings = self.__p_userSettingsHandle.getElementsByTagName("settings")[0]
		
		# delete all old elements
		userSettings.unlink()

		
		defaultXmlList = self.__l_settingXml['module']['items'][0]['default_settings']['items'][0]
		userXmlList = self.__l_userSettingXml['module']['items'][0]['settings']['items'][0]
		
		# search for difference between default and real current settings
		for elemType in defaultXmlList:
			if (elemType not in userXmlList):
				userXmlList[elemType] = defaultXmlList[elemType]
				continue
			# end if
			
			for item in defaultXmlList[elemType]['items']:
				# search item in current settings
				found = False
				
				for currentItem in userXmlList[elemType]['items']:
					if (item['name'] == currentItem['name']):
						found = True
						break
					# end if
				# end for

				if (not found):
					userXmlList[elemType]['items'].append(item)
				# end if
			# end for
		# end for

		# load last values from gui
		loadGuiChange(userXmlList, self)

		if (not writeXMLRec(self.__p_userSettingsHandle, userSettings, userXmlList)):
			self._p_logger.critical("Can't save settings!!!");
			return False
		# end if

		writer = open(self.getModulePath(True) + "/" + self.getName() + "_user.xml", "w", encoding='utf-8')
		#self.__p_userSettingsHandle.writexml(writer, encoding='utf-8', newl='\n', addindent='\t', indent='') # there is a bug in writexml
		self.__p_userSettingsHandle.writexml(writer, encoding='utf-8')
		writer.close()
	# end saveUserSettings

	## @brief load custom module settings
	# @param self The object pointer.
	def loadUserSettings(self):
		# before we are load the user settings, we have to load the default settings if some custom settings are not exists
		self.loadSettings()
		
		modulePath = self.getModulePath(True)
		fileName = self.getName() + "_user.xml"
		filePath = modulePath + "/" + fileName
		
		# Falls die Datei nicht vorhanden ist, wird sie erstellt.
		if (fileName in os.listdir(modulePath)):
			self.__p_userSettingsHandle = dom.parse(filePath)
		else:
			self.__p_userSettingsHandle = dom.parseString("<module><settings></settings><custom></custom></module>")
		# end if

		# parse xml structure into a list		
		self.__l_userSettingXml = readXMLRec(self.__p_userSettingsHandle)

		# load none GUI specific settings
		self.__loadNoneGuiSpecificSettings()
		
		elems = setGuiSettings(self.__l_userSettingXml['module']['items'][0]['settings']['items'][0], self)
		
		# update settings dict
		self.__updateSettings(elems)
	# end loadUserSettings
	
	## @brief load default module settings
	# @param self The object pointer.
	def loadSettings(self):
		self.__p_settingsHandle = dom.parse(self.getModulePath(True) + "/" + self.getName() + ".xml")
		self.__l_settingXml = readXMLRec(self.__p_settingsHandle)
		
		moduleNode = self.__l_settingXml['module']['items'][0]
		mainNode = moduleNode['main']['items'][0]

		# get display name
		displayName = ''
		if ('displayname' not in mainNode):
			self._p_logger.critical("No Attribute displayname was found in xml file!!!")

			return False
		else:
			displayName = mainNode['displayname']['content']
		# end if
		self.__v_displayName = displayName
		
		# if an icon is given in xml then load the relative path to icon filename
		# the filename endign have to be a file with is supportet by qimagereader from qt
		iconPath = False
		if ('icon' in mainNode):
			iconPath = mainNode['icon']['content']
			if (os.path.isfile(self.getModulePath(True) + '/' + iconPath)):
				iconPath = self.getModulePath(True) + '/' + iconPath
			else:
				iconPath = False
			# end if 
		# end if
		self.__v_iconPath = iconPath


		# save settings from gui elements
		xmlList = moduleNode['default_settings']['items'][0]
		elems = setGuiSettings(xmlList, self)

		# connect elements
		for elemClass in elems:
			for elem in elems[elemClass]:
				sig = False
				
				# get elem name withe elem class
				[elemName, elemClassName] = self.__getNameFromElem(elem)

				if (elemClass == 'textedit'):
					sig = SIGNAL('textChanged()')
					dest = partial(self.__onTextEditChanged, elemName, elem['handle'])
				elif (elemClass == 'lineedit'):
					sig = SIGNAL('validChange(PyQt_PyObject, PyQt_PyObject)')
					dest = self.__onValidChange
				elif (elemClass in ['checkbox', 'groupbox']):
					sig = SIGNAL('clicked(bool)')
					dest = partial(self.__onValidChange, elemName)
				elif (elemClass == 'radiobutton'):
					sig = SIGNAL('toggled(bool)')
					dest = partial(self.__onValidChange, elemName)
				elif (elemClass == 'betterslider'):
					sig = SIGNAL('changed(PyQt_PyObject)')
					dest = partial(self.__onValidChange, elemName)
				elif (elemClass == 'combobox'):
					sig = SIGNAL('currentIndexChanged(int)')
					dest = partial(self.__onComboBoxValidChange, elemName, elem['handle'])
				elif (elemClass == 'spinbox'):
					sig = SIGNAL("valueChanged(int)")
					dest = partial(self.__onSpinBoxValidChange, elemName, elem['handle'])
				# end if
				
				if (sig):
					self.disconnect(elem['handle'], sig, dest)
					self.connect(elem['handle'], sig, dest)
				# end if
			# end for
		# end for
		
		# update settings dict
		self.__d_settings = dict()
		self.__updateSettings(elems)
	# end loadSettings
	
	def __getNameFromElem(self, elem):
		objClass = type(elem['handle'])
		objName = elem['name']
		
		# check for custom elements
		if (issubclass(objClass, QLineEdit)):
			elemClassName = 'LineEdit'
		elif (issubclass(objClass, QComboBox)):
			elemClassName = 'ComboBox'
		#elif (issubclass(objClass, QSlider)):
		#	elemClassName = 'slider'
		else:
			elemClassName = elem['handle'].metaObject().className()
			if (elemClassName[0] == 'Q'):
				elemClassName = elemClassName[1:len(elemClassName)] # remove q from string like qLineEdit
			# end if
		# end if
		
		pos = objName.lower().find(elemClassName.lower())

		if (pos == 0 and len(elemClassName) != len(objName)):
			objName = objName[len(elemClassName):len(objName)]
		# end if
		
		return [objName, elemClassName]
	# end __getNameFromElem
	
	def __onComboBoxValidChange(self, elemName, elem, index):
		self.__d_settings[elemName] = elem.currentText()
	# end
	
	def __onSpinBoxValidChange(self, elemName, elem, index):
		self.__d_settings[elemName] = elem.value()
	# end
			
	def __onValidChange(self, elemName, elemValue):
		self.__d_settings[elemName] = elemValue
	# end __onValidChange
	
	def __onTextEditChanged(self, elemName, elemHandle):
		# debug putput
		#print('========== SIGNAL ==========')
		#print(elemName)
		#print(elemHandle)
		#print(elemHandle.metaObject().className())
		#print(elemHandle.toPlainText())
		#print(elemHandle.toHtml())
		#print('========== SIGNAL ==========')
		
		self.__d_settings[elemName] = elemHandle.toPlainText()
	# end __onTextEditChanged
	
	# update __d_settings dict with gui elements are used in xml file
	def __updateSettings(self, elems):
		# theses are the supported elements
		#textElems = [customGuiElements.customIntegerLineEdit, customGuiElements.customFloatLineEdit, customGuiElements.customStringLineEdit, customGuiElements.customListLineEdit, QLineEdit, QLabel]
		textElems = ['LineEdit', 'Label']
		textEditElems = ['TextEdit', 'PlainTextEdit']
		boolElems = ['CheckBox', 'RadioButton', 'GroupBox']
		#listElems = [customGuiElements.customIntegerComboBox, customGuiElements.customFloatComboBox, QComboBox]
		valueElems = [QSpinBox, QDoubleSpinBox]
		
		# check if element is supported
		for elemClass in elems:
			for elem in elems[elemClass]:
				objClass = type(elem['handle'])

				# get elem name
				[elemName, elemClassName] = self.__getNameFromElem(elem)
				
				#print(elemName)
				#print(elemClassName)
				#print()
				
				#if (classEqual(objClass, textElems)):
				if (elemClassName in textElems):
					self.__d_settings[elemName] = elem['handle'].text()
				elif (elemClassName in textEditElems):
					self.__onTextEditChanged(elemName, elem['handle'])
				elif (elemClassName in boolElems):
					if (elem['handle'].isCheckable()):
						self.__d_settings[elemName] = elem['handle'].isChecked()
					# end if
				elif (objClass in valueElems):
					self.__d_settings[elemName] = elem['handle'].value()
				#elif (objClass in listElems):
				elif (elemClassName == 'ComboBox'):
					self.__d_settings[elemName] = elem['handle'].currentText()
				elif (issubclass(objClass, QSlider)):
					functions = dir(elem['handle'])
					if ('editedValue' in functions):
						self.__d_settings[elem['name']]= elem['handle'].editedValue()
					else:
						self.__d_settings[elem['name']]= elem['handle'].value()
					# end if
				# end if
			# end for
		# end for
	# end __updateSettings
	
	## @brief virtual function: initialize function before settings were loaded
	# @param self The object pointer.
	def initPreSettings(self):
		"virtual"
	# end initPreSettings
	
	## @brief virtual function: initialize the module GUI
	# @param self The object pointer.
	def initGUI(self):
		"virtual"
	# end initGUI
	
	## @brief qt size hint function
	# get size hint information for this module if no mimimum size were set
	def sizeHint(self, *args, **kwargs):
		if (self.minimumSize().isNull()):
			cr = self.childrenRect()

			if (cr.width() != 0 and cr.height() != 0):
				size = QSize(cr.x() + cr.width() + 10, cr.y() + cr.height() + 10)
				
				if (size.width() > 780 or size.height() > 510):
					return QSize(780, 510)
				else:
					return size
				# end if
			else:
				return QSize(780, 510)
			# end if
		else:
			return self.minimumSize()
		# end if
		
		return abstractModuleClass.sizeHint(self, *args, **kwargs)
	# end sizeHint
	
	def showEvent(self, event):
		self.setWindowTitle(self.getName())
		
		return abstractModuleClass.showEvent(self, event)
	# end showEvent
	
	"""
	## @brief qt show event
	# set minimum size if no minimum size were set
	# use client bounding rectangle as minimum size
	def showEvent(self, event):
		if (self.minimumSize() == QSize(0, 0)):
			cr = self.childrenRect()
			
			if (cr.width() != 0 and cr.height() != 0):
				size = QSize(cr.x() + cr.width() + 10, cr.y() + cr.height() + 10)
				if (size.width() > 780 or size.height() > 510):
					self.setMinimumSize(QSize(780, 510))
				else:
					self.setMinimumSize(size)
				# end if
			# end if
		# end if

		return abstractModuleClass.showEvent(self, event)
	# end showEvent
	"""
	
# end class abstractGuiModuleClass


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
	def __init__(self, *args, **kwargs):
		abstractModuleClass.__init__(self, *args, **kwargs)
		self._setClassType("hidden")
	# end __init__

# end class hiddenModuleClass


## @brief setting module class
# @param self The object pointer.
class settingModuleClass(abstractGuiModuleClass):
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	# @param name module name
	# 
	# set current module name and class type
	# create client logger object
	def __init__(self, *args, **kwargs):
		abstractGuiModuleClass.__init__(self, *args, **kwargs)
		self._setClassType("setting")
		
		# set minimum size
		self.setMinimumSize(780, 510)
	# end __init__

# end class settingModuleClass


## @brief application module class
# @param self The object pointer.
class applicationModuleClass(abstractGuiModuleClass):
	# signal on close
	onInvisible = pyqtSignal(QWidget)
	
	## @brief class init function
	# @param self The object pointer.
	# @param parent Qt parent pointer
	# @param name module name
	# 
	# set current module name and class type
	# create client logger object
	def __init__(self, *args, **kwargs):
		abstractGuiModuleClass.__init__(self, *args, **kwargs)
		self._setClassType("application")
		
		self.__p_menuButton = False
		self.__p_menuAction = False
	# end __init__
	
	def onClose(self):
		abstractGuiModuleClass.onClose(self)
		
		event = QCloseEvent()
		event.accept()
		abstractGuiModuleClass.closeEvent(self, event)
	# end onclose
	
	## @brief override closeEvent
	# do not close the module. set module invisible
	def closeEvent(self, event):
		if (self.parent().metaObject().className() == "mainWindow"):
			self.getMenuButton().setChecked(False)

			return
			#return abstractGuiModuleClass.closeEvent(self, event)
		# end if
		
		event.ignore()
		
		# use onInactive function
		if (self.parent().isVisible()):
			self.onInactive()
			
			# do not visible this module
			self.parent().setVisible(False)
			
			# emit on invisible signal
			self.onInvisible.emit(self)
			
			if (self.__p_menuButton):
				#self.__p_menuButton.setAutoExclusive(False)
				self.__p_menuButton.setChecked(False)
				#self.__p_menuButton.setAutoExclusive(True)
			# end if
		# end if
	# end if
	
	
	## @brief get menu button pointer
	# @param self The object pointer.
	# @retval button pointer
	#
	# if no button ist available a menu button will be created 
	def getMenuButton(self):
		if (self.__p_menuButton == False):
			self.__p_menuButton = applicationMenuButton(self)
			self.__p_menuButton.setText(self.getName())
		# end if
		
		return self.__p_menuButton
	# end getMenuWidget
	
	## @brief set menu button
	# @param self The object pointer.
	# @param button Pointer to a applicationMenuButton instance.
	# @retval None
	def setMenuButton(self, button):
		self.__p_menuButton = button
	# end setMenuButton
	
	def getMenuAction(self):
		return self.__p_menuAction
	# end getMenuAction
	
	def setMenuAction(self, action):
		self.__p_menuAction = action
	# end setMenuAction
	
	## @brief set display name
	# @param
	# @param name Set name
	def setDisplayName(self, name):
		# set display name for menu button
		if (self.__p_menuButton != False and 'setText' in dir(self.__p_menuButton)):
			self.__p_menuWidget.setText(name)
		# end if

		abstractGuiModuleClass.setDisplayName(self, name)
	# end setDisplayName

# end class applicationModuleClass

