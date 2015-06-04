#! /usr/bin/python3

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
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
# 
# @mainpage pyGUI
# These project is a universal python3 GUI. You can add your own modules and use some global functions for your project.
#  
# @section Modules
# @subsection Allgemein
# Es gibt eine abstrakte Oberklasse(abstractModuleClass) von dieser alle Module abgeleitet werden.
# Drei verschiedene Modulklassen sind moeglich:
# - hidden
# - settings
# - application
#
# Die einzelnen Module werden in dieser Reihenfolge geladen.
# Innerhalb eines Modultyps werden die Module nach alphabethischer Reihenfolge geladen.
# Falls es notwendig ist, dass ein Modul zwingend von einem anderen des gleichen Typs abhaengt, sollte man den Ordner des Moduls mit einer Zahl vor dem Modulnahmen versehen.
# Falls Modul xy zwingend das Modul zz benoetigt, sollte (NUR) der Ordnernamen des Moduls zz z.B. in 10zz umbenannt werden.
# Damit ist sicher gestellt, dass das Modul zz vor dem Modul xy geladen wird.
# 
# Jedes Modul muss ein eigenen Unterordner mit dem Namen des Modules im Ordner modules besitzen.
# In diesem Ordner muessen folgende Dateien mindestens enthalten sein:
# - [MODULNAME].py
# - [MODULNAME].ui (nicht fuer hidden Module) 
# 
# Die genaue Struktur dieser Dateien kann in den Beispielmodulen nachgelesen werden.
# Die Klasse des Moduls muss immer module heissen und von der jeweils dazugehoerigen Elternklasse abgeleitet sein: 
# - class module(applicationModuleClass): 
# - class module(applicationModuleClass):
# - class module(hiddenModuleClass):
# 
# Fuer die Module "settings" und "application" koennen Werte verschiedener Qt Elemente automatisch gespeichert werden.
# Dazu fragt de rModulhandler die Funktion "getDefaultSettings" in jedem Modul ab.
# Falls die Funktion nicht vorhanden ist, wird davon ausgegangen, dass keine Einstellungen gespeichert werden sollen.
# Als Rueckgabewerte muss ein Dictionary zurueck gegeben werden in dem die zu speichernden Informationen enthalten sind.
# Um z.B. den Inhalt eines QLineEdits zu speichern saehe das dict wie folgt aus:  
# <pre>
#{
#"inhaltXY" = {"qName": "labelXY", "value" = "Irgend ein Inhalt"}
#}</pre>
# 
# Die beiden Parameter "qName" und "value" muessen fuer jeden Eintrag zwingend vorhanden ein.
# Der Schluessel "inhaltXY" kann hingegen frei gewaehlt werden.
# Dies entspricht danna auch dem Listeneintrag wenn das Modul waehrend der Laufzeit seine Einstellungen mit "self._getSettings()" abfragt.
# @n Der Wert zu "qName" ist der Name des dazugehoerigen Qt Elements und "value" der Inhalt der als default angegeben wird.
# Das heisst je nach Qt Element kann "value" auch leer sein.
# @n Neben QLabel werden von der GUI auch noch weitere Qt Elemente unterstuetzt:
# - QCheckBox, QRadioButton und QGroupBox:
# @n Es wird der Status "checked()" gespeichert. Dazu ist "value" als bool anzugeben. Die Groupbox muss dafuer "checkable" sein.
# <pre>{
#  "X" = {"qName": "checkBoxX", "value": False},
#  "Y" = {"qName": "radioButtonY", "value": True},
#  "Z" = {"qName": "groupBoxZ", "value": True}
#}</pre>
# - QComboBox
# <pre>{
#  "X" = {"qName": "comboBoxX", "value": "Inhalt"}
#}</pre>
# - QSpinBox und QDoubleSpinBox
# @n Beid er spinBox sollten Integers verwendet werden und fuer die doubleSpingBox floats.
# <pre>{
#  "X" = {"qName": "spinBoxX", "value": 2, "minVal": 0, "maxVal": 10, "step": 1},
#  "Y" = {"qName": "doubleSpinBoxY", "value": 1.0, "minVal": 0.0, "maxVal": 10.0, "step": 0.1},
#}</pre>
# - betterSlider
# @n vohanden sein muessen; "qName", "value", "type", "maxVal" und "minVal"
# @n "type": integer, double, logarithm
# @n optiional sind: "step" (default: 1), "pageStep" (default 10), "connectedLabels", "connectedLineEdits"
# <pre>{
#  "X": {"qName": "horizontalSliderX", "type": "double", "value": 10, "minVal": 0, "maxVal": 100, "step": 0.1, "pageStep": 20, "connectedLabels": ["labelTestSl"], "connectedLineEdits": ["lineEditTextSl"]},
#}</pre>
# - QTextEdit und QPlainTextEdit
# <pre>{
#  "X" = {"qName": "textEdit", "value": "Inhalt"}
#}</pre>
# 
# Falls in der Gui unter Settings die Einstellung Save on exit aktiviert ist, werden dann die geaenderten Einstellung automatisch beim Beenden des Programms gespeichert und nach erneutem Start wieder geladen.
# 
# @section Modultypen
# @subsection hidden-Modul
# Ein hidden Modul enthaelt keine Funktionen fuer die eigentliche Oberflaeche. In diesen Modulen werden nur Funktionen oder externe Klassen bereit gestellt die von anderen Modulen verwendet werden. 
# 
# @subsection settings-Modul
# Diese Module werden in dem Tab "settings" angezeigt und setzen z.B. einfach nur Einstellungen fuer andere Module (im Idealfall der hidden Module).
# Aber diese stellen schon eine graphische Oberflaeche fuer die Einstellungen durch den Benutzer bereit. 
# 
# @subsection application-Modul
# Diese Module sind die eigentliche Benutzeroberflaeche. Fuer jedes Modul wird ein eigener Tab geladen.
# In diesem Tab werden automatisch die Oberflaechenelemente von Qt geladen, die in der dazu gehoerigen ui-Datei gespeichert sind. 
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
# Alle anderen Funktionen sind als Virtuelle-Funktionen bereits vorhanden die ueberladen werden koennen.
# Diese werden in folgender Reihenfolge aufgerufen:
# - initPreSettings(self): Wird geladen bevor die Einstellungen aus der XML-Datei geladen werden.
# - initModule(self): Ist zum initialisieren von Klassen aus anderen Modulen und fuer Klassen aus dem eigenen Ordner gedacht. Dazu wird fuer diese Funktion vom Modulhandler in das Modulverzeichnis gewechselt.
# - initGui(self): Ist zum initialisieren der GUI Elemente gedacht.
# - onClose(self): Wird beim Beenden aufgerufen bevor die Klasse geloescht wird.
# - onActive(self): Wird jedes mal fuer das Modul aufgerufen, dass in der GUI ausgewaehlt wurde.
# - onInactive(self): Gegenteil von "onActive".
# - getDefaultSettings(self)
#
# Die Funktionen initPreSettings und initModule werden hintereinander nach der oben beschriebenen Modulreihenfolge ausgefuehrt.
# Nach dem diese Funktionen bei ALLEN Modulen ausgefuehrt wurden, wird nach der gleichen Reihenfolge die Funktion initGui ausgefuehrt.
# 


