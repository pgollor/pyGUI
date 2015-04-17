##
# @file customDialogs.py
# 
# @date 17.03.2014
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


from PyQt4.QtCore import SIGNAL, QRect, Qt, QPoint
from PyQt4.QtGui import QDialog, QDesktopWidget, QWidget, QMainWindow, QVBoxLayout,\
	QCheckBox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


class QWidgetSignals(QWidget):
	
	#onClose = pyqtSignal(name="onClose")
	#onShow = pyqtSignal(name="onShow")
	
	def __init__(self, parent = False):
		QWidget.__init__(self, parent)
		
		# get primary monitor resolution
		qdw = QDesktopWidget()
		mainScreenSize = qdw.availableGeometry(qdw.primaryScreen())
		
		# get center of the monitor
		center = mainScreenSize.center()
		
		# calculate width, height and x,y positions of the window
		r_width = round(mainScreenSize.width() / 2)
		r_height = round(mainScreenSize.height() / 2)
		r_x = round(center.x() - r_width / 2)
		r_y = round(center.y() - r_height / 2)
		
		# set default geometry of the window
		rect = QRect()
		rect.setX(r_x)
		rect.setY(r_y)
		rect.setWidth(r_width)
		rect.setHeight(r_height)
		self.setGeometry(rect)
	# end __init__
	
	def closeEvent(self, event):
		self._onCloseEvent()
		
		QWidget.closeEvent(self, event)
	# end closeEvent
	
	def showEvent(self, event):
		self._onShowEvent()

		QWidget.showEvent(self, event)
	# end showEvent
	
	def _onCloseEvent(self):
		# emit signal
		self.emit(SIGNAL("onClose()"))
		#self.onClose.emit()
	# end _oncliseEvent
	
	def _onShowEvent(self):
		# emit signal	
		self.emit(SIGNAL("onShow()"))
		#self.onShow.emit()
	# end _onShowEvent
		
# end class QWidgetSignals

class externQWidget(QWidget):
	def __init__(self, parent):
		QWidget.__init__(self, parent)
		
		self.checkBoxExtern = QCheckBox('undock', self)
		self.checkBoxExtern.setGeometry(5, 5, 70, 20)
		self.checkBoxExtern.setChecked(False)

		self.checkBoxExtern.toggled[bool].connect(self.onExtern)
		
		self.__v_pos = QPoint(100, 100)
	# end __init__
	
	def closeEvent(self, event):
		event.ignore()

		self.checkBoxExtern.setChecked(False)
		#self.__onExtern(False)

		#QWidget.closeEvent(self, event)
	# end closeEvent
	
	def onExtern(self, b):
		if (b):
			self.setWindowFlags(Qt.Dialog)
			self.move(self.__v_pos)
		else:
			self.__v_pos = self.pos()
			self.setWindowFlags(Qt.Widget)
			self.move(0, 0)
		# end if

		self.show()
	# end onExtern
	
# end class externQWidget


class QMainWindowSignals(QMainWindow, QWidgetSignals):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		super(QWidgetSignals, self).__init__(self)
	# end __init__
	
	def closeEvent(self, event):
		self._onCloseEvent()
		
		QMainWindow.closeEvent(self, event)
	# end closeEvent
		
	def showEvent(self, event):
		self._onShowEvent()
		
		QMainWindow.showEvent(self, event)
	# end showEvent
	
# end class QMainWindowSignals


class QDialogSignals(QDialog):
	
	def __init__(self, parent = None):
		QDialog.__init__(self, parent)

		# get primiry monitor resolution
		qdw = QDesktopWidget()

		mainScreenSize = qdw.availableGeometry(qdw.primaryScreen())
		# get center of the monitor
		center = mainScreenSize.center()
		# calculate width, height and x,y positions of the window
		r_width = round(mainScreenSize.width()/2)
		r_height = round(mainScreenSize.height()/2)
		r_x = round(center.x()-r_width/2)
		r_y = round(center.y()-r_height/2)
		
		# set default geometry of the window
		rect = QRect()
		rect.setX(r_x)
		rect.setY(r_y)
		rect.setWidth(r_width)
		rect.setHeight(r_height)
		self.setGeometry(rect)
	# end __init__
	
	def showEvent(self, event):
		# emit signal	
		self.emit(SIGNAL("onShow()"))
		
		# accept event	
		event.accept()
	# end showEvent
	
	def closeEvent(self, event):
		# emit signal
		self.emit(SIGNAL("onClose()"))
		
		# accept event
		event.accept()
	# end closeEvent

# end class QDialogSignals


class QDialogPlot(QDialogSignals):
	def __init__(self, parent=None):
		QDialogSignals.__init__(self, parent)
		#this adds minimize and maximize buttons
		self.setWindowFlags(Qt.Window)
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		
		layout = QVBoxLayout()
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		self.setLayout(layout)
	# end __init__
	
	def primitivePlot(self, x,y=[]):
		if (not self.isVisible()):
			self.show()
		# end if
		
		# clear figure
		self.figure.clear()
		
		# create figure and get axis from plot
		ax = self.figure.add_subplot(111)
		
		# don't hold - plot new data
		ax.hold(False)
		
		# plot data
		if (y == []):
			ax.plot(x)
		else:
			ax.plot(x, y)
		self.canvas.draw()
	# end primitivePlot
		
# end class QDialogPlot