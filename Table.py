import numpy as np
import cv2
import PDF_read_text
import Common


def middle_coordinate(start, end):
    """
    USED!
    :param start:
    :param end:
    :return:
    """
    return start + (end - start) / 2


def generate_domains(table_objects, direction, page, debug=False):
    """
    USED!
    :param table_objects:
    :param direction:
    :param page:
    :param debug:
    :return:
    """
    objects = table_objects[:]
    domains = []

    if direction == 'H':
        i = 0
    else:
        i = 1

    # Find left most object
    while len(objects) > 0:
        # if debug:
        #     print(f'New Cycle, {len(objects)} objects left')

        minimum = objects[0][i + 2]
        minimum_object = objects[0]

        for object in objects:
            if minimum >= object[i]:
                minimum = object[i]
                minimum_object = object
        # if debug:
        # print(f'New cycle min object: {minimum_object[4]}')
        # draw_object(page, minimum_object)

        maximum = minimum_object[i + 2]

        for object in objects:
            if object[i + 2] > maximum > middle_coordinate(object[i], object[i + 2]) - 1:

                maximum = object[i + 2]
                # if debug:
                # print(f'Max object {object[4]}')
                # draw_object(page, object)
        domains.append([int(minimum), int(maximum)])
        # if debug:
        #     print(f'{len(objects)} objects left')
        remove_objects = objects[:]
        for remove_object in remove_objects:

            middle = middle_coordinate(remove_object[i], remove_object[i + 2])
            # if debug:
            # print(f'{remove_object[4]} middle is {middle}, current domain: {[int(minimum), int(maximum)]}')

            if minimum <= middle <= maximum:
                # if debug:
                # print(f'From {[int(minimum), int(maximum)]} removing {remove_object[4]}')
                objects.remove(remove_object)
    if debug:
        print(domains)
    return domains


def generate_insulation_domains_y(table_objects, direction, page, debug=False):
    """
    USED!
    :param table_objects:
    :param direction:
    :param page:
    :param debug:
    :return:
    """
    objects = table_objects[:]
    domains = []

    if direction == 'H':
        i = 0
    else:
        i = 1

    # Find left most object
    while len(objects) > 0:
        # if debug:
        #     print(f'New Cycle, {len(objects)} objects left')

        minimum = objects[0][i + 2]
        minimum_object = objects[0]

        for object in objects:
            if minimum > object[i]:
                if object[4] == "kg/one":
                    minimum = object[i] + 5
                    minimum_object = object
                else:
                    minimum = object[i]
                    minimum_object = object
        # if debug:
        # print(f'New cycle min object: {minimum_object[4]}')
        # draw_object(page, minimum_object)
        if object[4] == "Shape":
            maximum = minimum_object[i + 2] - 6
        else:
            maximum = minimum_object[i + 2]

        for object in objects:
            if object[i + 2] > maximum > middle_coordinate(object[i], object[i + 2]) - 2:
                if object[4] == "Shape":
                    maximum = object[i + 2] - 6
                else:
                    maximum = object[i + 2]
                # if debug:
                # print(f'Max object {object[4]}')
                # draw_object(page, object)
        if len(domains) > 2:
            first = domains[0]
            second = domains[1]
            interval = second[1] - first[1]



            last = domains[-1][1]



            next_interval = maximum - last

            if interval*2.5 < next_interval:
                break
        domains.append([int(minimum), int(maximum)])
        # if debug:
        #     print(f'{len(objects)} objects left')
        remove_objects = objects[:]
        for remove_object in remove_objects:

            middle = middle_coordinate(remove_object[i], remove_object[i + 2])
            # if debug:
            # print(f'{remove_object[4]} middle is {middle}, current domain: {[int(minimum), int(maximum)]}')

            if minimum <= middle <= maximum:
                # if debug:
                # print(f'From {[int(minimum), int(maximum)]} removing {remove_object[4]}')
                objects.remove(remove_object)
    if debug:
        print(domains)
    return domains[1:]


def sort_line(line_objects, debug=False):
    """
    USED!
    Function is expected to be used to sort header objects by ascending X coordinate. (Left to Right)
    :param line_objects: pdf word objects
    :param debug:
    :return: sorted list of domains (start, end)
    """
    domains = []
    for line_object in line_objects:
        start = int(line_object[0])
        end = int(line_object[2])
        domains.append([start, end])
    domains.sort(key=lambda x: x[0])
    return domains


def sort_word_object_line(line_objects, debug=False):
    """
    USED!
    Function is expected to be used to sort header objects by ascending X coordinate. (Left to Right)
    :param line_objects: pdf word objects
    :param debug:
    :return: sorted list of domains (start, end)
    """

    line_objects.sort(key=lambda x: x[0])
    return line_objects