import sys, os, logging, optparse
from PyQt4 import QtGui
from mainWindow import mainWindow
from functions.guiLogger import QtLogger

# add dlls folder to environment
dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dlls")
global_path = os.environ.get('PATH', '')
if dll_path not in global_path:
	os.environ['PATH'] = os.pathsep.join((dll_path, global_path))
# end if




def parser():
	# parser
	parser = optparse.OptionParser(
		usage = "%prog [options]",
		description = "pyGUI - Modular GUI based on python and qt."
	)
	
	group = optparse.OptionGroup(parser, "Diagnostics")
	group.add_option("-d", "--debug",
		dest = "debug",
		action = "store_true",
		help = "Show debug output. And override loglevel with debug.",
		default = False
	)
	group.add_option("-l", "--loglevel",
		dest = "loglevel",
		action = "store",
		type = 'int',
		help = "Loglevel for python logger. " + str(logging.CRITICAL) + ": critical  " + str(logging.ERROR) + ": error  " + str(logging.WARNING) + ": warning  " + str(logging.INFO) + ":info  " + str(logging.DEBUG) + ":debug",
		default = logging.ERROR
	)
	parser.add_option_group(group)

	(options, args) = parser.parse_args()
	
	if (options.debug == True):
		options.loglevel = logging.DEBUG
	# end if
	
	return options
# end parser



## @brief main function
# create main window
if __name__ == '__main__':
	## set basic logging settings add own logger stream
	# Set loglevel not to debug, because qt create much debug outputs. 
	logging.basicConfig(level = logging.WARNING, format='%(asctime)-9s %(name)s [%(levelname)s]: %(message)s', datefmt='%H:%M:%S', handlers = [QtLogger()])
	
	# parser
	options = parser()

	# create Qt application
	app = QtGui.QApplication(sys.argv)
	
	if (options.debug == True):
		w = mainWindow(loglevel = options.loglevel, debug = options.debug)
		w.init(app.desktop().availableGeometry())
		w.show()
	else:
		try:
			w = mainWindow(loglevel = options.loglevel, debug = options.debug)
		
			# init main window
			w.init(app.desktop().availableGeometry())
	
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
	
	#app.setQuitOnLastWindowClosed(True)
	ret = app.exec_()
	
	# delete all objects
	del(w)
	del(app)

	os._exit(0) # kill abrupt
	sys.exit(ret)
# end if
