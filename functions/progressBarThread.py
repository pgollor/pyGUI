##
# @file progressBarThread.py
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
#
# @brief This Thread can communicate with third party processes and the global progress bar.

from PyQt4.QtCore import SIGNAL, QThread
import time


class progressBarThread(QThread):
	__v_active = False
	__v_progressVal = None
	__v_progressMaxValue = None
	__v_multiprocessing = True
	
	def __init__(self, *args):
		QThread.__init__(self, *args)
		self.setObjectName("ProgressBarThread")
	# end __init__
	
	def stop(self):
		self.__v_active = False
	# end if
	
	def clear(self):
		self.__v_progressVal = None
		self.__v_progressMaxValue = None
		self.__v_multiprocessing = True
	# end clear
	
	def setParameter(self, progressValue, progressMaxValue, multiprocessing = True):
		self.init(progressValue,progressMaxValue,multiprocessing)
	# end setParameter
	
	def init(self, progressValue = 0, progressMaxValue = 100, multiprocessing = True, name = ''):
		self.__v_progressVal = progressValue
		self.__v_progressMaxValue = float(progressMaxValue)
		self.__v_multiprocessing = multiprocessing
		
		self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [name, "init"])
	# init

	def run(self):
		self.__v_active = True
		
		oldVal = None

		while (self.__v_active):
			if (self.__v_progressVal == None):
				time.sleep(0.1)
				continue
			# end if
			
			# get value
			if (self.__v_multiprocessing):
				command = self.__v_progressVal.value
			else:
				command = self.__v_progressVal[0]
			# end if
			
			# commands
			if (command >= 0):
				# update
				value = command
			elif (command == -1):
				# init
				self.init()
			elif (command == -2):
				# abbruch oder ende
				self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [0, "disable"])
				self.clear()

				continue
			elif (command == -3):
				# clear
				self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [0, "clear"])
				self.clear()

				continue
			# end if
			
			# maximum
			if (value == self.__v_progressMaxValue):
				self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [100, "ready"])
			# end if
			
			# set value
			val = int(100 * (value / self.__v_progressMaxValue))

			if (oldVal != val):
				self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [val, "newVal"])
				oldVal = val
			# end if
			
			time.sleep(0.1)

			#if (self.__v_multiprocessing):
			#	time.sleep(0.25)
			#	value = self.__v_progressVal.value
			#else:
			#	time.sleep(0.05)
			#	value = self.__v_progressVal[0]
			# end if
		# end while
		
		self.emit(SIGNAL("sigProgressBarUpdate(PyQt_PyObject)"), [0, "disable"])
	# end run

# end class progressBarThread