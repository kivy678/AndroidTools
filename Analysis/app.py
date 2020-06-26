# -*- coding:utf-8 -*-

###########################################################################################

from util.parser import *
from common.singleton import Singleton

###########################################################################################

class APP_INFOR(Singleton):

	def __init__(self):
		super().__init__()

		self._pkgName = None
		self._applicatopmActivity = None
		self.ManifestJson = None
		
		self.pid = None
		self.tpid = None


	def parser(self, p):
		if isinstance(p, XmlParser):
			self._pkgName = p.parser('manifest', 'package')
			self._applicatopmActivity = p.parser('application', 'android:name')

		elif isinstance(p, JsonParser):
			self._ManifestJson = p.parser()

	@property
	def pkgName(self):
		return self._pkgName


	@pkgName.setter
	def pkgName(self, pkgName):
		self._pkgName = pkgName

