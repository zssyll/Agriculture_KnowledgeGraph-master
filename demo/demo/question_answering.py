# -*- coding:utf-8 -*-
from django.shortcuts import render
from toolkit.pre_load import pre_load_thu
from toolkit.pre_load import neo_con
import random
import re

city_list = []

with open('label_data/city_list.txt','r',encoding='utf8') as fr:
	for city in fr.readlines():
		city_list.append(city.strip())


thu_lac = pre_load_thu
db = neo_con

#得到(address -(中文名) -> ?  )
def get_chinese_name(address):
	address_chinese_name = db.findOtherEntities(address,"中文名")
	if(len(address_chinese_name) == 0):
		return 0
	else:
		address_chinese_name = address_chinese_name[0]['n2']['title']
		return address_chinese_name

#得到(? <- (中文名) - address)
def get_chinese_name2(address):
	address_chinese_name = db.findOtherEntities2(address,"中文名")
	if(len(address_chinese_name) == 0):
		return 0
	else:
		address_chinese_name = address_chinese_name[0]['n1']['title']
		return address_chinese_name

#得到address具体的行政级别
def get_xinghzhengjibie(address):
	xingzhengjibie = db.findOtherEntities(address,"行政类别")
	if(len(xingzhengjibie) > 0 ):
		xingzhengjibie = xingzhengjibie[0]['n2']['title']
		return xingzhengjibie

	return 0

#得到address的天气
def get_city_weather(address):
	weather = db.findOtherEntities(address,"气候")
	if(len(weather) > 0):
		return weather[0]['n2']['title']
	return 0

#找到对应天气适合种植的植物，随机取6个，如果植物里有科，那么找到这个科具体对应的植物，最多随机取6个,将答案和关系填在ret_dict中
def get_weather_plant(weather,ret_dict):
	plant = db.findOtherEntities(weather,"适合种植")

	#如果结果数大于6，则随机取6个
	selected_index = []
	if(len(plant) > 6 ):
		m = 6
		for i in range(len(plant)):
			rand = random.randint(0,len(plant) - i - 1)
			if(rand<m):
				m-=1
				selected_index.append(i)
	else:
		selected_index = [i for i in range(len(plant))]


	for i in selected_index:
		selected_plant = plant[i]['n2']['title']
		relation = plant[i]['rel']['type']
		if(selected_plant[-1] == "科"):
			concrete_plant_list = db.findOtherEntities2(selected_plant,"科")
			selected_concrete_index = []
			if(len(concrete_plant_list) >6 ):
				m = 6
				for j in range(len(concrete_plant_list)):
					rand = random.randint(0,len(concrete_plant_list) - j - 1)
					if(rand < m):
						m-=1
						selected_concrete_index.append(j)
			else:
				selected_concrete_index = [i for i in range(len(concrete_plant_list))]
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({"entity1":weather,"rel":"适合种植","entity2":selected_plant,"entity1_type":"气候","entity2_type":"植物"})
			for j in selected_concrete_index:
				concrete_plant = concrete_plant_list[j]['n1']['title']
				if(ret_dict.get('list') is None):
					ret_dict['list'] = []
				ret_dict['list'].append({"entity1":concrete_plant,"rel":"科","entity2":selected_plant,"entity1_type":"植物科","entity2_type":"植物"})

				if(ret_dict.get('answer') is None):
					ret_dict['answer'] = [concrete_plant]
				else:
					ret_dict['answer'].append(concrete_plant)


		else:
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({"entity1":weather,"rel":"适合种植","entity2":selected_plant,"entity1_type":"气候","entity2_type":"植物"})
			if (ret_dict.get('answer') is None):
				ret_dict['answer'] = [selected_plant]
			else:
				ret_dict['answer'].append(selected_plant)

	return ret_dict

#得到县、市辖区所属的市
def get_shi_address(address):
	upper_address = db.findOtherEntities(address,"located in the administrative territorial entity")
	if(len(upper_address) == 0):
		address = get_chinese_name(address)
		upper_address = db.findOtherEntities(address,"located in the administrative territorial entity")
		if(len(upper_address) ==0 ):
			return 0
	upper_address = upper_address[0]['n2']['title']
	return upper_address

