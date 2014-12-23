
#
# Build base directory structure
#
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker"
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker\etc"
New-Item -ItemType Directory -Force -Path $env:programfiles"\bpbroker\lib"


#
# Copy pthon27 binaries into our directory
#
Copy-Item "Python27" $env:programfiles"\bpbroker\" -Recurse -Force

$bpbroker_dir = "$env:programfiles\bpbroker"
$python = "$env:programfiles\bpbroker\Python27\python.exe"
$scripts_dir = "$bpbroker_dir\Python27\Scripts"
$pip = "$scripts_dir\pip.exe"


#
# Install python packages
#
&$python "$pip" install --upgrade bpbroker


#
# Register bpbroker 
#

