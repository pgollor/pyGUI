##
# @file testPlotEngine.py
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
# @brief This is a tiny demo module for the global plot engine.


from abstractModuleClass import applicationModuleClass
from guiqwt.builder import make
import numpy as np
import os.path as osp


##
# @brief application module for PyGUI
class module(applicationModuleClass):

	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
	# end __init__
	
	def __onPlotCurve(self):
		x = np.arange(1000) / 1000
		
		self.curve1 = make.curve(x, np.sin(2 * np.pi * x), color="b", linestyle="DashLine")
		self.curve2 = make.curve(x, np.sin(2 * np.pi * x * 2), color="b", linestyle="DashLine")
		curve31 = make.curve(x, np.sin(2 * np.pi * x * 4), color="b", linestyle="DashLine")
		curve32 = make.curve(x, np.sin(2 * np.pi * x * 5), color="r", linestyle="DashLine")
		
		window = self._newPlotWindow("testCurvePlot")
		self.plot1 = window.addCurvePlot(title = "Sine1", curves = self.curve1, xlabel = "xlabel", ylabel = "ylabel")
		self.plot2 = window.addCurvePlot(self.curve2, title = "Sine2", position = [0, 1])
		self.plot3 = window.addCurvePlot([curve31, curve32], title = "Sine3", pos = [1, 0, 1, 2])
		
		manager = window.getManager()
		manager.synchronize_axis(self.plot1.X_BOTTOM, [id(self.plot1), id(self.plot2)])
		manager.synchronize_axis(self.plot1.Y_LEFT, [id(self.plot1), id(self.plot2)])
		
		window.show()
	# end __onPlotCurve

	def __onReplotCurve(self):
		[x, y] = self.curve2.get_data()
		self.curve2.set_data(x, y * 2)
		self.plot2.replot()

		window = self._getPlotWindow("testCurvePlot")
		window.show()
	# end __onReplotCurve
	
	def __onDeleteAllPlots(self):
		self.deletePlotWindow("testCurvePlot")
		self.deletePlotWindow("testImagePlot")
		self.deletePlotWindow("simplePlot")
	# end __onDeleteAllPlots
	
	def __onPlotImage(self):
		filename = osp.join(osp.dirname(__file__), 'brain.png')
		image = make.image(filename=filename, colormap="bone")
		data2 = np.array(image.data.T[200:], copy=True)
		image2 = make.image(data2, title="Modified", alpha_mask=True)

		window = self._newPlotWindow("testImagePlot")

		#self.plot1 = self.p_plotWindow.addImagePlot([image, image2])
		window.addImageWidget([image, image2], show_xsection=True, show_ysection=True)

		window.show()
	# end if
	
	def __onSimplePlot(self):
		x = np.arange(1000) / 1000
		y = np.sin(2 * np.pi * x)

		self._plot("simplePlot", x, y)
	# end __onSimplePlot
	
	def __onCloseAllPlots(self):
		self._closeAllPlots()
		
		self._p_logger.debug('close all plots')
	# end __onCloseAllPlots

	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		pass
	#end _initModule

	def initGUI(self):
		self.pushButtonPlotCurve.clicked.connect(self.__onPlotCurve)
		self.pushButtonPlotImage.clicked.connect(self.__onPlotImage)
		self.pushButtonReplotCurve.clicked.connect(self.__onReplotCurve)
		self.pushButtonSimplePlot.clicked.connect(self.__onSimplePlot)
		self.pushButtonCloseAllPlots.clicked.connect(self.__onCloseAllPlots)
		self.pushButtonDeleteAllPlots.clicked.connect(self.__onDeleteAllPlots)
	# end _initGUI

	# ---------- overrided functions ----------

# end class module
