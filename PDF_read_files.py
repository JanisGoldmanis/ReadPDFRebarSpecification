import os
import PDF_read_text


def get_file_names(directory_path):
    filename_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filename_list.append(filename)
    return filename_list


def create_reinforcement_table_array(directory, debug=False):
    """
    :param directory: Path to folder with ONLY pdf files
    :param debug: Full console printout with debug steps
    :return: In console prints out drawings without reinforcement tables
    """
    file_names = get_file_names(directory)

    # Some checks will be done later. If files are OK.
    good_file_name_list = []
    bad_file_name_list = []
    arrays = []

    if debug:
        file_names = file_names[:15]

    # Parsing all files
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)

        # Check if reinforcement table exist
        if debug:
            print(f'{" "*4}Checking {file_name}')
        table_exists = PDF_read_text.table_exists(file_path, debug=debug)

        if not table_exists:
            bad_file_name_list.append(file_name)
        else:
            good_file_name_list.append(file_name)
    print()
    print(f'Bad Files:')
    for file_name in bad_file_name_list:
        print(f'{" " * 4}{file_name}')

    if debug:
        print(f'Good Files:')
        for file_name in good_file_name_list:
            print(f'{" " * 4}{file_name}')

    print(f'Finished checking {len(file_names)} drawings if specification exists')
    print()
    print(f'Starting creating arrays')

    for file_name in good_file_name_list:
        print(f'{" "*4}{file_name}')
        file_path = os.path.join(directory, file_name)
        arrays.append(PDF_read_text.create_array(file_path, debug))

    return arrays, good_file_name_list
