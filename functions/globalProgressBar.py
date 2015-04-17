##
# @file globalProgressBar.py
# 
# @date unknown
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

from PyQt4.QtGui import QProgressBar


class globalProgressBar(QProgressBar):
	def __init__(self, parent = False):
		QProgressBar.__init__(self, parent)
		
		self.__p_label = False
	# end __init__
	
	def setLabel(self, label):
		self.__p_label = label
	# end setLabel
	
	def init(self, module = False, value = 0, printModuleName = False, waitOnly = False):
		if (waitOnly):
			self.setMinimum(0)
			self.setMaximum(0)
			self.setTextVisible(False)
		else:
			self.setMinimum(0)
			self.setMaximum(100)
			self.setTextVisible(True)
			self.setValue(value)
		# end if
		
		self.setVisible(True)
		self.setEnabled(True)
		
		if (printModuleName):
			self.__p_label.setText(module.getDisplayName())
		else:
			self.__p_label.setText("")
		# end if
	# end use
	
	def clear(self, delText = True):
		self.setValue(0)
		if (delText):
			self.__p_label.setText("")
		# end if
	# end clear
	
	def setText(self, text):
		self.__p_label.setText(str(text))
	# end setText
	
	def setValue(self, val):
		# change value only if progressbar is enabled
		if (self.isEnabled()):
			QProgressBar.setValue(self, val)
	# end setValue
	
	def disable(self):
		self.clear()
		self.setEnabled(False)
		self.setVisible(False)
	# end disable
	
# end class globalProgressBar	