import os


import PDF_read_text
import Array_clean_up_shapes
import Array_verify
import Embeds


def get_reinforcement_array(file_path, debug_list):
    debug = True if "reinforcement_table" in debug_list else False

    reinforcement_table_exists, page_number, all_words = PDF_read_text.table_exists(file_path, debug=debug)

    if not reinforcement_table_exists:
        return None

    reinforcement_array = PDF_read_text.create_array(file_path, all_words, page_number, debug)
    return reinforcement_array


def get_embed_array(file_path, debug_list):
    debug = True if "embed_table" in debug_list else False

    embed_table_exists, page_number, all_words = PDF_read_text.embed_table_exists(file_path, debug=debug)

    if not embed_table_exists:
        return None, None

    full_embed_array = PDF_read_text.create_embed_array(file_path, all_words, page_number, debug)

    embed_array, material_array = Embeds.clean_up_embed_array(full_embed_array)

    return embed_array, material_array

def get_insulation_array(file_path, debug_list):
    debug = True if "insulation_table" in debug_list else False

    insulation_table_exists, page_number, all_words = PDF_read_text.insulation_table_exists(file_path, debug=debug)

    if not insulation_table_exists:
        return None

    insulation_array = PDF_read_text.create_insulation_table_array(file_path, all_words, page_number, debug)

    return insulation_array




def get_arrays(file_path, debug_list):
    debug = True if "arrays" in debug_list else False

    if debug:
        print(f'File path: {file_path}')

    reinforcement_array = get_reinforcement_array(file_path, debug_list)
    if debug:
        print(f'Reinforcement array: {reinforcement_array}')

    embed_array, material_array = get_embed_array(file_path, debug_list)
    if debug:
        print(f'Embed array: {embed_array}')
        print(f'Material array: {material_array}')

    insulation_array = get_insulation_array(file_path, debug_list)
    if debug:
        print(f'Insulation array: {insulation_array}')

    return [reinforcement_array, embed_array, material_array, insulation_array]


