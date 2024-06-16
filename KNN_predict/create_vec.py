# coding: utf-8
# 将csv转化为词向量
from neo_models import Neo4j
from read_csv import readCSVbyColumn
from hudong_class import HudongItem
from pyfasttext import FastText
from constants import constant_url


def create_predict(HudongItem_csv):
    # 读取neo4j内容
    db = Neo4j()
    db.connectDB()

    predict_List = readCSVbyColumn(HudongItem_csv, 'title')
    file_object = open('vector_use_neo4j.txt', 'a')
    not_in_neo4j = open('not_in_neo4j.txt', 'a')

    model = FastText(constant_url.MODEL_PATH)

    count = 0
    vis = set()
    for p in predict_List:

        res = db.matchHudongItembyTitle(p)
        if res is None:
            not_in_neo4j.write(p + "\n")
            continue
        cur = HudongItem(res)
        count += 1
        title = cur.title
        # title = p
        if title in vis:
            continue
        vis.add(title)
        wv_list = model[title]
        strr = str(title)
        for p in wv_list:
            strr += ' ' + str(p)[:7]
        file_object.write(strr + "\n")
        print(str(count) + ' / ' + str(len(predict_List)))
    file_object.close()
    not_in_neo4j.close()

create_predict(constant_url.HUDONG_WHEAT_CSV)
