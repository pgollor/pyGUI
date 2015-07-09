


##
# @file customGuiElements.py
# 
# @date unknown
# @author Stanislav Tereschenko
# @author Pascal Gollor (http://www.pgollor.de/cms/)
# 
# @copyright Dieses Projekt ist lizensiert als Inhalt der
# Creative Commons Namensnennung - Weitergabe unter gleichen Bedingungen 3.0 Unported-Lizenz.<br>
# Um eine Kopie der Lizenz zu sehen, besuchen Sie http://creativecommons.org/licenses/by-sa/3.0/.<br>
# -- englisch version --<br>
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#
# @defgroup custom_gui_elements custom Qt GUI elements
# @{
#
# @brief custom Qt GUI elements
#
# This classes are all children's from Qt Elements like lineEdit, comboBox, slider or so and provides some
# better and user friendlier functions. 
# 



from PyQt4.QtGui import QLineEdit, QIntValidator, QValidator,\
	QDoubleValidator, QComboBox, QMessageBox, QSlider, QLabel
from PyQt4.QtCore import Qt, QLocale, pyqtSlot
from PyQt4.Qt import pyqtSignal
from functools import partial
import numpy as np

QLocale.setDefault(QLocale(QLocale.English,QLocale.UnitedStates))


class abstractCustomLineEdit(QLineEdit):
	INTEGER = 0
	FLOAT = 1
	LIST = 2
	
	# signals
	
	def __init__(self, *args, **kwargs):
		QLineEdit.__init__(self, *args, **kwargs)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		self.__v_type = -1
		self.__v_lastValue = str()
	# end __initVars
	
	def _setType(self, t):
		self.__v_type = t
	# end _setType
	
	def getType(self):
		return self.__v_type
	# end getType
	
	def setText(self, value):
		self.__clearMessage()
		self.__v_lastValue = str(value)
		
		return QLineEdit.setText(self, str(value))
	# end setText
		
	def getClassName(self):
		objName = self.objectName()
		name= objName[8:len(objName)]
		return name
	# end getClassName
	
	def _change(self, value):
		if (str(value) != self.__v_lastValue):
			#self.emit(SIGNAL('validChange(PyQt_PyObject, PyQt_PyObject)'), self.getClassName(), value)
			
			#self.__sig_validChange.emit(self.getClassName(), value)
			if (self.__v_type == 0):
				self.validChange[str, int].emit(self.getClassName(), value)
			elif (self.__v_type == 1):
				self.validChange[str, float].emit(self.getClassName(), value)
			else:
				self.validChange[str, str].emit(self.getClassName(), value)
			# end if
			
			self.__clearMessage()
			self.__v_lastValue = str(value)
		# end if
		
	def __clearMessage(self):
		self.setStyleSheet('')
		self.setToolTip('')
	# end __clearMessage
	
	def _noValidInput(self, msg = '', quiet = False):
		#self.setText(self.__v_lastValue)
		QLineEdit.setText(self, str(self.__v_lastValue))
		
		self.setStyleSheet('border: 1px solid red')

		if (msg != ''):
			self.setToolTip(msg)
			
			if (quiet):
				pass
				#print(msg)
			else:
				QMessageBox.critical(None, 'Error', msg)
			# end if
		# end if
		
	# end _noValidInput
	
	def keyPressEvent(self, event):
		key = event.key()
		
		QLineEdit.keyPressEvent(self, event)
		
		if (key == Qt.Key_Enter or key == Qt.Key_Return):
			event.accept()
		else:
			event.ignore()
		# end if
	# end keyPressEvent
	
# end class abstractCustomLineEdit


class customStringLineEdit(abstractCustomLineEdit):
	validChange = pyqtSignal(str, str)
	
	def __init__(self, *args, **kwargs):
		abstractCustomLineEdit.__init__(self, *args, **kwargs)
	# end __init__
	
	def keyPressEvent(self, event):
		abstractCustomLineEdit.keyPressEvent(self, event)
		
		if (event.isAccepted()):
			self._change(self.text())
		# end if
		
		# Ansonsten wird die Eingabe fuer das Eltern Element verwendet... (z.B. Problem bei Lerrtaste)
		event.accept()
	# end keyPressEvent
	
	def setText(self, value):
		self._change(value)
		
		return abstractCustomLineEdit.setText(self, value)
	# end setText
	
	def focusOutEvent(self, event):
		self._change(self.text())
		
		abstractCustomLineEdit.focusOutEvent(self, event)
	# end focusOutEvent
	
