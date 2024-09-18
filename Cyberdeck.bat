@echo off

taskkill /f /im excel.exe


::dit kilt ook zichzelf... taskkill /f /im cmd.exe 

start "" "Cyberdeck Microsoft Excel.lnk" 

cd Python

::start "SerialReader" python SerialReader.py

::start "Cyberdeck-cli" python cyberdeck-cli.py

:: start "printToPDF" python printToPDF.py
::pause

start cmd /k