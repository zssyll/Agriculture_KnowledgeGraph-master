# -*- coding:utf8 -*-
import os

# Noe4j connection configure
NEO4J_URL = "http://192.168.0.108:7474"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "root"

# MongdDB connection configure
MONGODB_IP_URL = "192.168.0.108"
MONGODB_PORT = 27017


# model path
MODEL_PATH = "/home/admin/Downloads/wiki.zh.bin"
HUDONG_WHEAT_CSV = os.path.abspath("..") + "/data/hudong_wheat.csv"
PREDICT_LABELS = os.path.abspath("../..") + "/data/predict_labels_wheat.txt"
ENTITIES_JSON = os.path.abspath("../..") + "/data/entities.json"

