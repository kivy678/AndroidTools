@echo off

echo Start Analysis %4

::				script md5 DATA_PATH lib_path
ida.exe -c -A -S"%cd%\module\ipython\%1 %2 %3" %4

echo End Processing...
::pause
exit
