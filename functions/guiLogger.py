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
from PyQt4.QtCore import Qt, pyqtSlot, QSize, QEvent, pyqtSignal
from PyQt4.QtGui import QListWidgetItem, QBrush, QListWidget, QMenu, QApplication,\
	QCursor, QDockWidget


class QtLogger(logging.Handler):
	printObj = False
	
	def __init__(self, *args, **kwargs):
		logging.Handler.__init__(self, *args, **kwargs)
	# end __init__
	
	def emit(self, record):
		s = self.format(record)
		
		# add filename and line number to outptu on debug
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

class QtLoggerDockWidget(QDockWidget):
	def __init__(self, *args, **kwargs):
		QDockWidget.__init__(self, *args, **kwargs)
		
		self.dockLocationChanged[Qt.DockWidgetArea].connect(self.__onDockWidgetLoggerLocationChanged)
		
		self.setWindowTitle('Logging Window')
		self.setMinimumHeight(100)
	# end __init
	
	def changeEvent(self, event):
		# Ansosnten wird die Minimalgroesse des Dockwidgets um 20 pixel erhoeht wenn das Widget oben oder utnen angeordnet ist.
		if (event.type() == QEvent.LocaleChange):
			self.setFeatures(self.features() | QDockWidget.DockWidgetVerticalTitleBar)
			self.setMinimumHeight(100)
		# end if

		return QDockWidget.changeEvent(self, event)
	# end changeEvent
	
	@pyqtSlot(Qt.DockWidgetArea)
	def __onDockWidgetLoggerLocationChanged(self, area):
		if (area == Qt.BottomDockWidgetArea or area == Qt.TopDockWidgetArea):
			self.setFeatures(self.features() | QDockWidget.DockWidgetVerticalTitleBar)
		else:
			self.setFeatures(self.features() & ~QDockWidget.DockWidgetVerticalTitleBar)
		# end if
	# end
	
# end class QtLoggerDockWidget


class QtLoggerListWidget(QListWidget):
	itemAdded = pyqtSignal()
	
	def __init__(self, *args, **kwargs):
		QListWidget.__init__(self, *args, **kwargs)
		
		self.setVerticalScrollMode(self.ScrollPerPixel)
		
		self.setMinimumHeight(100)
		self.setAutoScroll(True)
		
		# connect own signal with own slot for scrolling
		self.itemAdded.connect(self.scrollToBottom)
	# end __init__
	
	def sizeHint(self):
		return QSize(100, 100)
	# end sizeHint
	
	@pyqtSlot()
	def __onConsoleClearAll(self):
		self.clear()
	# end __onConsoleClearAll
	
	@pyqtSlot()
	def __onConsoleCopy(self):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard )
		cb.setText(self.currentItem().text(), mode = cb.Clipboard)
	# end __onConsoleCopy
	
	@pyqtSlot()
	def __onConsoleEmpty(self):
		self.addItem('')
	# end __onConsoleEmpty
	
	def contextMenuEvent(self, event):
		# create poup menu
		popup = QMenu(self)

		# ad actions
		popup.addAction('clear all', self.__onConsoleClearAll)
		copyAction = popup.addAction('copy line', self.__onConsoleCopy)
		popup.addAction('insert empty line', self.__onConsoleEmpty)
		popup.addAction('jump to top', self.scrollToTop)
		popup.addAction('jump to bottom', self.scrollToBottom)

		if (self.count() == 0):
			copyAction.setEnabled(False)
		# end if

		popup.popup(QCursor.pos())
		
		return QListWidget.contextMenuEvent(self, event)
	# end contextMenuEvent
	
# end class qTloggerListWidget