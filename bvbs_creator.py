from Array_verify import shapes_groups

def create_abs(new_table,filename, destination_directory):

    header = ['Shape', 'Pos', 'Pcs', 'Grade', 'Diam', 'L', 'a', 'b', 'c', 'd', 'e', 'u', 'v', 'D', 'kg/1','kg/all']

    # Creates a list of dictionaries, where each dictionary represents a row in the table
    dict_table = []
    previous_shape = None
    for row in new_table[1:]:
        row_dict = {}
        shape = row[1]
        for i, column in enumerate(header):
            if not shape:
                shape = previous_shape
            row_dict[column] = row[i]
            previous_shape = shape
        dict_table.append(row_dict)


    abs_table = []
    abs_table.insert(0, header)

    # Iterate through all rows in dict_table
    for i in range(len(dict_table)):
        allowed_shape = dict_table[i].get('Shape')
        # print(allowed_shape)


    #BVBS header block
        group = "BF2D"
        project = "Hj" +"Dz0114"
        if "Rev" in filename:
            drawing = "r" + filename[:-10]
        else:
            drawing = "r" + filename[:-4]
        index = "i" + dict_table[i]['Shape']
        position = "p" + dict_table[i]['Pos']
        length = "l" + dict_table[i]['L']
        quantity = "n" + dict_table[i]['Pcs']
        weight = "e" + dict_table[i]['kg/1']
        diameter = "d" + dict_table[i]['Diam']
        steel_grade = "g" + dict_table[i]['Grade']

        value_bending_diameter = dict_table[i].get('D')
        value_bending_diameter = 0 if value_bending_diameter is None or value_bending_diameter.strip() == '' else value_bending_diameter
        bending_diameter = "s{}".format(value_bending_diameter)

        layer = "a0"
        delta = "t0"

        #BVBS geometry block
        if allowed_shape in ["A"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w{}".format(0)

        elif allowed_shape in ["B"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w{}".format(90)

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w{}".format(0)

        elif allowed_shape in ["C"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w" + dict_table[i]['u']

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w{}".format(0)

        elif allowed_shape == "D":
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w{}".format(90)

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w{}".format(90)

            geometry_legth_3 = "l" + dict_table[i]['c']
            geometry_angle_3 = "w{}".format(0)

        elif allowed_shape in ["J"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w" + dict_table[i]['u']

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w" + dict_table[i]['u']

            geometry_legth_3 = "l" + dict_table[i]['c']
            geometry_angle_3 = "w{}".format(0)

        elif allowed_shape in ["E"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w" + dict_table[i]['u']

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w" + dict_table[i]['v']

            geometry_legth_3 = "l" + dict_table[i]['c']
            geometry_angle_3 = "w{}".format(0)

        # elif allowed_shape in ["72"]:
        #     geometry_legth_1 = "Gl" + dict_table[i]['a']
        #     geometry_angle_1 = "w{}".format(45)
        #
        #     geometry_legth_2 = "l" + dict_table[i]['b']
        #     geometry_angle_2 = "w{}".format(90)
        #
        #     geometry_legth_3 = "l" + dict_table[i]['c']
        #     geometry_angle_3 = "w{}".format(45)
        #
        #     geometry_legth_4 = "l" + dict_table[i]['d']
        #     geometry_angle_3 = "w{}".format(0)

        elif allowed_shape in ["R"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w{}".format(90)

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w{}".format(90)

            geometry_legth_3 = "l" + dict_table[i]['c']
            geometry_angle_3 = "w{}".format(90)

            geometry_legth_4 = "l" + dict_table[i]['d']
            geometry_angle_4 = "w{}".format(90)

            geometry_legth_5 = "l" + dict_table[i]['e']
            geometry_angle_5 = "w{}".format(0)

        elif allowed_shape in ["U"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']
            geometry_angle_1 = "w{}".format(90)

            geometry_legth_2 = "l" + dict_table[i]['b']
            geometry_angle_2 = "w{}".format(90)

            geometry_legth_3 = "l" + dict_table[i]['c']
            geometry_angle_3 = "w{}".format(90)

            geometry_legth_4 = "l" + dict_table[i]['d']
            geometry_angle_4 = "w{}".format(90)

            geometry_legth_5 = "l" + dict_table[i]['e']
            geometry_angle_5 = "w{}".format(90)

            geometry_legth_6 = "l" + dict_table[i]['a']
            geometry_angle_6 = "w{}".format(0)

        #Private block
        rebar_class = "PnREBAR"
        rebar_type = "h" + dict_table[i]['Shape']

        #Merging for checksum
        if allowed_shape in shapes_groups["straight"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, rebar_class, rebar_type, "C"]
        elif allowed_shape in shapes_groups["bent_1"] + shapes_groups["bent_1_1"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2,rebar_class, rebar_type, "C"]
        elif allowed_shape in shapes_groups["bent_2"] + shapes_groups["bent_2_1"] + shapes_groups["bent_2_2"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2,geometry_legth_3, geometry_angle_3, rebar_class, rebar_type, "C"]
        elif allowed_shape in shapes_groups["bent_3"] + shapes_groups["bent_3_1"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2, geometry_legth_3, geometry_angle_3, geometry_legth_4, geometry_angle_4, rebar_class, rebar_type, "C"]
        elif allowed_shape in shapes_groups["bent_4"] + shapes_groups["bent_4_2"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2, geometry_legth_3, geometry_angle_3, geometry_legth_4, geometry_angle_4, geometry_legth_5, geometry_angle_5, rebar_class, rebar_type, "C"]
        elif allowed_shape in shapes_groups["bent_5"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2, geometry_legth_3, geometry_angle_3, geometry_legth_4, geometry_angle_4, geometry_legth_5, geometry_angle_5, geometry_legth_6, geometry_angle_6, rebar_class, rebar_type, "C"]
        else:
            new_row = []
        abs_table.append(new_row)

    for i, row in enumerate(abs_table):
        for j, value in enumerate(row):
            if j != len(row) - 1:
                abs_table[i][j] = value + "@"
            else:
                abs_table[i][j] = value

    result = []
    for row in abs_table[1:]:
        row_string = "".join(row)
        # print("row_string:", row_string)
        result.append(row_string)

    def calculate_checksum(C):
        n = len(C)
        iSum = 0
        for i in range(n):
            iSum += ord(C[i])
        lP = 96 - (iSum % 32)

        return lP

    checksum = []
    for row_string in result:
        checksum.append(calculate_checksum(row_string))

    #Create new file in specified directory
    folder = destination_directory
    file_name = filename[:-4] + ".abs"

    with open(f"{folder}/{file_name}", "w") as file:
        for i, row_string in enumerate(result):
            file.write(f"{row_string}{checksum[i]}@\n")
            # print(f"{row_string}{checksum[i]}@\n")