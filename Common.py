def join_nearby_word_objects_together(word_objects, tolerance, debug=False):
    """
    Given a line of words, check if adjacent words are near each other.
    If so - join them into single word object, with combined bbox.
    :param word_objects:
    :param debug:
    :return:
    """
    local_word_objects = word_objects[:]
    result_word_objects = [local_word_objects.pop(0)]
    while len(local_word_objects)>0:
        current_word = local_word_objects.pop(0)
        distance_from_previous = current_word[0] - result_word_objects[-1][2]
        if distance_from_previous < tolerance:
            result_word_objects[-1] = combine_two_words(result_word_objects[-1], current_word)
        else:
            result_word_objects.append(current_word)
    return result_word_objects


def combine_two_words(first_word, second_word, debug=False):
    new_word_obj = list(first_word[:])
    # print(new_word_obj)
    new_word_obj[2] = second_word[2]
    new_word_obj[4] = first_word[4]+' '+second_word[4]
    return new_word_obj
