import PDF_read_files
import time
import os
import PDF_read_text
import Array_clean_up_shapes
import Array_verify
import bvbs_creator
import Calculate_insulation
import csv
import Embeds


def generate_specifications(source_directory, destination_directory, debug=False):
    file_names = PDF_read_files.get_file_names(source_directory)

    # List with dictionaries, where each file has dictionary and info,
    # if it has reinforcement, embed and insulation tables
    files_status = []

    full_insulation_specification = []
    full_bruto_neto_specification = []

    files_with_no_embeds = []
    files_with_embeds = []

    total_area_dict = {}
    total_volume_dict = {}
    thickness_set = set()
    position_set = set()

    shape_set = set()
    shape_dict = {}

    total_file_count = len(file_names)
    print(f'Source directory: {source_directory}')
    print(f'Total {total_file_count} files in Source Directory')

    number = 0
    for file_name in file_names:
        start_time = time.time()
        number += 1

        file_status = {"name": file_name}
        file_path = os.path.join(source_directory, file_name)

        # Get reinforcement and create bvbs
        reinforcement_table_exists, page_number, all_words = PDF_read_text.table_exists(file_path, debug=debug)
        if not reinforcement_table_exists:
            file_status["reinforcement"] = "NO"
        if reinforcement_table_exists:
            file_status["reinforcement"] = "OK"
            reinforcement_array = PDF_read_text.create_array(file_path, all_words, page_number, debug)
            cleaned_up_reinforcement_array = Array_clean_up_shapes.clean_array(reinforcement_array, debug)
            correct, result = Array_verify.verify_table(cleaned_up_reinforcement_array, debug)
            for row in reinforcement_array:
                if row[0] not in shape_set:
                    shape_set.add(row[0])
                    shape_dict[row[0]] = 0
                shape_dict[row[0]] += 1
            if correct:
                bvbs_creator.create_abs(cleaned_up_reinforcement_array, file_name, destination_directory)
                file_status["bvbs"] = "OK"
            else:
                file_status["bvbs"] = "NO"

        # Get insulation table
        insulation_table_exists, page_number, all_words = PDF_read_text.insulation_table_exists(file_path,
                                                                                                debug=debug)
        if not insulation_table_exists:
            file_status["insulation"] = "NO"
        if insulation_table_exists:
            try:
                insulation_array = PDF_read_text.create_insulation_table_array(file_path, all_words, page_number,
                                                                               debug)

                insulation_array = Calculate_insulation.split_insulation_table(insulation_array)
                area_dict, volume_dict = Calculate_insulation.calculate_insulation(insulation_array)
                if "Rev" in file_name:
                    name = file_name[:-10]
                else:
                    name = file_name[:-4]
                wall_insulation_volume = 0
                for line in insulation_array:
                    if line[0] == '':
                        continue
                    line[2] = int(line[2])
                    dimensions = line[1].split('*')
                    dimensions = sorted([int(x) for x in dimensions])
                    volume = dimensions[0] * dimensions[1] * dimensions[2] / 10 ** 9
                    total_volume = volume * line[2]
                    wall_insulation_volume += total_volume
                    new_line = [name] + line + dimensions + [volume] + [total_volume]
                    full_insulation_specification.append(new_line)

                file_status["insulation"] = "OK"
                file_status["insulation_bruto"] = round(wall_insulation_volume, 2)
            except:
                file_status["insulation"] = "BAD"

        embed_table_exists, page_number, all_words = PDF_read_text.embed_table_exists(file_path, debug=debug)

        if not embed_table_exists:
            files_with_no_embeds.append(file_name)

        if embed_table_exists:

            array = PDF_read_text.create_embed_array(file_path, all_words, page_number, debug)

            embed_array, material_array = Embeds.clean_up_embed_array(array)

            files_with_embeds.append(file_name)

            for material in material_array:
                if "Frontrock" in material[0] or "Insulation" in material[0]:
                    file_status["insulation_neto"] = material[2]
                    if file_status["insulation"] == "NO":
                        wall_insulation_volume = 0
                        for embed in embed_array:
                            if "Frontrock" in embed[3]:
                                if "Rev" in file_name:
                                    name = file_name[:-10]
                                else:
                                    name = file_name[:-4]
                                file_status["insulation"] = "OK"
                                embed[2] = int(embed[2])
                                dimensions = embed[1].split('*')
                                dimensions = sorted([round(float(x), 0) for x in dimensions])
                                volume = dimensions[0] * dimensions[1] * dimensions[2] / 10 ** 9
                                total_volume = volume * embed[2]
                                wall_insulation_volume += total_volume
                                new_line = [name] + embed[:3] + dimensions + [volume] + [total_volume]
                                full_insulation_specification.append(new_line)
                        if file_status["insulation"] == "OK":
                            file_status["insulation_bruto"] = round(wall_insulation_volume, 2)

        files_status.append(file_status)

        end_time = round(time.time() - start_time, 2)
        try:
            reinf = file_status["reinforcement"]
        except:
            reinf = "NO"
        try:
            bvbs = file_status["bvbs"]
        except:
            bvbs = "NO"
        try:
            insulation = file_status["insulation"]
        except:
            insulation = "NO"
        try:
            neto = round(float(file_status["insulation_neto"]), 2)
        except:
            neto = "NO"
        try:
            bruto = round(file_status["insulation_bruto"], 2)
        except:
            bruto = "NO"
        try:
            percentage = round(100 * (1 - neto / bruto), 1)
        except:
            percentage = '-'

        if insulation == "OK":
            neto_bruto_line = [file_name, bruto, neto, percentage]
            full_bruto_neto_specification.append(neto_bruto_line)

        print(
            f'{number:>4}/{total_file_count:<4} | {file_name:<20}| T{end_time:<6}| R-{reinf} | B-{bvbs} | I-{insulation} | Br {bruto:>5} | Ne {neto:>5} | {percentage:>4} |')

    with open('InsulationData.csv', 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Panel',
                         'Position',
                         'Dimensions',
                         'Qty',
                         'Height',
                         'Width',
                         'Length',
                         'Volume (m3)',
                         'Total Volume (m3)'])

        # Write the data rows
        for row in full_insulation_specification:
            writer.writerow(row)

    with open('InsulationBrutoNeto.csv', 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Panel',
                         'Bruto',
                         'Neto',
                         'Difference %'])

        # Write the data rows
        for row in full_bruto_neto_specification:
            writer.writerow(row)



