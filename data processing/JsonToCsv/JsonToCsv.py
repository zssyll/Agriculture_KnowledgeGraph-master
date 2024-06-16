# -*- coding:utf8 -*-

"""
Title: JSON data convert to CSV
Author: Honyelchak
"""

import json
import csv


def json_to_csv():
    json_fp = open("./hudong_wheat.json", "r")
    csv_fp = open("./hudong_wheat.csv", "w")

    data_list = json.load(json_fp)
    # create sheet title
    sheet_title = data_list[0].keys()
    # save sheet data
    sheet_data = []

    for data in data_list:
        sheet_data.append(data.values())

    writer = csv.writer(csv_fp)
    writer.writerow(sheet_title)
    for row_data in sheet_data:
        writer.writerow(row_data)

    json_fp.close()
    csv_fp.close()


json_to_csv()