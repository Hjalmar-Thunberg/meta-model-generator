'''
Parses a file written in xml format (.xml, .xmi, .uml...) and generates a
meta-model file to be used with Eclipse Modeling Framework which uses Ecore format.

Prerequisites:
- pyecore

Usage:
filepath given as an argument with the minimum required information:
- classes with names
    - attributes with names and datatype
- (mapped datatypes)
'''

import os
import sys
# implementation of EMF/Ecore for Python3. It’s purpose is to handle model/metamodels in Python almost the same way the Java version does.
from pyecore.ecore import EClass, EDataType, EAttribute, EString, EObject, EInt, EChar, EBoolean, EFloat, EDouble, EShort, ELong
# implements a simple and efficient API for parsing and creating XML data.
from xml.etree import ElementTree as ET


def search_file(keyword):
    '''
    Searches after given keyword in file.

    Parameters: 
    -keyword: string

    Returns: keys and values of type string.
    '''
    dictionary = {}

    for child in root.findall(keyword):
        dictionary[child.attrib['xmi.id']] = child.attrib['name']
    return dictionary


def compare_dictionary(dictionary, attribute):
    '''
    Compares a given dictionary and attribute.

    Paramters: 
    - dictionary: keys and values of type string
    - attribute: string

    Returns: datatype value of type string.
    '''
    for key in dictionary.keys():
        # replace to usable name (e.g. 'lSVt6HPao6WE' -> 'int')
        if attribute.attrib['type'] in key:
            return dictionary.get(key)


def translate_datatype(datatype):
    '''
    Translates given datatype name to Ecore standard.

    Parameters:
    - datatype: string

    Returns: datatype name of type string.
    '''
    switcher = {
        'int': EInt,
        'char': EChar,
        'bool': EBoolean,
        'float': EFloat,
        'double': EDouble,
        'short': EShort,
        'long': ELong,
        'string': EString
    }
    return switcher.get(datatype, None)


def create_meta_class(classes, attributes, dict1=None, dict2=None):
    '''
    Creates meta-class with attributes and references.

    Parameters: 
    - classes: string
    - attributes: string
    - (optional) dict1: keys and values of type string
    - (optional) dict2: keys and values of type string

    Returns: 
    '''
    for uml_class in root.findall(classes):
        meta_class = EClass(
            uml_class.attrib['name'])  # create meta-class
        print(uml_class.attrib['name'])

        # find all class attributes
        for attribute in uml_class.findall(attributes):
            # look for matching datatype if needed, replace if found
            if dict1:
                datatype = translate_datatype(
                    compare_dictionary(dict1, attribute))
            # look for matching custom datatype if needed, replace if found
            if not datatype and dict2:
                datatype = EDataType(compare_dictionary(dict2, attribute))

            print(datatype)
            print(type(datatype))
            meta_class.eStructuralFeatures.append(
                EAttribute(attribute.attrib['name'], datatype))


# check if a filepath argument is included
if len(sys.argv) != 2:
    sys.exit('Missing file path')

file_path = sys.argv[1]
file_name = os.path.basename(file_path).rsplit('.', 1)[0]

# try parsing the file
# try:
tree = ET.parse(file_path)
root = tree.getroot()

#  namespace of http://schema.omg.org/spec/UML/1.3.
if root.tag == 'XMI':
    print('parsing ' + file_name + ' of type OMG')

    # find and store all datatypes and custom datatypes(classes) in dictionaries ({'xmi.id': ''name'...})
    datatypes = search_file(
        './/{http://schema.omg.org/spec/UML/1.3}DataType')
    c_datatypes = search_file(
        './/{http://schema.omg.org/spec/UML/1.3}Class')

    # create metaclasses with attributes and references, use given dictionaries to feed a correct datatype
    create_meta_class('.//{http://schema.omg.org/spec/UML/1.3}Class',
                      './/{http://schema.omg.org/spec/UML/1.3}Attribute', datatypes, c_datatypes)

# namespace of http://www.staruml.com.
elif root.tag == '{http://www.staruml.com}PROJECT':
    print('parsing ' + file_name + ' of type StarUML')

# namespace of http://schemas.microsoft.com/dsltools/ModelStore
elif root.tag == '{http://schemas.microsoft.com/dsltools/ModelStore}modelStoreModel':
    print('parsing ' + file_name + ' of type Microsoft')

# unsupported namespaces
else:
    print(root.tag + ' is not supported')

# except:
    print('error when parsing file')
