# -*- coding:utf-8 -*-

#############################################################################

import os
import sys

import difflib
import pandas as pd

from util.fsUtils import *
from util.hash import *

#############################################################################

BASE        = r'C:\tmp\data'
MOD_DIR     = Join(BASE, 'mod')
ORG_DIR     = Join(BASE, 'org')

#############################################################################

EXCEPT_FILE = ['Assembly-CSharp.csproj', 'Assembly-CSharp.sln']

#############################################################################

dict1 = dict()
set1 = set()

dict2 = dict()
set2 = set()

for path in Walk(MOD_DIR):
    dict1.update( {getSHA256(path): path} )


for path in Walk(ORG_DIR):
    dict2.update( {getSHA256(path): path} )

set1 = set(dict1.keys())
set2 = set(dict2.keys())


c = set1.symmetric_difference(set2)


COLUMNS_NAME = [
    'org',
    'mod',
]
df = pd.DataFrame(columns=COLUMNS_NAME)
df.index.name = 'file'


for i in c:
    filePath = dict1.get(i)
    if (filePath is not None) and                                   \
        (PathSplit(filePath)[1] not in EXCEPT_FILE):
        df.loc[PathSplit(filePath)[1], 'mod'] = i

    filePath = dict2.get(i)
    if (filePath is not None) and                                   \
        (PathSplit(filePath)[1] not in EXCEPT_FILE):
        df.loc[PathSplit(filePath)[1], 'org'] = i


print(df)

def differViewer(df):
    for index in df.index.tolist():

        with open(df.loc[index, 'org'], encoding="utf-8") as fr:
            text1 = fr.readlines()

        with open(df.loc[index, 'mod'], encoding="utf-8") as fr:
            text2 = fr.readlines()

        diff = difflib.unified_diff(text1, text2, fromfile='org', tofile='moding', n=2, lineterm='\n')
        sys.stdout.writelines(diff)

        print('*'*50)


#differViewer(df)

print('\n\nMain done...')
