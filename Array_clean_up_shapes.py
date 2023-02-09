import Array_verify

allowed_shape = Array_verify.get_labels()


def clean_array(array, debug):
    temp_array = array[:]
    result = []

    while len(temp_array) > 0:
        if len(temp_array) > 1:
            if temp_array[1][0] == '':
                temp_line = [temp_array.pop(0), temp_array.pop(0)]
            else:
                temp_line = [temp_array.pop(0)]
        else:
            temp_line = [temp_array.pop(0)]
        if temp_line[0][0] in allowed_shape:
            result += temp_line
        else:
            if debug:
                print('Removing')
                for line in temp_line:
                    print(line)
    return result
