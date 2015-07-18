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
#
# @defgroup abstractModule abstract modules
#
# @{
# @brief abstract module functions
#
# @section app application module
# The GUI can be 780 x 520 pixel or higher.
#


import sys, logging
from PyQt4.QtCore import QSize, pyqtSignal
from PyQt4.QtGui import QWidget, QCloseEvent
from functions.menu import applicationMenuButton
from functions.helper import settingsHandler
# try to import plot engine
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

	## module class types
	enumClassType = {
		"setting" : 1, ##< setting module
		"application" : 2, ##< application module
		"hidden" : 3 ##< hidden module
	}
	
	## static list poitns to global plot list
	d_plots = dict()
	
	## static pointer to global progressbar
	p_progressBar = False
	
	## static poitner to progressbar thread
	p_progressBarThread = False
	
	## static module dir
	# This list store all GUI modules
	d_modules = []
	
	## flag for plot windows support
	plotWindowSupport = g_plotWindowSupport

	## global logging level
	loglevel = logging.WARN
	
	## onClose signal
	__sig_onClose = pyqtSignal(object, name = "sigOnClose")

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
		self._p_logger.setLevel(abstractModuleClass.loglevel)
	#end __init__
	
	# @param self The object pointer.
	def __del__(self):
		if (self._p_loggerClient != False):
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
	# @param self The object pointer.
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
	
	def _addPlot(self, name, plt=False):
		if (not abstractModuleClass.plotWindowSupport):
			return False
		# end if
		
		plots = abstractModuleClass.d_plots
		
		if (name in plots):	
			return plots[name]
		# end if
		
		window = plt
		
		plots[name] = window
		
		return window
	# end _newPlot
	
	def _getPlot(self,name):
		plots = abstractModuleClass.d_plots
		
		if (name not in plots):
			#self._p_logger.error("There is no plot available with the given name.")
			return False
		# end if
		
		return plots[name]
	# end _getPlot
	
	def _getPlotWindow(self, name):
		plots = abstractModuleClass.d_plots
		
		if (name not in plots):
			#self._p_logger.error("There is no plot available with the given name.")
			return False
		# end if
		
		return plots[name]
	# end _getPlot
	
	def closeEvent(self, event):
		self.__sig_onClose.emit(self)
		
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
	## static settings handle
	settingsHandle = False
	
	def __init__(self, *args, **kwargs):
		abstractModuleClass.__init__(self, *args, **kwargs)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		## custom module settings list
		self.__l_noneGuiSpecificSettings = []
		
		## module display name
		self.__v_displayName = "mod"
		
		## dom settings handle
		#self.__p_settingsHandle = False
		
		## settings handler class
		self.__p_settingsHandler = False
		
		## dom custom settings handle
		#self.__p_userSettingsHandle = False
		
		## module settings as dict
		self.__d_settings = dict()
		
		## module setting xml list
		#self.__l_settingXml = []
		
		## module user setting xml list
		#self.__l_userSettingXml = []
		
		## absolute path to icon file
		self.__v_iconPath = False
		
		## GUI menu button
		self._p_menuButton = False
	# end __initVars
	

	## @brief set display name from mainWindow
	# @param self The object pointer.
	# @param name GUI module name
	def setDisplayName(self, name):
		self.__v_displayName = name
	# end setDisplayName

	## @brief get display name
	# @param self The object pointer.
	# @return name display name
	def getDisplayName(self):
		return self.__v_displayName
	# end getDisplayName
	
	## @brief return absolute icon path
	def getIconPath(self):
		return self.__v_iconPath
	# end getIconPath
	
	# @brief Set icon path
	# @param self The object pointer.
	# @param path Relative path to icon.
	# @param globalIcon False: Module path is parent path. True: GUI path is parent path. 
	def _setIconPath(self, path, globalIcon = False):
		if (globalIcon):
			self.__v_iconPath = self.getParentPath() + '/icons/' + path
		else:
			self.__v_iconPath = self.getModulePath(True) + '/' + path
		# end if
	# end _setIconPath
	
	## @brief get module settings from the GUI elements which were given in userSettings.ini.
	# @param self The object pointer.
	# @param key return settings from one specific element
	# @return settings list
	def _getSettings(self, key = False):
		# return false if no settings handler is available
		if (not self.__p_settingsHandler):
			return False
		# end if
		
		settings = self.__p_settingsHandler.getModuleSettings()
		
		if (key != False and key in settings):
			return settings[key]
		# end if
			
		return settings
	# end _getSettings
	
	def _setSettings(self, key, value):
		return self.__p_settingsHandler.setModuleSettings(key, value)
	# end _setSettings
	
	## @brief same as _getSettings
	# @param self The object pointer.
	# @param key return settings from one specific element
	# @retval settings list
	def getSettings(self, key = False):
		return self._getSettings(key)
	# end getSettings
	
	## @brief handle settings on first time
	# @param self The object pointer.
	def handleSettings(self):
		abstractGuiModuleClass.settingsHandle.beginGroup('module_settings')
		savedSettings = abstractGuiModuleClass.settingsHandle.value(self.getName())
		abstractGuiModuleClass.settingsHandle.endGroup()
		
		if (savedSettings == None):
			savedSettings = dict()
		# end if
		
		self.__p_settingsHandler = settingsHandler(self, savedSettings)
	# end handleSettings
	
	## @brief load user settings from global QSettings struct an store it into GUI elements
	# @param self The object pointer.
	def loadSettings(self):
		if (not self.__p_settingsHandler):
			return
		# end if
		
		abstractGuiModuleClass.settingsHandle.beginGroup('module_settings')
		savedSettings = abstractGuiModuleClass.settingsHandle.value(self.getName())
		abstractGuiModuleClass.settingsHandle.endGroup()
		
		if (savedSettings == None):
			return
		# end if

		self.__p_settingsHandler.load(savedSettings)
	# end laodSettings
	
	## @brief delete all settings
	# @param self The object pointer.
	def deleteSettings(self):
		self.__p_settingsHandler.delete()
		
		self.__p_settingsHandler.loadDefault()
	# end deleteSettings
	
	## @brief load default settings from module an store it into GUI elements
	# @param self The object pointer.
	def loadDefaultSettings(self):
		if (not self.__p_settingsHandler):
			return
		# end if

		self.__p_settingsHandler.loadDefault()
	# end loadDefaultSettings
	
	## @brief save settings into global QSettings struct
	# @param self The object pointer.
	def saveSettings(self):
		if (not self.__p_settingsHandler):
			return
		# end if
		
		settings = self.__p_settingsHandler.getSaveSettings()
		
		abstractGuiModuleClass.settingsHandle.beginGroup('module_settings')
		abstractGuiModuleClass.settingsHandle.setValue(self.getName(), settings)
		abstractGuiModuleClass.settingsHandle.endGroup()
	# end saveSettings
		

	## @brief virtual dummy function
	# @param self The object pointer.
	# @return return default settings dict
	#
	# dict construct ist:
	# d = {"variable name": {"qName": "[Qt Elment Name]", "value": "[Element Inhalt]"}}
	# 
	# @n qName can be none for none GUI elements
	def getDefaultSettings(self):
		return {}
	# end getDefaultSettings
	
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
	
	## @brief virtual function: This function is called if the parent dock widget gets invisible.
	# @param self The object pointer.
	def onHide(self):
		"virtual"
	# end onHide
	
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
	
	## @brief get menu button pointer
	# @param self The object pointer.
	# @return button pointer
	#
	# if no button ist available a menu button will be created 
	def getMenuButton(self):
		if (self._p_menuButton == False):
			self._p_menuButton = applicationMenuButton(self)
			self._p_menuButton.setText(self.getName())
		# end if
		
		return self._p_menuButton
	# end getMenuWidget
	
	## @brief set menu button
	# @param self The object pointer.
	# @param button Pointer to a applicationMenuButton instance.
	def setMenuButton(self, button):
		self._p_menuButton = button
	# end setMenuButton
	
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
		self.setMinimumSize(380, 250)
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
	# end __init__
	
	def onClose(self):
		abstractGuiModuleClass.onClose(self)
		
		event = QCloseEvent()
		event.accept()
		abstractGuiModuleClass.closeEvent(self, event)
	# end onclose

	## @brief override closeEvent
	# @param self The object pointer.
	# @param event QT event
	# do not close the module. set module invisible
	def closeEvent(self, event):
		if (self.parent().metaObject().className() == "mainWindow"):
			self._p_menuButton.setChecked(False)

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
			
			if (self._p_menuButton):
				#self._p_menuButton.setAutoExclusive(False)
				self._p_menuButton.setChecked(False)
				#self._p_menuButton.setAutoExclusive(True)
			# end if
		# end if
	# end if
	
	## @brief set display name
	# @param
	# @param name Set name
	def setDisplayName(self, name):
		# set display name for menu button
		if (self._p_menuButton != False and 'setText' in dir(self._p_menuButton)):
			self.__p_menuWidget.setText(name)
		# end if

		abstractGuiModuleClass.setDisplayName(self, name)
	# end setDisplayName

# end class applicationModuleClass

# @}
