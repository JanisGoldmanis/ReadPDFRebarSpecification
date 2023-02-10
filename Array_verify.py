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
    "bent_5":  ([1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1], [0,0,1,0,1,1,1,1,1,1,1,0,0,1,1,1]),
    }
# Visiem būs grāda precizitāte no tabulas, nevis kā failā .00 simtdaļa aiz komata.
# 14_5: Pagaidām nepastrādāsim. Projektā tikai 1 stiegra. Jāredz piemērs.
# 29_2: Var apstrādāt. Jāredz piemērs.
# 44 Neapstrādāsim, jo nav iedoti leņķi tabulās. Piemērs ir SF-A3-1-01R Rev_A. Projektā 16 stiegras.
# 49: Pagaidām nepastrādāsim. Projektā tikai 15 stiegras. Jāredz piemērs.
# 51: Var apstrādāt. Jāredz piemērs.
# 67_2:
# 67_3:
# 69_1:
# 72:
# 79_1:
# F: nav visi izmēri tabulās.
# G:
# K stiegra neapstrādāsim, jo ir DIM-X
# M
# N: BF2D. jāatrod ABS no UPB. Jāpārbauda.
# Q:
# XA: Telpiska
# XB: Jāpārbauda
# XE neapstrādāsim - pārāk mazs skaits (4)
# Y: Tās ir BF3D, tēpēc nevar automātiski savadīt no tabulas datiem. Nav info par locīšanas virzieniem. Jāpārbauda IS iespējas. Varētu pēc diametra. Ja mazā ks par 10mm, tad būs vienā plaknē.
# YE: Telpiska
# YG:
# YH:
# YJ:
# YM: BF2D. BF2D@HjSW0532@rUGV-1007@i@p204@l908@n2@e1.42@d16@gK500C-T@s64@a0@t0@Gl386@w45.58@l146@w-91.16@l146@w45.58@l286@w0@PnREBAR@hYM@C76@. Leņķi nav parādīti U un V vērtībās, bet tikai bildēs. Var nolasīt 45 un 90 grādus.
# Z: Telpiska

shapes_groups = {
    "straight": ["A"],
    "bent_1": ["B"],
    "bent_1_1": ["C"],
    "bent_2": ["D"],
    "bent_2_1": ["J"],
    "bent_2_2": ["E"],
    "bent_3": [],
    "bent_3_1": [],
    "bent_4": ["R"],
    "bent_4_2": [],
    "bent_5": ["U"]
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












