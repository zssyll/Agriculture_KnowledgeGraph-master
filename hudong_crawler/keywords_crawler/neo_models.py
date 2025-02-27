# coding: utf-8

from py2neo import Graph,Node,Relationship
from hudong_class import HudongItem
from constants import constant_url

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
		
	def connectDB(self):
		self.graph = Graph(constant_url.NEO4J_URL, username=constant_url.NEO4J_USERNAME, password=constant_url.NEO4J_PASSWORD)
		print('connect successed')
		
	def matchItembyTitle(self,value):
		answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回互动百科item
	def matchHudongItembyTitle(self,value):
		answer = self.graph.find_one(label="HudongItem",property_key="title",property_value=value)
		return answer
			
	# 返回限定个数的互动百科item
	def getAllHudongItem(self, limitnum):
		List = []
		ge = self.graph.find(label="HudongItem", limit=limitnum)
		for g in ge:
			List.append(HudongItem(g))
			
		print('load AllHudongItem over ...')
		return List
		
		
#test = Neo4j()
#test.connectDB()
#a = test.getLabeledHudongItem('labels.txt')
#print(a[10].openTypeList)