'''
Given a CSV file named projects_with_uml with a list of projects with UML files in them,
mine and store these UML files using wget of desired extensions.

Prerequisites:
- wget
- tqdm
'''

import csv
import os
from tqdm import tqdm

already = []

# Count lines in projects_with_uml.csv
with open('data/projects_with_uml.csv', 'r') as csvfile:
    lines = len(csvfile.readlines())

# Given a CSV file named projects_with_uml.csv
with open('data/projects_with_uml.csv', 'r') as csvfile:

    # Create dataset directory and save path
    os.chdir('data')
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    os.chdir('dataset')
    dataset_dir = os.getcwd()

    # Create new/ clear existing error log
    with open('error_log.txt', 'w') as f:
        f.write('')

    # Mine desired UML files from projects_with_uml.csv, displayed with a progress bar
    for uml_files in tqdm(csv.reader(csvfile), total=lines, position=0, leave=True):

        # Add project name to progressbar
        project_name = str(uml_files[0].split("/")[1])
        if not project_name:
            project_name = 'other'

        # Skip already mined projects and projects from eclipse
        if uml_files[1] not in already and 'https://git.eclipse.org/' not in uml_files[0]:

            # Create project directory
            if not os.path.exists(project_name):
                os.makedirs(project_name)
            os.chdir(project_name)

            # wget --timeout=seconds --tries=number -q [input file]
            wget = ' '.join(
                ['wget', '--timeout=3', '--tries=2', '-q', '--show-progress', uml_files[1].replace(' ', '_')])
            status = os.system(wget)

            # Go back to data folder
            os.chdir(dataset_dir)

            already.append(uml_files[1])

            # Write in error_log.txt if failed to mine current UML file
            if status != 0:
                with open('error_log.txt', 'a') as f:
                    f.write(str(status) + ': ' + uml_files[1])
                    f.write('\n')

    # Remove empty folders
    for entry in os.scandir(dataset_dir):
        if len(os.listdir(entry)) == 0:
            os.rmdir(entry)
