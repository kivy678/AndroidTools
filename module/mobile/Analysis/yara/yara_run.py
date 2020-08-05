# -*- coding:utf-8 -*-

#############################################################################

import os
import glob
import yara

#############################################################################

BASE = os.path.dirname(os.path.realpath(__file__))
rules = yara.compile(filepath=os.path.join(BASE, 'str.rule'))

#############################################################################

def run(_path):
	for dump in glob.glob(_path):
		with open(dump, 'rb') as fr:
			if rules.match(data=fr.read()):
				yield dump
