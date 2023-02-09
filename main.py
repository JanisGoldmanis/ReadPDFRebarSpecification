import time
import bvbs_creator
import PDF_read_files
import Array_clean_up_shapes
import Array_verify

print(f'Starting')
start_time = time.time()

directory = r"C:\Users\janis.goldmanis\Downloads\OneDrive_1_03-02-2023\Test"
destination_directory = r"C:\Users\janis.goldmanis\Downloads\bvs_Test"

arrays, file_name = PDF_read_files.create_reinforcement_table_array(directory, False)

header = ['Shape', 'Pos', 'Pcs', 'Grade', 'Diam', 'L', 'a', 'b', 'c', 'd', 'e', 'u', 'v', 'D', 'kg/1', 'kg/all']
column_count = len(header)

cleaned_up_arrays = []
removed_arrays = []

for array in arrays:

    new_array = Array_clean_up_shapes.clean_array(array, False)
    cleaned_up_arrays.append(new_array)

    table_column_count = len(new_array[0])
    difference = column_count - table_column_count

    for i in range(difference):
        for row in new_array:
            row.insert(-3, '')

for index in range(len(arrays)):
    correct, result = Array_verify.verify_table(cleaned_up_arrays[index], False)
    print(file_name[index], correct, result)

for index in range(len(arrays)):
    bvbs_creator.create_abs(cleaned_up_arrays[index], file_name[index], destination_directory)

print()


def transform_table(array):
    # Flips the table matrix
    result = []
    for row_index in range(len(array[0])):
        row = []
        for column_index in range(len(array)):
            row.append(array[column_index][row_index])
        result.append(row)
    return result


shape_set = set()
shape_dict = {}

for array in arrays:
    header = ['Shape', 'Pos', 'Pcs', 'Grade', 'Diam', 'L', 'a', 'b', 'c', 'd', 'e', 'u', 'v', 'D', 'kg/1', 'kg/all']

    array.insert(0, header)
    for row in array:
        if row[0] not in shape_set:
            shape_set.add(row[0])
            shape_dict[row[0]] = 0
        shape_dict[row[0]] += 1

        # for item in row:
        #     print(f'{item:>5}|', end='')
        # print()

print(shape_set)
print(shape_dict)

print(f'Allowed shapes: {Array_verify.get_labels()}')
for shape in shape_dict.keys():
    if shape not in Array_verify.get_labels():
        print(f'Key: "{shape}", Count: {shape_dict[shape]}')

print(f'Elapsed time: {round(time.time() - start_time, 1)}')
