import numpy as np
import cv2


class Table:
    def __init__(self, min_x, max_x, min_y, max_y, row_height=6, blank_height=3.2):
        self.min_x = int(round(min_x, 0))
        self.max_x = int(round(max_x, 0))
        self.min_y = int(round(min_y, 0))
        self.max_y = int(round(max_y, 0))

        self.columns = [21, 42, 57, 82, 98, 119, 140, 163, 184, 209, 230, 254, 275, 296, 317]

        self.height = round(max_y - min_y, 1)

        self.row_height = row_height
        self.blank_height = blank_height

        self.n = int(self.height / (self.row_height + self.blank_height))

        self.x_domains = []
        self.y_domains = []

    def __str__(self):
        return f'Bottom Corner {self.min_x},{self.min_y}, Top Corner {self.max_x},{self.max_y}'


def middle_coordinate(start, end):
    return start + (end - start) / 2


def draw_object(page, object):
    pix = page.get_pixmap()
    min_x = int(object[0])
    min_y = int(object[1])
    max_x = int(object[2])
    max_y = int(object[3])
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    bottom_left = (min_x, min_y)
    top_right = (max_x, max_y)
    cv2.rectangle(img, bottom_left, top_right, (255, 0, 0), 2)
    cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_domains(table_objects, direction, page, debug=False):
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
                    minimum = object[i]+5
                    minimum_object = object
                else:
                    minimum = object[i]
                    minimum_object = object
        # if debug:
            # print(f'New cycle min object: {minimum_object[4]}')
            # draw_object(page, minimum_object)
        if object[4] == "Shape":
            maximum = minimum_object[i+2]-6
        else:
            maximum = minimum_object[i + 2]

        for object in objects:
            if object[i + 2] > maximum > middle_coordinate(object[i],object[i+2])-2:
                if object[4] == "Shape":
                    maximum = object[i + 2] - 6
                else:
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


def draw_cv2_page_domains(page, domains, direction):
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
    domains_x = generate_domains(table_objects, 'H', page, debug)
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
            continue
        array.append(new_line)
    return array




