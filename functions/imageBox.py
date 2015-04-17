from PyQt4.QtCore import SIGNAL, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QWidget, QLabel, QFrame, QSizePolicy, QStackedLayout
import numpy as np

from PyQt4 import uic

class imageBox(QWidget):
	# ---------- Variables ----------
	__p_signalRoiChanged = pyqtSignal(list, name = "roiChanged")
	# ---------- Variables ----------
	
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
	
	def resizeEvent(self, event):
		self.__p_frameSize = self.frameROI_dummy.size()
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)
		QWidget.resizeEvent(self, event)
	#end resizeEvent
	
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
		self.gridLayout.addLayout(layout, 2, 2)
		
		layout.addWidget(self.frameROI_dummy)
		layout.addWidget(self.labelOverlayImage)
		layout.addWidget(self.labelBackgroundImage)
		
		#self.gridLayout.addLayout(layout,2,2)
		self.__p_frameSize = self.frameROI_dummy.size()
		
		# slider
		self.sliderWidth.connectLineEdit(self.lineEditWidth)
		self.sliderHeight.connectLineEdit(self.lineEditHeight)
		self.sliderXPos.connectLineEdit(self.lineEditXPos)
		self.sliderYPos.connectLineEdit(self.lineEditYPos)

		# connect signals
		self.connect(self.sliderWidth, SIGNAL("valueChanged(PyQt_PyObject)"), self.__onSliderChangeWidth)
		self.connect(self.sliderHeight, SIGNAL("valueChanged(PyQt_PyObject)"), self.__onSliderChangeHeight)
		self.connect(self.sliderXPos, SIGNAL("valueChanged(PyQt_PyObject)"), self.__onSliderChangeXPos)
		self.connect(self.sliderYPos, SIGNAL("valueChanged(PyQt_PyObject)"), self.__onSliderChangeYPos)
		
		self.connect(self.sliderWidth, SIGNAL("changed(PyQt_PyObject)"), self.__onChanged)
		self.connect(self.sliderHeight, SIGNAL("changed(PyQt_PyObject)"), self.__onChanged)
		self.connect(self.sliderXPos, SIGNAL("changed(PyQt_PyObject)"), self.__onChanged)
		self.connect(self.sliderYPos, SIGNAL("changed(PyQt_PyObject)"), self.__onChanged)
	# end __initGui
	"""
	def mousePressEvent(self, event):
		#noch im Testmodus
		
		return
		framePos = QPoint(self.__p_frameImage.x() + self.__p_frameRoi.x(), self.__p_frameImage.y() + self.__p_frameRoi.y())
		mousePos = event.pos()
		
		if (mousePos.x() >= framePos.x() and mousePos.x() < framePos.x() + self.__p_frameRoi.width() and mousePos.y() >= framePos.y() and mousePos.y() < framePos.y() + self.__p_frameRoi.height()):
			self.__v_mouseInRoi = mousePos
		else:
			self.__v_mouseInRoi = QPoint(-1, -1)
		# end if
		
		QWidget.mousePressEvent(self, event)
	# end mosuePressEvent
	
	def mouseMoveEvent(self, event):
		# noch im Testmodus
		
		return
		mousePos = event.pos()
		
		if (self.__v_mouseInRoi != QPoint(-1,-1)):
			mouseDiff = (self.__v_mouseInRoi - mousePos) / 10
			print(mouseDiff)
			print(self.__p_frameRoi.pos())
			
			#self.__onSliderChangeXPos(self.__p_frameRoi.x() - mouseDiff.x())
			#self.__onSliderChangeYPos(self.__p_frameRoi.y() - mouseDiff.y())
			width = self.__p_frameRoi.width()
			height = self.__p_frameRoi.height()

			newX = self.__p_frameRoi.x() - mouseDiff.x()
			newY = self.__p_frameRoi.y() - mouseDiff.y()
			diffX = self.__p_frameImage.width() - self.__p_frameRoi.width()
			diffY = self.__p_frameImage.height() - self.__p_frameRoi.height()
			if (newX < 0):
				newX = 0
			# end if
			if (newY < 0):
				newY = 0
			# end if
			if (newX > diffX):
				newX = diffX
			# end if
			if (newY > diffY):
				newY = diffY
			# end if

			geo = QRect(newX, newY, width, height)
			self.__p_frameRoi.setGeometry(geo)
			
			print()
		# end if
		
		QWidget.mouseMoveEvent(self, event)
	# end mouseMoveEvent
	"""
	
	@pyqtSlot(int)
	def __onChanged(self, val):
		width = self.sliderWidth.editedValue()
		height = self.sliderHeight.editedValue()
		xPos = self.sliderXPos.editedValue()
		yPos = self.sliderYPos.editedValue()
		
		roi = [width, height, xPos, yPos]
		
		if (roi != self.__l_lastRoi):
			if (self.__v_emitSignal):
				self.__p_signalRoiChanged.emit(roi)
			# end if
			self.__l_lastRoi = roi
		# end if
	# end __emitChange
	
	def __onSliderChangeHeight(self, value):		
		# set current position
		self.__v_actualImageHeight = value
		self.sliderHeight.setEditedValue(value)
		
		# resize
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)
		# reinit position slider
		self.sliderYPos.reInitInteger(maxval = self.__v_maxImageHeight - self.__v_actualImageHeight)
	# end __onSliderChangeHeight
		
	def __onSliderChangeWidth(self, value):
		# set current position
		self.__v_actualImageWidth = value
		self.sliderWidth.setEditedValue(value)

		# resize		
		self.__updateROISize(self.__v_actualImageWidth,self.__v_actualImageHeight,self.__v_actualImageXPos,self.__v_actualImageYPos)

		# reinit position slider
		self.sliderXPos.reInitInteger(maxval = self.__v_maxImageWidth - self.__v_actualImageWidth)
	# end __onSliderChangeWidth

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
		self.sliderXPos.setEditedValue(new_value)
	# end __onSliderChangeXPos
	
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
		self.sliderYPos.setEditedValue(new_value)
	# end __onSliderChangeYPos
	
	def __updateROISize(self,w,h,x,y):
		x_frame = round((x / self.__v_maxImageWidth) * self.__p_frameSize.width())
		y_frame = round((y / self.__v_maxImageHeight) * self.__p_frameSize.height())
		w_frame = round((w / self.__v_maxImageWidth) * self.__p_frameSize.width())
		h_frame = round((h / self.__v_maxImageHeight) * self.__p_frameSize.height())
		
		self.frameROI.setGeometry(x_frame,y_frame,w_frame,h_frame)
	# end __updateROISize
	
	def init(self, maxWidth, maxHeight, minWidth = 0, minHeight = 0, stepWidth = 1, stepHeight = 1, stepX = 1, stepY = 1):
		# set global variables
		self.__v_maxImageWidth = maxWidth
		self.__v_maxImageHeight = maxHeight
		self.__v_actualImageYPos = 0
		self.__v_actualImageXPos = 0
		self.__v_actualImageWidth = self.__v_maxImageWidth
		self.__v_actualImageHeight = self.__v_maxImageHeight

		# init slider
		self.sliderWidth.initInteger(minWidth, maxWidth, stepWidth)
		self.sliderHeight.initInteger(minHeight, maxHeight, stepHeight)
		self.sliderXPos.initInteger(0, self.__v_maxImageWidth - self.__v_actualImageWidth, stepX)
		self.sliderYPos.initInteger(0, self.__v_maxImageHeight - self.__v_actualImageHeight, stepY)
		
		# set slider values
		self.sliderWidth.setEditedValue(self.__v_actualImageWidth)
		self.sliderHeight.setEditedValue(self.__v_actualImageHeight)
		self.sliderXPos.setEditedValue(self.__v_actualImageXPos)
		self.sliderYPos.setEditedValue(self.__v_actualImageYPos)
		
		self.__l_lastRoi = [self.__v_actualImageWidth, self.__v_actualImageHeight, self.__v_actualImageXPos, self.__v_actualImageYPos]
	# end init

	def setBackgroundImage(self,image):
		self.labelBackgroundImage.setPixmap(image)#.scaled(self.frame.size(),Qt.IgnoreAspectRatio))
	# end setBackgroundImage
	
	def setOverlayImage(self,image):
		self.labelOverlayImage.setPixmap(image)#.scaled(self.frame.size(),Qt.IgnoreAspectRatio))
		self.labelOverlayImage.setVisible(True)
	# end setBackgroundImage
	
	def enableBackgroundImage(self,enable=True):
		self.labelBackgroundImage.setVisible(enable)
	# end enableROIFrame
	
	def enableOverlayImage(self,enable=True):
		self.labelOverlayImage.setVisible(enable)
	# end enableROIFrame
	
	def enableROIFrame(self,enable=True):
		self.frameROI.setVisible(enable)
	# end enableROIFrame
	
	def setROI(self, *args):
		"""
		setROI(width, height)
		setROI(width, height, x, y)
		setROI(np.array([width, height, x, y]))
		"""
		
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
	
	def roi(self):
		return [self.__v_actualImageWidth, self.__v_actualImageHeight, self.__v_actualImageXPos, self.__v_actualImageYPos]
	# end roi()
	
# end class imageBox