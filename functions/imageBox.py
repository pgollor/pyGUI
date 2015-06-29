##
# @file imageBox.py
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
# @defgroup imageBox global image box
# @{
# @brief Image box which can be used in all modules.
#
# This image box can be used like any QWidget in an ui file or directly in your code.
#


from PyQt4.QtCore import pyqtSignal, pyqtSlot
from PyQt4.QtGui import QWidget, QLabel, QFrame, QSizePolicy, QStackedLayout
import numpy as np
from PyQt4 import uic


class imageBox(QWidget):
	## roiChanged signal
	__p_signalRoiChanged = pyqtSignal(list, name = "roiChanged")
	
	## initial function
	def __init__(self, *args, **kwargs):
		QWidget.__init__(self, *args, **kwargs)
		
		self.__v_maxImageWidth = 0
		self.__v_maxImageHeight = 0
		
		self.__v_actualImageHeight = 0
		self.__v_actualImageWidth = 0
		self.__v_actualImageYPos = 0
		self.__v_actualImageXPos = 0
		
		self.__l_lastRoi = [0, 0, 0, 0]
		self.__v_emitSignal = True
		
		self.__p_frameSize = 0
		
		# create gui elements
		uic.loadUi("functions/imageBox.ui", self)
		self.__initGui()

		# init with default values
		self.init(800, 600, 10, 10)
	# end __init__
	
	## @brief Qt Resize event
	# @param self The object pointer.
	# @param event Qt event
	def resizeEvent(self, event):
		self.__p_frameSize = self.frameROI_dummy.size()
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)

		return QWidget.resizeEvent(self, event)
	#end resizeEvent
	
	## @brief initialize GUI
	# @param self The object pointer.
	def __initGui(self):
		self.setMinimumSize(420, 320)
		
		self.labelBackgroundImage = QLabel("")
		self.labelBackgroundImage.setSizePolicy(QSizePolicy.Ignored,  QSizePolicy.Ignored)
		self.labelBackgroundImage.setScaledContents(True)
		self.labelBackgroundImage.setStyleSheet("background-color: rgb(195, 195, 195);")
		
		self.labelOverlayImage = QLabel("")
		self.labelOverlayImage.setSizePolicy(QSizePolicy.Ignored,  QSizePolicy.Ignored)
		self.labelOverlayImage.setScaledContents(True)
		
		self.frameROI_dummy = QFrame()
		self.frameROI_dummy.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
		self.frameROI = QFrame(self.frameROI_dummy)
		self.frameROI.setStyleSheet("background-color: rgba(64, 255, 96, 50);")
		
		layout = QStackedLayout()
		layout.setStackingMode(QStackedLayout.StackAll)
		self.gridLayout.addLayout(layout, 2, 2) # add in the middle
		
		layout.addWidget(self.frameROI_dummy)
		layout.addWidget(self.labelOverlayImage)
		layout.addWidget(self.labelBackgroundImage)
		
		#self.gridLayout.addLayout(layout,2,2)
		self.__p_frameSize = self.frameROI_dummy.size()
		
		# connect line edits to slider
		self.sliderWidth.connectLineEdit(self.lineEditWidth)
		self.sliderHeight.connectLineEdit(self.lineEditHeight)
		self.sliderXPos.connectLineEdit(self.lineEditXPos)
		self.sliderYPos.connectLineEdit(self.lineEditYPos)

		# connect signals
		self.sliderWidth.sigChanged[int].connect(self.__onSliderChangeWidth)
		self.sliderHeight.sigChanged[int].connect(self.__onSliderChangeHeight)
		self.sliderXPos.sigChanged[int].connect(self.__onSliderChangeXPos)
		self.sliderYPos.sigChanged[int].connect(self.__onSliderChangeYPos)
		
		self.sliderWidth.sigChanged[int].connect(self.__onChanged)
		self.sliderHeight.sigChanged[int].connect(self.__onChanged)
		self.sliderXPos.sigChanged[int].connect(self.__onChanged)
		self.sliderYPos.sigChanged[int].connect(self.__onChanged)
	# end __initGui
	
	## @brief Changed slot for all slider.
	# @param self The object pointer.
	# @param val value
	@pyqtSlot(int)
	def __onChanged(self, val):
		width = self.sliderWidth.value()
		height = self.sliderHeight.value()
		xPos = self.sliderXPos.value()
		yPos = self.sliderYPos.value()
		
		roi = [width, height, xPos, yPos]
		
		if (roi != self.__l_lastRoi):
			if (self.__v_emitSignal):
				self.__p_signalRoiChanged.emit(roi)
			# end if
			self.__l_lastRoi = roi
		# end if
	# end __emitChange
	
	## @brief Changed slot for slider height.
	# @param self The object pointer.
	# @param value value
	@pyqtSlot(int)
	def __onSliderChangeHeight(self, value):		
		# set current position
		self.__v_actualImageHeight = value
		self.sliderHeight.setValue(value)
		
		# resize
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)
		# reinit position slider
		self.sliderYPos.setMaximum(self.__v_maxImageHeight - self.__v_actualImageHeight)
	# end __onSliderChangeHeight
	
	## @brief Changed slot for slider width.
	# @param self The object pointer.
	# @param value value
	@pyqtSlot(int)
	def __onSliderChangeWidth(self, value):
		# set current position
		self.__v_actualImageWidth = value
		self.sliderWidth.setValue(value)

		# resize		
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)

		# reinit position slider
		self.sliderXPos.setMaximum(self.__v_maxImageWidth - self.__v_actualImageWidth)
	# end __onSliderChangeWidth


	## @brief Changed slot for slider x position.
	# @param self The object pointer.
	# @param value value
	@pyqtSlot(int)
	def __onSliderChangeXPos(self, value):
		diff = self.__v_maxImageWidth - self.__v_actualImageWidth
		
		# check if value smaller then difference
		if (value <= diff):
			new_value = value
		else:
			new_value = diff
		# end if
		
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,new_value,self.__v_actualImageYPos)
		# set new values
		self.__v_actualImageXPos = new_value
		self.sliderXPos.setValue(new_value)
	# end __onSliderChangeXPos
	
	## @brief Changed slot for slider y position.
	# @param self The object pointer.
	# @param value value
	@pyqtSlot(int)
	def __onSliderChangeYPos(self, value):
		diff = self.__v_maxImageHeight - self.__v_actualImageHeight
		
		# check if value smaller then difference
		if (value <= diff):
			new_value = value
		else:
			new_value = diff					
		# end if
		
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,new_value)
		# set new values
		self.__v_actualImageYPos = new_value
		self.sliderYPos.setValue(new_value)
	# end __onSliderChangeYPos
	
	def __updateROISize(self, w, h, x, y):
		x_frame = round((x / self.__v_maxImageWidth) * self.__p_frameSize.width())
		y_frame = round((y / self.__v_maxImageHeight) * self.__p_frameSize.height())
		w_frame = round((w / self.__v_maxImageWidth) * self.__p_frameSize.width())
		h_frame = round((h / self.__v_maxImageHeight) * self.__p_frameSize.height())
		
		self.frameROI.setGeometry(x_frame,y_frame,w_frame,h_frame)
	# end __updateROISize
	
	## @brief Interface function for initializing the image box.
	# @param self The object pointer.
	# @param maxWidth Maximum width.
	# @param maxHeight Maximum Height.
	# @param minWidth Minimum width. Default 0.
	# @param minHeight Minimum height. Default 0.
	# @param stepWidth Step width for one change step. Default 1.
	# @param stepHeight Step height for one change step. Default 1.
	# @param stepX Step size for change in x position. Default 1.
	# @param stepY Step size for change in y position. Default 1.
	#
	# All parameters have to be in pixel.
	def init(self, maxWidth, maxHeight, minWidth = 0, minHeight = 0, stepWidth = 1, stepHeight = 1, stepX = 1, stepY = 1):
		# set global variables
		self.__v_maxImageWidth = maxWidth
		self.__v_maxImageHeight = maxHeight
		self.__v_actualImageYPos = 0
		self.__v_actualImageXPos = 0
		self.__v_actualImageWidth = self.__v_maxImageWidth
		self.__v_actualImageHeight = self.__v_maxImageHeight

		# init slider
		self.sliderWidth.init(minWidth, maxWidth, stepWidth)
		self.sliderHeight.init(minHeight, maxHeight, stepHeight)
		self.sliderXPos.init(0, self.__v_maxImageWidth - self.__v_actualImageWidth, stepX)
		self.sliderYPos.init(0, self.__v_maxImageHeight - self.__v_actualImageHeight, stepY)
		
		# set slider values
		self.sliderWidth.setValue(self.__v_actualImageWidth)
		self.sliderHeight.setValue(self.__v_actualImageHeight)
		self.sliderXPos.setValue(self.__v_actualImageXPos)
		self.sliderYPos.setValue(self.__v_actualImageYPos)
		
		self.__l_lastRoi = [self.__v_actualImageWidth, self.__v_actualImageHeight, self.__v_actualImageXPos, self.__v_actualImageYPos]
	# end init

	## @brief Interface function to set background image.
	# @param self The object pointer.
	# @param image Image as Qt pixmap.
	def setBackgroundImage(self, image):
		self.labelBackgroundImage.setPixmap(image)#.scaled(self.frame.size(),Qt.IgnoreAspectRatio))
	# end setBackgroundImage
	
	## @brief Interface function to set an overlay image.
	# @param self The object pointer.
	# @param image Image as Qt pixmap.
	def setOverlayImage(self, image):
		self.labelOverlayImage.setPixmap(image)#.scaled(self.frame.size(),Qt.IgnoreAspectRatio))
		self.labelOverlayImage.setVisible(True)
	# end setBackgroundImage
	
	## @brief Enable/Show background image.
	# @param self The object pointer.
	# @param enable True or False. Default True.
	def enableBackgroundImage(self, enable = True):
		self.labelBackgroundImage.setVisible(enable)
	# end enableROIFrame
	
	## @brief Enable/Show overlay image.
	# @param self The object pointer.
	# @param enable True or False. Default True.
	def enableOverlayImage(self, enable = True):
		self.labelOverlayImage.setVisible(enable)
	# end enableROIFrame
	
	## @brief Enable/Show roi frame.
	# @param self The object pointer.
	# @param enable True or False. Default True.
	def enableROIFrame(self, enable = True):
		self.frameROI.setVisible(enable)
	# end enableROIFrame
	
	## @brief Interface function to set region of interest.
	# @param self The object pointer.
	# @param *args Roi arguments.
	# @return True or False.
	#
	# Roi argument options:
	# - width, height
	# - width, height, x position, y position
	# - np.array([width, height, x position, y position])
	# 
	# X and y position are 0 if not specified. 
	def setROI(self, *args):
		self.__v_emitSignal = False
		
		if (len(args) == 1):
			if (len(args[0]) != 4):
				self.__v_emitSignal = True
				return False
			# end if

			data = args[0]
		elif (len(args) == 2):
			if (len(args[0]) != 2):
				self.__v_emitSignal = True
				return False
			# end if
			
			data = np.array([args[0], args[1], 0, 0])
		elif (len(args) == 4):
			data = np.array([args[0], args[1], args[2], args[3]])
		else:
			self.__v_emitSignal = True
			return False
		# end if
		
		self.__onSliderChangeWidth(data[0])
		self.__onSliderChangeHeight(data[1])
		self.__onSliderChangeXPos(data[2])
		self.__onSliderChangeYPos(data[3])
		
		self.__v_emitSignal = True
		
		return True
	# end setROI
	
	## @brief Get region of interest.
	# @param self The object pointer.
	# @return [width, height, x position, y position]
	def roi(self):
		return [self.__v_actualImageWidth, self.__v_actualImageHeight, self.__v_actualImageXPos, self.__v_actualImageYPos]
	# end roi()
	
# end class imageBox

## @}
	