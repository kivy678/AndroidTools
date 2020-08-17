# -*- coding:utf-8 -*-

#############################################################################

import os
from util.fsUtils import *

from module.mobile.cmd import shell

#############################################################################

BASE                = r'C:\tmp\data'
DECODE_DIR          = Join(BASE, 'mod')

APP_DIR             = Join(BASE, 'grow-castle-mod_1.24.2')
global_metadata     = Join(APP_DIR, r'assets\bin\Data\Managed\Metadata\global-metadata.dat')
il2cpp_so           = Join(APP_DIR, r'lib\armeabi-v7a\libil2cpp.so')


#justdcm = r'C:\Program Files (x86)\Progress\JustDecompile\Libraries\JustDecompile.exe'
#cmd = f'{justdcm} /lang:csharp /out:out /target:Assembly-CSharp.dll'

cppdmp = r'C:\Users\shw\Desktop\tool\game\Il2CppDumper-v6.4.4\Il2CppDumper.exe'
cmd = f'{cppdmp} {il2cpp_so} {global_metadata} {DECODE_DIR}'

#############################################################################

shell.runCommand(cmd)

#############################################################################

print('\n\nMain done...')
