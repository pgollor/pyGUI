##
# @file main.py
# 
# @date 25.07.2013
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
# 
# @mainpage pyGUI
# These project is a universal python3 GUI. You can add your own modules and use some global functions for your project.
#  
# @section Module
# @subsection Allgemein
# Es gibt eine abstrakte Oberklasse(abstractModuleClass) von dieser alle Module abgeleitet werden.
# Drei verschiedene Modulklassen sind möglich:
# - hidden
# - settings
# - application
#
# Die einzelnen Module werden in dieser Reihenfolge geladen. Innerhalb eines Modultyps werden die Module nach alphabethischer Reihenfolge geladen. Falls es notwendig ist, dass ein Modul zwingend von einem anderen Modul des gleichen Typs abhängt, sollte man den Ordner des Moduls mit einer Zahl vor dem Modulnahmen versehen.
# Falls Modul xy zwingend das Modul zz benötigt, sollte (NUR) der Ordnernamen des Moduls zz z.B. in 10zz umbenannt werden. Damit ist sicher gestellt, dass das Modul zz vor dem Modul xy geladen wird.
# 
# Jedes Modul besitzt zwingend ein eigenen Unterordner mit dem Namen des Modules im Ordner modules.
# In diesem Ordner müssen folgende Dateien mindestens enthalten sein:
# - [MODULNAME].py 
# - [MODULNAME].xml (nicht für hidden Module) 
# - [MODULNAME].ui (nicht für hidden Module) 
# 
# Die genaue Struktur dieser Dateien kann in den Beispielmodulen nachgelesen werden. Die Klasse des Moduls muss immer module heißen und von der jeweils dazugehörigen Elternklasse abgeleitet sein: 
# - class module(applicationModuleClass): 
# - class module(applicationModuleClass):
# - class module(hiddenModuleClass):
# 
# Für die Module settings und application können Werte verschiedener Qt Elemente automatisch gespeichert werden. Dazu werden diese einfach als Standardeinstellungen (default settings) in die dazugehörige xml eingetragen. die Syntax sieht dazu wie folgt aus: 
# - label: <label name="label" text="default text from xml" /> 
# - lineedit: <lineedit name="lineEditPiezoStep" text="0.02" /> 
# - checkbox: <checkbox name="checkBoxTest" checked="True" /> 
# - radiobutton: <radiobutton name="radioButton_1" checked="True" />
# - groupbox: <groupbox checked="False" name="groupBoxExtTrigger" />
# - combobox: <combobox index="0" name="comboBoxSerialPorts" />
# Falls in der Gui unter Settings die Einstellung Save on exit aktiviert ist, werden dann die geänderten Einstellung automatisch beim Beenden des Programms gespeichert und nach erneutem Start wieder geladen.
# 
# @section Modultypen
# @subsection hidden-Modul
# Ein hidden Modul enthält keine Funktionen für die eigentliche Oberfläche. In diesen Modulen werden nur Funktionen oder externe Klassen bereit gestellt die von anderen Modulen verwendet werden. 
# 
# @subsection settings-Modul
# Diese Module werden in dem Tab "settings" angezeigt und setzen z.B. einfach nur Einstellungen für andere Module (im Idealfall der hidden Module).
# Aber diese stellen schon eine graphische Oberfläche für die Einstellungen durch den Benutzer bereit. 
# 
# @subsection application-Modul
# Diese Module sind die eigentliche Benutzeroberfläche. Für jedes Modul wird ein eigener Tab geladen.
# In diesem Tab werden automatisch die Oberflächenelemente von Qt geladen, die in der dazu gehörigen ui-Datei gespeichert sind. 
#
# @section function Funktionen in der Modulklasse
# @subsection must-have must have
# Die Funktion die auf jeden Fall in der Modulklasse vorhanden sein muss ist die init Funktion:
# <pre>
# class module(applicationModuleClass):
#   def __init__(self, parent, name):
#     applicationModuleClass.__init__(self, parent, name)
#   # end __init__
# </pre>
# 
# @subsection optional
# Alle anderen Funktionen sind als Virtuelle-Funktionen bereits vorhanden die überladen werden können.
# Diese werden in folgender Reihenfolge aufgerufen:
# - initPreSettings(self): Wird geladen bevor die Einstellungen aus der XML-Datei geladen werden.
# - initModule(self): Ist zum initialisieren von Klassen aus anderen Modulen und für Klassen aus dem eigenen Ordner gedacht. Dazu wird für diese Funktion vom Modulhandler in das Modulverzeichnis gewechselt.
# - initGui(self): Ist zum initialisieren der GUI Elemente gedacht.
# - onClose(self): Wird beim Beenden aufgerufen bevor die Klasse gelöscht wird.
# - onActive(self): Wird jedes mal für das Modul aufgerufen, dass in der GUI ausgewählt wurde. 
#
# Die Funktionen initPreSettings und initModule werden hintereinander nach der oben beschriebenen Modulreihenfolge ausgeführt.
# Nach dem diese Funktionen bei ALLEN Modulen ausgeführt wurden, wird nach der gleichen Reihenfolge die Funktion initGui ausgeführt. 
# 


import sys
from PyQt4 import QtGui
from mainWindow import mainWindow
from functions.delete import delete


DEBUG = True


## @brief main function
# create main window
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	if (DEBUG == True):
		w = mainWindow()
		w.init()
		w.show()
	else:
		try:
			w = mainWindow()
		
			# init main window
			w.init()
	
			# show main gui	
			w.show()
		except Exception as e:
			message = "unresolved exception in main.py: "
			if (len(e.args) > 0):
				message += str(e.args)
			# end if
			print(message)
			sys.exit(0)
		# end try
	# end if
	
	ret = app.exec_()
	
	# delete all objects
	del(w)
	del(app)

	sys.exit(ret)
# end if
