import fitz
import cv2
import numpy as np
import Table


def convert_coordinates(height: int, coordinates: list[float, float, float, float]):
    """
    CURRENTLY NOT USED, NECESSARY FOR PDF MINER, BUT NOT pymupdf

    Transforms pdf bbox coordinates (origin point left bottom corner, up is Y positive) to
    image coordinates (origin point top left corner, down is Y positive)
    :param height: picture height
    :param coordinates: List [min_x, min_y, max_x, max_y]
    :return: List [min_x, min_y, max_x, max_y]
    """
    min_x = coordinates[0]
    min_y = coordinates[1]
    max_x = coordinates[2]
    max_y = coordinates[3]
    new_min_y = int(height - max_y)
    new_max_y = int(height - min_y)
    return [int(min_x), new_min_y, int(max_x), new_max_y]


def draw_cv2_page(word_object_list, page):
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
    return start + (end - start) / 2


def does_word_sentence_exist(page, debug=False):
    """
    Check if specific sentence "Reinforcement total weight (kg):" exists
    It's done by checking, if this set of words are at the same Y position.
    :param page:
    :param debug:
    :return:
    """
    req_words = ["Reinforcement", "total", "weight", "(kg):"]
    words = page.get_textpage().extractWORDS()
    good_words = []
    good_words_text = []
    for word in words:
        if word[4] in req_words:
            good_words.append(word)
            good_words_text.append(word[4])
    for req_word in req_words:
        if req_word not in good_words_text:
            if debug:
                print(f'{" " * 8}{req_word} not in {good_words_text}')
            return False

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
        if len(sentence_word_set) == 4:
            return True
    return False


def table_exists(file_path, debug=False):
    """
    Check if table exists in a specific pdf file
    :param file_path: String
    :param debug:
    :return: True or False
    """
    doc = fitz.open(file_path)
    for page in doc:
        if does_word_sentence_exist(page, debug):
            if debug:
                print(f'{" " * 8}Sentence exists!')
            return True
    if debug:
        print(f'{" " * 8}Sentence DOES NOT exist!')
    return False


def get_table_top(page, debug=False):
    req_words = ["Reinforcement", "Shape"]
    words = page.get_textpage().extractWORDS()
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


def get_table_bottom(page, debug=False):
    req_words = ["Reinforcement", "total", "weight", "(kg):"]
    words = page.get_textpage().extractWORDS()
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


def get_table_side(page, shape_word_object, debug=False):
    req_words = ["kg/all"]
    words = page.get_textpage().extractWORDS()
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


def draw_cv2_table(page, min_x, max_x, min_y, max_y):
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    bottom_left = (min_x, min_y)
    top_right = (max_x, max_y)
    cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_table_objects(page, min_x, max_x, min_y, max_y, debug=False):
    words = page.get_textpage().extractWORDS()
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


def create_array(file_path, debug=False):
    doc = fitz.open(file_path)
    for page in doc:
        if does_word_sentence_exist(page, debug):

            shape_word_object = get_table_top(page, debug)
            reinforcement_word_object = get_table_bottom(page, debug)
            kg_word_object = get_table_side(page, shape_word_object, debug)
            if debug:
                draw_cv2_page([shape_word_object, reinforcement_word_object, kg_word_object], page)

            min_x = int(shape_word_object[0])
            max_x = int(kg_word_object[2])
            min_y = int(shape_word_object[3])
            max_y = int(reinforcement_word_object[1])

            if debug:
                draw_cv2_table(page, min_x, max_x, min_y, max_y)

            table_objects = get_table_objects(page, min_x, max_x, min_y, max_y, debug)

            if debug:
                draw_cv2_page(table_objects, page)

            array = Table.create_array_from_word_objects(table_objects, page, debug)

            return array
