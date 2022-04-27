import os
import sys

# implementation of EMF/Ecore for Python3. It’s purpose is to handle model/metamodels in Python almost the same way the Java version does.
from pyecore.ecore import *
from pyecore.resources import ResourceSet, URI

# implements a simple and efficient API for parsing and creating XML data.
from xml.etree import ElementTree as ET


def _compare_dicts(dict1: dict, dict2: dict):
    '''
    Compare dictionaries and look for identical keys with values of identical keys.

    Params: dictionaries with nested dictionaries
    Return: False if match or no values, else True
    '''
    for key, value in dict1.items():
        if key == list(dict2.keys())[0] and \
                value.keys() == dict2[list(dict2.keys())[0]].keys():

            return False

    return True

# TODO: change in code so it uses this function


def _format_parent_tag(tag: str, ns: str) -> str:
    return tag.replace('{', '').split(ns + '}')[-1]

# TODO: fix comments


def _create_classes(tree, root: object, ns: str):
    '''
    Create Ecore classes.

    Params: ElementTree of type object
    Return: Ecore class of type object
    '''
    model = {}
    exist = {}

    for Class in list(root.iter()):
        if ns in str(Class) and Class.attrib and\
                _compare_dicts(exist, {Class.tag: Class.attrib}):
            meta_class = _create_attributes(EClass(
                Class.tag.replace(
                    '{', '').split(
                        ns + '}')[-1]), Class)

            model[Class] = meta_class
            exist[Class.tag] = Class.attrib

    return _create_references(tree, model)

# TODO: add defaultValueLiteral= to bools


def _create_attributes(ecore_class: object, Class: object):
    '''
    Create Ecore attributes to Ecore class.

    Params: Ecore class and ElementTree of type object
    Return: Ecore class of type object
    '''
    for attr, type in Class.attrib.items():
        ecore_class.eStructuralFeatures.append(
            EAttribute(
                attr, _get_type(type)))

    return ecore_class

# TODO: fix comments


def _create_references(tree, model):
    '''
    Create Ecore references.

    Params:
    Return: Ecore reference of type object.
    '''
    for parent in tree.iter():
        if ns in str(parent) and parent.attrib:
            for key, value in model.items():
                if key == parent:
                    for child in parent.findall(('.*')):
                        if ns in str(child):
                            for grandchild in child.findall('.*'):
                                if ns in str(grandchild):
                                    for k, v in model.items():
                                        if k == grandchild:
                                            value.eStructuralFeatures.append(EReference(child.tag.replace(
                                                '{', '').split(ns + '}')[-1].lower(), v, upper=-1, lower=1, containment=True))

    return list(model.values())


def _create_meta_model(model: list, file_name: str):
    '''
    Create Ecore package as Ecore meta-model.

    Params: list of Ecore objects.
    Return: Ecore schema of type object.
    '''
    ecore_schema = EPackage(
        file_name, nsURI='http://www.example.org/' + file_name, nsPrefix=file_name)
    ecore_schema.eClassifiers.extend(model)

    return ecore_schema


def _get_params():
    '''
    Get argument parameter, exit if none.

    Params: None
    Return: file_path and file_name of type string
    '''
    if len(sys.argv) != 2:
        sys.exit('Missing file path')

    file_path = sys.argv[1]
    file_name = os.path.basename(
        file_path).rsplit(
            '.', 1)[0]

    return file_path, file_name


def _get_type(type: str):
    '''
    Get and convert type to Ecore DataType standard.

    Params: attribute type of type string
    Return: EBoolean or Estring of type object
    '''
    switcher = {
        'false': EBoolean,
        'true': EBoolean,
    }
    return switcher.get(type, EString)


def _save_resource(ecore_schema: object, file_path: str, file_name: str):
    '''
    Save meta-model as .ecore file at file path location.

    Params:
    - ecore schema of type object.
    - file path of type string.
    -file name of type string.
    Return: Save message of type string.
    '''

    os.chdir(file_path)

    rset = ResourceSet()
    resource = rset.create_resource(
        URI(file_name + '.test.ecore'))
    resource.append(ecore_schema)
    resource.save()

    return 'saved meta-model at ' + file_path + ' as ' + file_name + '.ecore'


def _xml_parser(file_path: str):
    '''
    Parses an XML file.

    Params: file path of type string.
    Return:
    - root of type object.
    - ns of type string.

    '''
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = list(dict([node for _, node in ET.iterparse(
        file_path, events=['start-ns'])]).values())[0]

    return tree, root, ns


'''
Parses a file written in xml format (.xml, .xmi, .uml...), generates corresponding meta-model
file for Eclipse Modeling Framework (EMF) in .ecore format and save at file path location.

Prerequisites: pyecore (https://github.com/pyecore/pyecore)

Parameters: UML file path of type string.
Returns: None
'''
file_path, file_name = _get_params()
tree, root, ns = _xml_parser(file_path)
model = _create_classes(tree, root, ns)
ecore_schema = _create_meta_model(model, file_name)
message = _save_resource(ecore_schema, file_path.rsplit('/', 1)[0], file_name)

sys.exit(message)
