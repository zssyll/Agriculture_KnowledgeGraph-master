# coding: utf-8
from pyfasttext import FastText
from constants import constant_url

def text():
	model = FastText(constant_url.MODEL_PATH)
	print('load over..')
	s1 = '启航'
	s2 = '董启航'
	s3 = ' 董启文'
	print(model.nearest_neighbors('小麦', k=5))

text()