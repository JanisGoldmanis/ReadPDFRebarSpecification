# This list is used for generating CSV report, it should be in ascending order.
# insulation_allowed_thickness = [20, 50, 100, 150, 200, 250]

with open('Allowed_insulation_size.txt', 'r') as file:
    array = file.readlines()

insulation_allowed_thickness = [int(x) for x in array[0].split(',')]