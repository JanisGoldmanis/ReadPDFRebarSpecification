table1 = {'Shape': 'U', 'Pos': 'AK.26.6', 'Pcs': '20', 'Grade': 'B500B', 'Diam': '12', 'L': '1840', 'a': '163', 'b': '525', 'c': '302', 'd': '525', 'e': '302', 'u': '', 'v': '', 'D': '48', 'kg/1': '1.6', 'kg/all': '32.8'}
table2 = {'Shape': '', 'Pos': '', 'Pcs': '', 'Grade': '', 'Diam': '', 'L': '', 'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'u': '163', 'v': '500', 'D': '', 'kg/1': '', 'kg/all': ''}

new_table = {}

for key in table1:
    new_table[key] = table1[key]

if table2.get("u"):
    new_table["f"] = table2["u"]
    if table2.get("v"):
        new_table["g"] = table2["v"]

sorted_keys = sorted(new_table.keys())
final_table = {key: new_table[key] for key in sorted_keys}

print(final_table)