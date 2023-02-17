def calculate_insulation(array, debug=False):
    thickness_set = set()
    used_volume_by_thickness_dict = {}
    used_area_by_thickness_dict = {}
    for line in array:
        if "INS." not in line[0]:
            continue
        print(line)
        if line[0]=='':
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
        used_area_by_thickness_dict[thickness] += width*length
        used_volume_by_thickness_dict[thickness] += width*length*thickness
    return (used_area_by_thickness_dict, used_volume_by_thickness_dict)

