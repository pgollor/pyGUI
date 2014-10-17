##
# @file server.py
# 
# 	@date 03.03.2014
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


import struct, datetime, socketserver, pickle, logging.handlers, select
from delete import delete

from PyQt4.QtGui import QListWidgetItem, QBrush
from PyQt4.QtCore import Qt, QThread, SIGNAL


gp_loggingThread = False


## @brief logger server socket handler
#
# Handler for a streaming logging request.
#
# This basically logs the record using whatever logging policy is
# configured locally.
class LogRecordStreamHandler(socketserver.StreamRequestHandler):
	__v_running = True
	
	def __del__(self):
		self.stop()
	# end __del__
	
	def handle(self):
		"""
		Handle multiple requests - each expected to be a 4-byte length,
		followed by the LogRecord in pickle format. Logs the record
		according to whatever policy is configured locally.
		"""
		self.__v_running = True
		
		while (self.__v_running):
			chunk = self.connection.recv(4)
			if len(chunk) < 4:
				break
			slen = struct.unpack('>L', chunk)[0]
			chunk = self.connection.recv(slen)
			
			while len(chunk) < slen:
				chunk = chunk + self.connection.recv(slen - len(chunk))
			# end while
				
			obj = self.unPickle(chunk)
			record = logging.makeLogRecord(obj)
			
			self.handleLogRecord(record)
	# end handle
	
	def stop(self):
		self.__v_running = False
	# end stop

	def unPickle(self, data):
		return pickle.loads(data)
	# end unPickle

	def handleLogRecord(self, record):
		# if a name is specified, we use the named logger rather than the one
		# implied by the record.
		if self.server.logname is not None:
			name = self.server.logname
		else:
			name = record.name
		# end if
			
		logger = logging.getLogger(name)
		#logger.handle(record) # python standard logging
		
		# own qt logging
		self.__showError(record)
	# end handleLogRecord
		
	def __showError(self, record):
		global gp_loggingThread
		
		if (gp_loggingThread == False):
			return False
		# end if
		
		errMsg = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " "
		errMsg += str(record.name) + ": "
		errMsg += "[" + str(record.levelname) + "]: " + str(record.getMessage())
		
		item = QListWidgetItem(errMsg)
		
		if (record.levelno == logging.CRITICAL or record.levelno == logging.ERROR):
			item.setForeground(QBrush(Qt.red))
		elif (record.levelno == logging.WARN):
			item.setForeground(QBrush(Qt.blue))
		elif (record.levelno == logging.DEBUG):
			item.setForeground(QBrush(Qt.gray))
			
		gp_loggingThread.emit(SIGNAL("logReceived(PyQt_PyObject)"), item)
		
		return True
	# end __showError

# end class LogRecordStreamHandler


## @brief server logging thread
# This thread handle all client logger requests
class loggingThread(QThread):
	def __init__(self, parent = False):
		global gp_loggingThread
		
		self.__initVars()

		#if (gp_loggingThread != False):
		#	return
		## end if
		
		QThread.__init__(self, parent)
		self.setObjectName("loggingThread")
		
		gp_loggingThread = self
	# end __init__
	
	def __initVars(self):
		self.__p_socketserver = False
		self.__v_running = True
		self.__v_timeout = 0.1
	# end __initvars
	
	def __del__(self):
		self.stop()
		
		gp_loggingThread = False

		self.__initVars()
	# end __del__
	
	def run(self):
		self.__v_running = True
		
		host='localhost'
		port=logging.handlers.DEFAULT_TCP_LOGGING_PORT
		handler = LogRecordStreamHandler
		self.__p_socketserver = socketserver.ThreadingTCPServer((host, port), handler)
		self.__p_socketserver.logname = None
		
		while (self.__v_running):
			rd, wr, ex = select.select([self.__p_socketserver.socket.fileno()], [], [], self.__v_timeout)

			if rd:
				try:
					self.__p_socketserver.handle_request()
				except Exception as e:
					pass
			# end if
		# end while
	# end run
	
	def stop(self):
		self.__v_running = False
		
		if (self.__p_socketserver != False):
			#self.__p_socketserver.shutdown()
			self.__p_socketserver.socket.close()
			self.__p_socketserver.server_close()
			self.wait(100)
			del(self.__p_socketserver)
			self.__p_socketserver = False
		# end if
	# end stop
	
# end class loggingThread

