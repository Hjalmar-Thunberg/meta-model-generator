'''
Given a CSV file named projects_with_uml with a list of projects with UML files in them,
mine and store these UML files using wget of extensions .xmi and .uml.
'''

import csv
import os

# Given a CSV file named projects_with_uml
with open('data/projects_with_uml.csv', 'r') as csvfile:

    os.chdir('data')
    curr_dir = os.getcwd()

    # Create extention folders and error log
    if not os.path.exists('uml'):
        os.makedirs('uml')
    if not os.path.exists('xmi'):
        os.makedirs('xmi')
    with open('error_log.txt', 'w') as f:
        f.write('')

    # Mine .xmi and .uml UML files in projects_with_uml
    for uml_files in csv.reader(csvfile):

        # Skip git eclipse HTMLs and images
        if 'https://git.eclipse.org/' in uml_files[0] or uml_files[1].endswith('.png') or uml_files[1].endswith('.gif') or uml_files[1].endswith('.jpg') or uml_files[1].endswith('.jpeg'):
            continue

        # Change to correct extention directory
        if uml_files[1].endswith('.uml'):
            os.chdir('uml')
        elif uml_files[1].endswith('.xmi'):
            os.chdir('xmi')

        # wget --timeout=seconds --tries=number -q --show-progress [input file]
        wget = ' '.join(
            ['wget', '--timeout=3', '--tries=2', '-q', '--show-progress', uml_files[1]])
        status = os.system(wget)

        # Go back to data folder
        os.chdir(curr_dir)

        # Write in error_log.txt if failed to mine current UML file
        if status != 0:
            with open('error_log.txt', 'a') as f:
                f.write(str(status) + ': ' + uml_files[1])
                f.write('\n')
