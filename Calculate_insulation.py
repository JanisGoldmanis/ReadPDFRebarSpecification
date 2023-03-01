import Insulation_Allowed_Thickness

def calculate_insulation(array, debug=False):
    thickness_set = set()
    used_volume_by_thickness_dict = {}
    used_area_by_thickness_dict = {}
    for line in array:
        if "INS." not in line[0]:
            continue
        # print(line)
        if line[0] == '':
            continue
        dimensions = []
        for x in line[1].split('*'):
            if x != '':
                dimensions.append(int(x))
        dimensions = sorted(dimensions)
        thickness = dimensions[0]
        width = dimensions[1]
        length = dimensions[2]

        if thickness not in thickness_set:
            thickness_set.add(thickness)
            used_volume_by_thickness_dict[thickness] = 0
            used_area_by_thickness_dict[thickness] = 0
        used_area_by_thickness_dict[thickness] += width * length
        used_volume_by_thickness_dict[thickness] += width * length * thickness
    return (used_area_by_thickness_dict, used_volume_by_thickness_dict)


def split_insulation_table(insulation_array):
    if len(insulation_array[0]) == 6:
        temp_array = []
        for line in insulation_array:
            if len(line) == 6:
                temp_array.append(line[:3])
                temp_array.append(line[3:])
            else:
                temp_array.append(line)
    else:
        temp_array = insulation_array
    insulation_array = temp_array
    return insulation_array


def calculate_line_volume(line):
    allowed_thickness = Insulation_Allowed_Thickness.insulation_allowed_thickness
    position = line[0]
    dimensions = sorted([float(x) for x in line[1].split('*')])
    quantity = int(line[2])
    actual_volume = dimensions[0]*dimensions[1]*dimensions[2]*quantity
    suggested_volume = actual_volume

    if dimensions[0] in allowed_thickness:
        return suggested_volume, actual_volume, dimensions[0]
    if dimensions[1] in allowed_thickness:
        return suggested_volume, actual_volume, dimensions[1]
    if dimensions[2] in allowed_thickness:
        return suggested_volume, actual_volume, dimensions[2]

    #Find which dimension is most suitable for incrementation.

    Difference0 = 1000000
    for index in range(len(allowed_thickness)-1):
        if allowed_thickness[index] < dimensions[0] < allowed_thickness[index+1]:
            Difference0 = allowed_thickness[index+1] - dimensions[0]
            suggested_dimension_0 = allowed_thickness[index+1]
            break

    Difference1 = 1000000
    for index in range(len(allowed_thickness)-1):
        if allowed_thickness[index] < dimensions[1] < allowed_thickness[index+1]:
            Difference1 = allowed_thickness[index+1] - dimensions[1]
            suggested_dimension_1 = allowed_thickness[index+1]
            break

    Difference2 = 1000000
    for index in range(len(allowed_thickness)-1):
        if allowed_thickness[index] < dimensions[2] < allowed_thickness[index+1]:
            Difference2 = allowed_thickness[index+1] - dimensions[2]
            suggested_dimension_2 = allowed_thickness[index+1]
            break

    if Difference0 <= Difference1 and Difference0 <= Difference2:
        suggested_volume = suggested_dimension_0*dimensions[1]*dimensions[2]*quantity
        return suggested_volume, actual_volume, suggested_dimension_0

    if Difference1 <= Difference0 and Difference1 <= Difference2:
        suggested_volume = dimensions[0]*suggested_dimension_1*dimensions[2]*quantity
        return suggested_volume, actual_volume, suggested_dimension_1

    if Difference2 <= Difference0 and Difference2 <= Difference1:
        suggested_volume = dimensions[0]*dimensions[1]*suggested_dimension_2*quantity
        return suggested_volume, actual_volume, suggested_dimension_2

    return None, None, None


def generate_dict_of_volume_by_thickness(insulation_array):
    volume = {}

    for line in insulation_array:
        suggested_volume, actual_volume, thickness = calculate_line_volume(line)
        if thickness not in volume.keys():
            volume[thickness] = [0,0]
        volume[thickness][0] += suggested_volume
        volume[thickness][1] += actual_volume

    return volume