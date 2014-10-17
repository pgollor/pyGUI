##
# @file betterSlider.py
# 
# @date unknown
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


from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QSlider
import numpy as np
from functools import partial


class betterSlider(QSlider):
	__v_log = False
	__v_double = False
	__v_integer = False
	__l_connectedItems = []
	__v_minValue = -1
	__v_maxValue = -1
	__v_doubleStep = 0.1
	__v_factor = 1000
	__v_ndigits = 0
	__v_lastValue = -1
	
	
	def __init__(self, *args):
		QSlider.__init__(self, *args)
		
		self.__l_connectedItems = []
		self.__v_log = False
		
		# connect signals
		self.connect(self, SIGNAL("actionTriggered(int)"), self.__onActionTriggered)
		self.connect(self, SIGNAL("sliderReleased()"), self.__onSliderReleased)
		self.connect(self, SIGNAL("valueChanged(int)"), self.__onValueChanged)
	# end __init__
	
	def __del__(self):
		self.__l_connectedItems = []
		self.__v_log = False
	# end __del__
	
	def __onValueChanged(self, value):
		"""
		Signal ueberlagern, damit ddie berechnete Position gesendet wird
		"""
		
		self.emit(SIGNAL("valueChanged(PyQt_PyObject)"), self.editedValue(value))
	# end __onValueChanged
	
	def __onActionTriggered(self, action):
		"""
		1: ein Schritt nach rechts
		2: ein Schritt nach links
		3: mehrere Schritte nach rechts
		4: mehrere Schritte nach links
		7: mit der Maus gezogen
		"""

		if (action >= 1 and action <= 4):
			self.__emitChange()
		# end if
	# end __onActionTriggered
	
	def __onSliderReleased(self):
		self.__emitChange()
	# end __onSliderReleased
	
	def __onItemChange(self, lineEdit):
		value = float(lineEdit.text())
		value = self.setEditedValue(value)

		if (self.__v_lastValue != value):
			self.emit(SIGNAL("changed(PyQt_PyObject)"), value)
			self.__v_lastValue = value
		# end if
	# end __onItemChange
	
	def __emitChange(self):
		value = self.editedValue()

		# set text into connectet items
		if (len(self.__l_connectedItems) > 0):
			for label in self.__l_connectedItems:
				label.setText(str(round(value, self.__v_ndigits)))
			# end for
		# end if

		if (self.__v_lastValue != value):
			self.emit(SIGNAL("changed(PyQt_PyObject)"), value)
			self.__v_lastValue = value
		# end if
	# end __emitchange
	
	def __connectItem(self, item):
		if (item in self.__l_connectedItems):
			return
		# end if
		
		self.__l_connectedItems.append(item)
		val = self.editedValue()
		#item.setText(str(round(val,self.__v_ndigits)))
		item.setText(str(round(val,self.__v_ndigits)))
	# end __connectItem
	
	def __disconnectItem(self, item):
		if (item in self.__l_connectedItems):
			self.__l_connectedItems.remove(item)
		# end if
	# end __disconnectItem

	# -------------- #
	# init functions #
	# ------\/------ #

	def initDouble(self, minval, maxval, step):
		self.__v_log= False
		self.__v_double = True
		self.__v_integer = False
		self.__v_minValue = minval
		self.__v_maxValue = maxval
		self.__v_stepSize = step

		steps = int(round((maxval - minval) / step + 1))
		self.__v_ndigits = len(str(steps))
		
		self.setMinimum(0)
		self.setMaximum(steps-1)
			
		self.setSingleStep(1)
		self.setPageStep(10)
	# end initDouble
	
	def initInteger(self, minval, maxval, step):
		self.__v_log= False
		self.__v_double = False
		self.__v_integer = True
		self.__v_minValue = minval
		self.__v_maxValue = maxval
		self.__v_stepSize = step

		steps = int(round((maxval - minval) / step + 1))
		
		self.setMinimum(0)
		self.setMaximum(steps - 1)
			
		self.setSingleStep(1)
		self.setPageStep(10)
	# end initInteger
	
	def reInitInteger(self, minval = -1, maxval = -1, step = -1):
		if (minval == -1):
			minval = self.__v_minValue
		# end if
		
		if (maxval == -1):
			maxval = self.__v_maxValue
		# end if
		
		if (step == -1):
			step = self.__v_stepSize
		# end if
		
		self.initInteger(minval, maxval, step)
	# end reInitInteger
	
	def setLogarithm(self, b, minval = -1, maxval = -1):
		self.initLogarithm(minval, maxval)
	# end if
	
	def initLogarithm(self, minval = -1, maxval = -1):
		self.__v_log= True
		self.__v_double = False
		self.__v_integer = False
		self.__v_minValue = minval
		self.__v_maxValue = maxval

		if (minval > -1 and maxval > -1):
			minval = np.log10(minval) * 1000
			maxval = np.log10(maxval) * 1000
			step = np.round((maxval - minval) / 1000, 0)
			step = np.int32(step)

			self.setMinimum(minval)
			self.setMaximum(maxval)
			self.setSingleStep(step)
			self.setPageStep(step * 10)
		# end if

		return True
	# end initLogarithm

	# ------/\------ #
	# init functions #
	# -------------- #

	def __checkMinMax(self, value):
		if (value < self.__v_minValue):
			value = self.__v_minValue
		# end if
		if (value > self.__v_maxValue):
			value = self.__v_maxValue
		# end if
	
		return value
	# end __checkMinMax
	
	def setEditedValue(self, val, emitSignal = False):
		if (self.__v_log and val <= 0):
			return
		# end if
		
		newVal = val

		if (self.__v_double):
			val = self.__checkMinMax(val)
			
			newVal = round((np.double(val) - self.__v_minValue) / self.__v_stepSize, 0)
		elif (self.__v_integer):
			val = self.__checkMinMax(val)
			
			newVal = int(round((int(val) - self.__v_minValue) / self.__v_stepSize, 0))
		elif (self.__v_log):
			val = self.__checkMinMax(val)
			
			newVal = np.int32(round(np.log10(val) * 1000, 0))
		# end if
			
		if (len(self.__l_connectedItems) > 0):
			for label in self.__l_connectedItems:
				if (self.__v_integer):
					label.setText(str(int(round(val, self.__v_ndigits))))
				else:
					label.setText(str(round(val, self.__v_ndigits)))
				# end if
			# end for
		# end if

		self.setValue(newVal)
		
		if (emitSignal):
			self.__emitChange()
		# end if
		
		return val
	# end setEditedValue

	def editedValue(self, val = -1):
		if (val == -1):
			val = self.sliderPosition()
		# end if
		
		if (self.__v_double):
			val = self.__v_minValue + np.double(val) * self.__v_stepSize
			val = self.__checkMinMax(val)
		elif (self.__v_integer):
			val = int(self.__v_minValue + val * self.__v_stepSize)
			val = self.__checkMinMax(val)
		elif (self.__v_log):
			val = np.power(10, np.double(val) / 1000)
			val = np.round(val, 0)
			val = np.int32(val)
			val = self.__checkMinMax(val)
		# end if
		
		return val
	# end value


	# ------------------- #
	# interface functions #
	# --------\/--------- #
	
	def connectLabel(self, label):
		self.__connectItem(label)
	# end connectLabel
	
	def connectLineEdit(self, lineEdit):
		self.__connectItem(lineEdit)
		self.connect(lineEdit, SIGNAL("returnPressed()"), partial(self.__onItemChange, lineEdit))
	# end connectLineEdit
	
	def disconnectLabel(self, label):
		self.__disconnectItem(label)
	# end disconnectLabel
	
	def disconnectLineEdit(self, lineEdit):
		self.__disconnectItem(lineEdit)
	# end disconnectLabel
	
	def getConnectedLabels(self):
		return self.getConnectedItems()
	# end getConnectedLabels
	
	def getConnectedItems(self):
		return self.__l_connectedItems
	# end getConnectedLabels
	
	def logarithm(self):
		return self.__v_log
	# end logarithm
	
	# --------/\--------- #
	# interface functions #
	# ------------------- #
	
# end class betterSlider