import fitz
import cv2
import numpy as np
import Table


def draw_cv2_page(word_object_list, page):
    """
    USED!
    For debugging
    :param word_object_list:
    :param page:
    :return:
    """
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    print(f'{" " * 8}Size: {pix.w}x{pix.h}')
    for word in word_object_list:
        bbox = word[:4]
        min_x = int(bbox[0])
        min_y = int(bbox[1])
        max_x = int(bbox[2])
        max_y = int(bbox[3])
        bottom_left = (min_x, min_y)
        top_right = (max_x, max_y)
        cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def middle_point(start, end):
    """
    USED!
    :param start:
    :param end:
    :return:
    """
    return start + (end - start) / 2


def does_word_sentence_exist(page, req_words, debug=False):
    """
    USED!

    Check if specific sentence "Reinforcement total weight (kg):" exists
    It's done by checking, if this set of words are at the same Y position.
    :param page:
    :param debug:
    :return:
    """
    all_words = page.get_textpage().extractWORDS()
    good_words = []
    good_words_text = []
    for word in all_words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])
    if debug:
        draw_cv2_page(good_words, page)
    for req_word in req_words:
        if req_word not in good_words_text:
            if debug:
                print(f'{" " * 8}{req_word} not in {good_words_text}')
            return False, None

    for main_word in good_words:
        sentence_word_set = set()
        sentence_word_set.add(main_word[4])

        for secondary_word in good_words:
            if secondary_word[4] in sentence_word_set:
                continue
            start = secondary_word[1]
            end = secondary_word[3]
            secondary_word_middle_point = middle_point(start, end)

            if main_word[1] < secondary_word_middle_point < main_word[3]:
                sentence_word_set.add(secondary_word[4])
        if len(sentence_word_set) == len(req_words):
            return True, all_words
    return False, None


def table_exists(file_path, debug=False):
    """
    USED!

    Check if table exists in a specific pdf file
    :param file_path: String
    :param debug:
    :return: True or False and page number, None if it doesn't exist
    """
    doc = fitz.open(file_path)
    number = 0
    req_words = ["Reinforcement", "total", "weight", "(kg):"]
    for page in doc:
        sentence_exists, all_words = does_word_sentence_exist(page, req_words, debug)
        if sentence_exists:
            if debug:
                print(f'{" " * 8}Sentence exists!')
            return True, number, all_words
        number += 1
    if debug:
        print(f'{" " * 8}Sentence DOES NOT exist!')
    return False, None, None


def insulation_table_exists(file_path, debug=False):
    """
    USED!

    Check if insulation table exists in a specific pdf file
    :param file_path: String
    :param debug:
    :return: True or False and page number, None if it doesn't exist
    """
    doc = fitz.open(file_path)
    number = 0
    req_words = ["INSULATION", "SPECIFICATION"]
    for page in doc:
        sentence_exists, all_words = does_word_sentence_exist(page, req_words, debug)
        if sentence_exists:
            if debug:
                print(f'{" " * 8}Sentence exists!')
            return True, number, all_words
        number += 1
    if debug:
        print(f'{" " * 8}Sentence DOES NOT exist!')
    return False, None, None


def embed_table_exists(file_path, debug=False):
    """
    USED!

    Check if table exists in a specific pdf file
    :param file_path: String
    :param debug:
    :return: True or False and page number, None if it doesn't exist
    """
    doc = fitz.open(file_path)
    number = 0
    req_words = ["Embeds:", "Comments", "Quantity", "Material/Producer"]
    for page in doc:
        sentence_exists, all_words = does_word_sentence_exist(page, req_words, debug)
        if sentence_exists:
            if debug:
                print(f'{" " * 8}Sentence exists!')
            return True, number, all_words
        number += 1
    if debug:
        print(f'{" " * 8}Sentence DOES NOT exist!')
    return False, None, None


def get_table_top(all_words, debug=False):
    """
    USED!
    :param page:
    :param all_words:
    :param debug:
    :return:
    """
    req_words = ["Reinforcement", "Shape"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])

    for main_word in good_words:
        if main_word[4] == "Reinforcement":
            sentence_word_set = set()
            sentence_word_set.add(main_word[4])

        for secondary_word in good_words:
            if secondary_word[4] in sentence_word_set:
                continue
            start = secondary_word[0]
            end = secondary_word[2]
            secondary_word_middle_point = middle_point(start, end)

            if main_word[0] < secondary_word_middle_point < main_word[2]:
                sentence_word_set.add(secondary_word[4])
                if abs(main_word[3] - secondary_word[3]) < 20:
                    return secondary_word
    return None