def generate_x_domains(table_objects, debug=False):
    """
    USED!
    :param table_objects:
    :param debug:
    :return:
    """
    objects = table_objects[:]
    domains = []

    # Find header
    shape_object = ''
    header_obj_list = []
    for possible_shape_object in objects:
        if possible_shape_object[4] == "Shape":
            shape_object = possible_shape_object
            break
    min_y = shape_object[1]
    max_y = shape_object[3]

    for possible_header_object in objects:
        obj_min_y = possible_header_object[1]
        obj_max_y = possible_header_object[3]
        middle = middle_coordinate(obj_min_y, obj_max_y)
        if min_y < middle < max_y:
            header_obj_list.append(possible_header_object)
    header_domains = sort_line(header_obj_list)
    if debug:
        print(f'Header List: {header_obj_list}')
        print(f'Header Domains: {header_domains}')

    for object_to_remove in header_obj_list:
        objects.remove(object_to_remove)

    # Find left most object
    while len(objects) > 0:
        # if debug:
        #     print(f'New Cycle, {len(objects)} objects left')

        # Setup initial min x size, that will definitely be higher than at least one value looked at inside cycle
        minimum = objects[0][2]
        minimum_object = objects[0]

        # Find object most towards left
        for possible_minimum_object in objects:
            if minimum > possible_minimum_object[0]:
                minimum = possible_minimum_object[0]
                minimum_object = possible_minimum_object

        # if debug:
        # print(f'New cycle min object: {minimum_object[4]}')
        # draw_object(page, minimum_object)

        maximum = minimum_object[2]

        # "Rubber-band" the domain with other objects that should be in left-most domain
        for possible_stretching_object in objects:
            start = possible_stretching_object[0]
            end = possible_stretching_object[2]

            if end > maximum > start:
                maximum = end
                # if debug:
                # print(f'Max object {object[4]}')
                # draw_object(page, object)

        # Check if "Empty" domain should be added to domains, before adding new domain.

        while len(header_domains) > 0:
            current_header = header_domains.pop(0)
            header_start = current_header[0]
            header_end = current_header[1]
            if minimum > header_end:
                domains.append(current_header)
            else:
                break

        domains.append([int(minimum), int(maximum)])

        # if debug:
        #     print(f'{len(objects)} objects left')

        remove_objects = objects[:]
        for remove_object in remove_objects:
            start = remove_object[0]
            end = remove_object[2]
            middle = middle_coordinate(start, end)

            # if debug:
            # print(f'{remove_object[4]} middle is {middle}, current domain: {[int(minimum), int(maximum)]}')

            if minimum <= middle <= maximum:
                # if debug:
                # print(f'From {[int(minimum), int(maximum)]} removing {remove_object[4]}')
                objects.remove(remove_object)
    if debug:
        print(domains)
    return domains


def generate_insulation_x_domains(table_objects, debug=False):
    """
    USED!
    :param table_objects:
    :param debug:
    :return:
    """
    objects = table_objects[:]
    domains = []

    # Find left most object
    while len(objects) > 0:
        # if debug:
        #     print(f'New Cycle, {len(objects)} objects left')

        # Setup initial min x size, that will definitely be higher than at least one value looked at inside cycle
        minimum = objects[0][2]
        minimum_object = objects[0]

        # Find object most towards left
        for possible_minimum_object in objects:
            if minimum > possible_minimum_object[0]:
                minimum = possible_minimum_object[0]
                minimum_object = possible_minimum_object

        # if debug:
        # print(f'New cycle min object: {minimum_object[4]}')
        # draw_object(page, minimum_object)

        maximum = minimum_object[2]

        # "Rubber-band" the domain with other objects that should be in left-most domain
        for possible_stretching_object in objects:
            start = possible_stretching_object[0]
            end = possible_stretching_object[2]

            if end > maximum > start:
                maximum = end
                # if debug:
                # print(f'Max object {object[4]}')
                # draw_object(page, object)

        # Check if "Empty" domain should be added to domains, before adding new domain.

        domains.append([int(minimum), int(maximum)])

        # if debug:
        #     print(f'{len(objects)} objects left')

        remove_objects = objects[:]
        for remove_object in remove_objects:
            start = remove_object[0]
            end = remove_object[2]
            middle = middle_coordinate(start, end)

            # if debug:
            # print(f'{remove_object[4]} middle is {middle}, current domain: {[int(minimum), int(maximum)]}')

            if minimum <= middle <= maximum:
                # if debug:
                # print(f'From {[int(minimum), int(maximum)]} removing {remove_object[4]}')
                objects.remove(remove_object)
    if debug:
        print(domains)
    return domains


