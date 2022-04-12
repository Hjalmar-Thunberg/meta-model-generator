'''
'''

from distutils.log import error
import os
import sys
import pyecore.ecore as Ecore
from xml.etree import ElementTree as ET

# check if a filepath argument is included
if len(sys.argv) != 2:
    sys.exit('Missing file path')

file_path = sys.argv[1]
file_name = os.path.basename(file_path).rsplit('.', 1)[0]

# try parsing the given file
try:
    tree = ET.parse(file_path)
    root = tree.getroot()

    datatypes = {}
    classes = {}

    # namespace of http://schema.omg.org/spec/UML/1.3
    if root.tag == 'XMI':
        print('parsing ' + file_name + ' of type OMG')

    # namespace of http://www.staruml.com
    elif root.tag == '{http://www.staruml.com}PROJECT':
        print('parsing ' + file_name + ' of type StarUML')

    # namespace of http://schemas.microsoft.com/dsltools/ModelStore
    elif root.tag == '{http://schemas.microsoft.com/dsltools/ModelStore}modelStoreModel':
        print('parsing ' + file_name + ' of type Microsoft')

    # unsupported namespaces
    else:
        print(root.tag + ' is not supported')

except:
    print('error when parsing file')
