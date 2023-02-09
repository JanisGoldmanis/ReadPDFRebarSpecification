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


    #BVBS header block
        group = "BF2D"
        project = "Hj" +"Dz0114"
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
        if allowed_shape == "A":
            geometry_legth_1 = "Gl" + dict_table[i]['a']

            value_geometry_angle_1 = dict_table[i].get('u')
            value_geometry_angle_1 = 0 if value_geometry_angle_1 is None or value_geometry_angle_1.strip() == '' else value_geometry_angle_1
            geometry_angle_1 = "w{}".format(value_geometry_angle_1)

        elif allowed_shape in ["B","C"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']

            value_geometry_angle_1 = dict_table[i].get('u')
            value_geometry_angle_1 = 90 if value_geometry_angle_1 is None or value_geometry_angle_1.strip() == '' else value_geometry_angle_1
            geometry_angle_1 = "w{}".format(value_geometry_angle_1)

            geometry_legth_2 = "l" + dict_table[i]['b']

            value_geometry_angle_2 = dict_table[i].get('u')
            value_geometry_angle_2 = 0 if value_geometry_angle_2 is None or value_geometry_angle_2.strip() == '' else value_geometry_angle_2
            geometry_angle_2 = "w{}".format(value_geometry_angle_2)

        elif allowed_shape == "D":
            geometry_legth_1 = "Gl" + dict_table[i]['a']

            value_geometry_angle_1 = dict_table[i].get('u')
            value_geometry_angle_1 = 0 if value_geometry_angle_1 is None or value_geometry_angle_1.strip() == '' else value_geometry_angle_1
            geometry_angle_1 = "w{}".format(value_geometry_angle_1)

            geometry_legth_2 = "l" + dict_table[i]['b']

            value_geometry_angle_2 = dict_table[i].get('u')
            value_geometry_angle_2 = 90 if value_geometry_angle_2 is None or value_geometry_angle_2.strip() == '' else value_geometry_angle_2
            geometry_angle_2 = "w{}".format(value_geometry_angle_2)


            geometry_legth_3 = "l" + dict_table[i]['c']

            value_geometry_angle_3 = dict_table[i].get('u')
            value_geometry_angle_3 = 90 if value_geometry_angle_3 is None or value_geometry_angle_3.strip() == '' else value_geometry_angle_3
            geometry_angle_3 = "w{}".format(value_geometry_angle_3)

        elif allowed_shape in ["72", "YM"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']

            value_geometry_angle_1 = dict_table[i].get('u')
            value_geometry_angle_1 = 0 if value_geometry_angle_1 is None or value_geometry_angle_1.strip() == '' else value_geometry_angle_1
            geometry_angle_1 = "w{}".format(value_geometry_angle_1)

            geometry_legth_2 = "l" + dict_table[i]['b']

            value_geometry_angle_2 = dict_table[i].get('u')
            value_geometry_angle_2 = 90 if value_geometry_angle_2 is None or value_geometry_angle_2.strip() == '' else value_geometry_angle_2
            geometry_angle_2 = "w{}".format(value_geometry_angle_2)

            geometry_legth_3 = "l" + dict_table[i]['c']

            value_geometry_angle_3 = dict_table[i].get('u')
            value_geometry_angle_3 = 90 if value_geometry_angle_3 is None or value_geometry_angle_3.strip() == '' else value_geometry_angle_3
            geometry_angle_3 = "w{}".format(value_geometry_angle_3)

            geometry_legth_4 = "l" + dict_table[i]['d']

            value_geometry_angle_4 = dict_table[i].get('u')
            value_geometry_angle_4 = 90 if value_geometry_angle_4 is None or value_geometry_angle_4.strip() == '' else value_geometry_angle_4
            geometry_angle_4 = "w{}".format(value_geometry_angle_4)

        elif allowed_shape in ["R","Y"]:
            geometry_legth_1 = "Gl" + dict_table[i]['a']

            value_geometry_angle_1 = dict_table[i].get('u')
            value_geometry_angle_1 = 0 if value_geometry_angle_1 is None or value_geometry_angle_1.strip() == '' else value_geometry_angle_1
            geometry_angle_1 = "w{}".format(value_geometry_angle_1)

            geometry_legth_2 = "l" + dict_table[i]['b']

            value_geometry_angle_2 = dict_table[i].get('u')
            value_geometry_angle_2 = 90 if value_geometry_angle_2 is None or value_geometry_angle_2.strip() == '' else value_geometry_angle_2
            geometry_angle_2 = "w{}".format(value_geometry_angle_2)

            geometry_legth_3 = "l" + dict_table[i]['c']

            value_geometry_angle_3 = dict_table[i].get('u')
            value_geometry_angle_3 = 90 if value_geometry_angle_3 is None or value_geometry_angle_3.strip() == '' else value_geometry_angle_3
            geometry_angle_3 = "w{}".format(value_geometry_angle_3)

            geometry_legth_4 = "l" + dict_table[i]['d']

            value_geometry_angle_4 = dict_table[i].get('u')
            value_geometry_angle_4 = 90 if value_geometry_angle_4 is None or value_geometry_angle_4.strip() == '' else value_geometry_angle_4
            geometry_angle_4 = "w{}".format(value_geometry_angle_4)

            geometry_legth_5 = "l" + dict_table[i]['e']

            value_geometry_angle_5 = dict_table[i].get('u')
            value_geometry_angle_5 = 90 if value_geometry_angle_5 is None or value_geometry_angle_5.strip() == '' else value_geometry_angle_5
            geometry_angle_5 = "w{}".format(value_geometry_angle_5)

            # BVBS geometry types



        #Private block
        rebar_class = "PnREBAR"
        rebar_type = "h" + dict_table[i]['Shape']

        #Merging for checksum
        if allowed_shape == "A":
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, rebar_class, rebar_type, "C"]
        elif allowed_shape in ["B","C"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2,rebar_class, rebar_type, "C"]
        elif allowed_shape == "D":
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2,geometry_legth_3, geometry_angle_3, rebar_class, rebar_type, "C"]
        elif allowed_shape in ["72", "YM"]:
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2, geometry_legth_3, geometry_angle_3, geometry_legth_4, geometry_angle_4, rebar_class, rebar_type, "C"]
        elif allowed_shape == "R":
            new_row = [group, project, drawing, index, position, length, quantity, weight, diameter, steel_grade, bending_diameter, layer, delta, geometry_legth_1, geometry_angle_1, geometry_legth_2, geometry_angle_2, geometry_legth_3, geometry_angle_3, geometry_legth_4, geometry_angle_4, geometry_legth_5, geometry_angle_5, rebar_class, rebar_type, "C"]
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









    # Result array by rows: new_table
    # Result array by columns: result


"""
Konvertē no saraksta uz jaunu rindu txt failā:
                new_table.insert(0, header)
        with open('test.txt', 'w') as file:
            for row in new_table:
                row_str = '\t'.join(str(item) for item in row)
                file.write(row_str + '\n')
                print(f'{row_str:5}|' + '\n')


        for line in new_table:
            print(line)
"""