# end class customStringLineEdit


class abstractCustomMinMaxLineEdit(abstractCustomLineEdit):
	def __init__(self, *args, **kwargs):
		abstractCustomLineEdit.__init__(self, *args, **kwargs)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		self.__v_minValue = None
		self.__v_maxValue = None
	# end __initvars
	
	def setMinMax(self, minVal, maxVal,decimals = 0):
		self.__v_minValue = minVal
		self.__v_maxValue = maxVal
		
		if decimals == 0:
			self.validator().setRange(minVal, maxVal)
		else:
			self.validator().setRange(minVal, maxVal, decimals)
		# end if
		
		return True
	# end setMinMax
	
	def isMinMax(self):
		if (self.__v_minValue == None or self.__v_maxValue == None):
			return False
		# end if
		
		return True
	# end isMinMax
	
	def min(self):
		return self.__v_minValue
	# end min
	
	def max(self):
		return self.__v_maxValue
	# end max
	
# end class abstractCustomMinMaxLineEdit


class customIntegerLineEdit(abstractCustomMinMaxLineEdit):
	validChange = pyqtSignal(str, int)
	
	def __init__(self, *args, **kwargs):
		abstractCustomMinMaxLineEdit.__init__(self, *args, **kwargs)
		
		self._setType(self.INTEGER)
		
		self.setValidator(QIntValidator())
	# end __init__
	
	def __check(self, value='', quiet = False):
		if (value == ''):
			value = self.text()
		# end if
		
		if (self.validator().validate(str(value), 0)[0] != QValidator.Acceptable):
			msg = "GUI element \"" + self.objectName() + "\" has to be an integer"

			if (self.isMinMax()):
				msg += ' between ' + str(self.min()) + ' and ' + str(self.max())
			# end if
			
			self._noValidInput(msg, quiet)
			
			return False
		# end if
		
		try:
			value = int(value)
		except:
			pass
		# end try
		
		self._change(value)
		
		return True
	# end __check
	
	def setMinMax(self, minVal, maxVal):
		try:
			minVal = int(minVal)
			maxVal = int(maxVal)
		except:
			return False
		# end try
		
		#self.validator().setRange(minVal, maxVal)
		
		return abstractCustomMinMaxLineEdit.setMinMax(self, minVal, maxVal)
	# end setMinMax
	
	def setText(self, value):
		if (not self.__check(value = value, quiet = True)):
			return False 
		# end if

		return abstractCustomMinMaxLineEdit.setText(self, value)
	# end setText
	
	def text(self, *args, **kwargs):
		#return int(customMinMaxLineEdit.text(self, *args, **kwargs))
		
		ret = abstractCustomMinMaxLineEdit.text(self, *args, **kwargs)
		try:
			ret = int(ret)
		except:
			pass
		# end try
		
		return ret
	# end text
	
	def keyPressEvent(self, event):
		abstractCustomMinMaxLineEdit.keyPressEvent(self, event)
		
		if (event.isAccepted()):
			self.__check()
		# end if
		
		# Ansonsten wird die Eingabe fuer das Eltern Element verwendet... (z.B. Problem bei Lerrtaste)
		event.accept()
	# end keyPressEvent
	
	def focusOutEvent(self, event):
		self.__check()
		
		abstractCustomMinMaxLineEdit.focusOutEvent(self, event)
	# end focusOutEvent
	
# end class customIntegerLineEdit

