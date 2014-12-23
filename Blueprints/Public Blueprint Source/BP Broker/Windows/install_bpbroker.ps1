
$python_zip = "python-2.7.9.zip"



$script_path = split-path -parent $MyInvocation.MyCommand.Definition
$bpbroker_dir = "$env:programfiles\bpbroker"
$python = "$env:programfiles\bpbroker\Python27\python.exe"
$scripts_dir = "$bpbroker_dir\Python27\Scripts"
$pip = "$scripts_dir\pip.exe"


#
# Build base directory structure
#
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker"
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker\etc"
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker\lib"


#
# Unzip and Copy python27 binaries into our directory
#
if (Test-Path  ("$bpbroker_dir\Python27"))  { Remove-Item -Recurse -Force "$bpbroker_dir\Python27" }
$helper = New-Object -ComObject Shell.Application
$files = $helper.NameSpace("$script_path\$python_zip").Items()
$helper.NameSpace($bpbroker_dir).CopyHere($files)


#
# Install python packages
#
&$python "$pip" install --upgrade bpbroker


#
# Configure shortcuts
#
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$bpbroker_dir\bpbroker.lnk")
$Shortcut.TargetPath = "$scripts_dir\bpbroker.exe"
$Shortcut.Save()
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$bpbroker_dir\bpclient.lnk")
$Shortcut.TargetPath = "$scripts_dir\bpclient.exe"
$Shortcut.Save()
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$bpbroker_dir\bpmailer.lnk")
$Shortcut.TargetPath = "$scripts_dir\bpmailer.exe"
$Shortcut.Save()

