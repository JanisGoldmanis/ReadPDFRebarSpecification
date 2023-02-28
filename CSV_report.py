import Calculate_insulation
import PDF_read_files
import Arrays
import os
import csv


def write_csv(file_name, arrays, combined, csv_file_name):
    drawing_name = file_name
    if not combined:
        if "Rev" in file_name:
            file_name = file_name[:-10] + ".csv"
        else:
            file_name = file_name[:-4] + ".csv"
    else:
        file_name = csv_file_name

    # Check if file exists
    file_exists = os.path.isfile(file_name)

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';')

        if not file_exists:
            writer.writerow(['Type',
                             'GUID',
                             'Floor',
                             'Element name',
                             'Revision',
                             'Revision date',
                             'Revision description',
                             'Number of elements',
                             'Production height H (mm)',
                             'Production length L (mm)',
                             'Production width P (mm)',
                             'Assembly height H (mm)',
                             'Assembly length L (mm)',
                             'Assembly width P (mm)',
                             'Concrete (m3)',
                             'Element weight (t)',
                             'Net area (m2)',
                             'Gross area (m2)',
                             'Reinforcement weight, kg',
                             'Reinforcement weight on m2, kg',
                             'Drawn by',
                             'Date',
                             'Concrete class',
                             'Water/Cement ratio',
                             'Surface Type Mold/Corrosivity prot.',
                             'Surface tr. class Mold',
                             'Tolerance class Mold',
                             'Surface Type Other',
                             'Surface tr. class Other',
                             'Tolerance class Other',
                             'Surface Type Openings',
                             'Surface tr. class Openings',
                             'Tolerance class Openings',
                             'Phase',
                             'Class',
                             'ID Name',
                             'ID Assembly',
                             'Profile',
                             'Execution class',
                             'ID Quantity',
                             'ID Material',
                             'ID Fabricator',
                             'ID Weight (kg)',
                             'ID Length (mm)',
                             'ID Volume (m3)',
                             'Rebar size (mm)',
                             'Rebar weight (kg)',
                             'Mesh quantity',
                             'Mesh size (mm)',
                             'Mesh weight (kg)',
                             'Strand diameter (upper)',
                             'Strand quantity (upper)',
                             'Strand stress (upper)',
                             'Strand diameter (lower)',
                             'Strand quantity (lower)',
                             'Strand stress (lower)',
                             'Reinforcement class',
                             'Strand lenght (mm)',
                             'Strand weight (kg)',
                             '3D Model status',
                             'Drawing status',
                             'Correction/Change status',
                             'Locked',
                             'Rotation',
                             'Crane',
                             'Nominal thickness (mm)',
                             'LOD',
                             'Version'])

        # Write the header row
        # for array in arrays:
        #     if array is None:
        #         continue
        #     for row in array:
        #         writer.writerow(row)

        if "Rev" in file_name:
            name = drawing_name[:-10]
        else:
            name = drawing_name[:-4]
        writer.writerow(['', '', '', name])

        if arrays[3] != None:
            insulation_thickness_dict = Calculate_insulation.generate_dict_of_volume_by_thickness(arrays[3])

            insulation_totals = []
            for key in sorted(insulation_thickness_dict.keys()):
                volumes = insulation_thickness_dict[key]
                key = round(key, 1)
                suggested_volume = round(volumes[0] / (10 ** 9), 2)
                actual_volume = round(volumes[1] / (10 ** 9), 2)
                insulation_totals.append([f'INSULATION h={round(key)}', '', round(key), '', '', 'MINERAL WOOL-HARD', 'Frontrock S', '', '',suggested_volume, actual_volume])

            for line in insulation_totals:
                writer.writerow(line)

        if arrays[1] != None:
            for line in arrays[1]:
                writer.writerow(line)



def create_csv(source_directory, destination_directory, csv_file_name='', combined=False, debug_list=None):
    if debug_list is None:
        debug_list = []

    file_names = PDF_read_files.get_file_names(source_directory)

    for file_name in file_names:
        file_path = os.path.join(source_directory, file_name)
        arrays = Arrays.get_arrays(file_path, debug_list)
        write_csv(file_name, arrays, combined, csv_file_name)
