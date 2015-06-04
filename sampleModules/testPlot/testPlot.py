## @file testPlot.py
#
# @date 17.03.2014
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
# @brief This is a demo module to demonstrate the global plot handling.


from abstractModuleClass import applicationModuleClass
from customDialogs import QDialogPlot
import numpy as np


class module(applicationModuleClass):
	# ---------- Private ----------

	def __init__(self, parent, name):
		applicationModuleClass.__init__(self, parent, name)
		
		self.__p_dialog = False
		
		self.setDisplayName('testPlot')
	# end __init__

	def __onPlotSample1(self):
		self.__p_dialog.show()
		
		# create data
		data = [np.random.random() for i in range(100)]
		
		# create figure and get axis from plot
		ax = self.__p_dialog.figure.add_subplot(111)
		
		# don't hold - plot new data
		ax.hold(False)
		
		# plot data
		ax.plot(data)
		self.__p_dialog.canvas.draw()
	# end __onPlotSample1
	
	def __onPlotSample2(self):
		# create data
		data = [np.random.random() for i in range(10)]
		
		self.__p_dialog.primitivePlot(data)
	# end __onPlotSample2
	
	def __onPlotSample3(self):
		self.__p_dialog.show()
		self.__p_dialog.figure.clear()
		ax = self.__p_dialog.figure.add_subplot(111)
		
		ax.hold(True)
		for j in range(2):
			data = [np.random.random() for i in range(10)]
			ax.plot(data)
		ax.hold(False)
		
		self.__p_dialog.canvas.draw()
	# end __onPlotSample3
	
	def __onPlotSample4(self):
		# create data
		data = [1,1,2,3,2,1]
		
		self.__p_dialog.primitivePlot(range(0,12,2), data)
	# end __onPlotSample4
	
	# ---------- Private ----------


	# ---------- overrided functions ----------

	def initModule(self):
		pass
		#print(self._l_customSettings)
		# to add some custom settings
		#self._l_customSettings["blubb"].append({'test': 123})
	#end _initModule

	def initGUI(self):
		self.pushButtonPlotSample1.clicked.connect(self.__onPlotSample1)
		self.pushButtonPlotSample2.clicked.connect(self.__onPlotSample2)
		self.pushButtonPlotSample3.clicked.connect(self.__onPlotSample3)
		self.pushButtonPlotSample4.clicked.connect(self.__onPlotSample4)
		
		self.__p_dialog = QDialogPlot(self._getParent())
		#self.__p_dialog.setGeometry(100,100,100,100)
	# end _initGUI
	
	def onClose(self):
		self.__p_dialog = False
	# end onClose

	# ---------- overrided functions ----------

# end class module
