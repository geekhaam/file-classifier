import pyuac
import os, sys, shutil

if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()

os.chdir("C:/")
os.chdir("file-classifier")
filename = 'test.txt'
src = 'C:/file-classifier/'
dir = 'C:/'

shutil.copy2(dir + filename, src + filename)
print(os.getcwd())