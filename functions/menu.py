##
# @file menu.py
# 
# @date 26.07.2014
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
# @brief menu buttons for main window tool bar


from PyQt4.QtGui import QToolButton, QIcon, QToolBar
from PyQt4.QtCore import Qt, QSize, pyqtSignal, QObject


class menuButton(QToolButton):	
	def __init__(self, *args, **kwargs):
		QToolButton.__init__(self, *args, **kwargs)

		# set maximum and mimium size
		self.setMaximumSize(100, 60) # width, height
		self.setMinimumSize(80, 60) # width, height
		
		# make menu button auto exclusive like QRadioButton
		self.setAutoExclusive(True)
		
		# make button checkable. this is required for css functions like checked ...
		self.setCheckable(True)
	# end __init__

	def setText(self, text):
		text = str(text)
		
		met = self.fontMetrics()
		maxWidth = self.maximumWidth() - 20 # max width minus border
		
		self.setToolTip(text)
		
		if (met.width(text) > maxWidth):
			postStr = '...'

			while (met.width(text + postStr) > maxWidth):
				text = text[0:len(text) - 1]
			# end while
			
			text += postStr
		# end if

		return QToolButton.setText(self, text)
	# end setText

# end class Menubutton


class applicationMenuButton(menuButton):
	clicked = pyqtSignal(QObject)
	doubleClicked = pyqtSignal(QObject)
	
	def __init__(self, module, *args, **kwargs):
		menuButton.__init__(self, *args, **kwargs)
		
		# set global variables
		self.__p_module = module
		
		# init menu button style
		# add standard icon
		self.setIcon(QIcon(module.getParentPath() + '/icons/computer200.svg'))
		self.setIconSize(QSize(32,32))
		
		# display text under the icon
		self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		
		## connect signal clicked from parent class
		super(menuButton, self).clicked.connect(self.__onClick)
		
		self.setAutoExclusive(False)
	# end __init__

	def __del__(self):
		if (self.__p_module):
			self.__p_module = False
		# end if
	# end __del__
	
	def __onClick(self):
		self.clicked[QObject].emit(self.__p_module)
	# end __onClick
	
	def mouseDoubleClickEvent(self, event):
		self.doubleClicked[QObject].emit(self.__p_module)
		
		return menuButton.mouseDoubleClickEvent(self, event)
	# end mouseDoubleClickEvent
	
# end class applicationMenuButton


class menuToolBar(QToolBar):
	def __init__(self, *args, **kwargs):
		QToolBar.__init__(self, *args, **kwargs)
		
		self.setMinimumHeight(64)
	# end __init__
	
# end class menuToolBar
