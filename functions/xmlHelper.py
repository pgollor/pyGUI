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

from PyQt4.QtGui import QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox


def setGuiSettings(xmlList, parentElement):
	retList = {"label" : list(), "lineedit" : list(), "checkbox" : list(), "radiobutton" : list(), "combobox" : list(), "groupbox" : list()}
	setText = ['label', 'lineedit']
	checked = ['checkbox', 'radiobutton', 'groupbox']
	
	for elemClassName in xmlList:
		if (elemClassName in retList):
			for item in xmlList[elemClassName]['items']:
				elem = parentElement.findChild((QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox), item['name'])

				if (not elem):
					continue
				# end if
				
				if (elemClassName in setText):
					elem.setText(item['text'])
				elif (elemClassName in checked):
					elem.setChecked(str2bool(item['checked']))
				elif (elemClassName == 'combobox'):
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
					
					if (index >= 0 and index < elem.count()):
						elem.setCurrentIndex(index)
					else:
						elem.setCurrentIndex(0)
					# end if
				else:
					continue
				# end if
				
				retList[elemClassName].append(item['name'])
			# end for
		# end if
	# end for
	
	return retList
# end setGuiSettings


def loadGuiChange(xmlList, parentElement):
	supportetElements = ['label', 'lineedit', 'checkbox', 'radiobutton', 'groupbox', 'combobox']
	setText = ['label', 'lineedit']
	checked = ['checkbox', 'radiobutton', 'groupbox']
	
	for elemClassName in xmlList:
		if (elemClassName in supportetElements):
			for item in xmlList[elemClassName]['items']:
				elem = parentElement.findChild((QLabel, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGroupBox), item['name'])

				if (not elem):
					continue
				# end if
				
				if (elemClassName in setText):
					item['text'] = elem.text()
				elif (elemClassName in checked):
					item['checked'] = str(elem.isChecked())
				elif (elemClassName == 'combobox'):
					item['index'] = elem.currentText()
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