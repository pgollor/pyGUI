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
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Germany License.<br>
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to<br>
# Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#
# @brief This Thread can communicate with third party processes and the global progress bar.

from PyQt4.QtCore import QThread, pyqtSignal
import time


class progressBarThread(QThread):
	__sig_update = pyqtSignal(list, name = "sigProgressBarUpdate")
		
	def __init__(self, *args, **kwargs):
		QThread.__init__(self, *args, **kwargs)
		
		# set object name
		self.setObjectName("ProgressBarThread")
		
		# init vars
		self.__v_active = False
		self.__v_progressVal = False
		self.__v_progressMaxValue = False
		self.__v_multiprocessing = False
	# end __init__
	
	def stop(self):
		self.__v_active = False
	# end if
	
	def clear(self):
		self.__v_progressVal = False
		self.__v_progressMaxValue = False
		self.__v_multiprocessing = False
	# end clear
	
	def setParameter(self, progressValue, progressMaxValue, multiprocessing = False):
		self.init(progressValue, progressMaxValue, multiprocessing)
	# end setParameter
	
	def init(self, progressValue = 0, progressMaxValue = 100, multiprocessing = False, name = ''):
		self.__v_progressVal = progressValue
		self.__v_progressMaxValue = float(progressMaxValue)
		self.__v_multiprocessing = multiprocessing
		
		self.__sig_update.emit([name, "init"])
	# init

	def run(self):
		self.__v_active = True
		
		oldVal = None
		
		while (self.__v_active):
			if (self.__v_progressVal == False):
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
				self.__sig_update.emit([0, "disable"])
				self.clear()
				
				continue
			elif (command == -3):
				# clear
				self.__sig_update.emit([0, "clear"])
				self.clear()
				
				continue
			# end if
			
			# maximum
			if (value == self.__v_progressMaxValue):
				self.__sig_update.emit([100, "ready"])
			# end if
			
			# set value
			val = int(100 * (value / self.__v_progressMaxValue))
			
			if (oldVal != val):
				self.__sig_update.emit([val, "newVal"])
				oldVal = val
			# end if
			
			time.sleep(0.1)
		# end while
		
		self.__sig_update.emit([0, "disable"])
	# end run

# end class progressBarThread