import os
import subprocess

DIR = os.path.dirname(__file__)
Target = os.path.join(DIR,"main.py") 
pyinstaller = r"F:\Anaconda2\Scripts\pyinstaller.exe"
# pyinstaller = r"C:\Python27\Scripts\pyinstaller.exe"

DIR = os.path.dirname(Target)
spec_path = os.path.join(DIR,"sepc")
dist_path = os.path.join(DIR,"dist")
work_path = os.path.join(DIR,"build")
icon_path = os.path.join(DIR,"icon.ico")

cmd = '"{pyinstaller}" -D --specpath "{spec_path}" --distpath "{dist_path}" --workpath "{work_path}" "{Target}"'.format(pyinstaller=pyinstaller,spec_path=spec_path,dist_path=dist_path,work_path=work_path,Target=Target)
if os.path.exists(icon_path):
    cmd += " -i {icon_path}".format(icon_path=icon_path)

print(cmd)
subprocess.call(cmd)

# os.startfile(dist_path.replace("\\","/"))
