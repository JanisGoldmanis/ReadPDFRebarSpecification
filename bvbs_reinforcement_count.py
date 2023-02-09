reinforcement_count = {'A': 3034, 'D': 4067, 'E': 700, 'J': 101, 'U': 228, 'XB': 152, '49': 15, 'C': 1150, 'Y': 1006, 'B': 1486, 'F': 30, 'R': 732, 'XE': 4, 'YM': 279, 'Z': 105, 'G': 141, 'XA': 44, 'K': 21, '44': 16, 'YE': 103, 'YH': 19, 'YJ': 14, '72': 70, 'M': 4, 'N': 51, 'YG': 19, '51': 9, '79_1': 5, '69_1': 4, '14_5': 1, '29_2': 8, '67_2': 11, '67_3': 14, 'Q': 3}

sorted_dict = sorted(reinforcement_count.items(), key=lambda item: item[1], reverse=True)
for key, value in sorted_dict:
    print(key, value)
sum_of_values = sum(value for value in reinforcement_count.values())

print(sum_of_values)

shapes_groups = {
    "straight": ["A"],
    "bent_1": ["B"],
    "bent_1_1": ["C"],
    "bent_2": ["D"],
    "bent_2_1": ["J"],
    "bent_2_2": ["E"],
    "bent_3": ["72","XB","YM"],
    "bent_3_1": [],
    "bent_4": ["R", "Y", "U"],
    "bent_4_2": ["44","G", "Z"]
}

total_count = 0
not_counted_keys = []
for group, keys in shapes_groups.items():
    for key in keys:
        if key in reinforcement_count:
            total_count += reinforcement_count[key]
        else:
            not_counted_keys.append((key, group))

print(total_count)
print(not_counted_keys)