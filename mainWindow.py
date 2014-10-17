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
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#
# @brief Main window from Qt GUI and global module handler


import os, sys

# add sub dirs do path
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/functions/')


from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, Qt, QPoint
from PyQt4.QtGui import QMainWindow, QTreeWidgetItem, QMenu, QApplication,\
	QDialog, QAction
import imp, re
import xml.dom.minidom as dom
from xmlHelper import readXMLNodes, getXMLNodeByAttributeValue, str2bool
from delete import delete
from progressBarThread import progressBarThread

# import logger classes
import guiLogger.server as logServer
import guiLogger.client as logClient


## @brief main gui class
class mainWindow(QMainWindow):

	# ---------- Private ----------
	
	## @brief init class function
	# @param self The object pointer.
	# @param parent Qt parent object pointer.
	# 
	# <pre>
	# - create logger thread
	# - create main window logger client
	# - create global progressbar
	# </pre>
	def __init__(self, parent=None):
		self.__initVars()
		
		QMainWindow.__init__(self, parent)

		#self.setupUi(self) # debug
		uic.loadUi("./main.ui", self)

		# init logger server
		self.__p_loggerThread = logServer.loggingThread(self)
		self.connect(self.__p_loggerThread, SIGNAL("logReceived(PyQt_PyObject)"), self.__onLogReceived, Qt.QueuedConnection)
		self.__p_loggerThread.start()

		# init logger client
		self.__p_loggerClient = logClient.clientLogger("mainWindow")
		self.__p_logger = self.__p_loggerClient.getLogger()
		
		# set parameters for global progress bar
		self.progressBarGlobal.setLabel(self.labelProgressBarGlobal)
		self.progressBarGlobal.disable()
		
		# progress bar
		self.__p_progressBarThread = progressBarThread(self)
		self.connect(self.__p_progressBarThread, SIGNAL('sigProgressBarUpdate(PyQt_PyObject)'), self.__onProgressBarUpdate)
		self.__p_progressBarThread.start()
	# end __init__

	## @brief del function
	# @param self The object pointer.
	#
	# delete all member variables and threads
	def __del__(self):
		if (self.__p_loggerClient != False):
			delete(self.__p_loggerClient)
			self.__p_loggerClient = False
		# end if
		
		# delete thread if exist
		if (self.__p_loggerThread != False):
			self.__p_loggerThread.stop()
			self.__p_loggerThread.wait(500)
			if (not self.__p_loggerThread.isFinished()):
				raise Exception("logger server thread not closed")
			# end if
			del(self.__p_loggerThread)
			self.__p_loggerThread = False
		# end if
		
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
		self.__v_settingsFilePath = "./"
		
		## filename from main settings xml file
		self.__v_settingsFileName = "main.xml"
		
		## filename from used modules xml file
		self.__v_moduleSettingsFileName = 'modules.xml'
		
		## modules list
		self.__l_modules = list()
		
		## current module object
		self.__p_currentModule = False
		
		## about dialog
		self.__p_about = False
		
		## license dialog
		self.__p_license = False
		
		## main settings dom object
		self.__p_settingsHandle = False
		
		## list of unused modules
		self.__p_usedModulesHandle = False
		
		## main GUI logger client object
		self.__p_loggerClient = False
		
		## main gui logger object
		self.__p_logger = False
		
		## logger server object thread
		self.__p_loggerThread = False
		
		## current tab/module
		self.__l_currentTab = {"parent": False, "index": -1}
		
		## list of used modules
		self.__l_usedModules = []
		
		## progressbar object thread
		self.__p_progressBarThread = False
	# end __initVars
	
	## @brief init function
	# @param self The object pointer.
	# 
	# This init function load the modules an initialize the main gui. 
	def init(self):		
		self.__p_logger.debug("try load main window settings")
		self.__loadSettings()
		
		# load used modules
		self.__loadUsedModules()

		self.__p_logger.debug("try load modules...")
		self.__readModules()
		self.__p_logger.debug("load modules finished")
		
		# expend all trees
		for i in range(self.treeWidgetModules.topLevelItemCount()):
			item = self.treeWidgetModules.topLevelItem(i)
			item.setExpanded(True)
		# end for
		
		# set current tab
		if (self.__l_currentTab["parent"] != False and self.__l_currentTab["index"] > -1):
			# visible settings tab if current tab is an settings tab
			if (self.__l_currentTab["parent"] == self.tabWidgetSettings):
				self.tabWidgetModules.setCurrentIndex(1)

			# set tab as current tab
			self.__l_currentTab["parent"].setCurrentIndex(self.__l_currentTab["index"])

			self.__onChangeModule(-1)
		# end if

		# init gui
		self.connect(self.actionSettingsLoad, SIGNAL("triggered()"), self.__onSettingsLoad)
		self.connect(self.actionSettingsDefault, SIGNAL("triggered()"), self.__onSettingsDefault)
		self.connect(self.actionSettingsSave, SIGNAL("triggered()"), self.__onSettingsSave)
		self.connect(self.actionSettingsSaveAll, SIGNAL("triggered()"), self.__onSettingsSaveAll)

		self.connect(self.tabWidgetModules, SIGNAL("currentChanged(int)"), self.__onChangeModule)
		self.connect(self.tabWidgetSettings, SIGNAL("currentChanged(int)"), self.__onChangeModule)
		
		# connect signals from main tab
		self.connect(self.pushButtonSelectAll, SIGNAL("clicked()"), self.__selectAll)
		self.connect(self.pushButtonUnselectAll, SIGNAL("clicked()"), self.__unselectAll)
		self.connect(self.treeWidgetModules, SIGNAL("itemChanged(QTreeWidgetItem*, int)"), self.__onTreeWidgetChanged)

		# about
		self.__p_about = QDialog(self)
		uic.loadUi("./about.ui", self.__p_about)
		self.connect(self.actionAbout, SIGNAL("triggered()"), self.__p_about, SLOT("exec()"))

		# license
		self.__p_license = QDialog(self)
		uic.loadUi("./license.ui", self.__p_license)
		self.connect(self.actionLicense, SIGNAL("triggered()"), self.__p_license, SLOT("exec()"))
	# end init
	
	## @brief private slot for updating the progressbar
	# @param self The object pointer.
	# @param ret List with command and command value.
	#
	# <pre>
	# ret[0]: values
	# ret[1]: commands
	#
	# valid commands:
	# - init
	# - clear
	# - disable
	# - newVal or ready
	# </pre>
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
	
	## @brief private slot to show logging information
	# @param self The object pointer.
	# @param item listWidgetItem
	def __onLogReceived(self, item):
		self.listWidgetConsole.addItem(item)
		self.listWidgetConsole.scrollToItem(item)
	# end __onLogReceived

	## @brief search for modules
	# @param self The object pointer.
	#
	# Load all modules from self.__v_modulePath
	def __readModules(self):
		# init variables
		loadOrder = ["hidden", "setting", "application"]

		currentDir = os.path.abspath(os.curdir)
		modulesPath = currentDir + "/" + self.__v_modulePath
		content = os.listdir(modulesPath)
		content.sort()
		modules = []
		moduleNames = []
		
		# clear gui list
		self.treeWidgetModules.reset()
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
			item = self.treeWidgetModules.topLevelItem(index)
			item.addChildren(itemList[moduleClassType])
			
			index += 1
		# end for
		
		# init modules
		for module in modules:
			if (module["modHandle"] == False):
				continue

			module["handle"] = module["modHandle"].module(self, module["name"])
			self.__p_logger.debug("load module " + module["name"])
		# end for

		# open modules
		self.__l_modules = dict()
		for module in modules:
			try:
				widget = False
				self.__l_modules[module["name"]] = module
				
				# if module not used
				if (module["modHandle"] == False):
					continue
				# end if
				
				moduleDir = modulesPath + module["suffix"] + module["name"]
	
				# find *.py files in the specific modules directory
				os.chdir(moduleDir)
				content = os.listdir(moduleDir)
				includes = dict()
				for filename in content:
					if (os.path.isfile(moduleDir + "/" + filename)):
						if (re.match(".*\.py$", filename) and not (module["name"] + ".py") == filename ):
							name = filename[0:-3]
							includes[name] = imp.load_source(name, moduleDir + "/" + filename)
						# end if
					# end if
				# end for
				os.chdir(currentDir)
				
				# set module settings
				module["handle"].setModulePath(self.__v_modulePath + module["suffix"] + module["name"], os.path.abspath(os.curdir))
				module["handle"].setModuleArray(self.__l_modules)
				module["handle"].setIncludes(includes)
				module["handle"].setProgressBar(self.progressBarGlobal)
				module["handle"].setProgressBarThread(self.__p_progressBarThread)
	
				# check for module type
				moduleClassType = module["handle"].getClassType()
				if (moduleClassType == "application"):
					widget = self.tabWidgetModules
					# load [moduleName].ui
					uic.loadUi(moduleDir + "/" + module["name"] + ".ui", module["handle"])
				elif (moduleClassType == "setting"):
					widget = self.tabWidgetSettings
					# load [moduleName].ui
					uic.loadUi(moduleDir + "/" + module["name"] + ".ui", module["handle"])
				# end if
				
				module["handle"].initPreSettings()
	
				if (moduleClassType != "hidden"):
					module["handle"].loadSettings()
				# end if
	
				# join in specific modules folder
				os.chdir(moduleDir)
				module["handle"].initModule()
				os.chdir(currentDir)
	
				if (moduleClassType != "hidden"):
					widget.addTab(module["handle"], module["handle"].getDisplayName())
				else:
					module["handle"].setParent(None)
				# end if
			except Exception as e:
				msg = "Fehler in Module " + module["name"]
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
		for module in usedModules:
			if (module not in self.__l_modules):
				self.__l_usedModules.remove(module)
			# end if
		# end for
	# end __readModules

	## @brief load settings from main.xml
	# @param self The object pointer.
	def __loadSettings(self):
		if (self.__v_settingsFileName in os.listdir(self.__v_settingsFilePath)):
			self.__p_settingsHandle = dom.parse(self.__v_settingsFilePath + self.__v_settingsFileName)
		else:
			self.__p_settingsHandle = dom.parseString("<settings></settings>")
		# end if

		# settings
		settings = self.__p_settingsHandle.getElementsByTagName("settings")[0]

		# main window
		x = 50
		y = 50
		items = readXMLNodes(settings, "lastPosition")

		if (len(items) > 0 and "x" in items[0] and "y" in items[0]):
			x = int(items[0]["x"])
			y = int(items[0]["y"])
		# end if

		# set geometry
		geo = self.geometry()
		geo.setX(x)
		geo.setY(y)
		self.setGeometry(geo)

		# checked
		items = readXMLNodes(settings, "checked")
		for item in items:
			if (item["name"] == "saveonexit"):
				self.actionSaveSettingsOnExit.setChecked(str2bool(item["checked"]))
		# end for

		# last current tab
		items = readXMLNodes(settings, "lastTab")
		if (len(items) > 0 and "module" in items[0] and "settings" in items[0]):
			moduleId = int(items[0]["module"])
			settingsId = int(items[0]["settings"])

			if (moduleId > -1):
				self.__l_currentTab["parent"] = self.tabWidgetModules
				self.__l_currentTab["index"] = moduleId
			elif (settingsId > -1):
				self.__l_currentTab["parent"] = self.tabWidgetSettings
				self.__l_currentTab["index"] = settingsId
			# end if
		# end if
	# end __loadSettings

	## @brief save settings to main.xml
	# @param self The object pointer.
	def __saveSettings(self):
		settings = self.__p_settingsHandle.getElementsByTagName("settings")[0]

		# gui position
		geo = self.geometry()
		node = settings.getElementsByTagName("lastPosition")
		if (len(node) > 0):
			node = node[0]
			node.setAttribute("x", str(geo.x()))
			node.setAttribute("y", str(geo.y()))
		else:
			node = self.__p_settingsHandle.createElement("lastPosition")
			node.setAttribute("x", str(geo.x()))
			node.setAttribute("y", str(geo.y()))
			settings.appendChild(node)
		# end if

		# check fields
		node = getXMLNodeByAttributeValue(settings, "checked", "name", "saveonexit")
		checked = str(self.actionSaveSettingsOnExit.isChecked())
		if (node):
			node.setAttribute("checked", checked)
		else:
			node = self.__p_settingsHandle.createElement("checked")
			node.setAttribute("name", "saveonexit")
			node.setAttribute("checked", checked)
			settings.appendChild(node)
		# end if

		# current tab
		settingsID = -1
		moduleID = self.tabWidgetModules.currentIndex()
		name = self.tabWidgetModules.tabText(moduleID)

		if (name == "Settings"):
			widget = self.tabWidgetSettings.currentWidget()
			if (widget is not None):
				name = widget.getName()
				settingsID = self.tabWidgetSettings.currentIndex()
				moduleID = -1
		# end if

		node = settings.getElementsByTagName("lastTab")
		if (len(node) > 0):
			node = node[0]
			node.setAttribute("module", str(moduleID))
			node.setAttribute("settings", str(settingsID))
		else:
			node = self.__p_settingsHandle.createElement("lastTab")
			node.setAttribute("module", str(moduleID))
			node.setAttribute("settings", str(settingsID))
			settings.appendChild(node)
		# end if

		# save to xml
		writer = open(self.__v_settingsFilePath + self.__v_settingsFileName, "w")
		self.__p_settingsHandle.writexml(writer)
		writer.close()
	# end __saveSettings
	
	## @brief get used module list from modules.xml
	# @param self The object pointer.
	# 
	# Load only the modules which were selected by the user
	def __loadUsedModules(self):
		# falls die datei nicht vorhandne ist wird sie erstellt
		if (self.__v_moduleSettingsFileName in os.listdir(self.__v_settingsFilePath)):
			self.__p_usedModulesHandle = dom.parse(self.__v_settingsFilePath + self.__v_moduleSettingsFileName)
		else:
			self.__p_usedModulesHandle = dom.parseString("<usedModules></usedModules>")
		# end if
		
		modulesHandle = self.__p_usedModulesHandle.getElementsByTagName("usedModules")[0]
		
		modules = readXMLNodes(modulesHandle, "module")
		for module in modules:
			self.__l_usedModules.append(module["name"])
		# end for
	# end __loadUsedModules
	
	## @brief save used modules into modules.xml
	# @param self The object pointer.
	def __saveUsedModules(self):
		# modules
		self.__l_usedModules = []
		for i in range(self.treeWidgetModules.topLevelItemCount()):
			item = self.treeWidgetModules.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				if (child.checkState(0) == Qt.Checked):
					self.__l_usedModules.append(child.text(0))
				# end if
			# end for
		# end for
		
		node = self.__p_usedModulesHandle.getElementsByTagName("usedModules")[0]
		modules = readXMLNodes(node, "module")

		for module in modules:
			node.removeChild(module["hand"])
		# end for

		for module in self.__l_usedModules:
			childNode = self.__p_usedModulesHandle.createElement("module")
			childNode.setAttribute("name", module)
			node.appendChild(childNode)
		# end for
		
		# save to xml
		writer = open(self.__v_settingsFilePath + self.__v_moduleSettingsFileName, "w")
		self.__p_usedModulesHandle.writexml(writer)
		writer.close()
	# end __saveUsedModules

	## @brief private slot for main bar: settings -> load
	# @param self The object pointer.
	def __onSettingsLoad(self):
		if (self.__p_currentModule and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.loadSettings()
		# end if
	# end __onSettingsLoad

	## @brief private slot for menu bar: settings -> save
	# @param self The object pointer.
	def __onSettingsSave(self):
		if (self.__p_currentModule and "getClassType" in dir(self.__p_currentModule) and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.saveSettings()
		# end if
	# end __onSettingsSave

	## @brief private slot for menu bar: settings -> save all
	# @param self The object pointer.
	def __onSettingsSaveAll(self):
		for name in self.__l_modules:
			if (self.__l_modules[name]["modHandle"] == False):
				continue
			# end if
			
			if (self.__l_modules[name]["handle"].getClassType() != "hidden"):
				self.__l_modules[name]["handle"].saveSettings()
			# end if
		# end for
	# def __onSettingsSaveAll

	## @brief private slot for menu bar: settings -> load default
	# @param self The object pointer.
	def __onSettingsDefault(self):
		if (self.__p_currentModule and self.__p_currentModule.getClassType() != "hidden"):
			self.__p_currentModule.loadDefaultSettings()
	# end __onSettingsDefault

	## @brief private slot for change the current module
	# @param self The object pointer.
	# @param ID current tab index (default -1)
	def __onChangeModule(self, ID):
		ID = self.tabWidgetModules.currentIndex()
		name = self.tabWidgetModules.tabText(ID)

		if (name == "Settings"):
			widget = self.tabWidgetSettings.currentWidget()
			if (widget is None):
				self.__p_currentModule = False
				return
			# end if
			name = widget.getName()
		else:
			widget = self.tabWidgetModules.currentWidget()
		# end if

		self.__p_currentModule = widget

		if (name != "Main"):
			self.__p_currentModule.onActive()
	# end __onChangeModule
	
	## @brief private slot for push button select all
	# @param self The object pointer.
	def __selectAll(self):
		self.__l_usedModules = []
		for i in range(self.treeWidgetModules.topLevelItemCount()):
			item = self.treeWidgetModules.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				child.setCheckState(0, Qt.Checked)
				self.__l_usedModules.append(child.text(0))
			# end for
		# end for
	# end __selectAll
	
	## @brief private slot for push button unselect all
	# @param self The object pointer.
	def __unselectAll(self):
		self.__l_usedModules = []
		for i in range(self.treeWidgetModules.topLevelItemCount()):
			item = self.treeWidgetModules.topLevelItem(i)
			for c in range(item.childCount()):
				child = item.child(c)
				child.setCheckState(0, Qt.Unchecked)
			# end for
		# end for
	# end __unselectAll
	
	def __treeWidgetChild(self, childName, treeWidget = False):
		if (treeWidget == False):
			treeWidget = self.treeWidgetModules
		
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
		module = self.__l_modules[name]
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
	
	def __onTreeWidgetChanged(self, item, column):
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
				for modName in self.__l_modules:
					if (modName in self.__l_usedModules and name in self.__l_modules[modName]["dependencies"]):
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
		# pre close
		for name in self.__l_modules:
			if (self.__l_modules[name]["modHandle"] == False):
				continue
			# end if
			
			self.__l_modules[name]["handle"].onPreClose()
		# end for
		
		# save main settings
		self.__saveSettings()
		
		# save used modules
		self.__saveUsedModules()

		# save module settings
		if (self.actionSaveSettingsOnExit.isChecked()):
			self.__onSettingsSaveAll()
		# end if

		# close all modules
		for name in self.__l_modules:
			if (self.__l_modules[name]["modHandle"] == False):
				continue
			# end if

			self.__l_modules[name]["handle"].onClose()

			for inc in self.__l_modules[name]["handle"].getIncludes():
				del(inc)
			# end for

			delete(self.__l_modules[name]["handle"])
			delete(self.__l_modules[name]["modHandle"])
		# end for

		# accept close event (maybe not used???)
		event.accept()
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

	
	def __onConsoleClear(self):
		self.listWidgetConsole.clear()
	# end __onConsoleClear
	
	def __onConsoleCopy(self):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(self.listWidgetConsole.currentItem().text(), mode=cb.Clipboard)
	# end __onConsoleCopy
	
	def __onConsoleEmpty(self):
		self.listWidgetConsole.addItem('')
	# end __onConsoleEmpty
	
	def contextMenuEvent(self, event):
		pos = event.pos()
		lw = self.listWidgetConsole
		qm = self.menubarMain.height()
		
		if (pos.x() >= lw.pos().x() and pos.x() < lw.pos().x() + lw.width() and pos.y() >= lw.pos().y() + qm and pos.y() < lw.pos().y() + lw.height() + qm):
			popup = QMenu(self)
			popup.addAction('clear all', self.__onConsoleClear)
			a = popup.addAction('copy line', self.__onConsoleCopy)
			popup.addAction('insert empty line', self.__onConsoleEmpty)
			if (self.listWidgetConsole.count() == 0):
				a.setEnabled(False)
			# end if
			
			pos = QPoint(pos.x() + self.x(), pos.y() + self.y() + qm)
			popup.popup(pos)
		# end if
	# end contextMenuEvent

#end class mainWindow
