# -*- coding:utf-8 -*-

#############################################################################

import os
import glob
import yara

#############################################################################

BASE = os.path.dirname(os.path.realpath(__file__))
rules = yara.compile(filepath=os.path.join(BASE, 'str.rule'))

#############################################################################

for dump in glob.glob(os.path.join(r'C:\tmp\dump', '*')):
	with open(dump, 'rb') as fr:
		if rules.match(data=fr.read()):
			print(dump)
