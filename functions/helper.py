##
# @file helper.py
# 
# @date 10.02.2015
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


## @brief check if checkClass in compareClassList
def classEqual(checkClass, compareClassList):
	if (checkClass in compareClassList):
		return True
	# end if
	
	# convert classes to string
	checkClass = str(checkClass)
	compareClassList = str(compareClassList)
	
	# remove some sub strings
	checkClass = '.' + checkClass.replace('<class \'', '')
	
	if (compareClassList.find(checkClass) >= 0):
		return True
	# end if
	
	return False
# end if