class customFloatLineEdit(abstractCustomMinMaxLineEdit):
	validChange = pyqtSignal(str, float)
	
	def __init__(self, *args, **kwargs):
		abstractCustomMinMaxLineEdit.__init__(self, *args, **kwargs)
		
		self._setType(self.FLOAT)
		validator = QDoubleValidator()
		validator.setNotation(QDoubleValidator.StandardNotation)
		self.setValidator(validator)
	# end __init__
		
	def __check(self, value='', quiet=False):
		if (value == ''):
			value = self.text()
		# end if
		
		if (self.validator().validate(str(value), 0)[0] != QValidator.Acceptable):
			msg = "GUI element \"" + self.objectName() + "\" has to be a float"

			if (self.isMinMax()):
				msg += ' between ' + str(self.min()) + ' and ' + str(self.max())
			# end if
			
			self._noValidInput(msg, quiet)
			
			return False
		# end if
		
		try:
			value = float(value)
		except:
			pass
		# end try
		
		self._change(value)
		
		return True
	# end __check
	
	def setMinMax(self, minVal, maxVal):
		try:
			minVal = float(minVal)
			maxVal = float(maxVal)
		except:
			return False
		# end try
		
		return abstractCustomMinMaxLineEdit.setMinMax(self, minVal, maxVal, decimals=1000)
	# end setMinMax
	
	def setText(self, value):
		if (not self.__check(value = value, quiet = True)):
			return False
		# end if
		
		return abstractCustomMinMaxLineEdit.setText(self, value)
	# end setText
	
	def text(self, *args, **kwargs):
		ret = abstractCustomMinMaxLineEdit.text(self, *args, **kwargs)
		try:
			ret = float(ret)
		except:
			pass
		# end try
		
		return ret
	# end text
	
	def keyPressEvent(self, event):
		abstractCustomMinMaxLineEdit.keyPressEvent(self, event)
		
		if (event.isAccepted()):
			self.__check()
		# end if
		
		# Ansonsten wird die Eingabe fuer das Eltern Element verwendet... (z.B. Problem bei Lerrtaste)
		event.accept()
	# end keyPressEvent
	
	def focusOutEvent(self, event):
		self.__check()
		
		abstractCustomMinMaxLineEdit.focusOutEvent(self, event)
	# end focusOutEvent
	
# end class customFloatLineEdit

class customListLineEdit(abstractCustomLineEdit):
	validChange = pyqtSignal(str, str)
	
	def __init__(self, *args, **kwargs):
		abstractCustomLineEdit.__init__(self, *args, **kwargs)
		
		self._setType(self.LIST)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		self.__l_list = []
	# end __initVars
	
	def __check(self, value = '', quiet = False):
		if (value == ''):
			value = self.text()
		# end if
		
		#print(value)
		#print(self.__l_list)
		value = str(value)

		if (value not in self.__l_list):
			self._noValidInput('input string is not in list', quiet)

			return False
		# end if
		
		self._change(value)
		
		return True
	# end __check
	
	def setList(self, strList):
		if (type(strList) != list):
			self.__l_list = str(strList).split(sep = ',')
		else:
			self.__l_list = strList
		# end if
		
		return True
	# end setList
	
	def setText(self, value):
		if (not self.__check(value = value, quiet = True)):
			return False
		# end if
		
		return abstractCustomLineEdit.setText(self, value)
	# end setText
	
	def keyPressEvent(self, event):
		abstractCustomLineEdit.keyPressEvent(self, event)
		
		if (event.isAccepted()):
			self.__check()
		# end if
		
		# Ansonsten wird die Eingabe fuer das Eltern Element verwendet... (z.B. Problem bei Lerrtaste)
		event.accept()
	# end keyPressEvent
	
	def focusOutEvent(self, event):
		self.__check()
		
		abstractCustomLineEdit.focusOutEvent(self, event)
	# end focusOutEvent
	
# end class customListLineEdit



class abstractCustomComboBox(QComboBox):
	def __init__(self, *args, **kwargs):
		QComboBox.__init__(self, *args, **kwargs)
	# end __init__
	
	def currentText(self, *args, **kwargs):
		return self.convert(QComboBox.currentText(self, *args, **kwargs))
	# end currentText
	
	def itemText(self, *args, **kwargs):
		return self.convert(QComboBox.itemText(self, *args, **kwargs))
	# end itemText
# end class abstractCustomComboBox


class customIntegerComboBox(abstractCustomComboBox):
	def __init__(self, *args, **kwargs):
		abstractCustomComboBox.__init__(self, *args, **kwargs)
	# end __init__
	
	def convert(self, value):
		try:
			value = int(value)
		except:
			pass
		# end try
		
		return value
	# end __convert
	
# end class customIntegerComboBox


class customFloatComboBox(abstractCustomComboBox):
	def __init__(self, *args, **kwargs):
		abstractCustomComboBox.__init__(self, *args, **kwargs)
	# end __init__
	
	def convert(self, value):
		try:
			value = float(value)
		except:
			pass
		# end try
		
		return value
	# end __convert
	
# end class customFloatComboBox


# ---------- slider ----------
# ----------   \/   ----------


