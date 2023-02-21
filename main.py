import time
import PDF_read_files
import Directories
import Get_Specifications

start_time = time.time()

mode = "rebar"

# Directories, separate file is used to define folders for different people and not push changes for it to git
directory = Directories.directory
destination_directory = Directories.destination_directory

if mode == "rebar":
    PDF_read_files.generate_bvbs(directory, destination_directory)
elif mode == "insulation_full":
    PDF_read_files.generate_total_insulation_report(directory, destination_directory, debug=False)
elif mode == "embeds":
    PDF_read_files.generate_embed_specification(directory, destination_directory, debug=False)
elif mode == "specifications":
    Get_Specifications.generate_specifications(directory, destination_directory, debug=False)


print(f'\nElapsed time: {round(time.time() - start_time, 1)}')
