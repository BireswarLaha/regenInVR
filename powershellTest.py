import subprocess, sys

#ref: https://stackoverflow.com/questions/14508809/run-powershell-function-from-python-script
subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". \"./hello_world.ps1\";"], stdout=sys.stdout)

#https://stackoverflow.com/questions/21944895/running-powershell-script-within-python-script-how-to-make-python-print-the-pow
p = subprocess.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". \"./hello_world1.ps1\";"], stdout=sys.stdout)
p.communicate()
