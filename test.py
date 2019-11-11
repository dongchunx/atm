# encoding:utf-8
import json
import datetime
import jieba
import re
import pandas as pd
import nltk

from jieba import posseg
from common import token, get_number_in_group
from common import get_true_or_false

# jieba测试
# str1 = "请筛选出豫皖苏的客户"
# list1 = jieba.lcut(str1)
# print("jieba:")
# print(list1)
# init_slot(dictionary)
# jieba.add_word('在保客户数', tag='n')
# list2 = posseg.lcut(str)
# print("posseg:")
# print(list2)

# str1 = '保单保额在20-30万、40-50万、50-60万的客户情况'
# # str2 = "我想看上海长宁支公司的保单数"
# list2 = posseg.lcut(str2)
# print(list2)
# jieba.add_word('保单保额')
# jieba.add_word('车商兼代')
# list1 = jieba.lcut(str1)
# query = '提前十天签单'
# list1 = posseg.lcut(query)
# print(list1)


# re测试
# a = re.findall(r'之后\d+天', "我要看18年12月31日()之后90天的保单098uhuf8*(")
# a = re.findall(r'\w+', "放假监管机构监管机构")
# b = ' '.join(a)
# cut_list = posseg.lcut(b)
# print(a)
# print(b)
# print(cut_list)

# 批量拿表中数据
# df = pd.read_excel("C:\\Users\\dcx18\\Desktop\\智A\\字段名及对应tag_id(2).xls", sheet_name="非车")
# df_li = df.values.tolist()
# data = {}
# for i in df_li:
#     data[i[2]] = i[3]
# print(data)
#         dict1[i[2]] = i[0]
# print(dict1)
# list1 = []
# for i in df_li:
#     if i[1] == 2:
#         if '分公司' in i[2]:
#             list1.append(i[2].replace('分公司', ''))
# print
dict1 = {}
json_dict = json.dumps(dict1)
str1 = json_dict.replace("\"", "\\\"")
dict2 = {"c": str1}
print(dict2)
