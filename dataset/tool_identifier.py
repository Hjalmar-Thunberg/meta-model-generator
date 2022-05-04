import os
import json

# implements a simple and efficient API for parsing and creating XML data.
from xml.etree import ElementTree as ET

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

    return tree, root

'''
Loops through every uml file in the directory and finds how many times each namespace occurrs.

Params: None.
Return: None.
'''


directory = 'data/unfiltered_uml'
stats = {}
ns = None

for subdir, dirs, files in os.walk(directory):
    ns = None
    for file in files:
        if '.xmi' in file or '.uml' in file:
            try:
                path = subdir + "\\" + file
                tree, root = _xml_parser(path)
                
                ns = list(dict([node for _, node in ET.iterparse(
                      path, events=['start-ns'])]).values())[0]
                for tool in root.iter():
                    if tool.tag == "XMI.exporter" and tool.text == "convertMondrianToCwm":
                        print(path)
                        stats[tool.text] = stats.get(tool.text, 0) + 1
                        #stats[tool.text] = ns

                #if ns == "org.omg/standards/UML":
                #    print(path)
            except:
                break

#    if ns:
#        stats[ns] = stats.get(ns, 0) + 1

print(json.dumps(stats, indent=4, sort_keys=True))