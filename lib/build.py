import os  
from os import path
from shutil import copyfile

def properties():
    modulePath = path.abspath(path.dirname(__file__))
    if not path.isfile(modulePath+'/hanlp-1.3.2/hanlp.properties'):
        copyfile(modulePath+'/hanlp-1.3.2/hanlp.default.properties', modulePath+'/hanlp-1.3.2/hanlp.properties')
        with open(modulePath+'/hanlp-1.3.2/hanlp.properties', 'r+') as file:
            properties = file.read()
            file.seek(0)
            file.truncate()
            file.write(properties.replace('root=/hanlp/lib/hanlp-1.3.2', 'root='+modulePath+'/hanlp-1.3.2/'))
            print('Create hanlp.properties in '+modulePath+'/hanlp-1.3.2/')