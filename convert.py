import Levenshtein as lev

# 特殊字段字典，键为特殊字段，值为需要修改的值
special_fields = {
    "Timor-Leste": "East Timor",
    "Iran (Islamic Republic of)": "Iran",
    "Republic of Moldova": "Moldova",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Congo": "Republic of the Congo",
    # "Somalia": "Somaliland",
    # 以下国家无数据
    # "": "Ivory Coast",
    # "": "Kosovo",
}


def find_best_match(query, candidates):
    """在候选列表中找到与查询字符串最相似的项"""
    best_match = None
    min_distance = float("inf")

    for candidate in candidates:
        distance = lev.distance(query, candidate)
        if distance < min_distance:
            min_distance = distance
            best_match = candidate

    return best_match


def convert(input, standard_format_data, output=None):
    # 首先检查是否是特殊字段
    if input in special_fields:
        return special_fields[input]

    # 对传入的国家名，在标准化列表中查找最相似的国家名
    best_match = find_best_match(input, standard_format_data)
    if best_match:
        result = best_match
    else:
        result = input  # 如果没有找到匹配项，则保留原名

    return result
