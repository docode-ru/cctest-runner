#!/usr/bin/env python
import os
import shutil
import re
import argparse

def change_content(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        in_function = False
        for line in lines:
            if re.match(r'^\s*def\s', line):    # If the line starts with 'def', it's the start of a function
                in_function = True
            elif re.match(r'^\s*print', line): # If the line starts with 'print', it's a print statement
                continue
            elif in_function and line.strip() == '':  # If the line is empty, it's the end of a function
                in_function = False
            elif not in_function:
                file.write(line)

def copy_and_change(src_directory, dest_directory):
    # Copy the source directory to the destination directory
    shutil.copytree(src_directory, dest_directory)

    # Change the content of the copied files
    for root, dirs, files in os.walk(dest_directory):
        for file in files:
            file_path = os.path.join(root, file)
            change_content(file_path)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Copy files from a source directory to a destination directory and change their content.')

# Add arguments for the source and destination directories
parser.add_argument('src_directory', type=str, help='the source directory')
parser.add_argument('dest_directory', type=str, help='the destination directory')

# Parse the command line arguments
args = parser.parse_args()

# Copy and change the files
copy_and_change(args.src_directory, args.dest_directory)