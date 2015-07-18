##
# @file mainWindow.py
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
# @brief Main window from Qt GUI and global module handler
#


import os, sys, logging

# add sub directories to path
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/functions/')


from abstractModuleClass import abstractModuleClass, abstractGuiModuleClass
from functools import partial
from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSlot, QSettings, QProcess, QObject
from PyQt4.QtGui import QMainWindow, QTreeWidgetItem,	QDialog, QIcon, QStatusBar, QTabWidget, QDockWidget
import imp, re
from functions.helper import str2bool
from functions.delete import delete
from functions.progressBarThread import progressBarThread
from functions.guiLogger import QtLogger, QtLoggerListWidget, QtLoggerDockWidget

# This is a special value defined in Qt4 but does not seem to be exported
# by PyQt4
QWIDGETSIZE_MAX = ((1 << 24) - 1)



## @brief main window GUI class
class mainWindow(QMainWindow):
	# ---- private begin ----
	
	## @brief initialize class function
	# @param self The object pointer.
	# @param loglevel Logging level for main window and all modules.
	# @param debug Enabled debugging. Default is false.
	# 
	# initialize:
	# - create logger thread
	# - create main window logger client
	# - create global progress bar thread
	# - add dialogs
	# - manage central widget
	def __init__(self, loglevel, debug = False, *args, **kwargs):
		QMainWindow.__init__(self, *args, **kwargs)
		
		self.__initVars()

		# load main ui before setting debug level
		uic.loadUi("./main.ui", self)

		# create logger widget
		self.__p_loggerDockWidget = QtLoggerDockWidget('Logging', self)
		self.__p_loggerDockWidget.setObjectName('Logging')
		self.__p_loggerListWidget = QtLoggerListWidget(self.__p_loggerDockWidget)
		
		# ... add list widget to dock widget
		self.__p_loggerDockWidget.setWidget(self.__p_loggerListWidget)
		
		# ... add dock widget to main window
		self.addDockWidget(Qt.BottomDockWidgetArea, self.__p_loggerDockWidget)

		
		# init QtLogger
		QtLogger.printObj = self.__p_loggerListWidget

		# init logger for main window
		self.__p_logger = logging.getLogger("mainWindow")
		
		# ... set log level
		self.__p_logger.setLevel(loglevel)
		
		# ... set debug level for modules
		abstractModuleClass.loglevel = loglevel
		

		# Hide debugging menu in none debugging mode
		if (debug):
			# add debug menu
			self.menuDebug = self.menuBar().addMenu("Debug")

			# add debug actions to menu
			self.actionPrintSettings = self.menuDebug.addAction("print settings")
			self.actionDelAllSettings = self.menuDebug.addAction("del all settings")
			
			# connect signals to actions
			self.actionPrintSettings.triggered.connect(self.__onPrintSettings)
			self.actionDelAllSettings.triggered.connect(self.__onDelAllSettings)
		# end if
		
		# add help if operating system is windows
		if (sys.platform == "win32"):
			self.menuQ.addAction("GUI help", self.__onHelp)
			#action.triggered.connect(self.__onHelp)
		# end if
		
		# progress bar
		# ... set parameters
		self.progressBarGlobal.setLabel(self.labelProgressBarGlobal)
		self.progressBarGlobal.disable()
		
		# ... create progress bar thread
		self.__p_progressBarThread = progressBarThread(self)
		self.__p_progressBarThread.sigProgressBarUpdate.connect(self.__onProgressBarUpdate)
		self.__p_progressBarThread.start()
		
		# add dialogs
		# ... about dialog
		self.__p_about = QDialog(self)
		uic.loadUi("./about.ui", self.__p_about)
		self.actionAbout.triggered.connect(self.__p_about.exec)

		# ... license dialog
		self.__p_license = QDialog(self)
		uic.loadUi("./license.ui", self.__p_license)
		self.actionLicense.triggered.connect(self.__p_license.exec)
		
		# ... select module dialog
		self.__p_selectModule = QDialog(self)
		uic.loadUi('./selectModule.ui', self.__p_selectModule)
		self.actionModules.triggered.connect(self.__p_selectModule.exec)
		
		# init GUI
		# ... set central widget to none
		#self.setCentralWidget(None)
		self.centralWidget().setFixedSize(0,0)
		
		# ... Add all dock widgets on startup into the left area. An show tabs on top.
		self.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.North)
		
		# ... create and add status bar
		self.__p_statusBar = QStatusBar()
		self.setStatusBar(self.__p_statusBar)
		
		# ... move progress bar widget into status bar
		self.__p_statusBar.addWidget(self.widgetProgressBar, 1)

		# ... set tool button style
		self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		
		# settings
		# ... create main settings object
		self.__p_settingsHandle = QSettings('./' + self.__v_userSettingsFileName, QSettings.IniFormat)
		
		# ... set QSettings handle
		abstractGuiModuleClass.settingsHandle = self.__p_settingsHandle
	# end __init__
	

	## @brief del function
	# @param self The object pointer.
	#
	# Delete all member variables and threads.
	def __del__(self):
		# set static variables to false
		QtLogger.printObj = False
		abstractGuiModuleClass.settingsHandle = False
		abstractModuleClass.d_modules = dict()
		abstractModuleClass.p_progressBar = False
		abstractModuleClass.p_progressBarThread = False
		
		# stop and delete progressBar
		if (self.__p_progressBarThread != False):
			self.__p_progressBarThread.sigProgressBarUpdate.disconnect(self.__onProgressBarUpdate)
			self.__p_progressBarThread.stop()
			self.__p_progressBarThread.wait(500)
			self.__p_progressBarThread = False
		# end if
		
		# set all variables to false to free memory
		self.__initVars()
	# end __del__
	
	## @brief Initialize class variables.
	# @param self The object pointer.
	def __initVars(self):
		self.__p_loggerDockWidget = False
		self.__p_loggerListWidget = False
		
		## main window status bar
		self.__p_statusBar = False
		
		## global module directory
		# with "/" at the end!!!
		self.__v_modulePath = "modules/"
		
		## filename from used modules xml file
		self.__v_userSettingsFileName = 'userSettings.ini'
		
		## current tab index
		self.__v_currentTabIndex = -1
		
		## about dialog
		self.__p_about = False
		
		## license dialog
		self.__p_license = False
		
		## select module dialog
		self.__p_selectModule = False
		
		## main settings object
		self.__p_settingsHandle = False
		
		## main gui logger object
		self.__p_logger = False
		
		## list of used modules
		self.__l_usedModules = []
		
		## progress bar object thread
		self.__p_progressBarThread = False
		
		## module counter
		self.__v_moduleCounter = 0
	# end __initVars
	
	
	## @brief private slot for updating the progressbar
	# @param self The object pointer.
	# @param ret List with command and command value.
	#
	# @n ret[0]: values
	# @n ret[1]: commands
	#
	# @n valid commands:
	# - init
	# - clear
	# - disable
	# - newVal or ready
	#
	@pyqtSlot(list)
	def __onProgressBarUpdate(self, ret):
		value, command = ret
		
		if (command == 'init'):
			self.progressBarGlobal.init(self)
			
			if (value != ''):
				self.progressBarGlobal.setText(value)
			# end if
		elif (command == 'clear'):
			self.progressBarGlobal.clear()
		elif (command == 'disable'):
			self.progressBarGlobal.disable()
		elif (command == 'newVal' or command == 'ready'):
			try:
				value = int(value)
			except:
				self.__p_logger.error('Only Integers for progressBar value are allowed. But %s were set!!!', str(value))
				return
			# end if
	
			self.progressBarGlobal.setValue(value)
		# end if
	# end if
	
	## @brief get user settings like used module list and gui position
	# @param self The object pointer.
	# 
	# Load only the modules which were selected by the user.
	def __loadSettings(self):
		# main group
		self.__p_settingsHandle.beginGroup('main')
		displayName = self.__p_settingsHandle.value("displayName", "pyGUI")
		geo = self.__p_settingsHandle.value("geo")
		#state = self.__p_settingsHandle.value('state')
		self.__p_settingsHandle.endGroup()
		
		saveOnExit = self.__p_settingsHandle.value("settings/saveOnExit", True)
		
		# modules group
		self.__p_settingsHandle.beginGroup('module')
		self.__l_usedModules = self.__p_settingsHandle.value('used', [])
		self.__p_settingsHandle.endGroup()

		# restore state and geometry if information is available
		#if (state):
		#	self.restoreState(state)
		# end if
		if (geo):
			self.restoreGeometry(geo)
		# end if

		# if no used modules are available		
		if (self.__l_usedModules == None):
			self.__l_usedModules = []
		# end if

		# restore settings
		self.actionSaveSettingsOnExit.setChecked(str2bool(saveOnExit))
		
		# set display name
		self.setWindowTitle(displayName)
	# end __loadSettings

	
	## @brief save window and user settings
	# @param self The object pointer.
	#
	# saved settings are:
	# - main window position and size
	# - current active module
	def __saveSettings(self):
		# modules
		self.__l_usedModules = list()
		for i in range(self.__p_selectModule.treeWidgetModules.topLevelItemCount()):
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(i)

			for c in range(item.childCount()):
				child = item.child(c)

				if (child.checkState(0) == Qt.Checked):
					self.__l_usedModules.append(child.text(0))
				# end if
			# end for
		# end for
		
		# main window settings
		self.__p_settingsHandle.setValue("main/geo", self.saveGeometry())
		if (self.__v_moduleCounter > 0):
			self.__p_settingsHandle.setValue("main/state", self.saveState())
		# end if
		self.__p_settingsHandle.setValue("main/displayName", self.windowTitle().split()[0])
		
		# used module settings
		self.__p_settingsHandle.setValue("module/used", self.__l_usedModules)
		
		# settings
		self.__p_settingsHandle.setValue("settings/saveOnExit", self.actionSaveSettingsOnExit.isChecked())
	# end __saveSettings

	
	# --- module handler begin ---
	

	## @brief search for modules
	# @param self The object pointer.
	#
	# Load all modules from self.__v_modulePath
	def __loadModules(self):
		# init variables
		loadOrder = ["hidden", "setting", "application"]

		currentDir = os.path.abspath(os.curdir)
		modulesPath = currentDir + "/" + self.__v_modulePath
		content = os.listdir(modulesPath)
		content.sort()
		modules = []
		moduleNames = []
		
		# clear gui list
		self.__p_selectModule.treeWidgetModules.reset()
		itemList = {"hidden": [], "setting": [], "application": []}

		# search for modules in module order
		index = 0
		for moduleClassType in loadOrder:
			# find modules
			for name in content:
				# only direcotries without .* and ..
				if (not os.path.isdir(modulesPath + name) or re.match("^\.", name)):
					continue
				# end if
				
				# don't load modules twice
				if (name in moduleNames):
					continue
				# end if

				m = re.match("^(\d+)(.*)$", name)
				suffix = ""
				if (m):
					suffix = m.group(1)
					name = m.group(2)
				# end if

				# change into module directory
				moduleDir = modulesPath + suffix + name
				os.chdir(moduleDir)

				# import module
				fullpath_to_py = moduleDir + "/" + name + ".py"
				if not os.path.isfile(fullpath_to_py):
					continue
				# end if
				
				modHandle = imp.load_source(name, fullpath_to_py)

				# switch back to main directory
				os.chdir(currentDir)

				# auf klasse pruefen
				if (moduleClassType + "ModuleClass" in dir(modHandle)):
					moduleNames.append(suffix+name)
					
					# search for dependencies
					dependencies = ""
					dependenciyList = list()
					if ("dependencies" in dir(modHandle)):
						dependenciyList = modHandle.dependencies
						for d in modHandle.dependencies:
							dependencies += d + ", "
						# end for
						
						dependencies = dependencies[0:len(dependencies) - 2]
					# end if
					item = QTreeWidgetItem([name, dependencies])
					item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
					
					path = modulesPath + suffix + name
					path = re.sub(r'[\\/]+', '/', path)
					module = {"name" : name, "modHandle" : modHandle, "handle" : False, "suffix" : suffix, "path" : path, "dependencies": dependenciyList}
					
					# don't load unused modules
					if (name not in self.__l_usedModules):
						item.setCheckState(0, Qt.Unchecked)
						module["modHandle"] = False
						delete(modHandle)
					else:
						item.setCheckState(0, Qt.Checked)
					# end fi
					
					modules.append(module)

					itemList[moduleClassType].append(item)

					continue
				else:
					delete(modHandle)
				# end if
			# end for
			
			# add items to tree widget
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(index)
			item.addChildren(itemList[moduleClassType])
			
			index += 1
		# end for - search for modules in module order
		
		# init modules
		for module in modules:
			if (module["modHandle"] == False):
				continue
			# end if
			#module["handle"] = module["modHandle"].module(None, module["name"])
			module["handle"] = module["modHandle"].module(self, module["name"])
			
			#self.__p_logger.debug("load module " + module["name"])
		# end for - init modules


		# set static functions
		abstractModuleClass.d_modules = dict()
		abstractModuleClass.p_progressBar = self.progressBarGlobal
		abstractModuleClass.p_progressBarThread = self.__p_progressBarThread


		# open modules and load GUI
		firstDockWidget = None
		for module in modules:
			moduleName = module['name']
			moduleHand = module['handle']
			
			try:
				# Wichtig: Damit auch bei nicht geladenen Modulen die dependencies ueberprueft werden koennen.
				abstractModuleClass.d_modules[moduleName] = module
				
				# if module not used
				if (module["modHandle"] == False):
					continue
				# end if
				
				moduleDir = modulesPath + module["suffix"] + moduleName
	
				# find *.py files in the specific modules directory
				os.chdir(moduleDir)
				content = os.listdir(moduleDir)
				includes = dict()
				for filename in content:
					if (os.path.isfile(moduleDir + "/" + filename)):
						if (re.match(".*\.py$", filename) and not (moduleName + ".py") == filename ):
							name = filename[0:-3]
							includes[name] = imp.load_source(name, moduleDir + "/" + filename)
						# end if
					# end if
				# end for
				os.chdir(currentDir)

				# set module settings
				moduleHand.setModulePath(self.__v_modulePath + module["suffix"] + moduleName, os.path.abspath(os.curdir))
				moduleHand.setIncludes(includes)
	
				# check for module type
				moduleClassType = moduleHand.getClassType()

				# module type specific init
				if (moduleClassType != 'hidden'):
					# load [moduleName].ui
					self.__p_logger.setLevel(logging.WARN)
					uic.loadUi(moduleDir + "/" +moduleName + ".ui", moduleHand)
					self.__p_logger.setLevel(abstractModuleClass.loglevel)

					# load module settings
					moduleHand.initPreSettings()
					moduleHand.handleSettings()
					moduleHand.loadSettings()
				# end if

				# join in specific modules folder for initModule
				os.chdir(moduleDir)
				moduleHand.initModule()
				os.chdir(currentDir)
	
				# add module widget to GUI
				if (moduleClassType != 'hidden'):
					iconPath = False
					icon = None
					
					# get icon path
					iconPath = moduleHand.getIconPath()
					
					# try to load icon
					if (iconPath != False):
						icon = QIcon(iconPath)
					# end if
					
					displayName = moduleHand.getDisplayName()
					
					# init menu button
					button = moduleHand.getMenuButton()
					button.setText(displayName)
					
					# dock widget for current module
					# ... create
					dockWidget = mainWindowDockWidget(displayName, self)
					
					# ... set object name and title
					dockWidget.setObjectName(displayName)
					dockWidget.setWindowTitle(displayName)
					
					# ... add module as widget
					dockWidget.setWidget(moduleHand)
					
					# ... add dock widget to main window
					self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)
					
					# ... hide dock widget
					dockWidget.setVisible(False)
					
					# tabify all dock widgets
					if (firstDockWidget == None):
						firstDockWidget = dockWidget
					else:
						self.tabifyDockWidget(firstDockWidget, dockWidget)
					# end if
					
					# ... Set window icon.
					dockWidget.setWindowIcon(moduleHand.getMenuButton().icon())
					
					# ... Connect signal for checking and unchecking menu button on visibility change.
					#     If module is tabbed then set active module as current module.
					dockWidget.visibilityChanged[bool].connect(partial(self.__onModuleVisibilityChanged, dockWidget))


					# add button for application module and action for setting module					
					if (moduleClassType == 'application'):
						# get menu button
						button = moduleHand.getMenuButton()
						
						# set icon for menu button
						if (icon != None):
							button.setIcon(icon)
						# end if
						
						# add menu button to tool bar
						self.toolBar.addWidget(button)
						
						# connect signal from application menu button
						button.clicked[QObject].connect(self.__onModuleButtonClicked)
					else:
						# get action
						action = dockWidget.toggleViewAction()
						
						# set icon
						if (icon != None):
							action.setIcon(icon)
						# end if
						
						# add action to settings menu
						self.menuModuleSettings.addAction(action)
					# end if
				else:
					moduleHand.setParent(None)
				# end if
			except Exception as e:
				msg = "Error in module " + moduleName
				self.__p_logger.critical(msg)
				print(msg)
				raise e
			# end try
		# end for


		# init gui
		for module in modules:
			if (module["modHandle"] == False):
				continue
			# end if
			
			self.__v_moduleCounter += 1
			
			moduleDir = modulesPath + module["suffix"] + module["name"]
			moduleClassType = module["handle"].getClassType()
			
			if (moduleClassType != "hidden"):
				os.chdir(moduleDir)

				try:
					module["handle"].initGUI()
				except Exception as e:
					msg = "Fehler in Module " + module["name"]
					self.__p_logger.critical(msg)
					print(msg)
					raise e
				# end try

				os.chdir(currentDir)
			# end if
		# end for
		
		usedModules = self.__l_usedModules.copy()
		# remove not known used modules
		for moduleName in usedModules:
			if (moduleName not in abstractModuleClass.d_modules):
				self.__l_usedModules.remove(moduleName)
				
				continue
			# end if
	# end __loadModules
	
	
	# --- module slots begin ---
	

	## @brief Slot for dock widget visibility change.
	# @param self The object pointer.
	# @param dockWidget dockWidget form current module
	# @param v visibility as True or False
	@pyqtSlot(QDockWidget, bool)
	def __onModuleVisibilityChanged(self, dockWidget, v):
		module = dockWidget.widget()
		
		module.getMenuButton().setChecked(dockWidget.isVisible())
		
		if (v):
			mainWindowDockWidget.setAsCurrent(dockWidget)
			
			#self.__p_currentModule = module
			#self.__p_currentModule.onActive()
		else:
			module.onHide()
		# end if
	# end __onModuleVisibilityChanged
	
	## @brief if menu button was clicked
	# @param self The object pointer.
	# @param module: module pointer
	# visible this module in mdiArea
	@pyqtSlot(QObject)
	def __onModuleButtonClicked(self, module):
		modParent = module.parent()
		
		# show or hide dock widget
		modParent.setVisible(not modParent.isVisible())
		
		# set menu button checked or none checked
		module.getMenuButton().setChecked(modParent.isVisible())
		
		#self.__p_currentModule = module
	# end __onModuleButtonClicked
	
	# --- module slots end ---
	
	# --- module handler end ---
	
	
	# --- gui slots begin ---
	
	
	## @brief Qt slot to move dock widget to bottom dock widget area.
	# @param self The object pointer.
	@pyqtSlot()
	def onMoveLoggerToBottom(self):
		self.removeDockWidget(self.__p_loggerDockWidget)
		self.addDockWidget(Qt.BottomDockWidgetArea, self.__p_loggerDockWidget)
		self.__p_loggerDockWidget.show()
	# end onMoveLoggerToBottom
	
	
	## @brief show on help dialog
	# @param self The object pointer.
	@pyqtSlot()
	def __onHelp(self):
		path = os.path.abspath(os.curdir) + "/doc/index.chm"
		QProcess.startDetached("hh.exe " + path)
	# end __onHelp
	
	## @brief private slot for menu bar: settings -> load default
	# @param self The object pointer.
	@pyqtSlot()
	def __onSettingsDefault(self):
		currentDockWidget = mainWindowDockWidget.getCurrentWidget()
		if (currentDockWidget == None):
			return
		# end if
		currentModule = currentDockWidget.widget()
		
		currentModule.loadDefaultSettings()
		self.__p_logger.debug('Load default settings for %s.', currentModule.windowTitle())
	# end __onSettingsDefault
	
	## @brief private slot for main bar: settings -> load
	# @param self The object pointer.
	@pyqtSlot()
	def __onSettingsLoad(self):
		currentDockWidget = mainWindowDockWidget.getCurrentWidget()
		if (currentDockWidget == None):
			return
		# end if
		currentModule = currentDockWidget.widget()
		
		currentModule.loadSettings()
		self.__p_logger.debug('Load settings for %s.', currentModule.windowTitle())
	# end __onSettingsLoad
	
	## @brief private slot for menu bar: settings -> save
	# @param self The object pointer.
	@pyqtSlot()
	def __onSettingsSave(self):
		currentDockWidget = mainWindowDockWidget.getCurrentWidget()
		if (currentDockWidget == None):
			return
		# end if
		currentModule = currentDockWidget.widget()
		
		currentModule.saveSettings()
		self.__p_logger.debug('Save settings for %s.', currentModule.windowTitle())
	# end __onSettingsSave
	
	## @brief debug function: Print settings from current active module
	# @param self The object pointer.
	@pyqtSlot()
	def __onPrintSettings(self):
		currentDockWidget = mainWindowDockWidget.getCurrentWidget()
		if (currentDockWidget == None):
			return
		# end if
		currentModule = currentDockWidget.widget()
		
		print(currentModule.windowTitle())
		print(currentModule.getSettings())
		# end if
	# end __onPrintSettings
	
	## @brief debug function: Delete all module settings
	# @param self The object pointer.
	@pyqtSlot()
	def __onDelAllSettings(self):
		modules = abstractModuleClass.d_modules
		
		# dell all module settings
		self.__p_settingsHandle.remove('module_settings')
		#self.__p_settingsHandle.setValue()
		#self.__p_settingsHandle.endGroup()
		
		for name in modules:
			if (modules[name]["modHandle"] == False):
				continue
			# end if
			
			if (modules[name]["handle"].getClassType() != "hidden"):
				modules[name]["handle"].deleteSettings()
			# end if
			
		# end for
	# end __onDelAllSettings

	## @brief private slot for menu bar: settings -> save all
	# @param self The object pointer.
	@pyqtSlot()
	def __onSettingsSaveAll(self):
		modules = abstractModuleClass.d_modules
		
		for name in modules:
			if (modules[name]["modHandle"] == False):
				continue
			# end if
			
			if (modules[name]["handle"].getClassType() != "hidden"):
				modules[name]["handle"].saveSettings()
			# end if
		# end for
	# def __onSettingsSaveAll
	
	
	# --- gui slots end ---
	
	
	
	# --- main tab slots begin ---
	
	## @brief private slot for push button select all
	# @param self The object pointer.
	@pyqtSlot()
	def __selectAll(self):
		self.__l_usedModules = []
		for i in range(self.__p_selectModule.treeWidgetModules.topLevelItemCount()):
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				child.setCheckState(0, Qt.Checked)
				self.__l_usedModules.append(child.text(0))
			# end for
		# end for
	# end __selectAll
	
	## @brief private slot for push button unselect all
	# @param self The object pointer.
	@pyqtSlot()
	def __unselectAll(self):
		self.__l_usedModules = []
		for i in range(self.__p_selectModule.treeWidgetModules.topLevelItemCount()):
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				child.setCheckState(0, Qt.Unchecked)
			# end for
		# end for
	# end __unselectAll
	
	@pyqtSlot(QTreeWidgetItem, int)
	def __onTreeWidgetChanged(self, item, column):
		modules = abstractModuleClass.d_modules
		name = item.text(column)

		if (item.checkState(column) == Qt.Checked):
			if (self.__checkForDependencies(name)):
				if (name not in self.__l_usedModules):
					self.__l_usedModules.append(name)
				# end if
			else:
				item.setCheckState(column, Qt.Unchecked)
			# end if
		else:
			if (name in self.__l_usedModules):
				# if another module depend this module ?
				for modName in modules:
					if (modName in self.__l_usedModules and name in modules[modName]["dependencies"]):
						self.__l_usedModules.remove(modName)
						item = self.__treeWidgetChild(modName)
						item.setCheckState(column, Qt.Unchecked)
					# end if
				# end for
				
				self.__l_usedModules.remove(name)
			# end if
		# end if
	# end __onTreeWidgetChanged
	
	# --- main tab slots end ---
	
	
	def __treeWidgetChild(self, childName, treeWidget = False):
		if (treeWidget == False):
			treeWidget = self.__p_selectModule.treeWidgetModules
		# end if
		
		for i in range(treeWidget.topLevelItemCount()):
			item = treeWidget.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				if (child.text(0) == childName):
					return child
				# end if
			# end for
		# end for
		
		return False
	# end __treeWidgetChild
	
	def __checkForDependencies(self, name):
		module = abstractModuleClass.d_modules[name]
		#module = self.__l_modules[name]
		for depModule in module["dependencies"]:
			if (depModule not in self.__l_usedModules):
				child = self.__treeWidgetChild(depModule)
				if (child != False):
					self.__l_usedModules.append(depModule)
					child.setCheckState(0, Qt.Checked)
				else:
					self.__p_logger.critical("module %s not found", depModule)
					return False
				# end if
			# end if
		# end for
		
		return True
	# end __checkForDependencies



	# ---- private end ----
	
	
	
	## @brief init function
	# @param self The object pointer.
	# @param availGeo available geometry as QRect
	# 
	# This init function load the modules an initialize the main gui. 
	def init(self, availGeo):
		self.__p_logger.debug("available geometry " + str(availGeo))
		self.__p_logger.debug("try load main window settings")
		
		self.setDockNestingEnabled(True)
		
		# load settings
		self.__loadSettings()

		# load modules
		self.__p_logger.debug("try load modules...")
		self.__loadModules()
		self.__p_logger.debug("load modules finished")

		# load state after modules		
		state = self.__p_settingsHandle.value('main/state')
		if (state):
			self.restoreState(state)
		# end if
		
	
		# expend all trees in module dialog
		for i in range(self.__p_selectModule.treeWidgetModules.topLevelItemCount()):
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(i)
			item.setExpanded(True)
		# end for

		# connect signals from settings menue
		self.actionSettingsLoad.triggered.connect(self.__onSettingsLoad)
		self.actionSettingsDefault.triggered.connect(self.__onSettingsDefault)
		self.actionSettingsSave.triggered.connect(self.__onSettingsSave)
		self.actionSettingsSaveAll.triggered.connect(self.__onSettingsSaveAll)
		
		# connect signals from main tab
		self.__p_selectModule.pushButtonSelectAll.clicked.connect(self.__selectAll)
		self.__p_selectModule.pushButtonUnselectAll.clicked.connect(self.__unselectAll)
		self.__p_selectModule.treeWidgetModules.itemChanged[QTreeWidgetItem, int].connect(self.__onTreeWidgetChanged)
		
		# check for window height
		# if available desktop height smaler than main window height, then move the logger dock widget to the left site
		if (availGeo.height() < self.height()):
			self.__p_logger.warn('Main Window was to height.')
		# end if
		
		# scroll log window
		self.__p_loggerListWidget.scrollToBottom()
	# end init


	## @brief main windows close event
	# @param self The object pointer.
	# @param event Qt event
	# 
	# Save all settings before closing.
	def closeEvent(self, event):
		modules = abstractModuleClass.d_modules
		
		# pre close
		for name in modules:
			if (modules[name]["modHandle"] == False):
				continue
			# end if
			
			modules[name]["handle"].onPreClose()
		# end for


		if (self.actionSaveSettingsOnExit.isChecked()):
			# save user settings
			self.__saveSettings()
			
			# save module settings
			self.__onSettingsSaveAll()
		# end if
		
		# delete all plots
		abstractModuleClass.deleteAllPlots()

		# close all modules
		for name in modules:
			if (modules[name]["modHandle"] == False):
				continue
			# end if

			modules[name]["handle"].onClose()

			for inc in modules[name]["handle"].getIncludes():
				del(inc)
			# end for

			delete(modules[name]["handle"])
			delete(modules[name]["modHandle"])
		# end for
		
		del(modules)
		del(abstractModuleClass.d_modules)

		#QMainWindow.__del__(self)
	# end closeEvent

	## @brief public interface function to freeze the GUI
	# @param self The object pointer.
	# @param freeze boolean
	# 
	# true: The user can't change the current module
	def setFreeze(self, freeze = False):
		curId = self.tabWidgetModules.currentIndex()

		for i in range(int(self.tabWidgetModules.count())):
			w = self.tabWidgetModules.widget(i)

			if (i != curId):
				w.setEnabled(not freeze)
			# end if
		# end for
	# end setFreeze

	## @brief return Output Widget object
	# @param self The object pointer.
	# @retval pointer logging output widget object
	def getOutputWidget(self):
		return self.listWidgetConsole
	# end getOutptuWidget

