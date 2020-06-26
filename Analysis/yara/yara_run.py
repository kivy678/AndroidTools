# -*- coding:utf-8 -*-

import os
import glob
import yara

rules = yara.compile(filepath='dex.rule')

for dump in glob.glob(os.path.join(r'C:\tmp\dump', '*')):
	with open(dump, 'rb') as fr:
		matches = rules.match(data=fr.read())
		print(dump, matches)
