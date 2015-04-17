##
# @file xmlHelper.py
# 
# @date 28.07.2013
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

from PyQt4.QtGui import QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox,\
	QSpinBox, QDoubleSpinBox, QSlider, QTextEdit, QPlainTextEdit


supportedQtElements = (QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox, QSpinBox, QDoubleSpinBox, QSlider, QTextEdit, QPlainTextEdit)
supportedClassNames = ['label', 'lineedit', 'textedit', 'checkbox', 'radiobutton', 'groupbox', 'combobox', 'spinbox', 'betterslider']
supportedTextElements = ['label', 'lineedit']
supportedCheckedElements = ['checkbox', 'radiobutton', 'groupbox']


def setGuiSettings(xmlList, parentElement):
	global supportedQtElements, supportedClassNames, supportedTextElements, supportedCheckedElements
	
	retList = {
						supportedClassNames[0] : list(),
						supportedClassNames[1] : list(),
						supportedClassNames[2] : list(),
						supportedClassNames[3] : list(),
						supportedClassNames[4] : list(),
						supportedClassNames[5] : list(),
						supportedClassNames[6] : list(),
						supportedClassNames[7] : list(),
						supportedClassNames[8] : list()
						}
	
	for elemClassName in xmlList:
		if (elemClassName in retList):
			for item in xmlList[elemClassName]['items']:
				elem = parentElement.findChild(supportedQtElements, item['name'])

				if (not elem):
					continue
				# end if
				
				# min and max or list values for line edit		
				if (elemClassName == "lineedit"):
					elemFunctions = dir(elem)
					
					if ('maxVal' in item and 'minVal' in item and 'setMinMax' in elemFunctions):
						elem.setMinMax(item['minVal'], item['maxVal'])
					# end if
					
					if ('list' in item and 'setList' in elemFunctions):
						elem.setList(item['list'])
					# end if
				# end if
				
				# set element values
				if (elemClassName == 'textedit'):
					elem.setPlainText(item['plainText'])
				elif (elemClassName in supportedTextElements):
					elem.setText(item['text'])
				elif (elemClassName in supportedCheckedElements):
					elem.setChecked(str2bool(item['checked']))
				elif (elemClassName == 'combobox'):
					# force using content
					if ('content' in item):
						index = elem.findText(str(item['content']))
					else:
					
						# if index is integer then set index directly
						index = 0
						try:
							index = int(item['index'])
							
							# Wenn der Zahlenwert groesser als die Anzahl der Elemente ist,
							# dann koennte es sein, dass dies ein Wert und kein Index ist.
							if (index >= elem.count()):
								index = elem.findText(str(item['index']))
							# end if
						except:
							# string is given
							index = elem.findText(str(item['index']))
						# end try
					# end if
					
					if (index >= 0 and index < elem.count()):
						elem.setCurrentIndex(index)
					else:
						elem.setCurrentIndex(0)
					# end if
				elif (elemClassName == 'spinbox'):
					if ('type' not in item or item['type'] == 'int'):
						elem.setValue(int(item['value']))
					else:
						elem.setValue(float(item['value']))
					# end if
				#elif (elemClassName == 'betterslider' and isinstance(elem, betterSlider)):
				elif (elemClassName == 'betterslider'):
					# own better slider class
					# supported elements for betterSlider class:
					# type: integer, double, logarithm
					# value: current value
					# minVal: minimum value
					# maxVal: maximum value
					# step: step size for normal change (optional not for logarithm)
					# pageStep: step size for page change (optional not for logarithm)
					# connectedLabels: list for connected labels separated by , (optional)
					# connectedLineEdits: list for connected line edits separated by , (optional)
					
					if ('type' not in item or 'value' not in item or 'maxVal' not in item or 'minVal' not in item):
						continue
					# end if
					
					if ('step' not in item):
						item['step'] = 1
					# end if
					if ('pageStep' not in item):
						item['pageStep'] = 10
					# end if

					# init betterSlider with type and values
					try:
						if (item['type'] == 'integer'):
							elem.initInteger(int(item['minVal']), int(item['maxVal']), int(item['step']))
							elem.setPageStep(int(item['pageStep']))
							elem.setEditedValue(int(item['value']))
						elif (item['type'] == 'double'):
							elem.initDouble(float(item['minVal']), float(item['maxVal']), float(item['step']))
							elem.setPageStep(float(item['pageStep']))
							elem.setEditedValue(float(item['value']))
						elif (item['type'] == 'logarithm'):
							elem.initLogarithm(float(item['minVal']), float(item['maxVal']))
							elem.setEditedValue(float(item['value']))
						else:
							continue
						# end if
					except:
						continue
					# end try
					
					# add conected items
					if ('connectedLabels' in item):
						connectedLabels = item['connectedLabels'].split(',')
						for name in connectedLabels:
							label = parentElement.findChild(QLabel, name.strip())
							if (label):
								elem.connectLabel(label)
							# end if
						# end for
					# end if
					if ('connectedLineEdits' in item):
						connectedLineEdits = item['connectedLineEdits'].split(',')
						for name in connectedLineEdits:
							lineedit = parentElement.findChild(QLineEdit, name.strip())
							if (lineedit):
								elem.connectLineEdit(lineedit)
							# end if
						# end for
					# end if
				else:
					continue
				# end if
				
				retList[elemClassName].append({'name': item['name'], 'handle': elem})
			# end for
		# end if
	# end for
	
	return retList
