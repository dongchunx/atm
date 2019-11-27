# encoding:utf-8
import json
import datetime
import jieba
import re
import pandas as pd

from jieba import posseg
from common import token, get_number_in_group
from common import get_true_or_false

# jieba测试
# str1 = "请筛选出男客户"
# list1 = jieba.lcut(str1)
# print("jieba:")
# print(list1)
# init_slot(dictionary)
# jieba.add_word('在保客户数', tag='n')
# list2 = posseg.lcut(str)
# print("posseg:")
# print(list2)

# str1 = '提前一天签单'
# str2 = '提前两天签单'
# str3 = '提前三天签单'
# str4 = '提前四天签单'
# str5 = '提前五天签单'
# str6 = '提前十五天签单'
# str8 = '提前半年签单'
# str2 = "提前10天签单"
# str3 = "提前10-15天签单"
# str7 = '提前两个月签单'
# str8 = '提前半个月签单'
# str9 = '提前一个月签单'
# str10 = '提前十个月签单'
# str5 = '提前5个月签单'
# str13 = '提前10天到15天签单'
# str6 = '提前10-15天和提前30天签单的客户数统计'
# str12 = '提前10-15天和提前十天到半个月签单的客户数统计'
# list1 = posseg.lcut(str1)
# list2 = posseg.lcut(str2)
# print(list1)
# print(list2)
# l1 = [str1, str2, str3, str4, str5, str6, str7, str8, str9, str10]
# for i in l1:
#     list_word = re.findall(r'提前.*签单', i)
#     word_list = posseg.lcut(list_word[0])
#     print(word_list)
# print(index, word, flag)
# jieba.add_word('L')
# jieba.add_word('车商兼代')
# list1 = jieba.lcut(str1)
# query = '提前十天签单'
# list1 = posseg.lcut(query)


# re测试
a = re.findall(r'{}.*'.format('年龄'), "19年投保的客户中有多少被保人当前年龄在20-30、40-50、60-70岁")
# a = re.findall(r'\w+', "放假监管机构监管机构")
# a = re.findall(r'提前.*签单', '提前10-15天和提前一天签单的客户数统计')
# b = ' '.join(a)
# cut_list = posseg.lcut(b)
print(a)
# print(b)
# print(cut_list)

# 批量拿表中数据
# df = pd.read_excel("C:\\Users\\dcx18\\Desktop\\智A\\字段名及对应tag_id(2).xls", sheet_name="非车")
# df_li = df.values.tolist()
# data = {"cond": [], "dimension": [], "target": []}
# for i in df_li:
#     if i[0] == "筛选":
#         data["cond"].append(i[2])
#     elif i[0] == "维度":
#         data["dimension"].append(i[2])
#     elif i[0] == "指标":
#         data["target"].append(i[2])
# print(data)
# print(data)
#         dict1[i[2]] = i[0]
# print(dict1)
# list1 = []
# for i in df_li:
#     if i[1] == 2:
#         if '分公司' in i[2]:
#             list1.append(i[2].replace('分公司', ''))
# print
