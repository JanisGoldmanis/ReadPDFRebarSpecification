#Check reinforcement data

# Dictionary of tuples what to check.
# First list in tuple - needs value
# Second list in tuple - needs to be float

reinforcement_shapes ={
    "straight":([1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1], [0,0,1,0,1,1,1,0,0,0,0,0,0,0,1,1]),
    "bent_1":  ([1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1], [0,0,1,0,1,1,1,1,0,0,0,0,0,1,1,1]),
    "bent_1_1":([1,1,1,1,1,1,1,1,0,0,0,1,0,1,1,1], [0,0,1,0,1,1,1,1,0,0,0,1,0,1,1,1]), #stiegra ar 2 taisnajām daļām un 1 locījumu, kas nav 90 grādi    "bent_2":  ([1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1], [0,1,1,0,1,1,1,1,1,0,0,0,0,1,1,1]),
    "bent_2":  ([1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1], [0,0,1,0,1,1,1,1,1,0,0,0,0,1,1,1]),
    "bent_2_1":([1,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1], [0,0,1,0,1,1,1,1,1,0,0,1,0,1,1,1]), #stiegra ar 3 taisnajām daļām un 1 locījumu, kas nav 90 grādi    "bent_2_2":([1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1], [0,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1]), #stiegra ar 3 taisnajām daļām un 2 locījumiem, kas nav 90 grādi    "bent_3":  ([1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1], [0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1]),
    "bent_2_2":([1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1], [0,0,1,0,1,1,1,1,1,0,0,1,1,1,1,1]), #stiegra ar 3 taisnajām daļām un 2 locījumiem, kas nav 90 grādi
    "bent_3":  ([1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1], [0,0,1,0,1,1,1,1,1,1,0,0,0,1,1,1]),
    "bent_3_1":([1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1], [0,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1]),
    "bent_4":  ([1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1], [0,0,1,0,1,1,1,1,1,1,1,0,0,1,1,1]),
    "bent_4_2":([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], [0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1]), #stiegra ar 5 taisnajām daļām un 2 locījumiem, kas nav 90 grādi
    }
shapes_groups = {
    "straight": ["A"],
    "bent_1": ["B"],
    "bent_1_1": ["C"],
    "bent_2": ["D"],
    "bent_2_1": ["J"],
    "bent_2_2": ["E"],
    "bent_3": [], #YM: jāpaŗbauda, jo ir arī ne tikai 45 un 90 grādi, XB: jāpārbauda,
    "bent_3_1": [],
    "bent_4": ["R"],
    "bent_4_2": []
}


def generate_label_dict():
    label_dict = {}
    for key in shapes_groups.keys():
        for label in shapes_groups[key]:
            label_dict[label] = key
    return label_dict


def get_labels():
    shapes_all = []
    for labels in shapes_groups.values():
        shapes_all.extend(labels)
    return shapes_all

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def verify_line(line : list[str], checking_tuple) -> tuple:
    """
    line - single line from table
    checking tuple - first entry is values that need to contain something
                     second entry is values, that need to contain floats
    return:
    boolean result, if everything is ok
    string report, what isn't ok
    """
    req_value = checking_tuple[0]
    req_float = checking_tuple[1]
    for index in range(len(line)):

        # Check if necessary fields contain values
        if req_value[index]:
            if line[index] == '':
                return False, f'Check First {line}'

        # Check if empty spaces contain blanks
        else:
            if line[index] != '':
                return False, f'Check Second {line}'
        if req_float[index]:
            if not is_number(line[index]):
                return False, f'Check Third {line}'
    return True, "Everything is good"


def verify_table(array, debug=False):
    label_group_dict = generate_label_dict()
    for line in array:
        if line[0] == '':
            continue
        group = label_group_dict[line[0]]
        binary_tuple = reinforcement_shapes[group]
        correct, result = verify_line(line, binary_tuple)
        if not correct:
            if debug:
                print(f'INCORRECT TABLE {result}')
            return False, result
    return True, result