def get_table_bottom(all_words, debug=False):
    """
    USED!
    :param all_words:
    :param debug:
    :return:
    """
    req_words = ["Reinforcement", "total", "weight", "(kg):"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])

    for main_word in good_words:
        if main_word[4] == "Reinforcement":
            sentence_word_set = set()
            sentence_word_set.add(main_word[4])

            for secondary_word in good_words:
                if secondary_word[4] in sentence_word_set:
                    continue
                start = secondary_word[1]
                end = secondary_word[3]
                secondary_word_middle_point = middle_point(start, end)

                if main_word[1] < secondary_word_middle_point < main_word[3]:
                    sentence_word_set.add(secondary_word[4])
            if len(sentence_word_set) == 4:
                return main_word
    return None


def get_table_side(all_words, shape_word_object, debug=False):
    """
    USED!
    :param all_words:
    :param shape_word_object:
    :param debug:
    :return:
    """
    req_words = ["kg/all"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])
    for word in good_words:
        start = word[1]
        end = word[3]
        middle = middle_point(start, end)
        if shape_word_object[1] < middle < shape_word_object[3]:
            return word


def get_insulation_table_top(all_words, debug=False):
    """
    USED!
    :param page:
    :param all_words:
    :param debug:
    :return:
    """
    req_words = ["INSULATION", "SPECIFICATION"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])

    for main_word in good_words:
        if main_word[4] == "INSULATION":
            sentence_word_set = set()
            sentence_word_set.add(main_word[4])
        else:
            continue

        for secondary_word in good_words:
            if secondary_word[4] in sentence_word_set:
                continue
            start = secondary_word[1]
            end = secondary_word[3]
            secondary_word_middle_point = middle_point(start, end)

            if main_word[1] < secondary_word_middle_point < main_word[3]:
                sentence_word_set.add(secondary_word[4])
                # if abs(main_word[0] - secondary_word[0]) < 20:
                return main_word
    return None


def get_embed_table_top(all_words, debug=False):
    """
    USED!
    :param page:
    :param all_words:
    :param debug:
    :return:
    """
    req_words = ["Embeds:", "Comments"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])

    for main_word in good_words:
        if main_word[4] == "Embeds:":
            sentence_word_set = set()
            sentence_word_set.add(main_word[4])
        else:
            continue

        for secondary_word in good_words:
            if secondary_word[4] in sentence_word_set:
                continue
            start = secondary_word[1]
            end = secondary_word[3]
            secondary_word_middle_point = middle_point(start, end)

            if main_word[1] < secondary_word_middle_point < main_word[3]:
                sentence_word_set.add(secondary_word[4])
                # if abs(main_word[0] - secondary_word[0]) < 20:
                return main_word
    return None

def get_embed_table_bottom(all_words, debug=False):
    """
    USED!
    :param page:
    :param all_words:
    :param debug:
    :return:
    """
    req_words = ["CAST", "UNIT", "TOTAL", "WEIGHT"]
    words = all_words
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])

    for main_word in good_words:
        if main_word[4] == "CAST":
            sentence_word_set = set()
            sentence_word_set.add(main_word[4])
        else:
            continue

        for secondary_word in good_words:
            if secondary_word[4] in sentence_word_set:
                continue
            start = secondary_word[1]
            end = secondary_word[3]
            secondary_word_middle_point = middle_point(start, end)

            if main_word[1] < secondary_word_middle_point < main_word[3]:
                sentence_word_set.add(secondary_word[4])
                # if abs(main_word[0] - secondary_word[0]) < 20:
                return main_word
    return None


def draw_cv2_table(page, min_x, max_x, min_y, max_y):
    """
    USED!
    For debug
    :param page:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :return:
    """
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    bottom_left = (min_x, min_y)
    top_right = (max_x, max_y)
    cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_cv2_point(page, x, y):
    """
    USED!
    For debug
    :param page:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :return:
    """
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    first_start = (x, 0)
    first_end = (x, pix.h)
    second_start = (0, y)
    second_end = (pix.w, y)
    cv2.rectangle(img, first_start, first_end, (255, 0, 0), 2)
    cv2.rectangle(img, second_start, second_end, (255, 0, 0), 2)
    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_table_objects(all_words, min_x, max_x, min_y, max_y, debug=False):
    """
    USED!
    :param all_words:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :param debug:
    :return:
    """
    words = all_words
    good_objects = []

    for word in words:
        w_min_x = word[0]
        w_min_y = word[1]
        w_max_x = word[2]
        w_max_y = word[3]
        center_x = middle_point(w_min_x, w_max_x)
        center_y = middle_point(w_min_y, w_max_y)

        if min_x < center_x < max_x and min_y < center_y < max_y:
            good_objects.append(word)
    return good_objects


