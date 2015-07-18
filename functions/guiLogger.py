##
# @file guiLogger.py
# 
# @date 2015-03-28
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
# @brief print logs into Qt list element


import logging
from PyQt4.QtCore import Qt, pyqtSlot, QEvent, pyqtSignal
from PyQt4.QtGui import QListWidgetItem, QBrush, QListWidget, QMenu, QApplication,\
	QCursor, QDockWidget, QSizePolicy


## @brief custom python logger
#
class QtLogger(logging.Handler):
	printObj = False
	
	def __init__(self, *args, **kwargs):
		logging.Handler.__init__(self, *args, **kwargs)
	# end __init__
	
	def emit(self, record):
		s = self.format(record)
		
		# add filename and line number to output on debug
		if (record.levelno == logging.DEBUG):
			s += '\n' + str(record.filename) + ' at ' + str(record.lineno)
		# end if

		if (QtLogger.printObj != False):
			item = QListWidgetItem(s)

			if (record.levelno == logging.CRITICAL or record.levelno == logging.ERROR):
				item.setForeground(QBrush(Qt.red))
			elif (record.levelno == logging.WARN):
				item.setForeground(QBrush(Qt.blue))
			elif (record.levelno == logging.DEBUG):
				item.setForeground(QBrush(Qt.gray))
			# end if
			
			# add item to list view and scroll to them
			if (QtLogger.printObj.count() > 100):
				QtLogger.printObj.takeItem(0)
			# end if
			
			QtLogger.printObj.addItem(item)
			#QtLogger.printObj.scrollToItem(item)
			#QtLogger.printObj.scrollToBottom()
			#QtLogger.printObj.insertItem(0, item)
			
			QtLogger.printObj.itemAdded.emit()
		else:
			print(s)
		# end if
	# end emit

# end class qtLogger


## @brief dock widget for logging window
#
class QtLoggerDockWidget(QDockWidget):
	def __init__(self, *args, **kwargs):
		QDockWidget.__init__(self, *args, **kwargs)
		
		# connect signals  if doock widget area was changed
		self.dockLocationChanged[Qt.DockWidgetArea].connect(self.__onDockWidgetLoggerLocationChanged)
		
		# set minimum size
		self.setMinimumHeight(100)
		
		# set sice policy
		#self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		
		# set dock widget floatable
		self.setFeatures(self.features() | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetVerticalTitleBar)
	# end __init
	
	## @brief qt change event
	# @param self The object pointer.
	# @param event qt event
	#
	# Reset minimum size. Because qt change minimum size if title bar were changed.
	def changeEvent(self, event):
		if (event.type() == QEvent.LocaleChange):
			self.setFeatures(self.features() | QDockWidget.DockWidgetVerticalTitleBar)
			self.setMinimumHeight(100)
		# end if

		return QDockWidget.changeEvent(self, event)
	# end changeEvent
	
	## @brief slot if dock widget was moved
	# @param self The object pointer.
	# @param area DockWidgetArea
	#
	# If Dock widget on left or right area: Show title bar on top
	# If dock widget is on top or bottom area: Show title bar at the left site. 
	@pyqtSlot(Qt.DockWidgetArea)
	def __onDockWidgetLoggerLocationChanged(self, area):
		if (area == Qt.BottomDockWidgetArea or area == Qt.TopDockWidgetArea):
			self.setFeatures(self.features() | QDockWidget.DockWidgetVerticalTitleBar)
		else:
			self.setFeatures(self.features() & ~QDockWidget.DockWidgetVerticalTitleBar)
		# end if
	# end
	
# end class QtLoggerDockWidget


## @brief Qt list widget for logger
class QtLoggerListWidget(QListWidget):
	itemAdded = pyqtSignal()
	
	def __init__(self, *args, **kwargs):
		QListWidget.__init__(self, *args, **kwargs)
		
		# set minimum height
		self.setMinimumHeight(100)
		
		# auto scroll per pixel
		self.setAutoScroll(True)
		self.setVerticalScrollMode(self.ScrollPerPixel)
		
		# set size policy
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		
		# connect own signal with own slot for scrolling
		self.itemAdded.connect(self.scrollToBottom)
		
		# create popup menu
		self.__p_popup = QMenu(self)
		
		# ... add actions
		self.__p_popup.addAction('clear all', self.clear)
		self.__p_copyAction = self.__p_popup.addAction('copy line', self.__onConsoleCopy)
		self.__p_popup.addAction('insert empty line', self.__onConsoleEmpty)
		self.__p_popup.addAction('jump to top', self.scrollToTop)
		self.__p_popup.addAction('jump to bottom', self.scrollToBottom)
		
		self.__p_popup.addSeparator()
		
		self.__p_popup.addAction('Move to Bottom Area.', self.parent().parent().onMoveLoggerToBottom)
	# end __init__
	
	## @brief Qt slot to copy current list widget line.
	# @param self The object pointer.
	@pyqtSlot()
	def __onConsoleCopy(self):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(self.currentItem().text(), mode = cb.Clipboard)
	# end __onConsoleCopy
	
	## @brief Qt slot to add empty line into list widget.
	# @param self The object pointer.
	@pyqtSlot()
	def __onConsoleEmpty(self):
		self.addItem('')
	# end __onConsoleEmpty
	
	## @brief Qt slot to move parent dock widget to bottom dock widget area.
	# @param self The object pointer.
	#@pyqtSlot()
	#def __onMoveToBottom(self):
	#	dockWidget = self.parent()
	#	mainWindow = dockWidget.parent()
	#	
	#	print(dockWidget)
	#	print(mainWindow)
	#	
	#	mainWindow.removeDockWidget(dockWidget)
	#	mainWindow.addDockWidget(Qt.BottomDockWidgetArea, dockWidget)
	# end __onMoveToBottom
	
	## @brief qt context menu event
	# @param self The object pointer.
	# @param event qt event
	def contextMenuEvent(self, event):
		# enable or disable sections
		if (self.count() == 0):
			self.__p_copyAction.setEnabled(False)
		# end if

		# open popup menu
		self.__p_popup.popup(QCursor.pos())
		
		return QListWidget.contextMenuEvent(self, event)
	# end contextMenuEvent
	
# end class qTloggerListWidget
