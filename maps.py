# https://github.com/pyecharts/pyecharts
# pyecharts==1.9.1

import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot

from convert import convert

# from pyecharts_snapshot.main import make_a_snapshot

# example data
# data = [
#     ("United States", 2900),
#     ("China", 3300),
#     ("Brazil", 2000),
#     ("Canada", 1800),
#     # 更多的国家及其对应的数据值...
# ]


def read_file(file_name):
    """读取文件，返回包含每行内容的列表"""
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def create_map(data, name):
    max_value = max([value for _, value in data])
    # 创建Map对象
    map_chart = (
        Map()
        # 添加数据，并设置标签样式
        .add(name, data, maptype="world", label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=name),
            # 设置视觉映射选项, is_piecewise是否使用分段
            visualmap_opts=opts.VisualMapOpts(max_=max_value, is_piecewise=False),
            # 设置提示信息显示
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .set_series_opts(showLegendSymbol=False)  # 是否显示地理信息标记(小红点)
    )
    # 渲染图表
    output_html = map_chart.render(f"{name}.html")
    # 保存为图片
    make_snapshot(snapshot, output_html, f"{name}.png")


def get_map(file_path, standard_format_data):
    df = pd.read_excel(file_path)
    locations = df["location"].values.tolist()
    data_columns = df.columns[1:5]
    # 生成4个热力图
    for column in data_columns:
        country_names = []
        data = []
        for loc, value in zip(locations, df[column].values):
            if loc not in country_names:
                country_names.append(loc)
                value = round(float(value.split(" ")[0]), 1)
                if loc == "Somalia":  # 地图上分为两块
                    country_names.append(loc)
                    data.append((loc, value))
                    data.append(("Somaliland", value))
                else:
                    loc = convert(loc, standard_format_data)
                    data.append((loc, value))
        create_map(data, column)


if __name__ == "__main__":
    data_path = "data.xlsx"
    standard_format_data = read_file("pyecharts_country_names.txt")
    data = get_map(data_path, standard_format_data)