## custom abstract slider
# It is a QSlider with some more user friendly functions.
# You can use the abstractSlider not directly. Please use customIntegerSlider, customFloatSlider oder customLogarithmSlider.
class CustomAbstractSlider(QSlider):
	INTEGER = 0
	FLOAT = 1
	LOGARITHM = 2
	
	## value changed signal
	sigChanged = pyqtSignal()
	
	## initial class function
	# @param self The object pointer.
	# @param sliderType Slider type (integer, float or logarithm).
	# @param *args arguments as list
	# @param **kwargs arguments as dict
	def __init__(self, sliderType, *args, **kwargs):
		QSlider.__init__(self, *args, **kwargs)
		
		# set slider type
		self.__v_type = sliderType
		
		self.__l_connectedItems = list()
		self.__v_ndigits = 2
		self.__v_lastVal = 0
		
		self._v_step = 1
		self._v_minVal = 0
		self._v_maxVal = 0
		
		# default no tracking
		self.setTracking(False)
		
		# connect signals
		self.valueChanged.connect(self._onValueChange)
	# end __init__
	
	@pyqtSlot(int)
	def _onValueChange(self, value = -1):
		# get value from child class
		value = self.value()
		
		# do nothing if value do not changed
		if (self.__v_lastVal == value):
			return
		# end if
		self.__v_lastVal = value
		
		# show rounded value to all connectet items
		for item in self.__l_connectedItems:
			item.setText(str(round(value, self.__v_ndigits)))
		# end for
		
		# emit change signal in child class
		self._emitChange()
	# end _onValueChange 
	
	@pyqtSlot(str)
	def __onItemChange(self, lineEdit):
		self.setValue(lineEdit.text())
		
		# show rounded value to all connectet items
		value = self.value()
		for item in self.__l_connectedItems:
			item.setText(str(round(value, self.__v_ndigits)))
		# end for

		#value = float(lineEdit.text())
		#value = self.setEditedValue(value)

		#if (self.__v_lastValue != value):
		#	#self.emit(SIGNAL("changed(PyQt_PyObject)"), value)
		#	if (self.__v_double):
		#		self.changed[float].emit(value)
		#	else:
		#		self.changed[int].emit(value)
		#	# end if
		#	self.__v_lastValue = value
		# end if
	# end __onItemChange
	
	## connect qt elements 
	def __connectItem(self, item):
		# do not connect if is already a connected element
		if (item in self.__l_connectedItems):
			return False
		# end if
		
		self.__l_connectedItems.append(item)
		val = self.value()
		
		# add rounded value
		item.setText(str(round(val, self.__v_ndigits)))
		
		return True
	# end __connectItem
	
	## disconnect qt elements
	def __disconnectItem(self, item):
		if (item not in self.__l_connectedItems):
			return False
		# end if
		
		self.__l_connectedItems.remove(item)
		
		return True
	# end __disconnectItem
	
	
	# ------------------- #
	# protected functions #
	# --------\/--------- #
	
	## emit the change signal
	# @param self The object pointer.
	def _emitChange(self):
		pass
	# end _emitChange
	
	def _checkMinMax(self, value):
		if (value < self._v_minVal):
			value = self._v_minVal
		# end if
		
		if (value > self._v_maxVal):
			value = self._v_maxVal
		# end if
		
		return value
	# end _checkMinMax
	
	# --------/\--------- #
	# protected functions #
	# ------------------- #

	def setRange(self, minVal, maxVal):
		self.setMinimum(minVal)
		self.setMaximum(maxVal)
	# end setRange
	
	def setValue(self, value):
		QSlider.setValue(self, value)
		
		self._onValueChange()
		
		return True
	# end setValue

	def minimum(self):
		return self._v_minVal
	# end minimum
	
	def maximum(self):
		return self._v_maxVal
	# end maximum

	
	# ------------------- #
	# interface functions #
	# --------\/--------- #
	
	
	## Initialize slider
	# @param self The object pointer.
	# @param minVal Minimum value.
	# @param maxVal Maximum value.
	# @param step Step. Default 1.
	# @param pageStep Page step. Default 10.
	def init(self, minVal, maxVal, step = 1, pageStep = 10):
		self.setSingleStep(step)
		self.setPageStep(pageStep)
		self.setRange(minVal, maxVal)
	# end init
	

	## get slider type as int or string
	# @param self The object pointer.
	# @param asString boolean for choosing return format
	# @return slider type
	def getSliderType(self, asString = False):
		if (asString):
			if (self.__v_type == CustomAbstractSlider.INTEGER):
				return "integer"
			elif (self.__v_type == CustomAbstractSlider.FLOAT):
				return "float"
			elif (self.__v_type == CustomAbstractSlider.LOGARITHM):
				return "logarithm"
			# end if
		# end if
		
		return self.__v_type
	# end getSliderType
		
	## connect QLabel with this slider
	# @param self The object pointer.
	# @param label The QLabel object pointer.
	# @return return True or False
	def connectLabel(self, label):
		return self.__connectItem(label)
	# end connectLabel
	
	## connect QLineEdit with this slider
	# @param self The object pointer.
	# @param lineEdit The QLineEdit object pointer.
	# @return True or False
	def connectLineEdit(self, lineEdit):
		if (not self.__connectItem(lineEdit)):
			return False
		# end if
		
		# connect signal for line edit
		lineEdit.returnPressed.connect(partial(self.__onItemChange, lineEdit))
		
		return True
	# end connectLineEdit
	
	## connect a QT Element with this slider
	# @param self The object pointer.
	# @param elem Qt object pointer from QLineEdit oder QLabel
	# @return return True or False
	def connectElem(self, elem):
		if (type(elem) == QLabel):
			self.connectLabel(elem)
		elif (type(elem) == QLineEdit):
			self.connectLineEdit(elem)
		else:
			return False
		# end if
		
		return True
	# end connectElem
	
	## disconnect QLabel
	# @param self The object pointer.
	# @param label The QLabel object pointer.
	# @return return True or False
	def disconnectLabel(self, label):
		return self.__disconnectItem(label)
	# end disconnectLabel
	
	## disconnect QLineEdit
	# @param self The object pointer.
	# @param lineEdit The QLineEdit object pointer.
	# @return True or False
	def disconnectLineEdit(self, lineEdit):
		return self.__disconnectItem(lineEdit)
	# end disconnectLabel
	

	## get list with all connected items
	# @param self The object pointer.
	# @return object pointer list 
	def getConnectedItems(self):
		return self.__l_connectedItems
	# end getConnectedLabels
	
	
