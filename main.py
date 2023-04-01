import time
import PDF_read_files
import Directories
import Get_Specifications
import CSV_report


# try:

start_time = time.time()
mode = "csv"
with open('Directories.txt', 'r') as file:
    array = file.readlines()

# Directories, separate file is used to define folders for different people and not push changes for it to git
directory = array[0].rstrip()
destination_directory = array[1].rstrip()

if mode == "rebar":
    PDF_read_files.generate_bvbs(directory, destination_directory)
elif mode == "insulation_full":
    PDF_read_files.generate_total_insulation_report(directory, destination_directory, debug=False)
elif mode == "embeds":
    PDF_read_files.generate_embed_specification(directory, destination_directory, debug=False)
elif mode == "specifications":
    Get_Specifications.generate_specifications(directory, destination_directory, debug=False)
elif mode == "csv":
    CSV_report.create_csv(directory,
                          destination_directory,
                          csv_file_name='Data.csv',
                          combined=True,
                          debug_list=[""])

    # debug_list=["arrays"] to debug arrays

print(f'\nElapsed time: {round(time.time() - start_time, 1)}')

# except Exception as e:
#     print(f"Exception error: {e}")

exit = input('Press any button to exit')