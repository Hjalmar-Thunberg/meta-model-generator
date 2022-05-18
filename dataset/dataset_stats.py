import os
import json

# implements a simple and efficient API for parsing and creating XML data.
from xml.etree import ElementTree as ET

def _xml_parser(file_path):
    '''
    Parses an XML file.

    Params: file path of type string.
    Return:
    - root of type object.
    - ns of type string.

    '''
    tree = ET.parse(file_path)
    root = tree.getroot()

    return tree, root

namespaces = {}
exporters = {}
types = {}
fs = 0
projects = 0

for subdir, dirs, files in os.walk('data/unfiltered_uml'):
    ns = None
    path = None
    projects+=1
    
    for file in files:

        fs+=1
        if ".gif" in file: 
            types['.gif'] = types.get('.gif', 0) + 1
        elif ".jpeg" in file:
            types['.jpeg'] = types.get('.jpeg', 0) + 1
        elif ".jpg" in file:
            types['.jpg'] = types.get('.jpg', 0) + 1
        elif ".png" in file:
            types['.png'] = types.get('.png', 0) + 1
        elif ".uml" in file:
            types['.uml'] = types.get('.uml', 0) + 1
        elif ".xmi" in file:
            types['.xmi'] = types.get('.xmi', 0) + 1


        if '.xmi' in file or '.uml' in file:
            try:
                path = subdir + "/" + file
                ns = list(dict([node for _, node in ET.iterparse(path, events=['start-ns'])]).values())[0]
                namespaces[ns] = namespaces.get(ns, 0) + 1

                tree, root = _xml_parser(path)
                for tool in root.iter():
                    if tool.tag == "XMI.exporter":
                        exporters[ns] = tool.text

            except:
                continue

print('Total files: ' + str(fs))
print('Total projects: ' + str(projects))
print('---------------------------------------------------')

print('File types: ' + str(len(types)))
print(json.dumps(types, indent=2, sort_keys=True))
print('---------------------------------------------------')

print('XML Namespaces: ' + str(len(namespaces)))
print(json.dumps(namespaces, indent=2, sort_keys=True))
print('---------------------------------------------------')

print('Proprietary tools: ' + str(len(exporters)))
print(json.dumps(exporters, indent=2, sort_keys=True))