@echo off
set loopcount=1
:loop
echo Bot tai khoi dong lan thu %loopcount%

py bot.py

set /a loopcount=loopcount+1

goto loop
:exitloop
pause