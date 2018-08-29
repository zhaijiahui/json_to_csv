#-*-coding:utf-8-*-
# function: json_to_csv
# auther: zhaijiahui
import csv
import json
import sys
import codecs
from collections import OrderedDict


def list_dictionary(dic,title,value,key=''):
	flag = 0
	for k,v in dic.items():
		if type(dic[k]) is OrderedDict: # keep sequence
			temp = dic[k]
			key = k
			flag = 1
			list_dictionary(temp,title,value,key)
		else:
			if flag:
				title.append(k)
			else:
				title.append(key+"_"+k)
			value.append(dic[k])

def trans(path):
	jsonData = codecs.open(path, 'r', 'utf-8')
	# csvfile = open(path+'.csv', 'wb') # python2
	csvfile = open(path+'.csv', 'w', newline='') # python3
	writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
	value_list = []
	for line in jsonData:
		dic = json.loads(line,object_pairs_hook=OrderedDict)
		title = []
		value = []
		list_dictionary(dic,title,value)
		# print(value)
		value_list.append(value)
		
	writer.writerow(title)
	for i in value_list:
		try:
			writer.writerow(i)
		except Exception as e: # UnicodeEncodeError
			pass

	jsonData.close()
	csvfile.close()

if __name__ == '__main__':
	try:
		path=str(sys.argv[1]) # 获取path参数
		trans(path)
		print('Complete! save to: '+path+'.csv')
		# trans('target.json')
	except IndexError as e:
		print('Usage: python jsontocsv.py test.json')