# end class AbstractBetterSlider


## custom integer slider
class customIntegerSlider(CustomAbstractSlider):
	sigChanged = pyqtSignal(int)
	
	## initial class function
	# @param self The object pointer.
	# @param *args arguments as list
	# @param **kwargs arguments as dict
	def __init__(self, *args, **kwargs):
		CustomAbstractSlider.__init__(self, CustomAbstractSlider.INTEGER, *args, **kwargs)
	# end __init
	
	def _emitChange(self):
		value = self.value()
		self.sigChanged[int].emit(value)
	# end _emitChange
	
	def setSingleStep(self, singleStep):
		self._v_step = singleStep
		
		return CustomAbstractSlider.setSingleStep(self, 1)
	# end setSingleStep
	
	def setMinimum(self, minVal):
		self._v_minVal = int(minVal)
		
		return CustomAbstractSlider.setMinimum(self, 0)
	# end setMaximum
		
	def setMaximum(self, maxVal):
		self._v_maxVal = int(maxVal)
		
		steps = int(round((self._v_maxVal - self._v_minVal) / self._v_step + 1))
		
		return CustomAbstractSlider.setMaximum(self, steps - 1)
	# end setMaximum
	
	def value(self):
		pos = CustomAbstractSlider.value(self)
		
		customVal = int(self._v_minVal + pos * self._v_step)
		
		return customVal
	# end value
	
	@pyqtSlot(int)
	def setValue(self, value):
		value = self._checkMinMax(int(value))
		
		# calculate slider position
		pos = int(round((int(value) - self._v_minVal) / self._v_step, 0))
		
		CustomAbstractSlider.setValue(self, pos)
		
		return value
	# end setValue
	
# end class


