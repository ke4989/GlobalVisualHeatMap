import re


def extract_names_from_js(file_path):
    # "name":"Siachen Glacier","full_name":"Siachen Glacier"
    name_pattern = re.compile(r'"name":"(.*?)","full_name":"(.*?)"')
    names = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            matches = name_pattern.findall(line)
            for match in matches:
                names.append(match[0])

    return names


# https://assets.pyecharts.org/assets/maps/world.js
file_path = "world.js"

names = extract_names_from_js(file_path)
with open("pyecharts_country_names.txt", "w", encoding="utf-8") as file:
    for name in names:
        file.write(name + "\n")
