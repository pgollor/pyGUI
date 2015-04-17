##
# @file settingsHelper.py
# 
# @date 28.06.2013
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
# @brief Helper function to handle Qt GUI settings

from PyQt4.QtGui import QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox


def getFieldValues(parent=False):
	if not parent:
		return False
	# end if

	widgets = parent.findChildren((QLineEdit,QCheckBox,QComboBox,QRadioButton,QGroupBox))
	fieldValues = {}

	for widget in widgets:
		name = widget.objectName()
		if type(widget) == QLineEdit:
			name = name[8::]
			value = widget.text()
		elif type(widget) == QCheckBox:
			name = name[8::]
			value = widget.isChecked()
		elif type(widget) == QComboBox:
			name = name[8::]
			value = widget.currentText()
		elif type(widget) == QGroupBox:
			if widget.isCheckable():
				name = name[8::]
				value = widget.isChecked()
			else:
				continue
			# end if
		elif type(widget) == QRadioButton:
			name = name[11::]
			value = widget.isChecked()
		# end if
		
		#print(name,":",value, type(value))
		fieldValues[name] = value
	# end for

	return fieldValues
# end getFieldValues
	
def setValues(settingsHandle,values):
	for name, value in values.items():
		setValue(settingsHandle, name, value)
	# end for
# end setValues

def getValues(settingsHandle):
	values = dict()
	for key, value in settingsHandle.items():
		values[key] = getValue(settingsHandle,key)
	#end for

	return values
#end getValues

def setValue(settingsHandle,name,value):
	if name in settingsHandle:
		if value == "":
			#self._p_logger.warn("Parameter \"" + name + "\" has empty value")
			print("Parameter \"" + name + "\" has empty value")
			return
		# end if

		Type = settingsHandle[name]["Type"]
		if Type == "float":
			val = float(value)

			if val > settingsHandle[name]["maxValue"]:
				val = settingsHandle[name]["maxValue"]
			# end if
			if val < settingsHandle[name]["minValue"]:
				val = settingsHandle[name]["minValue"]
			#end if

			settingsHandle[name]["value"] = val
		elif Type == "int":
			val = int(value)

			if val > settingsHandle[name]["maxValue"]:
				val = settingsHandle[name]["maxValue"]
			# end if
			if val < settingsHandle[name]["minValue"]:
				val = settingsHandle[name]["minValue"]
			#end if

			settingsHandle[name]["value"] = val
		elif Type == "string":
			settingsHandle[name]["value"] = value
		elif Type == "bool":
			settingsHandle[name]["value"] = bool(value)
		else:
			#self._p_logger.warn("Type \"" + Type + "\" is not supported")
			print("Type \"" + Type + "\" is not supported")
	else:
		#self._p_logger.warn("Parameter \"" + name + "\" is not available")
		print("Parameter \"" + name + "\" is not available")
	# end if
# end setValue

def getValue(settingsHandle,name):
	if name in settingsHandle:
		return settingsHandle[name]["value"]
	# end if
# end getValue