## custom float slider
class customFloatSlider(CustomAbstractSlider):
	sigChanged = pyqtSignal(float)
	
	## initial class function
	# @param self The object pointer.
	# @param *args arguments as list
	# @param **kwargs arguments as dict
	def __init__(self, *args, **kwargs):
		CustomAbstractSlider.__init__(self, CustomAbstractSlider.FLOAT, *args, **kwargs)
	# end __init
	
	def _emitChange(self):
		value = self.value()
		self.sigChanged[float].emit(value)
	# end _emitChange

	# -------------------- #
	# overloaded functions #
	# ---------\/--------- #
	
	def setSingleStep(self, singleStep):
		self._v_step = singleStep
		
		return CustomAbstractSlider.setSingleStep(self, 1)
	# end setSingleStep
	
	def setMinimum(self, minVal):
		self._v_minVal = float(minVal)
		
		return CustomAbstractSlider.setMinimum(self, 0)
	# end setMaximum
		
	def setMaximum(self, maxVal):
		self._v_maxVal = float(maxVal)
		
		steps = int(round((self._v_maxVal - self._v_minVal) / self._v_step + 1))
		
		return CustomAbstractSlider.setMaximum(self, steps - 1)
	# end setMaximum
	
	## returns custom value and overload original function
	# @param self The object pointer.
	def value(self):
		pos = CustomAbstractSlider.value(self)
		
		customVal = self._v_minVal + np.double(pos) * self._v_step
		
		return customVal
	# end value
	
	@pyqtSlot(float)
	def setValue(self, value):
		# check range
		value = self._checkMinMax(float(value))
		
		# calculate slider position
		pos = round((np.double(value) - self._v_minVal) / self._v_step, 0)
		
		# set sldier position
		CustomAbstractSlider.setValue(self, pos)
		
		return value
	# end setValue

	
	# ---------/\--------- #
	# overloaded functions #
	# -------------------- #

# end class customFloatSlider


## custom logarithm slider 
class customLogarithmSlider(CustomAbstractSlider):
	sigChanged = pyqtSignal(float)
	
	## initial class function
	# @param self The object pointer.
	# @param *args arguments as list
	# @param **kwargs arguments as dict
	def __init__(self, *args, **kwargs):
		CustomAbstractSlider.__init__(self, CustomAbstractSlider.LOGARITHM, *args, **kwargs)
	# end __init
	
	def _emitChange(self):
		value = self.value()
		self.sigChanged[float].emit(value)
	# end _emitChange

	# -------------------- #
	# overloaded functions #
	# ---------\/--------- #
	
	def setSingleStep(self, singleStep):
		return
		#self._v_step = singleStep
		#return CustomAbstractSlider.setSingleStep(self, 1)
	# end setSingleStep
	
	def setMinimum(self, minVal):
		self._v_minVal = minVal
		
		if (self._v_maxVal == 0):
			return CustomAbstractSlider.setMinimum(self, minVal)
		# end if
		
		minVal = np.log10(int(minVal)) * 1000
		maxVal = np.log10(int(self._v_maxVal)) * 1000
		
		# set step size
		step = np.round((maxVal - minVal) / 1000, 0)
		CustomAbstractSlider.setSingleStep(self, np.int32(step))
	
		return CustomAbstractSlider.setMinimum(self, minVal)
	# end setMaximum
		
	def setMaximum(self, maxVal):
		self._v_maxVal = maxVal
		
		if (self._v_minVal == 0):
			return CustomAbstractSlider.setMinimum(self, maxVal)
		# end if
		
		minVal = np.log10(int(self._v_minVal)) * 1000
		maxVal = np.log10(int(maxVal)) * 1000
		
		# set step size
		step = np.round((maxVal - minVal) / 1000, 0)
		CustomAbstractSlider.setSingleStep(self, np.int32(step))
		
		return CustomAbstractSlider.setMaximum(self, maxVal)
	# end setMaximum
	
	## returns custom value and overload original function
	# @param self The object pointer.
	def value(self):
		pos = CustomAbstractSlider.value(self)
		
		customVal = np.power(10, np.double(pos) / 1000)
		customVal = np.int32(np.round(customVal, 0))
		
		return customVal
	# end value
	
	@pyqtSlot(int)
	def setValue(self, value):
		# check range
		value = self._checkMinMax(int(value))
		
		# calculate slider position
		pos = np.int32(round(np.log10(value) * 1000, 0))
		
		# set slider position
		CustomAbstractSlider.setValue(self, pos)
		
		return value
	# end setValue
	
# end class customLogarithmSlider



## alias class for customFloatSlider
class customDoubleSlider(customFloatSlider):
	
	## initial class function
	# @param self The object pointer.
	# @param *args arguments as list
	# @param **kwargs arguments as dict
	def __init__(self, *args, **kwargs):
		customFloatSlider.__init__(self, *args, **kwargs)
	# end __init

# end class customDuableSlider


# @}
