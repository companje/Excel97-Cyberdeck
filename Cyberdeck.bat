@echo off

start "" "Cyberdeck Microsoft Excel.lnk" 

cd Python

start "SerialReader" python SerialReader.py

start "Cyberdeck-cli" python cyberdeck-cli.py

   