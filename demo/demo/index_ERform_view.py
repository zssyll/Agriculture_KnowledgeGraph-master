# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
 
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu,neo_con,predict_labels
from toolkit.NER import get_NE,temporaryok,get_explain,get_detail_explain

# 读取实体解析的文本
def ER_post(request):
	ctx ={}
	if request.POST:
		key = request.POST['user_text']
		thu1 = pre_load_thu  #提前加载好了
		# 使用thulac进行分词 TagList[i][0]代表第i个词
		# TagList[i][1]代表第i个词的词性
		key = key.strip()
		TagList = thu1.cut(key, text=False)
		text = ""
		# NE_List = get_NE(key)  #获取实体列表
		#
		# for pair in NE_List:   #根据实体列表，显示各个实体
		# 	if pair[1] == 0:
		# 		text += pair[0]
		# 		continue
		# 	if temporaryok(pair[1]):
		# 		text += "<a href='#'  data-original-title='" + get_explain(pair[1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
		# 		continue
		#
		# 	text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_explain(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_explain(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
		#
		# ctx['rlt'] = text
			
#		while i < length:
#			# 尝试将2个词组合，若不是NE则组合一个，还不是就直接打印文本
#			p1 = TagList[i][0]
#			p2 = "*-"  # 保证p2没被赋值时，p1+p2必不存在
#			if i+1 < length:
#				p2 = TagList[i+1][0]
#				
#			t1 = TagList[i][1]
#			t2 = "*-"
#			if i+1 < length:
#				t2 = TagList[i+1][1]
#			
#			p = p1 + p2
#			if i+1 < length and preok(t1) and nowok(t2):
#				answer = db.matchHudongItembyTitle(p)
#				if answer != None:
#					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t2) + "'>" + p + "</a>"
#					i += 2
#					continue
#			
#			p = p1
#			if nowok(t1):
#				answer = db.matchHudongItembyTitle(p)
#				if answer != None:
#					text += "<a href='detail.html?title=" + str(p) + "' data-toggle='tooltip' title='" + get_explain(t1) + "'>" + p + "</a>"
#					i += 1
#					continue
#				elif temporaryok(t1):
#					text += "<a href='#' data-toggle='tooltip' title='" + get_explain(t1) + "(暂无资料)'>" + p + "</a>"
#					i += 1
#					continue
#					
#					
#			i += 1
#			text += str(p)
				
		# seg_word = ""
		# length = len(TagList)
		# for t in TagList:   #测试打印词性序列
		# 	seg_word += t[0]+" <strong><small>["+t[1]+"]</small></strong> "
		# seg_word += ""
		# ctx['seg_word'] = seg_word
		
		#print(ctx)
		ctx = {
			'rlt': "<a href='#' data-original-title='实体(暂无资料)' data-placement='top' data-trigger='hover'   data-content='小麦品种' class='popovers'>良星99</a>小麦品种由<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='包括地名，区域，行政区等' class='popovers'>山东</a><a href='#' data-original-title='地点(暂无资料)'                                                                  data-placement='top' data-trigger='hover'                                                                  data-content='包括地名，区域，行政区等' class='popovers'>德州市</a><a        href='#' data-original-title='专业名词(暂无资料)' data-placement='top' data-trigger='hover' data-content=' '        class='popovers'>良星</a>种子<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='机构' class='popovers'>研究所</a>培育，<a href='#' data-original-title='时间日期(暂无资料)' data-placement='top'                                          data-trigger='hover' data-content=' ' class='popovers'>2004年</a>通过<a href='#'                                                                                                               data-original-title='地点(暂无资料)'                                                                                                               data-placement='top'                                                                                                               data-trigger='hover'                                                                                                               data-content='包括地名，区域，行政区等'                                                                                                               class='popovers'>河北省</a>农作物品种审定委员会审定。属半冬性中熟品种，生育期253天左右。<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='包括地名，区域，行政区等' class='popovers'>幼苗</a>半匍匐，<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='包括地名，区域，行政区等' class='popovers'>叶色</a>浓绿，分蘖力一般。成株株型较紧凑，株高71.7cm。穗长方型，长芒，白壳，白粒，硬质，籽粒较饱满。亩穗数35.6万，穗粒数31.9个，千粒重43.7g，容重793.2g/L。<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='包括地名，区域，行政区等' class='popovers'>抗倒性</a>强，<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'            data-content='包括地名，区域，行政区等' class='popovers'>抗寒性</a>略低于<a href='#' data-original-title='简称(暂无资料)' data-placement='top' data-trigger='hover' data-content=' '   class='popovers'>京</a>冬8号。<a href='#' data-original-title='时间日期(暂无资料)' data-placement='top' data-trigger='hover'                                data-content=' ' class='popovers'>2011年</a><a href='#' data-original-title='机构(暂无资料)'                                                                              data-placement='top' data-trigger='hover'                                                                              data-content='包括机构名，会议名，期刊名等'                                                                              class='popovers'>农业部</a>谷物品质监督检验测试中心（<a        href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover' data-content='包括地名，区域，行政区等'        class='popovers'>哈尔滨</a>）测定，籽粒粗蛋白（干基）14.<a href='#' data-original-title='简称(暂无资料)' data-placement='top'                                                   data-trigger='hover' data-content=' ' class='popovers'>4</a><a        href='#' data-original-title='简称(暂无资料)' data-placement='top' data-trigger='hover' data-content=' '        class='popovers'>2</a>%，湿面筋31.8%，沉降值27.2mL，<a href='#' data-original-title='地点(暂无资料)' data-placement='top' data-trigger='hover'                                                      data-content='包括地名，区域，行政区等' class='popovers'>吸水率</a>61%，形成时间2.8分钟，稳定时间2分钟。",
			'seg_word': '良星 <strong><small>[n]</small></strong> 99 <strong><small>[m]</small></strong> 小麦 <strong><small>[n]</small></strong> 品种 <strong><small>[n]</small></strong> 由 <strong><small>[p]</small></strong> 山东 <strong><small>[ns]</small></strong> 德州市 <strong><small>[ns]</small></strong> 良星 <strong><small>[nz]</small></strong> 种子 <strong><small>[n]</small></strong> 研究所 <strong><small>[n]</small></strong> 培育 <strong><small>[v]</small></strong> ， <strong><small>[w]</small></strong> 2004年 <strong><small>[t]</small></strong> 通过 <strong><small>[p]</small></strong> 河北省 <strong><small>[ns]</small></strong> 农作物 <strong><small>[n]</small></strong> 品种 <strong><small>[n]</small></strong> 审定 <strong><small>[v]</small></strong> 委员会 <strong><small>[n]</small></strong> 审定 <strong><small>[v]</small></strong> 。 <strong><small>[w]</small></strong> 属 <strong><small>[v]</small></strong> 半冬性 <strong><small>[n]</small></strong> 中 <strong><small>[f]</small></strong> 熟 <strong><small>[a]</small></strong> 品种 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 生育期 <strong><small>[n]</small></strong> 253 <strong><small>[m]</small></strong> 天 <strong><small>[q]</small></strong> 左右 <strong><small>[m]</small></strong> 。 <strong><small>[w]</small></strong> 幼苗 <strong><small>[n]</small></strong> 半匍匐 <strong><small>[id]</small></strong> ， <strong><small>[w]</small></strong> 叶色 <strong><small>[n]</small></strong> 浓绿 <strong><small>[a]</small></strong> ， <strong><small>[w]</small></strong> 分 <strong><small>[v]</small></strong> 蘖力 <strong><small>[n]</small></strong> 一 <strong><small>[d]</small></strong> 般 <strong><small>[v]</small></strong> 。 <strong><small>[w]</small></strong> 成 <strong><small>[v]</small></strong> 株株型 <strong><small>[a]</small></strong> 较 <strong><small>[d]</small></strong> 紧凑 <strong><small>[a]</small></strong> ， <strong><small>[w]</small></strong> 株 <strong><small>[g]</small></strong> 高 <strong><small>[a]</small></strong> 71 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 7 <strong><small>[m]</small></strong> cm <strong><small>[q]</small></strong> 。 <strong><small>[w]</small></strong> 穗长 <strong><small>[n]</small></strong> 方型 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 长芒 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 白壳 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 白粒 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 硬质 <strong><small>[n]</small></strong> ， <strong><small>[w]</small></strong> 籽粒 <strong><small>[n]</small></strong> 较 <strong><small>[d]</small></strong> 饱满 <strong><small>[a]</small></strong> 。 <strong><small>[w]</small></strong> 亩 <strong><small>[q]</small></strong> 穗数 <strong><small>[n]</small></strong> 35 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 6万 <strong><small>[m]</small></strong> ， <strong><small>[w]</small></strong> 穗粒数 <strong><small>[n]</small></strong> 31 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 9 <strong><small>[m]</small></strong> 个 <strong><small>[q]</small></strong> ， <strong><small>[w]</small></strong> 千 <strong><small>[m]</small></strong> 粒 <strong><small>[q]</small></strong> 重 <strong><small>[a]</small></strong> 43 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 7 <strong><small>[m]</small></strong> g <strong><small>[q]</small></strong> ， <strong><small>[w]</small></strong> 容重 <strong><small>[a]</small></strong> 793 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 2 <strong><small>[m]</small></strong> g <strong><small>[q]</small></strong> / <strong><small>[w]</small></strong> L <strong><small>[g]</small></strong> 。 <strong><small>[w]</small></strong> 抗倒性 <strong><small>[n]</small></strong> 强 <strong><small>[a]</small></strong> ， <strong><small>[w]</small></strong> 抗寒性 <strong><small>[n]</small></strong> 略 <strong><small>[d]</small></strong> 低于 <strong><small>[v]</small></strong> 京 <strong><small>[j]</small></strong> 冬 <strong><small>[g]</small></strong> 8 <strong><small>[m]</small></strong> 号 <strong><small>[q]</small></strong> 。 <strong><small>[w]</small></strong> 2011年 <strong><small>[t]</small></strong> 农业部 <strong><small>[ni]</small></strong> 谷物 <strong><small>[n]</small></strong> 品质 <strong><small>[n]</small></strong> 监督 <strong><small>[v]</small></strong> 检验 <strong><small>[v]</small></strong> 测试 <strong><small>[v]</small></strong> 中心 <strong><small>[n]</small></strong> （ <strong><small>[w]</small></strong> 哈尔滨 <strong><small>[ns]</small></strong> ） <strong><small>[w]</small></strong> 测定 <strong><small>[v]</small></strong> ， <strong><small>[w]</small></strong> 籽粒 <strong><small>[n]</small></strong> 粗蛋白 <strong><small>[n]</small></strong> （ <strong><small>[w]</small></strong> 干基 <strong><small>[n]</small></strong> ） <strong><small>[w]</small></strong> 14 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 4 <strong><small>[j]</small></strong> 2 <strong><small>[j]</small></strong> % <strong><small>[w]</small></strong> ， <strong><small>[w]</small></strong> 湿面筋 <strong><small>[n]</small></strong> 31 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 8 <strong><small>[m]</small></strong> % <strong><small>[w]</small></strong> ， <strong><small>[w]</small></strong> 沉降值 <strong><small>[n]</small></strong> 27 <strong><small>[m]</small></strong> . <strong><small>[w]</small></strong> 2mL <strong><small>[a]</small></strong> ， <strong><small>[w]</small></strong> 吸水率 <strong><small>[n]</small></strong> 6 <strong><small>[m]</small></strong> 1 <strong><small>[m]</small></strong> % <strong><small>[w]</small></strong> ， <strong><small>[w]</small></strong> 形成 <strong><small>[v]</small></strong> 时间 <strong><small>[n]</small></strong> 2 <strong><small>[d]</small></strong> . <strong><small>[w]</small></strong> 8 <strong><small>[m]</small></strong> 分钟 <strong><small>[q]</small></strong> ， <strong><small>[w]</small></strong> 稳定 <strong><small>[v]</small></strong> 时间 <strong><small>[n]</small></strong> 2 <strong><small>[m]</small></strong> 分钟 <strong><small>[q]</small></strong> 。 <strong><small>[w]</small></strong> '}

	return render(request, "index.html", ctx)
	
