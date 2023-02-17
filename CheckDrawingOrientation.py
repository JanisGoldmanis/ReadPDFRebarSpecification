import Directories
import os
import fitz

directory = Directories.directory

def get_file_names(directory_path):
    """
    USED!
    Gets all files in a directory
    :param directory_path:
    :return:
    """
    filename_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filename_list.append(filename)
    return filename_list

file_names = get_file_names(directory)
bad_files = []
number = 0
for file_name in file_names:
    print(number,file_name)
    file_path = os.path.join(directory, file_name)
    doc = fitz.open(file_path)
    page = doc[0]
    pix = page.get_pixmap()
    if pix.h > pix.w:
        print(file_name)
        bad_files.append(file_name)
    number += 1

print()
print('Result')
for file_name in bad_files:
    print(file_name)

