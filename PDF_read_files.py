import os

import Embeds
import PDF_read_text
import Array_clean_up_shapes
import Array_verify
import bvbs_creator
import time
import Calculate_insulation
import csv

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


def generate_bvbs(source_directory, destination_directory, debug=False):
    """
    USED!
    Main function that iterates through all files, finds page with information, creates array, generates BVBS
    :param source_directory:
    :param destination_directory:
    :param debug:
    :return:
    """
    file_names = get_file_names(source_directory)
    bad_files = []
    shape_set = set()
    shape_dict = {}

    total_file_count = len(file_names)
    print(f'Source directory: {source_directory}')
    print(f'Total {total_file_count} files in Source Directory')

    number = 0
    for file_name in file_names:
        start_time = time.time()
        number += 1
        file_path = os.path.join(source_directory, file_name)

        # Check if table exists in any page of PDF
        table_exists, page_number, all_words = PDF_read_text.table_exists(file_path, debug=debug)

        if not table_exists:
            bad_files.append(file_name)
            continue
        array = PDF_read_text.create_array(file_path, all_words, page_number, debug)

        cleaned_up_array = Array_clean_up_shapes.clean_array(array, debug)

        correct, result = Array_verify.verify_table(cleaned_up_array, debug)

        for row in array:
            if row[0] not in shape_set:
                shape_set.add(row[0])
                shape_dict[row[0]] = 0
            shape_dict[row[0]] += 1

        if correct:
            bvbs_creator.create_abs(cleaned_up_array, file_name, destination_directory)
        else:
            bad_files.append(file_name)

        end_time = round(time.time() - start_time, 2)
        print(f'{number:>4}/{total_file_count} | {file_name} T{end_time}')

    if len(bad_files) > 0:
        print()
        print('Bad files:')
        for name in bad_files:
            print(name)

    good_shapes = Array_verify.get_labels()
    print()
    print(f'Allowed shapes: {good_shapes}')
    for shape in shape_dict.keys():
        if shape not in good_shapes:
            print(f'Shape: {shape}, Count: {shape_dict[shape]}')


def generate_total_insulation_report(source_directory, destination_directory, debug=False):
    """

    :param source_directory:
    :param destination_directory:
    :param debug:
    :return:
    """
    file_names = get_file_names(source_directory)
    bad_files = []
    good_files = []

    full_specification = []

    total_file_count = len(file_names)
    print(f'Source directory: {source_directory}')
    print(f'Total {total_file_count} files in Source Directory')

    total_area_dict = {}
    total_volume_dict = {}
    thickness_set = set()
    position_set = set()

    number = 0
    for file_name in file_names:

        # print(file_name)


        start_time = time.time()
        number += 1
        file_path = os.path.join(source_directory, file_name)

        table_exists, page_number, all_words = PDF_read_text.insulation_table_exists(file_path, debug=debug)
        if not table_exists:
            bad_files.append(file_name)
            continue

        array = PDF_read_text.create_insulation_table_array(file_path, all_words, page_number, debug)

        if len(array[0]) == 6:
            temp_array = []
            for line in array:
                if len(line)== 6:
                    temp_array.append(line[:3])
                    temp_array.append(line[3:])
                else:
                    temp_array.append(line)

        array = temp_array

        # for line in array:
        #     print(line)

        area_dict, volume_dict = Calculate_insulation.calculate_insulation(array)

        good_files.append(file_name)

        if "Rev" in file_name:
            name = file_name[:-10]
        else:
            name = file_name[:-4]


        for line in array:
            if line[0] == '':
                continue
            line[2] = int(line[2])
            dimensions = line[1].split('*')
            dimensions = sorted([int(x) for x in dimensions])
            new_line = [name]+line+dimensions
            full_specification.append(new_line)



        for key in area_dict.keys():
            if key not in thickness_set:
                thickness_set.add(key)
                total_area_dict[key] = 0
                total_volume_dict[key] = 0
            total_area_dict[key] += area_dict[key]
            total_volume_dict[key] += volume_dict[key]

        end_time = round(time.time() - start_time, 2)
        print(f'{number:>4}/{total_file_count} | {file_name} T{end_time}')



    if len(bad_files)>0:
        print("Bad Files:")
        for file_name in bad_files:
            print(file_name)

    for key in sorted(thickness_set):
        area = round(total_area_dict[key]/(10**6),2)
        volume = round(total_volume_dict[key]/(10**9),2)
        print(f'H={key}, Area={area}, Volume={volume}')

    # for line in full_specification:
    #     print(line)

    with open('InsulationData.csv', 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Panel', 'Position', 'Dimensions', 'Qty', 'Height', 'Width', 'Length'])

        # Write the data rows
        for row in full_specification:
            writer.writerow(row)


def generate_embed_specification(source_directory, destination_directory, debug=False):
    """
    USED!
    Main function that iterates through all files, finds page with information, creates array, generates BVBS
    :param source_directory:
    :param destination_directory:
    :param debug:
    :return:
    """
    file_names = get_file_names(source_directory)
    bad_files = []
    good_files = []

    insulation_types_per_drawing = []
    shape_set = set()
    shape_dict = {}

    material_set = set()

    total_file_count = len(file_names)
    print(f'Source directory: {source_directory}')
    print(f'Total {total_file_count} files in Source Directory')

    number = 0
    for file_name in file_names:
        start_time = time.time()
        number += 1
        file_path = os.path.join(source_directory, file_name)
        print(f'Drawing: {file_name}')
        # Check if table exists in any page of PDF
        table_exists, page_number, all_words = PDF_read_text.embed_table_exists(file_path, debug=debug)

        if not table_exists:
            bad_files.append(file_name)
            continue
        good_files.append(file_name)

        array = PDF_read_text.create_embed_array(file_path, all_words, page_number, debug)

        embed_array, material_array = Embeds.clean_up_embed_array(array)

        insulation_types_per_drawing.append(Embeds.insulation_type(material_array))


        # Embeds.print_embed_array(embed_array)
        #
        # Embeds.print_material_array(material_array)

        for material in material_array:
            if material[0] not in material_set:
                material_set.add(material[0])


    if len(bad_files) > 0:
        print()
        print('Bad files:')
        for name in bad_files:
            print(name)

    for material in material_set:
        print(material)

    # Open a file for writing
    file = open("InsulationType.csv", "w")

    # Write information to the file
    for index in range(len(good_files)):
        # string = f'{good_files[index],insulation_types_per_drawing[index]}
        file.write(f'{good_files[index],insulation_types_per_drawing[index]}\n')

    # Close the file
    file.close()