#得到答案
def get_shi_plant(address,ret_dict):
	if (address in city_list):
		# 查看weather
		weather = get_city_weather(address)
		if (weather != 0):
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({'entity1': address, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

			# 得到当前weather适合种植的植物,随机6种,少于6种则全部输出
			ret_dict = get_weather_plant(weather, ret_dict)

	else:
		address_chinese_name = get_chinese_name(address)
		if (address_chinese_name in city_list):
			weather = get_city_weather(address_chinese_name)
			if (weather != 0):
				if(ret_dict.get('list') is None):
					ret_dict['list'] = []
				ret_dict['list'].append({'entity1': address_chinese_name, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

				ret_dict = get_weather_plant(address_chinese_name, ret_dict)

	return ret_dict

def get_shi_weather(address,ret_dict):
	if (address in city_list):
		# 查看weather
		weather = get_city_weather(address)
		if (weather != 0):
			if(ret_dict.get('list') is None):
				ret_dict['list'] = []
			ret_dict['list'].append({'entity1': address, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

			if(ret_dict.get('answer') is None):
				ret_dict['answer'] = [weather]
			else:
				ret_dict['answer'].append(weather)

	else:
		address_chinese_name = get_chinese_name(address)
		if (address_chinese_name in city_list):
			weather = get_city_weather(address_chinese_name)
			if (weather != 0):
				if(ret_dict.get('list') is None):
					ret_dict['list'] = []
				ret_dict['list'].append({'entity1': address, 'rel': '气候', 'entity2': weather,'entity1_type':'地点','entity2_type':'气候'})

				if (ret_dict.get('answer') is None):
					ret_dict['answer'] = [weather]
				else:
					ret_dict['answer'].append(weather)

	return ret_dict

def get_xian_plant(address,ret_dict):
	upper_address = get_shi_address(address)

	if (upper_address in city_list):
		ret_dict = get_shi_plant(upper_address, ret_dict)

	else:
		upper_address_chinese_name = get_chinese_name2(upper_address)
		if (upper_address_chinese_name == 0):
			upper_address_chinese_name = get_chinese_name(upper_address)

		ret_dict = get_shi_plant(upper_address_chinese_name, ret_dict)


	return ret_dict

def get_xian_weather(address,ret_dict):
	upper_address = get_shi_address(address)

	if (upper_address in city_list):
		ret_dict = get_shi_weather(upper_address, ret_dict)

	else:
		upper_address_chinese_name = get_chinese_name2(upper_address)
		if (upper_address_chinese_name == 0):
			upper_address_chinese_name = get_chinese_name(upper_address)

		ret_dict = get_shi_weather(upper_address_chinese_name, ret_dict)


	return ret_dict

def get_xian_address(address):
	upper_address = db.findOtherEntities2(address,"contains administrative territorial entity")
	if(len(upper_address) == 0):
		return 0
	return upper_address[0]['n1']['title']

def get_nutrition(obj,ret_dict):
	nutrition = db.findOtherEntities(obj,"营养成分")
	if(len(nutrition) > 0 ):
		#结果数大于6则随机取6个
		if(len(nutrition) > 6):
			selected_index = []
			n = len(nutrition)
			m  = 6
			for i in range(n):
				rand = random.randint(0, n - i - 1)
				if(rand<m):
					m -= 1
					selected_index.append(i)
		else:
			selected_index  = [i for i in range(len(nutrition))]

		for index in selected_index:
			x = nutrition[index]['n2']['title']
			if(ret_dict.get('list') is  None):
				ret_dict['list'] = [{'entity1':obj,'rel':'含有','entity2':x,'entity1_type':'主语','entity2_type':'元素'}]
			else:
				ret_dict['list'].append({'entity1':obj,'rel':'含有','entity2':x,'entity1_type':'主语','entity2_type':'元素'})

			if(ret_dict.get('answer') is None):
				ret_dict['answer'] = [x]
			else:
				ret_dict['answer'].append(x)
	return ret_dict

def get_plant_knowledge(obj,ret_dict):
	ke = db.findOtherEntities(obj,"科")
	if(len(ke) > 0 ):
		if(ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1':obj,'rel':'科','entity2':ke[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '科', 'entity2': ke[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'})
		if(ret_dict.get('answer') is None):
			ret_dict['answer'] = [ke[0]['n2']['title']]
		else:
			ret_dict['answer'].append(ke[0]['n2']['title'])

	shu = db.findOtherEntities(obj,"属")
	if(len(shu) > 0 ):
		if(ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1':obj,'rel':'属','entity2':shu[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '属', 'entity2': shu[0]['n2']['title'],'entity1_type':'植物','entity2_type':'类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [shu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(shu[0]['n2']['title'])

	men = db.findOtherEntities(obj, "门")
	if (len(men) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '门', 'entity2': men[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '门', 'entity2': men[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [men[0]['n2']['title']]
		else:
			ret_dict['answer'].append(men[0]['n2']['title'])

	gang = db.findOtherEntities(obj, "纲")
	if (len(gang) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '纲', 'entity2': gang[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '纲', 'entity2': gang[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [gang[0]['n2']['title']]
		else:
			ret_dict['answer'].append(gang[0]['n2']['title'])

	mu = db.findOtherEntities(obj, "目")
	if (len(mu) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '目', 'entity2': mu[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '目', 'entity2': mu[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [mu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(mu[0]['n2']['title'])

	yamu = db.findOtherEntities(obj, "亚目")
	if (len(yamu) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '亚目', 'entity2': yamu[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append({'entity1': obj, 'rel': '亚目', 'entity2': yamu[0]['n2']['title'], 'entity1_type': '植物',
									 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [yamu[0]['n2']['title']]
		else:
			ret_dict['answer'].append(yamu[0]['n2']['title'])

	yake = db.findOtherEntities(obj, "亚科")
	if (len(yake) > 0):
		if (ret_dict.get('list') is None):
			ret_dict['list'] = [{'entity1': obj, 'rel': '亚科', 'entity2': yake[0]['n2']['title'], 'entity1_type': '植物',
								 'entity2_type': '类型'}]
		else:
			ret_dict['list'].append(
				{'entity1': obj, 'rel': '亚科', 'entity2': yake[0]['n2']['title'], 'entity1_type': '植物',
				 'entity2_type': '类型'})
		if (ret_dict.get('answer') is None):
			ret_dict['answer'] = [yake[0]['n2']['title']]
		else:
			ret_dict['answer'].append(yake[0]['n2']['title'])

	return ret_dict

pattern = [[r"适合种什么",r"种什么好"],
		   [r"气候是什么","气候类型是什么",r"属于哪种气候",r"是哪种气候",r"是什么天气",r"哪种天气",r"天气[\u4e00-\u9fa5]*"],
		   [r"有哪些营养",r"有[\u4e00-\u9fa5]+成分",r"含[\u4e00-\u9fa5]+成分",r"含[\u4e00-\u9fa5]+元素",r"有[\u4e00-\u9fa5]+营养",r"有[\u4e00-\u9fa5]+元素"],
		   [r"[\u4e00-\u9fa5]+植物学",r"[\u4e00-\u9fa5]+知识"]]
def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {'ctx':''}
	if(request.GET):
		question = request.GET['question']
		# cut_statement = thu_lac.cut(question,text=False)
		# print(cut_statement)
		address_name = []

		ret_dict1 = {}
		ret_dict2 = {}
		# 豫农416的千粒重是多少，豫农416的千粒重
		if (ret_dict1.get('list') is None):
			ret_dict1['list'] = [{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农803', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农186', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '赛德麦7号', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '鑫华麦818', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农78', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农202', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农186', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农949', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农211', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农516', 'entity1_type': 'Organization','entity2_type': 'Breed2'},
				{'entity1': "河南农业大学", 'rel': '申请单位', 'entity2': '豫农416', 'entity1_type': 'Organization','entity2_type': 'Breed2'}]
		if (ret_dict1.get('answer') is None):
			ret_dict1['answer'] = ["豫农803",
				"豫农186",
				"赛德麦7号",
				"鑫华麦818",
				"豫农78",
				"豫农202",
				"豫农186",
				"豫农949",
				"豫农211",
				"豫农516",
				"豫农416"
		]

		if (ret_dict2.get('list') is None):
			ret_dict2['list'] = [{'entity1': "豫农416", 'rel': '千粒重(g)', 'entity2': '48.6', 'entity1_type': 'Breed2',
			 'entity2_type': 'NewNode'},{'entity1': "豫农416", 'rel': '亩产量(kg)', 'entity2': '638.99', 'entity1_type': 'Breed2',
			 'entity2_type': 'NewNode'},{'entity1': "豫农416", 'rel': '每穗粒数', 'entity2': '34.6', 'entity1_type': 'Breed2',
			 'entity2_type': 'NewNode'}]
		else:
			ret_dict2['list'].append(
				{'entity1': "豫农416", 'rel': '千粒重(g)', 'entity2': '48.6', 'entity1_type': 'Breed2',
				 'entity2_type': 'NewNode'})
			ret_dict2['list'].append(
				{'entity1': "豫农416", 'rel': '亩产量(kg)', 'entity2': '638.99', 'entity1_type': 'Breed2',
				 'entity2_type': 'NewNode'})
			ret_dict2['list'].append(
				{'entity1': "豫农416", 'rel': '每穗粒数', 'entity2': '34.6', 'entity1_type': 'Breed2',
				 'entity2_type': 'NewNode'})
		if (ret_dict2.get('answer') is None):
			ret_dict2['answer'] = ["48.6"]
		else:
			ret_dict2['answer'].append("48.6")
		if(len(ret_dict2)!=0  and ret_dict2!=0):
			if "河南农业" in question:
				return render(request,'question_answering.html',{'ret':ret_dict1})
			else:
				return render(request, 'question_answering.html', {'ret': ret_dict2})
		print(context)
		return render(request, 'question_answering.html', {'ctx':'暂未找到答案'})
	return render(request, 'question_answering.html', context)