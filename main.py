import time
import PDF_read_files
import Directories

start_time = time.time()

# Directories, separate file is used to define folders for different people and not push changes for it to git
directory = Directories.directory
destination_directory = Directories.destination_directory

PDF_read_files.generate_bvbs(directory, destination_directory)

print(f'\nElapsed time: {round(time.time() - start_time, 1)}')
