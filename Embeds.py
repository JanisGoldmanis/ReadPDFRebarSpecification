def clean_up_embed_array(array, debug=False):
    embed_array = []
    material_array = []
    flag = False


    for line in array:
        temp_line = []
        if line[0] == "Total:":
            flag = True
            continue
        if not flag:
            if len(line) == 6:
                for word in line:
                    temp_line.append(word)
            elif len(line) == 5:
                line.insert(1,'')
                for word in line:
                    temp_line.append(word)
            else:
                print(f'Bad line! {line}')
                continue
            embed_array.append(temp_line)
        else:
            material_array.append(line[:])
    return embed_array, material_array


def print_embed_array(embed_array):
    longest_entries = []
    count = len(embed_array[0])
    for _ in range(count):
        longest_entries.append(0)

    for line in embed_array:
        for index in range(count):
            if longest_entries[index] < len(line[index]):
                longest_entries[index] = len(line[index])
    print('Embed Report')
    for line in embed_array:
        for index in range(count):
            word = line[index]
            length = len(word)
            dif = longest_entries[index] - length
            print(f'| {word}{" "*dif} ',end='')
        print()

def print_material_array(material_array):
    longest_entries = []
    count = len(material_array[0])
    for _ in range(count):
        longest_entries.append(0)

    for line in material_array:
        for index in range(count):
            if longest_entries[index] < len(line[index]):
                longest_entries[index] = len(line[index])

    print('Material report:')
    for line in material_array:
        for index in range(count):
            word = line[index]
            length = len(word)
            dif = longest_entries[index] - length
            print(f'| {word}{" "*dif} ',end='')
        print()


def insulation_type(material_array):
    for material_line in material_array:
        if "Insulation" in material_line[0] and "Frontrock S" not in material_line[0]:
            return "Insulation"
        elif "Insulation" in material_line[0] and "Frontrock S" in material_line[0]:
            return "Both"
        elif "Frontrock S" in material_line[0]:
            return "Frontrock S"
        else:
            return "None"


def create_material_list():
    pass