def get_embed_table_objects(all_words, min_x, min_y, max_y, debug=False):
    """
    USED!
    :param all_words:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :param debug:
    :return:
    """
    words = all_words
    good_objects = []

    for word in words:
        w_min_x = word[0]
        w_min_y = word[1]
        w_max_x = word[2]
        w_max_y = word[3]
        center_x = middle_point(w_min_x, w_max_x)
        center_y = middle_point(w_min_y, w_max_y)

        if min_x < center_x and min_y < center_y < max_y:
            good_objects.append(word)
    return good_objects



def get_insulation_table_objects(all_words, x, y, debug=False):
    """
    USED!
    :param all_words:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :param debug:
    :return:
    """
    words = all_words
    good_objects = []

    for word in words:
        w_min_x = word[0]
        w_min_y = word[1]
        w_max_x = word[2]
        w_max_y = word[3]
        center_x = middle_point(w_min_x, w_max_x)
        center_y = middle_point(w_min_y, w_max_y)

        if x < center_x and y < center_y:
            good_objects.append(word)
    return good_objects


def create_array(file_path, all_words, page_number, debug=False):
    """
    USED!
    :param file_path:
    :param all_words:
    :param page_number:
    :param debug:
    :return:
    """
    doc = fitz.open(file_path)
    page = doc[page_number]

    all_words = all_words

    shape_word_object = get_table_top(all_words, debug)
    reinforcement_word_object = get_table_bottom(all_words, debug)
    kg_word_object = get_table_side(all_words, shape_word_object, debug)
    if debug:
        draw_cv2_page([shape_word_object, reinforcement_word_object, kg_word_object], page)

    min_x = int(shape_word_object[0])
    max_x = int(kg_word_object[2])
    min_y = int(shape_word_object[1])
    max_y = int(reinforcement_word_object[1])

    if debug:
        draw_cv2_table(page, min_x, max_x, min_y, max_y)

    table_objects = get_table_objects(all_words, min_x, max_x, min_y, max_y, debug)

    if debug:
        draw_cv2_page(table_objects, page)

    array = Table.create_array_from_word_objects(table_objects, page, debug)

    return array


def create_insulation_table_array(file_path, all_words, page_number, debug=False):
    """
    USED!
    :param file_path:
    :param all_words:
    :param page_number:
    :param debug:
    :return:
    """
    doc = fitz.open(file_path)
    page = doc[page_number]

    all_words = all_words

    insulation_specification_word_object = get_insulation_table_top(all_words, debug)

    if debug:
        draw_cv2_page([insulation_specification_word_object], page)

    min_x = int(insulation_specification_word_object[0])
    max_y = int(insulation_specification_word_object[3])

    if debug:
        draw_cv2_point(page, min_x, max_y)

    table_objects = get_insulation_table_objects(all_words, min_x, max_y, debug)

    if debug:
        draw_cv2_page(table_objects, page)

    array = Table.create_insulation_array_from_word_objects(table_objects, page, debug)

    if len(array[0]) == 6:
        temp_array = []
        for line in array:
            if len(line) == 6:
                temp_array.append(line[:3])
                temp_array.append(line[3:])
            else:
                temp_array.append(line)
    else:
        temp_array = array

    return temp_array


def create_embed_array(file_path, all_words, page_number, debug=False):
    """
    USED!
    :param file_path:
    :param all_words:
    :param page_number:
    :param debug:
    :return:
    """
    doc = fitz.open(file_path)
    page = doc[page_number]

    all_words = all_words

    embed_word_object = get_embed_table_top(all_words, debug)
    table_bottom = get_embed_table_bottom(all_words, debug)


    if debug:
        draw_cv2_page([embed_word_object, table_bottom], page)

    min_x = int(embed_word_object[0])

    min_y = int(embed_word_object[3])
    max_y = int(table_bottom[1])

    if debug:
        draw_cv2_point(page, min_x, min_y)
        draw_cv2_point(page, min_x, max_y)

    table_objects = get_embed_table_objects(all_words, min_x,min_y, max_y, debug)

    if debug:
        draw_cv2_page(table_objects, page)

    array = Table.create_embed_array_from_word_objects(table_objects, page, debug)

    return array