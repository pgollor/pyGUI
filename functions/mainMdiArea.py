##
# @file mainMdiArea.py
# 
# @date 10.04.2015
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
# @brief handle mdiAreaMain


from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMdiArea, QMenu, QCursor, QWidget



class mainMdiArea(QMdiArea):
	dropModule = pyqtSignal(str)
	dockOut = pyqtSignal(QWidget)
	
	def __init__(self, *args, **kwargs):
		QMdiArea.__init__(self, *args, **kwargs)
		
		self.setMinimumSize(780, 510)
		
		self.setAcceptDrops(True)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
	# end __init__
	
	def contextMenuEvent(self, event):
		if (self.currentSubWindow() and not self.currentSubWindow().isMaximized()):
			popup = QMenu(self)
			popup.addAction('show side by side', self.__onShowSideBySide)
			popup.addAction('cascade', self.__onShowCascade)
			popup.addSeparator()
			popup.addAction('dock out current module', self.__onDockOut)
			popup.addSeparator()
			popup.addAction('close all', self.closeAllSubWindows)
		
			popup.popup(QCursor().pos())
		# end if
		
		return QMdiArea.contextMenuEvent(self, event)
	# end contextMenuEvent
	
	@pyqtSlot()
	def __onDockOut(self):
		win = self.activeSubWindow()
		if (not win):
			return
		# end if
		
		self.dockOut.emit(win)
	# end __onDockOut
	
	@pyqtSlot()
	def __onShowSideBySide(self):
		self.tileSubWindows()
	# end __onShowSideBySide
	
	@pyqtSlot()
	def __onShowCascade(self):
		self.cascadeSubWindows()
	# end __onShowCascade
	
	def visibleSubWindowList(self):
		l = self.subWindowList().copy()
		for subWindow in l:
			if not subWindow.isVisible():
				l.remove(subWindow)
			# end if
		# end for
		
		return l
	# end visibleSubWindowList
	
	"""
	## dragEnterEvent
	# @param event: QEvent
	# Das event muss akzeptiert werden, damit ein drop erfolgen kann.
	def dragEnterEvent(self, event):
		event.accept()
		
		return QMdiArea.dragEnterEvent(self, event)
	# end dragEnterEvent
	
	def dropEvent(self, event):
		mimeData = event.mimeData()
		
		if (mimeData.hasFormat('text/plain')):
			# drop bestaetigen
			event.setDropAction(Qt.CopyAction)
		
			# event akzeptieren
			event.accept()
		
			self.dropModule.emit(mimeData.text())
		else:
			event.ignore()
		# end f
		
		return QMdiArea.dropEvent(self, event)
	# end dropEvent
	"""
	
# end class mainMdiArea