# end setGuiSettings


def loadGuiChange(xmlList, parentElement):
	global supportedQtElements, supportedClassNames, supportedTextElements, supportedCheckedElements
	
	for elemClassName in xmlList:
		if (elemClassName in supportedClassNames):
			for item in xmlList[elemClassName]['items']:
				elem = parentElement.findChild(supportedQtElements, item['name'])

				if (not elem):
					continue
				# end if
				
				# search for supported element class to get value changes
				if (elemClassName == 'textedit'):
					item['plainText'] = elem.toPlainText()
				elif (elemClassName in supportedTextElements):
					item['text'] = elem.text()
				elif (elemClassName in supportedCheckedElements):
					item['checked'] = str(elem.isChecked())
				elif (elemClassName == 'combobox'):
					# force using content
					if ('index' in item):
						item.pop('index')
					# end if

					item['content'] = elem.currentText()
				elif (elemClassName == 'spinbox'):
					item['value'] = elem.value()
				elif (elemClassName == 'betterslider'):
					# own better slider class
					item['value'] = elem.editedValue()
				else:
					continue
				# end if

			# end for
		# end if
	# end for
	
	return xmlList
# end loadGuiChange

def readXMLNodes(hand, tagName):
	liste = list()

	for node in hand.getElementsByTagName(tagName):
		if node.nodeType == node.ELEMENT_NODE:
			d = dict(list(node.attributes.items()))
			d["hand"] = node
			liste.append(d)
		# end if
	# end for

	return liste
# end readXMLNodes

def readXMLRec(hand):
	elems = dict()
	
	for node in hand.childNodes:
		if (node.attributes == None):
			continue
		# end if
		
		items = node.attributes.items()
		childs = node.childNodes
		if (node.nodeName not in elems):
			elems[node.nodeName] = dict()
			elems[node.nodeName]['items'] = list()
			elems[node.nodeName]['content'] = ''
		# end if
		
		if ('wholeText' in dir(node.firstChild)):
			elems[node.nodeName]['content'] = node.firstChild.wholeText
		# end if
		
		if (len(childs) == 0):
			items = dict(list(items))
			elems[node.nodeName]['items'].append(items)
		else:
			elems[node.nodeName]['items'].append(readXMLRec(node))
		# end if
	# end for
	
	return elems
# end readXMLRec

def writeXMLRec(hand, parentNode, settingsList):
	for name in settingsList:
		elem = settingsList[name]

		if ("__class__" not in dir(elem) or not elem.__class__ == dict):
			return False
		# end if
		
		for childElem in elem['items']:
			childNode = hand.createElement(str(name))
			
			for childName in childElem:
				if ("__class__" in dir(childElem[childName]) and childElem[childName].__class__ == list):
					writeXMLRec(hand, childNode, childElem)
				else:
					childNode.setAttribute(str(childName), str(childElem[childName]))
				# end if
			# end for
			
			parentNode.appendChild(childNode)
		# end for
		
		if ('contents' in elem):
			print("noch nicht implementiert")
		# end if

	# end for
	
	return True
# end writeXMLRec

def getXMLNodeByAttributeValue(hand, elementName, AttributeName, AttributeValue):
	foundNode = False
	for node in hand.getElementsByTagName(elementName):
		if (node.attributes[AttributeName].value == AttributeValue):
			foundNode = node
			break
		# end if
	# end for

	return foundNode
# end getXMLNodeByAttributeValue
	
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
# end str2bool