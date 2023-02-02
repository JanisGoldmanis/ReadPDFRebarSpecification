from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfpage import PDFPage

import Table

debug = True


def generate_domains(min_v, max_v, n, char_height=5.7, space_height=2.1):
    """
    :param n:
    :param min_v: Table min Y dimension
    :param max_v: Table max Y dimension
    :param char_height: Character height, should be ~5,7
    :param space_height: Clear space between rows, ~2.1-2.3
    :param debug: generate console printouts
    :return: list of start/end for each row Y coordinate domain
    """
    domains = []
    max_v = round(max_v - space_height, 1)
    for num in range(n):
        domains.append([max_v, round(max_v - char_height, 1)])
        max_v = round(max_v - (char_height + space_height), 1)
    return domains


def generate_list_of_values(valid_objects, domains, row_height=5.7):
    """
    Given a list of pdf text objects, function returns left most column of objects split into rows.
    If multiple objects have similar X coordinate, they are combined.
    If objects have blank rows in column, blank entries are returned inside list.
    """
    result = []
    for _ in domains:
        result.append('')

    # Getting left-most object
    first_column_x_domain = [valid_objects[0].bbox[0], 0]
    most_left_object = valid_objects[0]
    most_left_objects = []
    for lt_obj in valid_objects:
        if lt_obj.bbox[0] < first_column_x_domain[0]:
            first_column_x_domain[0] = lt_obj.bbox[0]
            first_column_x_domain[1] = lt_obj.bbox[2]
            most_left_object = lt_obj
    if first_column_x_domain[1] == 0:
        first_column_x_domain[1] = most_left_object.bbox[2]

    most_left_objects.append(most_left_object)

    valid_objects.remove(most_left_object)

    min_x = first_column_x_domain[0]
    max_x = first_column_x_domain[1]

    # adjust first_column_domain with others who are overlapping it when comparing X coordinate.
    for lt_obj in valid_objects[:]:
        if min_x < lt_obj.bbox[0] + (lt_obj.bbox[2] - lt_obj.bbox[0]) / 2 < max_x:
            if lt_obj.bbox[2] > max_x:
                max_x = lt_obj.bbox[2]
            most_left_objects.append(lt_obj)
            valid_objects.remove(lt_obj)

    # Generating table column from objects that are "most" to the left
    for obj in most_left_objects:
        text = obj.get_text()
        n_rows = text.count('\n')
        list = text.split('\n')[:-1]  # All text objects had new row symbol at the end of them
        text_domains = generate_domains(obj.bbox[1], obj.bbox[3], n_rows)
        for index in range(len(text_domains)):
            text_domain = text_domains[index]
            text_entry = list[index]
            center = text_domain[0] + (text_domain[1] - text_domain[0]) / 2

            for result_index in range(len(domains)):
                result_domain = domains[result_index]
                if result_domain[0] > center > result_domain[1]:
                    result[result_index] = text_entry
    return result


# Open the PDF file
with open("A3.COW.2.2.pdf", "rb") as file:
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(char_margin=1, word_margin=1, boxes_flow=0, detect_vertical=True)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(file, set(), maxpages=1):
        interpreter.process_page(page)
        layout = device.get_result()

        # Initialize table corner coordinates
        top_left = [0, 0]
        bot_right = [0, 0]

        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                if "Reinforcement specification:" in lt_obj.get_text():
                    print(lt_obj.bbox)
                    print(lt_obj.get_text())
                    top_left = [round(lt_obj.bbox[0], 1), round(lt_obj.bbox[1], 1)]
                if "kg/all" in lt_obj.get_text():
                    print(lt_obj.bbox)
                    print(lt_obj.get_text())
                    if bot_right[0] < lt_obj.bbox[2]:
                        bot_right[0] = round(lt_obj.bbox[2], 1)
                if "Reinforcement total weight (kg):" in lt_obj.get_text():
                    print(lt_obj.bbox)
                    print(lt_obj.get_text())
                    bot_right[1] = round(lt_obj.bbox[3], 1)

        table = Table.Table(top_left[0], bot_right[0], bot_right[1], top_left[1])
        print(f'Number of rows:{table.n}')
        print(f'Height:{table.height}')

        table.y_domains = generate_domains(table.min_y, table.max_y, table.n, table.row_height, table.blank_height)
        # print(table.y_domains)

        # Filtering from all objects - which object bbox center is inside table
        valid_objects = []
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                center_point = [lt_obj.bbox[0] + (lt_obj.bbox[2] - lt_obj.bbox[0]) / 2,
                                lt_obj.bbox[1] + (lt_obj.bbox[3] - lt_obj.bbox[1]) / 2]
                if table.min_x < center_point[0] < table.max_x:
                    if table.min_y < center_point[1] < table.max_y:
                        valid_objects.append(lt_obj)

        # Generating Column data

        result = []

        for i in range(9):
            result.append(generate_list_of_values(valid_objects, table.y_domains))

        for i in range(2):
            result.append(generate_list_of_values(valid_objects, table.y_domains))

        while len(valid_objects) > 0:
            result.append(generate_list_of_values(valid_objects, table.y_domains))


        def transform_table(array):
            # Flips the table matrix
            result = []
            for row_index in range(len(array[0])):
                row = []
                for column_index in range(len(array)):
                    row.append(array[column_index][row_index])
                result.append(row)
            return result


        new_table = transform_table(result)

        header = ['Shape', 'Pos', 'Pcs', 'Grade', 'Diam', 'L', 'a', 'b', 'c', 'd', 'e', 'u', 'v', 'D', 'kg/1', 'kg/all']

        # Inserting missing columns
        column_count = len(header)
        table_column_count = len(new_table[0])
        difference = column_count - table_column_count

        for i in range(difference):
            for row in new_table:
                row.insert(-3, '')

        new_table.insert(0, header)
        for row in new_table:
            for item in row:
                print(f'{item:>5}|', end='')
            print()

        # Result array by rows: new_table
        # Result array by columns: result

        # for line in new_table:
        #     print(line)