def draw_cv2_page_domains(page, domains, direction):
    """
    USED!
    For debug
    :param page:
    :param domains:
    :param direction:
    :return:
    """
    pix = page.get_pixmap()
    if direction == 'H':
        min_y = 0
        max_y = pix.h
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
        for domain in domains:
            bottom_left = (domain[0], min_y)
            top_right = (domain[1], max_y)
            cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
        cv2.imshow("Preview", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        min_x = 0
        max_x = pix.w
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
        for domain in domains:
            bottom_left = (min_x, domain[0])
            top_right = (max_x, domain[1])
            cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
        cv2.imshow("Preview", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def create_array_from_word_objects(table_objects, page, debug=False):
    """
    USED!
    :param table_objects:
    :param all_words:
    :param page:
    :param debug:
    :return:
    """
    domains_x = generate_x_domains(table_objects, debug)
    if debug:
        draw_cv2_page_domains(page, domains_x, 'H')
    domains_y = generate_domains(table_objects, 'V', page, debug)
    if debug:
        draw_cv2_page_domains(page, domains_y, 'V')

    array = []
    for row in domains_y:
        new_line = []
        # if debug:
        #     print(f'Checking {row}')
        for column in domains_x:
            # if debug:
            #     print(f'Checking {column}')
            min_x = column[0]
            max_x = column[1]
            min_y = row[0]
            max_y = row[1]
            flag = False
            # print(min_x,max_x,min_y, max_y)
            for word in table_objects:
                middle_x = middle_coordinate(word[0], word[2])
                middle_y = middle_coordinate(word[1], word[3])
                # if debug:
                #     print(f'Checking {word}')
                if min_x < middle_x < max_x:
                    # print(f'Middle X is correct, checking middle y {min_y} < {middle_y} < {max_y}')
                    # print(word)
                    if min_y < middle_y < max_y:
                        # print(f'Middle Y is correct')
                        new_line.append(word[4])
                        flag = True
                        break
            if not flag:
                new_line.append('')
        if new_line[0] == "Shape":
            print(f'Skipping {new_line}')
            continue
        array.append(new_line)
    # for line in array:
    #     print(line)
    return array


def create_embed_array_from_word_objects(table_objects, page, debug=False):
    """
    USED!
    :param table_objects:
    :param all_words:
    :param page:
    :param debug:
    :return:
    """
    domains_y = generate_domains(table_objects, 'V', page, debug)
    if debug:
        draw_cv2_page_domains(page, domains_y, 'V')

    array = []
    for row in domains_y:
        new_line = []
        # if debug:
        #     print(f'Checking {row}')
        min_y = row[0]
        max_y = row[1]
        flag = False
        # print(min_x,max_x,min_y, max_y)
        for word in table_objects:
            middle_y = middle_coordinate(word[1], word[3])
            # if debug:
            #     print(f'Checking {word}')
            if min_y < middle_y < max_y:
                # print(f'Middle Y is correct')
                new_line.append(word)
        array.append(sort_word_object_line(new_line))
    temp_array = []
    for line in array:
        # print(line)
        new_line = Common.join_nearby_word_objects_together(line, tolerance=4)
        temp_line = []
        for word in new_line:
            temp_line.append(word[4])
        # print(temp_line)
        temp_array.append(temp_line)

    return temp_array



def create_insulation_array_from_word_objects(table_objects, page, debug=False):
    """
    USED!
    :param table_objects:
    :param all_words:
    :param page:
    :param debug:
    :return:
    """

    domains_y = generate_insulation_domains_y(table_objects, 'V', page, debug)
    if debug:
        draw_cv2_page_domains(page, domains_y, 'V')

    filtered_table_objects = []
    max_y = domains_y[-1][1]
    min_y = domains_y[0][0]
    for word in table_objects:
        start = word[1]
        end = word[3]
        middle = middle_coordinate(start, end)
        if min_y < middle < max_y:
            filtered_table_objects.append(word)

    table_objects = filtered_table_objects

    if debug:
        PDF_read_text.draw_cv2_page(table_objects, page)

    domains_x = generate_insulation_x_domains(table_objects, debug)

    if debug:
        draw_cv2_page_domains(page, domains_x, 'H')

    array = []
    for row in domains_y:
        new_line = []
        # if debug:
        #     print(f'Checking {row}')
        for column in domains_x:
            # if debug:
            #     print(f'Checking {column}')
            min_x = column[0]
            max_x = column[1]
            min_y = row[0]
            max_y = row[1]
            flag = False
            # print(min_x,max_x,min_y, max_y)
            for word in table_objects:
                middle_x = middle_coordinate(word[0], word[2])
                middle_y = middle_coordinate(word[1], word[3])
                # if debug:
                #     print(f'Checking {word}')
                if min_x < middle_x < max_x:
                    # print(f'Middle X is correct, checking middle y {min_y} < {middle_y} < {max_y}')
                    # print(word)
                    if min_y < middle_y < max_y:
                        # print(f'Middle Y is correct')
                        new_line.append(word[4])
                        flag = True
                        break
            # if not flag:
            #     new_line.append('')
        if "INS." not in new_line[0]:
            print('Skipping new line')
            print(new_line)
            continue

        array.append(new_line)
    # for line in array:
    #     print(line)
    return array
