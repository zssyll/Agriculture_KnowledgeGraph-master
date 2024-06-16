import json
from py2neo import Node, Relationship ,Graph
from langconv import *
import re
from constants import constant_url
class loadDatatoNeo4j(object):
	graph = None
	def __init__(self):
		print("start load data ...")
	def connectDB(self):
		self.graph = Graph(constant_url.NEO4J_URL, username = constant_url.NEO4J_USERNAME , password = constant_url.NEO4J_PASSWORD)
		print("connect neo4j success!")

	def readData(self):
		count = 0
		with open("wheat_new_node.csv",'w') as fw:
			fw.write("title,lable"+'\n')
		with open("wheat_wikidata_relation.csv","w") as fw:
			fw.write("HudongItem1,relation,HudongItem2"+'\n')
		with open("wheat_wikidata_relation2.csv","w") as fw:
			fw.write("HudongItem,relation,NewNode"+'\n')
		# /home/admin/Downloads/Agriculture_KnowledgeGraph-master/wikidataSpider/wikidataRelation/wheat_entity_relation.json
		with open("../wikidataRelation/wheat_entity_relation.json","r") as fr:
			with open("new_node.csv",'a') as fwNewNode:
				with open("wheat_wikidata_relation.csv",'a') as fwWikidataRelation:
					with open("wheat_wikidata_relation2.csv",'a') as fwWikidataRelation2:
						newNodeList = list()
						for line in fr:
							# print(line)
							entityRelationJson = json.loads(line)
							entity1 = entityRelationJson['entity1']
							entity2 = entityRelationJson['entity2']
							#搜索entity1
							find_entity1_result = self.graph.find_one(
								property_key = "title" ,
								property_value = entity1,
								label = "HudongItem"
							)
							#搜索entity2
							find_entity2_result = self.graph.find_one(
								property_key = "title",
								property_value = entity2,
								label = "HudongItem"
							)
							count += 1
							print(count/264092)
							# 如果entity1不在实体列表中(emmmmmm,不可能吧)，那么就不要继续了
							if(find_entity1_result is None):
								continue

							#去掉entityRelationJson['relation']中的逗号和双引号
							entityRelationList = re.split(",|\"",entityRelationJson['relation'])
							entityRelation = ""
							for item in entityRelationList:
								entityRelation = entityRelation + item
							#去掉entity2字符串中的逗号,并将繁体转成简体
							entity2List = re.split(",|\"",entity2)
							entity2 = "" 
							for item in entity2List:
								entity2 = entity2 + item
							entity2 = Converter('zh-hans').convert(entity2)

							# 如果entity2既不在实体列表中，又不在NewNode中，则新建一个节点，该节点的lable为newNode，然后添加关系
							if(find_entity2_result is None):
								if(entity2 not in newNodeList):
									fwNewNode.write(entity2+","+"newNode"+'\n')
									newNodeList.append(entity2)
								fwWikidataRelation2.write(entity1+","+entityRelation+","+entity2+'\n')
							#如果entity2在实体列表中，直接连关系即可
							else:
								fwWikidataRelation.write(entity1+","+entityRelation+","+entity2+'\n')



if __name__ == "__main__":
	loadData = loadDatatoNeo4j()
	loadData.connectDB()
	loadData.readData()









		
