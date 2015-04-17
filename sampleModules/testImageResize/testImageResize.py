## @file testImageResize.py
#
# @date 26.07.2013
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
# @brief This is a demo module to demonstrate the global image resize object.


from PyQt4.QtCore import SIGNAL
from abstractModuleClass import applicationModuleClass
from functools import partial
from imageBox import imageBox


class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
		
		self.__initVars()
	# end __init__
	
	def __initVars(self):
		self.__v_maxFrameHeight = False
		self.__v_maxFrameWidth = False
		self.__v_maxImageWidth = False
		self.__v_maxImageHeight = False
		self.__v_actualImageHeight = False
		self.__v_actualImageWidth = False
		self.__v_actualImageVPos = False
		self.__v_actualImageHPos = False
	# end __initVars
		
	def __onRoiChanged(self, roi):
		self._p_logger.info("new roi: %i, %i, %i, %i", roi[0], roi[1], roi[2], roi[3])
	# end __onRoiChanged

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		pass
	#end _initModule

	def initGUI(self):
		self.imageBoxWidget.init(800, 600, 80, 60, 2)

		self.connect(self.imageBoxWidget, SIGNAL("roiChanged(PyQt_PyObject)"), self.__onRoiChanged)
	# end _initGUI
	
	def onClose(self):
		self.__initVars()
	# end onClose

	# ---------- overrided functions ----------

# end class module
