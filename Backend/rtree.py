import os
from os import listdir
from os.path import isfile, join
mypath = '/Users/fabriziovasquez/Downloads/DB2/Proyecto03/ProyectoIIIBaseDeDatosII/Resources/lfw'

onlyfiles = [f for f in listdir(mypath)]

for path, subdirs, files in os.walk(mypath):
    for name in files:
        print(os.path.join(path, name))

def upload():
    print(onlyfiles)

#upload()






