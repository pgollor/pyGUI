from PyQt4.QtGui import QLineEdit, QIntValidator, QValidator,\
	QDoubleValidator, QComboBox, QMessageBox

from PyQt4.QtCore import Qt, SIGNAL, QLocale

QLocale.setDefault(QLocale(QLocale.English,QLocale.UnitedStates))

class abstractCustomLineEdit(QLineEdit):
	INTEGER = 0
	FLOAT = 1
	LIST = 2
	
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
			self.emit(SIGNAL('validChange(PyQt_PyObject, PyQt_PyObject)'), self.getClassName(), value)
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
				print(msg)
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
	def __init__(self, *args, **kwargs):
		abstractCustomMinMaxLineEdit.__init__(self, *args, **kwargs)
		
		self._setType(self.INTEGER)
		
		self.setValidator(QIntValidator())
	# end __init__
	
	def __check(self, value='', quiet=False):
		if (value == ''):
			value = self.text()
		# end if
		
		if (self.validator().validate(str(value), 0)[0] != QValidator.Acceptable):
			msg = 'Input has to be an integer'

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
			msg = 'Input has to be a float'

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

