from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource
import os
from pathlib import Path

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / 'outputs'

LINE_COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'brown']


def bokeh_line(lines_data, title='利用率趨勢', y_label='利用率 (%)', save_name=None):
    """
    使用 Bokeh 绘制多条折线的时间序列图。

    :param lines_data: 多条线的数据列表, 格式:
        [[time_list, value_list, line_name], [time_list, value_list, line_name], ...]
    :param title:   图表标题
    :param y_label: Y轴标签
    :param save_name: 输出文件路径, None 则自动保存到 outputs/{title}.html
    """
    p = figure(height=400, width=700, title=title,
               x_axis_type="datetime", x_axis_label='时间', y_axis_label=y_label,
               y_range=(0, 100))

    for i, (time_list, value_list, line_name) in enumerate(lines_data):
        color = LINE_COLORS[i % len(LINE_COLORS)]
        source = ColumnDataSource(data={
            'time': time_list,
            'time_str': [t.strftime("%Y-%m-%d %H:%M:%S") for t in time_list],
            'value': value_list
        })
        p.line(x='time', y='value', source=source, line_width=2,
               color=color, legend_label=line_name)
        p.scatter(x='time', y='value', source=source, size=5,
                  color=color, alpha=0.5)

    hover = HoverTool(tooltips=[("時間", "@time_str"), ("值", "@value%")], mode='vline')
    p.add_tools(hover)

    p.xaxis.formatter = DatetimeTickFormatter(
        minutes="%H:%M",
        hours="%H:%M",
        days="%m-%d"
    )
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_filename = save_name if save_name else str(OUTPUTS_DIR / f"{title}.html")
    output_file(output_filename, title=title)
    save(p)
    print(f"[*] Bokeh 折線圖已生成: {output_filename}")