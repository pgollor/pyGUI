##
# @file changeDir.py
# 
# @date 17.09.2013
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


import os


class changeDir():
	__v_startPath = ""

	# ---------- Private ----------

	def __init__(self, path = ""):
		self.__v_startPath = os.path.abspath(os.curdir)
		if (path != ""):
			self.changePath(path)
		# end if
	# end __init__

	def __del__(self):
		self.changeBack()
	# end __del__

	# ---------- Private ----------


	# ---------- Public ----------

	def changePath(self, path):
		os.chdir(path)
	# end changePath

	def changeBack(self):
		if (self.__v_startPath != ""):
			os.chdir(self.__v_startPath)
			self.__v_startPath = ""
		# end if
	#end changeBack

	# ---------- Public ----------

#end class changeDir