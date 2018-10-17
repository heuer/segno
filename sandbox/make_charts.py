# -*- encoding: utf-8 -*-
"""\
Create the benchmark charts.
"""
import csv
from decimal import Decimal
import pygal


def create_chart(title, data, filename):
    chart = pygal.HorizontalBar(title=title, x_title='Time (ms)', js=(),
                                print_labels=True, show_legend=False)
    for name, val in data:
        chart.add(name, val)
    chart.render_to_file(filename)


def create_charts():
    color_map = {
        'PyQRCode': '#F44336',
        'qrcode': '#3F51B5',
        'qrcode path': '#3F51B5',
        'qrcode rects': '#26854F',
        'qrcodegen': '#009688',
        'Segno': '#FFC107',
    }
    create_data = []
    svg_data = []
    png_data = []
    with open('out/results.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            name, val = row
            if name.endswith(' create'):
                create_data.append((name.replace(' create', ''), val))
            elif name.endswith(' PNG'):
                png_data.append((name.replace(' PNG', ''), val))
            elif ' SVG' in name:
                svg_data.append((name.replace(' SVG', ''), val))
    for data, title, filename in ((create_data, 'Create a 1-M QR Code', 'out/chart_create.svg'),
                                  (svg_data, 'Create a 1-M QR Code and write SVG', 'out/chart_svg.svg'),
                                  (png_data, 'Create a 1-M QR Code and write PNG', 'out/chart_png.svg')):
        create_chart(title,
                     [(name, [{'value': float(val), 'color': color_map[name], 'label': name}]) for name, val in sorted(data, key=lambda t: Decimal(t[1]))],
                     filename)


if __name__ == '__main__':
    create_charts()