#end class mainWindow


## @brief dock widget class for main window dock widgets
class mainWindowDockWidget(QDockWidget):
	__l_widgets = list()
	__p_currentWidget = None
	
	def __init__(self, *args, **kwargs):
		QDockWidget.__init__(self, *args, **kwargs)
		
		# add this object to static list
		mainWindowDockWidget.__l_widgets.append(self)
	# end __init__
	
	def __del__(self):
		# move this object from static list
		mainWindowDockWidget.__l_widgets.pop(self)
		
		if (mainWindowDockWidget.__l_widgets == []):
			mainWindowDockWidget.__p_currentWidget = None
		# end if
	# end __del__
	
	# --- static methods begin ---
	
	@staticmethod
	def resetState():
		for dockWidget in mainWindowDockWidget.__l_widgets:
			dockWidget.setStyleSheet("")
		# end for
	# end if
	
	@staticmethod
	def getCurrentWidget():
		return mainWindowDockWidget.__p_currentWidget
	# end getCurrentWidget
	
	@staticmethod
	def setAsCurrent(dockWidget):
		# Do nothing if module already current active module.
		if (mainWindowDockWidget.__p_currentWidget == dockWidget):
			return False
		# end if
		
		# reset all modules
		mainWindowDockWidget.resetState()
		
		# mark last module as inactive
		if (mainWindowDockWidget.__p_currentWidget and mainWindowDockWidget.__p_currentWidget.widget()):
			mainWindowDockWidget.__p_currentWidget.widget().onInactive()
		# end if
		
		# set current dock widget as active module
		mainWindowDockWidget.__p_currentWidget = dockWidget
		
		# get GUI module and call onActive function
		dockWidget.widget().onActive()
		
		#frame = QFrame()
		dockWidget.setStyleSheet("QDockWidget::title { background-color: rgb(148, 148, 148); border: 1px solid grey; margin: 1px 1px 2px 1px; padding: 2px 1px 1px 0px; }")
		#dockWidget.setStyleSheet("::title { font: bold; }")
		#dockWidget.setTitleBarWidget(frame)
		
		return True
	# end setAsCurrent
	
	# --- static methods end ---
	
	def setVisible(self, visible):
		QDockWidget.setVisible(self, visible)
		
		if (visible):
			# set as current widget
			mainWindowDockWidget.setAsCurrent(self)
			
			# If dock widget is tabbed, then show on top.
			otherTabbedWidgets = self.parent().tabifiedDockWidgets(self)
			
			if (otherTabbedWidgets != []):
				self.raise_()
			# end if
		# end if
	# end setVisible
	
	def mousePressEvent(self, event):
		mainWindowDockWidget.setAsCurrent(self)
		
		return QDockWidget.mousePressEvent(self, event)
	# end focusInEvent
	
# end class mainWindowDockWidget

