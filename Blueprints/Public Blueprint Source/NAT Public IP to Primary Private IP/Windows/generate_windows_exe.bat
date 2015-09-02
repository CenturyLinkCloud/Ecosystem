@echo off

copy ..\noarch\clc_api_nat_ip.py .
c:\python27\scripts\pyinstaller.exe --noconfirm --clean --onefile clc_api_nat_ip.spec
del clc_api_nat_ip.py
move dist\clc_api_nat_ip.exe .
rmdir /S /Q build
rmdir /S /Q dist


