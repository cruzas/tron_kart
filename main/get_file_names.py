"""
Get name of files/folders in a certain directory with a certain pattern.

@author: Nelson Dos Santos
"""

import os

def get_file_names(path, pattern, t=1):
    """t represents the position in the file name where to search pattern:
0 = if the file name starts with 'pattern';
1 = if 'pattern' is at the end;
2 = 'pattern' is in the name of the file
"""
    file_names = [] # will hold eventually the files name (in path) that contain 'pattern'
    for file in os.listdir(path):
            if t == 0:
                if file.startswith(pattern):
                    file_names.append(file)
            if t == 1:
                if file.endswith(pattern):
                    file_names.append(file)
            if t == 2:
                if pattern in file:
                    file_names.append(file)
    return file_names
#

# Define here the path to the folder and the pattern 
##path = "sounds/"
##pattern = ".mp3"
##
##def test():
##    fnames = get_file_names(path, pattern)
##    print(fnames)
###
##
##test()
