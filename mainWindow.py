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


import os, sys, logging
from abstractModuleClass import abstractModuleClass, abstractGuiModuleClass
from functools import partial
from functions.mainMdiArea import mainMdiArea

# add sub dirs do path
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/functions/')


from PyQt4 import uic
#from PyQt4.Qt import QRect
from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot, QSettings, QProcess
from PyQt4.QtGui import QMainWindow, QTreeWidgetItem,	QDialog, QIcon, QWidget
import imp, re
from functions.helper import str2bool
from functions.delete import delete
from functions.progressBarThread import progressBarThread
from functions.guiLogger import QtLogger

# This is a special value defined in Qt4 but does not seem to be exported
# by PyQt4
QWIDGETSIZE_MAX = ((1 << 24) - 1)



## @brief main gui class
class mainWindow(QMainWindow):
	# ---------- Private ----------
	
	## @brief init class function
	# @param self The object pointer.
	# @param parent Qt parent object pointer.
	# 
	# init:
	# - create logger thread
	# - create main window logger client
	# - create global progress bar
	def __init__(self, loglevel, debug = False, *args, **kwargs):
		self.__initVars()
		
		QMainWindow.__init__(self, *args, **kwargs)

		#self.setupUi(self) # debug
		uic.loadUi("./main.ui", self)
		
		# init QtLogger
		QtLogger.printObj = self.listWidgetConsole

		# init logger
		self.__p_logger = logging.getLogger("mainWindow")
		self.__p_logger.setLevel(loglevel) # set log level to debug for main window
		# ... also set debug level for modules
		abstractModuleClass.loglevel = loglevel
		
		# Hide debugging menu in none debugging mode
		if (debug):
			# add debug menu
			self.menuDebug = self.menuBar().addMenu("Debug")
																						
			# add debug actions to menu
			self.actionPrintSettings = self.menuDebug.addAction("print settings")
			self.actionDelAllSettings = self.menuDebug.addAction("del all settings")
			
			# connect signals fo actions
			self.actionPrintSettings.triggered.connect(self.__onPrintSettings)
			self.actionDelAllSettings.triggered.connect(self.__onDelAllSettings)
		# end if
		
		# add help if operating system is windows
		if (sys.platform == "win32"):
			self.menuQ.addAction("GUI help", self.__onHelp)
			#action.triggered.connect(self.__onHelp)
		# end if
		
		# set parameters for global progress bar
		self.progressBarGlobal.setLabel(self.labelProgressBarGlobal)
		self.progressBarGlobal.disable()
		
		# progress bar
		self.__p_progressBarThread = progressBarThread(self)
		self.connect(self.__p_progressBarThread, SIGNAL('sigProgressBarUpdate(PyQt_PyObject)'), self.__onProgressBarUpdate)
		self.__p_progressBarThread.start()
		
		# about
		self.__p_about = QDialog(self)
		uic.loadUi("./about.ui", self.__p_about)
		self.actionAbout.triggered.connect(self.__p_about.exec)

		# license
		self.__p_license = QDialog(self)
		uic.loadUi("./license.ui", self.__p_license)
		self.actionLicense.triggered.connect(self.__p_license.exec)
		
		# setlect module dialog
		self.__p_selectModule = QDialog(self)
		uic.loadUi('./selectModule.ui', self.__p_selectModule)
		self.actionModules.triggered.connect(self.__p_selectModule.exec)
		
		# add mdiArea
		self.setCentralWidget(self.centralwidget)
		self.mdiAreaMain = mainMdiArea(self.centralwidget)
		self.centralwidget.layout().addWidget(self.mdiAreaMain, 0, 0)
		self.centralwidget.layout().addWidget(self.widgetProgressBar, 1, 0)

		self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		
		# create main settings object
		self.__p_settingsHandle = QSettings('./' + self.__v_userSettingsFileName, QSettings.IniFormat)
		
		# set QSettings handle
		abstractGuiModuleClass.settingsHandle = self.__p_settingsHandle
	# end __init__

	## @brief del function
	# @param self The object pointer.
	#
	# delete all member variables and threads
	def __del__(self):
		# delete list item pointer
		QtLogger.printObj = False
		
		# del progressBar
		if (self.__p_progressBarThread != False):
			self.disconnect(self.__p_progressBarThread, SIGNAL('sigProgressBarUpdate(PyQt_PyObject)'), self.__onProgressBarUpdate)
			self.__p_progressBarThread.stop()
			self.__p_progressBarThread.wait(500)
			del(self.__p_progressBarThread)
			self.__p_progressBarThread = False
		# end if
		
		self.__initVars()
	# end __del__
	
	## @brief init class variables
	# @param self The object pointer.
	# 
	# initialize variables
	def __initVars(self):
		## global module directory
		# with "/" at the end!!!
		self.__v_modulePath = "modules/"
		
		## path for GUI xml files
		self.__v_settingsFilePath = os.path.abspath(os.curdir) + '/'
		
		## filename from used modules xml file
		self.__v_userSettingsFileName = 'userSettings.ini'

		## current module object
		self.__p_currentModule = None
		
		## current tab index
		self.__v_currentTabIndex = -1
		
		self.__s_currentName = ""
		
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
		
		## bottom layout in menu bar
		self.__p_bottomMenuLayout = False
		
		## list of used modules
		self.__l_usedModules = []
		
		## progressbar object thread
		self.__p_progressBarThread = False
		
		##
		self.__v_lastModule = ''
		
		self.__p_openSetttingWidget = False		
	# end __initVars
	
	## @brief init function
	# @param self The object pointer.
	# @param availGeo available geometry as QRect
	# 
	# This init function load the modules an initialize the main gui. 
	def init(self, availGeo):
		self.__p_logger.debug("available geometry " + str(availGeo))
		self.__p_logger.debug("try load main window settings")
		
		# load settings
		self.__loadSettings()

		self.__p_logger.debug("try load modules...")
		self.__loadModules()
		self.__p_logger.debug("load modules finished")
	
		# expend all trees
		for i in range(self.__p_selectModule.treeWidgetModules.topLevelItemCount()):
			item = self.__p_selectModule.treeWidgetModules.topLevelItem(i)
			item.setExpanded(True)
		# end for

		# init gui
		self.actionSettingsLoad.triggered.connect(self.__onSettingsLoad)
		self.actionSettingsDefault.triggered.connect(self.__onSettingsDefault)
		self.actionSettingsSave.triggered.connect(self.__onSettingsSave)
		self.actionSettingsSaveAll.triggered.connect(self.__onSettingsSaveAll)
		
		# signals for action logger and dockWidgetLogger
		self.dockWidgetLogger.visibilityChanged[bool].connect(self.__onDockWidgetLoggerVisibilityChanged)
		
		# connect signals from main tab
		self.__p_selectModule.pushButtonSelectAll.clicked.connect(self.__selectAll)
		self.__p_selectModule.pushButtonUnselectAll.clicked.connect(self.__unselectAll)
		self.__p_selectModule.treeWidgetModules.itemChanged[QTreeWidgetItem, int].connect(self.__onTreeWidgetChanged)
		
		# connect signals from mdi area
		#self.mdiAreaMain.dropModule.connect(self.__onDropModuleInMdiArea)
		self.mdiAreaMain.subWindowActivated.connect(self.__onModuleActivated)
		self.mdiAreaMain.dockOut.connect(self.__onDockOut)
		
		## check for window height
		# if available desktop height smaler than main window height, then move the logger dock widget to the left site
		if (availGeo.height() < self.height()):
			self.dockWidgetLogger.setDockWidgetArea(Qt.LeftDockWidgetArea)
		# end if
	# end init


	@pyqtSlot()
	def __onHelp(self):
		path = os.path.abspath(os.curdir) + "/doc/index.chm"
		QProcess.startDetached("hh.exe " + path)
	# end __onHelp
	
	@pyqtSlot(bool)
	def __onDockWidgetLoggerVisibilityChanged(self, visible):
		self.actionLogger.setChecked(visible)
	# end __onDockWidgetLoggerVisibilityChanged
	
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
				modHandle = imp.load_source(name, moduleDir + "/" + name + ".py")

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
		# end for
		
		# init modules
		for module in modules:
			if (module["modHandle"] == False):
				continue
			# end if
			#module["handle"] = module["modHandle"].module(None, module["name"])
			module["handle"] = module["modHandle"].module(self, module["name"])
			
			#self.__p_logger.debug("load module " + module["name"])
		# end for

		# open modules
		abstractModuleClass.d_modules = dict()
		abstractModuleClass.p_progressBar = self.progressBarGlobal
		abstractModuleClass.p_progressBarThread = self.__p_progressBarThread
		
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
				moduleHand.setModulePath(self.__v_modulePath + module["suffix"] + module["name"], os.path.abspath(os.curdir))
				moduleHand.setIncludes(includes)
	
				# check for module type
				moduleClassType = moduleHand.getClassType()
				
				action = False

				# module type specific init
				if (moduleClassType == "application"):
					# load [moduleName].ui
					self.__p_logger.setLevel(logging.WARN)
					uic.loadUi(moduleDir + "/" +moduleName + ".ui", moduleHand)
					self.__p_logger.setLevel(logging.DEBUG)

					# get menu button and connect
					button = moduleHand.getMenuButton()
					a = self.toolBar.addWidget(button)
					moduleHand.setMenuAction(a)
					
					# connect signal from application menu button
					button.clicked.connect(self.__onModuleShow) # clicked[Widget] wird nicht benoetigt, da dies in pyqtSlot entahlten sind
					button.doubleClicked.connect(self.__onModuleShowMaximized)
				elif (moduleClassType == "setting"):
					# load [moduleName].ui
					
					self.__p_logger.setLevel(logging.WARN)
					uic.loadUi(moduleDir + "/" + moduleName + ".ui", moduleHand)
					self.__p_logger.setLevel(logging.DEBUG)

					action = self.menuModuleSettings.addAction(moduleName)

					# connect signals
					#self.connect(action, SIGNAL('triggered()'), partial(self.__onSettingWidgetShow, module['handle']))
					action.triggered.connect(partial(self.__onSettingWidgetShow, module['handle']))
					self.connect(moduleHand, SIGNAL('onClose(PyQt_PyObject)'), self.__onSettingWidgetClose)
				# end if

				iconPath = False	
				if (moduleClassType != "hidden"):
					moduleHand.initPreSettings()
					moduleHand.handleSettings()
					moduleHand.loadSettings()
					
					iconPath = moduleHand.getIconPath()
				# end if

				# use module icons
				# application: icon for menu button
				# setting: icon for QAction
				icon = None
				if (iconPath != False):
					icon = QIcon(iconPath)
					if (moduleClassType == 'application'):
						moduleHand.getMenuButton().setIcon(icon)
					elif (moduleClassType == 'setting'):
						action.setIcon(icon)
					# end if
				# end if

				# join in specific modules folder for initModule
				os.chdir(moduleDir)
				moduleHand.initModule()
				os.chdir(currentDir)
	
				# add module widget to GUI
				if (moduleClassType == 'application'):
					# init menu button
					button = moduleHand.getMenuButton()
					button.setText(moduleHand.getDisplayName())
					
					# add module to mdiArea an set visible = false
					#self.widgetMain.layout().addWidget(moduleHand)
					sw = self.mdiAreaMain.addSubWindow(moduleHand)
					sw.setVisible(False)
					
					# set window options like title ect.
					sw.setWindowTitle(moduleName)
					sw.setWindowIcon(moduleHand.getMenuButton().icon())
				
					# connect on invisible signal
					moduleHand.onInvisible[QWidget].connect(self.__onModuleInvisible)
					
					#moduleHand.setParent(self)
				elif (moduleClassType == 'setting'):
					moduleHand.setWindowTitle(moduleHand.getDisplayName())
					moduleHand.setParent(self, Qt.Window)
				else:
					moduleHand.setParent(None)
				# end if
			except Exception as e:
				msg = "Fehler in Module " + moduleName
				self.__p_logger.critical(msg)
				print(msg)
				raise e
			# end try
		# end for
		
		#self.mdiAreaMain.cascadeSubWindows()

		# init gui
		for module in modules:
			if (module["modHandle"] == False):
				continue
			# end if
			
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

			if (moduleName == self.__v_lastModule):
				mod = abstractModuleClass.getModuleByName(moduleName)
				if (mod != False):
					self.__onModuleShowMaximized(mod['handle'])
					mod['handle'].getMenuButton().setChecked(True)
				# end if
			# end if
		# end for
	# end __loadModules
	
	def __onSettingWidgetShow(self, module):
		if (self.__p_openSetttingWidget != False):
			self.__p_logger.error('There ist already a settings module opend.')
			return
		# end if

		self.__p_openSetttingWidget = module
		module.show()
	# end __onSettingWidgetShow
	
	def __onSettingWidgetClose(self, module):
		self.__p_openSetttingWidget = False
	# end __onSettingWidgetClose
	
	## @brief if module docks out from mdiArea
	@pyqtSlot(QWidget)
	def __onDockOut(self, win):
		# get module widget from subWindow 
		module = win.widget()

		# delete sub window
		win.setWidget(None)
		self.mdiAreaMain.removeSubWindow(win)
		del(win)
		
		# set new parent for module
		module.setParent(self, Qt.Window)
		
		# set icon and show module
		module.setWindowIcon(module.getMenuButton().icon())
		module.show()
		module.move(self.geometry().center() - module.geometry().center())
	# end __onDockOut
	
	## Qt slot: emit if module ignore close event and set visible = false
	# @param module: module pointer
	@pyqtSlot(QWidget)
	def __onModuleInvisible(self, module):
		if (len(self.mdiAreaMain.visibleSubWindowList()) == 0):
			self.__p_currentModule = None
		# end if
	# end __onMpduleInvisible
	
	## @brief connect with subWindowActivated from mdiAreaMain
	# @param widget: current widget in mdiArea
	@pyqtSlot(QWidget)
	def __onModuleActivated(self, widget):
		# do nothing on mainWindow close
		if (widget == None):
			return
		# end if
		
		self.__p_currentModule = widget.widget() 
		self.__p_currentModule.onActive()
		
		# inactive other visible windows
		subWindows = self.mdiAreaMain.visibleSubWindowList()
		if (len(subWindows) > 1):
			for subWin in subWindows:
				if (subWin != widget):
					subWin.widget().onInactive()
				# end if
				
				#subWin.widget().getMenuButton().setChecked(True)
			# end for
		# end if
	# end __onModuleActivated
	
	## @brief if a menu button was double clicked
	# @param module: module pointer which module have to be displayed
	# show only one module in full screen
	@pyqtSlot(QWidget)
	def __onModuleShowMaximized(self, module):
		mdiWindow = module.parent()
		
		# set new module as current module
		self.__p_currentModule = module

		# maximize module
		mdiWindow.showMaximized()
	# end __onModuleShowMaximized
	
	## @brief if menu button was double clicked
	# @param module: module pointer
	# visible this module in mdiArea
	@pyqtSlot(QWidget)
	def __onModuleShow(self, module):
		mdiWindow = module.parent()
		
		if (mdiWindow.metaObject().className() != "QMdiSubWindow"):
			module.setParent(None)
			mdiWindow = self.mdiAreaMain.addSubWindow(module)
			module.setVisible(True)
			mdiWindow.setWindowIcon(module.getMenuButton().icon())
		# end if
		
		# Falls das Module schon sichtbar ist, wird es nur aktiviert.
		if (mdiWindow.isVisible()):
			if (not module.getMenuButton().isChecked() and self.mdiAreaMain.activeSubWindow() == mdiWindow):
				mdiWindow.close()
			else:
				module.getMenuButton().setChecked(True)
				self.mdiAreaMain.setActiveSubWindow(mdiWindow)
			# end if
		else:
			#self.mdiAreaMain.cascadeSubWindows()
			mdiWindow.setVisible(True)
		# end if
		
		self.__p_currentModule = module
	# end __onModuleShow
	
	"""
	## @brief slot for dropModule signal from mdiArea
	# @param name: string name of module
	@pyqtSlot(str)
	def __onDropModuleInMdiArea(self, name):
		mod = abstractModuleClass.getModuleByName(name)

		mod['handle'].parent().setVisible(True)
		#self.mdiAreaMain.setActiveSubWindow(mod['handle'].parent())
		#self.mdiAreaMain.tileSubWindows()
		self.mdiAreaMain.cascadeSubWindows()
	# end __onDropModuleInMdiArea
	"""

	
	## @brief get user settings like used module list and gui position
	# @param self The object pointer.
	# 
	# Load only the modules which were selected by the user.
	def __loadSettings(self):
		# main group
		self.__p_settingsHandle.beginGroup('main')
		displayName = self.__p_settingsHandle.value("displayName", "pyGUI")
		geo = self.__p_settingsHandle.value("geo")
		state = self.__p_settingsHandle.value('state')
		self.__p_settingsHandle.endGroup()
		
		saveOnExit = self.__p_settingsHandle.value("settings/saveOnExit", True)
		
		# modules group
		self.__p_settingsHandle.beginGroup('module')
		self.__l_usedModules = self.__p_settingsHandle.value('used', [])
		self.__v_lastModule = self.__p_settingsHandle.value('last', '')
		self.__p_settingsHandle.endGroup()

		# restore state and geometry if information ist available
		if (state):
			self.restoreState(state)
		# end if
		if (geo):
			self.restoreGeometry(geo)
		# end if

		# if no used moduels ar available		
		if (self.__l_usedModules == None):
			self.__l_usedModules = []
		# end if
		
		# set last used module
		if (self.__v_lastModule == None):
			self.__v_lastModule = ''
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
		
		# current module
		if (self.__p_currentModule != None):
			lastMod = self.__p_currentModule.getName()
		else:
			lastMod = ''
		# end if
		
		
		# main window settings
		self.__p_settingsHandle.setValue("main/geo", self.saveGeometry())
		self.__p_settingsHandle.setValue("main/state", self.saveState())
		self.__p_settingsHandle.setValue("main/displayName", self.windowTitle().split()[0])
		
		# used moduel setttings
		self.__p_settingsHandle.setValue("module/used", self.__l_usedModules)
		self.__p_settingsHandle.setValue("module/last", lastMod)
		
		# settings
		self.__p_settingsHandle.setValue("settings/saveOnExit", self.actionSaveSettingsOnExit.isChecked())
	# end __saveSettings


	## @brief private slot for main bar: settings -> load
	# @param self The object pointer.
	def __onSettingsLoad(self):
		# Use open settings widget if it's opend.
		if (self.__p_openSetttingWidget):
			self.__p_openSetttingWidget.loadSettings()
			return
		# end if
		
		# If no settings widget is open check if current module is no hidde module. It's only a safty function.
		if (self.__p_currentModule != None and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.loadSettings()
		# end if
	# end __onSettingsLoad
	
	## @brief private slot for menu bar: settings -> save
	# @param self The object pointer.
	def __onSettingsSave(self):
		if (self.__p_openSetttingWidget):
			self.__p_openSetttingWidget.saveSettings()
			return
		# end if
		
		if (self.__p_currentModule != None and "getClassType" in dir(self.__p_currentModule) and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.saveSettings()
		# end if
	# end __onSettingsSave
	
	## @brief debug function: Print settings from current active module
	# @param self The object pointer.
	@pyqtSlot()
	def __onPrintSettings(self):
		if (self.__p_openSetttingWidget):
			print(self.__p_openSetttingWidget.getSettings())
			return
		# end if
		
		if (self.__p_currentModule):
			print(self.__p_currentModule.getSettings())
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

	## @brief private slot for menu bar: settings -> load default
	# @param self The object pointer.
	def __onSettingsDefault(self):
		if (self.__p_openSetttingWidget):
			self.__p_openSetttingWidget.loadDefaultSettings()
			return
		# end if
		
		if (self.__p_currentModule != None and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.loadDefaultSettings()
		# end if
	# end __onSettingsDefault
	
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

	# ---------- Private ----------

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

