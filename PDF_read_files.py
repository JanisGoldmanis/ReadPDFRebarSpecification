import os
import PDF_read_text
import Array_clean_up_shapes
import Array_verify
import bvbs_creator
import time


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
