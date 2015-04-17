##
# @file plotEngine.py
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


from guiqwt.plot import PlotManager, ImageWidget
from guiqwt.curve import CurvePlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QIcon, QToolButton, QGridLayout, QWidget, QMainWindow
from guiqwt.image import ImagePlot
from guiqwt.signals import (SIG_PLOT_AXIS_CHANGED)



class noneBugCurvePlot(CurvePlot):
	def __init__(self, *args, **kwargs):
		CurvePlot.__init__(self, *args, **kwargs)
	# end __init__
	
	def do_zoom_rect_view(self, start, end):
		CurvePlot.do_zoom_rect_view(self, start, end)
		self.emit(SIG_PLOT_AXIS_CHANGED, self)
	# end do_zoom_rect_view
	
	def do_autoscale(self, replot=True):
		CurvePlot.do_autoscale(self, replot=replot)
		self.emit(SIG_PLOT_AXIS_CHANGED, self)
# end class noneBugCurvePlot


class plotWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		QMainWindow.__init__(self, *args, **kwargs)
		
		self.__initVars()
		
		# init self
		geo = self.geometry()
		geo.setWidth(800)
		geo.setHeight(600)
		geo.setX(100)
		geo.setY(100)
		self.setGeometry(geo)
		
		self.setWindowTitle("plot window")
		
		self.__initLayout()
	# end __init__
	
	def __del__(self):
		if (self.__p_manager):
			del self.__p_manager
		# end if
		
		self.__initVars()
	# end __del__
	
	def __initVars(self):
		self.__p_manager = False
		self.__p_toolbar = False
		self.__p_resizeButton = False
		self.__l_layoutChilds = []
		self.__v_wasInitialized = False
	# end __initVars
	
	def __initLayout(self):
		# layout
		layout = QGridLayout()
		central_widget = QWidget(self)
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)
		
		# create plot manager
		self.__p_manager = PlotManager(self)
		
		# toolbar
		if (self.__p_toolbar):
			self.__p_toolbar.clear()
		else:
			self.__p_toolbar = self.addToolBar("tools")
		# end if
		
		# resize button
		icon = QIcon("icons/center.png")
		button = QToolButton()
		button.setIcon(icon)
		button.setToolTip("Resize")
		self.connect(button, SIGNAL("clicked()"), self.__onAutoScale)
		
		self.__p_manager.add_toolbar(self.__p_toolbar, id(self.__p_toolbar))
		self.__p_toolbar.addWidget(button)
		self.__v_wasInitialized = True
	# end __initManager
	
	def reInit(self):
		for plot in self.__l_layoutChilds:
			self.centralWidget().layout().removeWidget(plot)
			del plot
		# end if
		self.__l_layoutChilds = []
		
		# layout
		oldLayout = self.centralWidget().layout()
		del oldLayout

		if (self.__p_manager):
			del self.__p_manager
			self.__p_manager = False
		# end if
		
		self.__initLayout()
	# end reInit
	
	def addCurvePlot(self, curves, *args, **kwargs):
		return self.__addPlot(curves, noneBugCurvePlot, *args, **kwargs)
	# end addCurvePlot
	
	def addImagePlot(self, images, *args, **kwargs):
		return self.__addPlot(images, ImagePlot, *args, **kwargs)
	# end addImagePlot
	
	def addImageWidget(self, images, *args, **kwargs):
		widget = ImageWidget(self, *args, **kwargs)
		plot = widget.get_plot()
		
		if (images.__class__ is not list):
			plot.add_item(images)
		else:
			for image in images:
				plot.add_item(image)
			# end for
		# end if
		
		self.centralWidget().layout().addWidget(widget)
		
		self.__l_layoutChilds.append(widget)
		
		return widget
	# end addImageWidget
	
	def getManager(self):
		return self.__p_manager
	# end getManager
	
	def __addPlot(self, dataList, plotClass, *args, **kwargs):
		"""
		pos[0]: row
		pos[1]: column
		pos[2]: rowspan 
		pos[3]: columnspan
		"""
		pos = []
		if ('position' in kwargs):
			pos = kwargs.pop('position')
		# end if
		if ('pos' in kwargs):
			pos = kwargs.pop('pos')
		# end if

		plot = plotClass(self, *args, **kwargs)
		
		if (dataList.__class__ is not list):
			plot.add_item(dataList)
		else:
			for data in dataList:
				plot.add_item(data)
			# end for
		# end if
		
		self.__registerPlot(plot, pos)
		
		return plot
	# end __addPlot
	
	def __registerPlot(self, plot, pos):
		# check for position
		if (pos != []):
			if (len(pos) == 2):
				pos.append(1) # rowspan
				pos.append(1) # columnspan
			# end if

			self.centralWidget().layout().addWidget(plot, pos[0], pos[1], pos[2], pos[3])
		else:
			self.centralWidget().layout().addWidget(plot)
		# end if
		self.__l_layoutChilds.append(plot)

		self.__p_manager.add_plot(plot)
	# end __registerPLot
	
	def show(self, *args, **kwargs):
		if (self.__v_wasInitialized):
			self.__p_manager.register_all_curve_tools()
			self.__v_wasInitialized = False
		# end if
		
		QMainWindow.show(self, *args, **kwargs)
	# end show
	
	def showEvent(self, event):
		# emit signal	
		self.emit(SIGNAL("onShow()"))
		
		# execute not overloaded showEvent
		QMainWindow.showEvent(self, event)
	# end showEvent

	def closeEvent(self, event):
		# emit signal
		self.emit(SIGNAL("onClose()"))
		
		# execute not overloaded closeEvent
		QMainWindow.closeEvent(self, event)
	# end closeEvent
	
	def __onAutoScale(self):
		plot = self.__p_manager.get_active_plot()
		plot.do_autoscale(True)
	# end __onAutoScale
	
# end class plotWindow

