# -*- coding: UTF-8 -*-

# noncar_target  = {}
#
# noncar_target['投保人客户数']  = ['投保人客户数', '投保客户数', '客户数']
# noncar_target['被保险人客户数'] = ['被保险人客户数', '被保人客户数']
# noncar_target['保费和'] = ['保费和', '保费收入', '保费情况']
# noncar_target['入账保费和'] = ['入账保费和', '入账保费收入', '入账保费情况']
# noncar_target['客均保费'] = ['客均保费']
import re
from datetime import datetime

import jieba
from jieba import posseg

from common import judge_utils, get_true_or_false, get_field_attribute, get_include_target, get_include_condition, \
    get_include_dimension, get_number


def get_noncar_targets(words_list):
    # targets = []
    # targets_dict = noncar_target
    #
    # for key in targets_dict.keys():
    #     for item in targets_dict[key]:
    #         if item in words_list:
    #             targets.append(key)
    #
    # print(target)
    # return list(set(targets))
    return


# 获取车险维度字段中险种类信息
def get_noncardim_insurance(query):
    pass


def get_noncardim_source(query):
    data = {'channel_1': None, 'channel_2': None, 'channel_3': None, 'branch': None}
    # data['group'] = None
    # data['depart'] = None

    if '二级机构' in query:
        data['channel_1'] = '二级机构'
    if '三级机构' in query:
        data['channel_2'] = '三级机构'
    if '四级机构' in query:
        data['channel_3'] = '四级机构'

    if '各分公司' in query:
        data['branch'] = '分公司'
    # if '部门组' in query:
    #     data['group'] = '部门组'
    # if '部门' in query:
    #     data['depart'] = '部门'

    print(data)
    return data


def noncar_cross_class(query):
    data = {}
    data['is_life'] = None
    data['is_car'] = None
    data['is_health'] = None

    if "非车" in query:

        if "寿险" in query:
            data['is_life'] = '是'
        if '车险' in query:
            data['is_non_car'] = '是'
        if '不是健康险' in query:
            data['is_health'] = '否'
        elif '健康险' in query:
            data['is_health'] = '是'

    print(data)
    return data


# notCar_insurance = ['驾意险', '人意险', '家财险', '交通意外险', '健康险']
def get_not_car_insurance(query, dictionary):
    data = {'notCar_insurance': []}

    for item in dictionary['notCar_insurance']:
        if item in query:
            data['notCar_insurance'].append(item)

    print(data)
    return data


def get_noncar_tools(query, dictionary):
    data = {}
    data['tools'] = []

    for tool in dictionary['noncar_tools']:
        if tool in query:
            data['tools'].append(tool)

    print(data)
    return data


# data = {}
# data.update(get_noncar_tools('第三方'))
# print(data)


def get_noncar_business(query, dictionary):
    data = {}
    data['business_list'] = []
    for item in dictionary['business_list']:
        if item in query:
            data['business_list'].append(item)
    if data:
        print(data)
    return data


# 非车性别 筛选
def get_not_car_gender(word_list, query, body):
    data = {}
    list1 = []
    list2 = ['男性', '男', '男孩', '男人', '男子', '男生']
    list3 = ['女性', '女', '女孩', '女人', '女子', '女生']
    for i in list2:
        if i in word_list:
            list1.append('1')
            if '被保' in query or '被投保' in query:
                body['iATM_non_car_index_insured_customer'] = '投保人客户数'
            else:
                body['iATM_non_car_index_customer'] = '投保人客户数'
            break
    for i in list3:
        if i in word_list:
            list1.append('2')
            if '被保' in query or '被投保' in query:
                body['iATM_non_car_index_insured_customer'] = '投保人客户数'
            else:
                body['iATM_non_car_index_customer'] = '投保人客户数'
            break
    data['notCar_gender'] = ','.join(list1)
    return data


# 判断新老客户数  维度/分组
def get_non_car_new_customer_group(query, word_list):
    num_mark = 0
    dimensionality_list2 = ["占比", "比例", "分布"]
    key_word = ['新老', '新老客户', '是否新客户']
    for i in key_word:
        if i in word_list:
            num_mark = 1
    extra_word = ['新客', '新客户', '老客', '老客户']
    for i in extra_word:
        if i in word_list:
            index = word_list.index(i)
            for num_dev in range(0, 4):
                num_dimension = index + num_dev
                if index + num_dev >= len(word_list):
                    num_dimension = len(word_list) - 1
                for word_dimension in dimensionality_list2:
                    if word_list[num_dimension] == word_dimension:
                        num_mark = 1
    list1 = ['新客', '新客户']
    list2 = ['老客', '老客户']
    for i in list1:
        if i in word_list:
            for j in list2:
                if j in word_list:
                    num_mark = 1
    return num_mark


# 非车是否老客户 筛选
def get_new_customer(word_list, query, tag_id, body):
    data = {}
    list_new = ['新客', '新客户']
    for i in list_new:
        if i in word_list:
            data[tag_id] = '1'
            data = judge_utils(word_list, i, data, tag_id)
            if '被保' in query or '被投保' in query:
                body['iATM_non_car_index_insured_customer'] = '被保人客户数'
            else:
                body['iATM_non_car_index_customer'] = '投保人客户数'
    list_old = ['老客户', '老客']
    for i in list_old:
        if i in word_list:
            data[tag_id] = '0'
            if '被保' in query or '被投保' in query:
                body['iATM_non_car_index_insured_customer'] = '被保人客户数'
            else:
                body['iATM_non_car_index_customer'] = '投保人客户数'
    return data


# 是否当年新客户 筛选
def get_current_year_new_customer(word_list, old_tag_id, current_tag_id, data):
    if old_tag_id in data.keys():
        if data[old_tag_id] == '1':
            dict_current = get_true_or_false(word_list, ['当年'], 'current_year')
            if dict_current:
                data[current_tag_id] = dict_current['current_year']
                data.pop(old_tag_id, 0)
    return data


# 判断个团单  维度/分组
def get_non_car_personal_or_group_group(query, word_list):
    num_mark = 0
    dimensionality_list2 = ["占比", "比例", "分布"]
    if '个人' in word_list:
        index = word_list.index('个人')
        if '渠道' in word_list:
            if abs(index - word_list.index('渠道')) > 2:
                for num_dev in range(0, 4):
                    num_dimension = index + num_dev
                    if index + num_dev >= len(word_list):
                        num_dimension = len(word_list) - 1
                    for word_dimension in dimensionality_list2:
                        if word_list[num_dimension] == word_dimension:
                            num_mark = 1
    key_word = ['个团', '个团单', '个团险']
    for i in key_word:
        if i in word_list:
            num_mark = 1
    extra_word = ['个单', '个险', '团体', '团单', '团险']
    for i in extra_word:
        if i in word_list:
            index = word_list.index(i)
            for num_dev in range(0, 4):
                num_dimension = index + num_dev
                if index + num_dev >= len(word_list):
                    num_dimension = len(word_list) - 1
                for word_dimension in dimensionality_list2:
                    if word_list[num_dimension] == word_dimension:
                        num_mark = 1
    list1 = ['个人', '个单', '个险']
    list2 = ['团体', '团单', '团险']
    for i in list1:
        if i in word_list:
            for j in list2:
                if j in word_list:
                    num_mark = 1
    return num_mark


# 判断性别  维度/分组
def get_non_car_gender_group(query, word_list):
    num_mark = 0
    key_word = ['男女']
    dimensionality_list2 = ["占比", "比例", "分布"]
    for i in key_word:
        if i in word_list:
            num_mark = 1
    key_word_dev = ['性别']
    if get_field_attribute(word_list, query, key_word_dev) == 1:
        num_mark = 1
    extra_word = ['男性', '女性']
    for i in extra_word:
        if i in word_list:
            index = word_list.index(i)
            for num_dev in range(0, 4):
                num_dimension = index + num_dev
                if index + num_dev >= len(word_list):
                    num_dimension = len(word_list) - 1
                for word_dimension in dimensionality_list2:
                    if word_list[num_dimension] == word_dimension:
                        num_mark = 1
    list1 = ['男性', '男', '男孩', '男人', '男子', '男生']
    list2 = ['女性', '女', '女孩', '女人', '女子', '女生']
    for i in list1:
        if i in word_list:
            for j in list2:
                if j in word_list:
                    num_mark = 1
    return num_mark


def get_gender_group(word_list, query, tag_id):
    data = {}
    gender_list = ['女', '男', '性别', '男女']
    for i in gender_list:
        for j in word_list:
            if i in j:
                gender_code = get_field_attribute(word_list, query, j)
                if gender_code == 1:
                    data[tag_id] = 1
    return data


# 机构(需改善)
def get_not_car_organization(word_list, query, tag_id, dictionary):
    data = {}
    list_result = []
    org_level = 0
    organization_2 = ['青海', '山西', '湖南', '苏州', '北京', '辽宁', '安徽', '云南', '温州', '广西', '福建', '甘肃', '无锡', '西藏', '海南', '常州',
                      '浙江', '贵州', '青岛', '上海', '四川', '吉林', '重庆', '宁波', '新疆', '东莞', '江苏', '深圳', '宁夏', '大连', '江西', '厦门',
                      '河南', '山东', '广东', '湖北', '内蒙古', '黑龙江', '陕西', '河北', '天津']
    notCar_organization_list = posseg.lcut(query)
    non_car_organization_1100 = dictionary['notCar_organization']
    for level in non_car_organization_1100.keys():
        dict1 = non_car_organization_1100[level]
        for i in dict1.keys():
            if i in query:
                list_result.append(dict1[i])
                org_level = str(level)
    for word, flag in notCar_organization_list:
        if word == '大连':
            list_result.append('2102002020100')
            org_level = '2'
        else:
            if flag == 'ns':
                if word in organization_2:
                    organization = word + "分公司"
                    for i in non_car_organization_1100.keys():
                        dict1 = non_car_organization_1100[i]
                        if organization in dict1.keys():
                            list_result.append(dict1[organization])
                            org_level = '2'
                else:
                    if word == '汉中':
                        list_result.append('7010100610700')
                        org_level = '3'
                    else:
                        for i in non_car_organization_1100.keys():
                            dict1 = non_car_organization_1100[i]
                            for j in dict1.keys():
                                if word in j:
                                    list_result.append(dict1[j])
                                    org_level = '3'
    final_list = list(set(list_result))
    data[tag_id] = ','.join(final_list)
    return data, org_level


# 渠道
def get_not_car_channel(word_list, query, tag_id, dictionary):
    # 非车渠道
    data = {}
    dict_dev = {'车商': '1', '车商兼代': '28', '车商兼业代理（网销）': '43', '车商专代': '37',
                '车商专业代理（网销）': '44',
                '电销': '2', '电销呼出': '16', '电销呼入': '13', '网电融合（电网）': '10', '个人': '3', '个人营销非便利店': '23',
                '交叉': '4', '产险营销便利店': '38', '公司直营门店': '11', '普通专代': '21', '其他代理类': '0',
                '其他兼业兼代（不含车商）': '22, 24', '运输业务': '29', '直拓': '12, 15', '第三方网销': '19', '普通兼业代理（网销）': '42',
                '普通专业代理（网销）': '45', '其他网销': '18', '网电融合（网电）': '51', '银行兼业代理（网销）': '41', '自营网销': '14',
                '银邮': '6', '银保通': '33', '银行代理': '27', '邮局业务': '40'}
    # 枚举值中含'（网销）'的词汇
    list_dev = ['车商经纪', '个代产', '寿险营销便利店', '银团代产', '普通经纪', '个人营销']
    dict_dev1 = {'车商经纪': '39', '车商经纪（网销）': '46', '个代产': '32, 26, 34', '个代产（网销）': '53', '寿险营销便利店': '36',
                 '寿险营销便利店（网销）': '54', '银团代产': '25, 35',
                 '银团代产（网销）': '52', '普通经纪': '31', '普通经纪（网销）': '47', '个人营销（网销）': '55', }
    result = ""
    for word in word_list:
        error_list = ['个人']
        if word in dictionary['notCar_channel'].keys():
            for i in error_list:
                if word == i:
                    index = word_list.index(word)
                    if '渠道' in word_list:
                        if abs(index - word_list.index('渠道')) <= 2:
                            result = result + dict_dev[word] + ','
                else:
                    result = result + dict_dev[word] + ','
        for i in list_dev:
            if i == word:
                if '网销' in word_list:
                    i = i + '（' + '网销' + '）'
                result = result + dict_dev1[i] + ','
        if word == '网销':
            index = word_list.index(word)
            if 0 < +index - 1 < index + 1 < len(word_list) - 1:
                if not (word_list[index - 1] == '（' and word_list[index + 1] == '）'):
                    result = result + '5,'
    final_result = result[:len(result) - 1]
    data[tag_id] = final_result
    return data


def get_not_car_time_code(query, word_list, tag_id1, tag_id2, tag_id3, tag_id4, time_period):
    data = {}
    # 时间是否有效，默认填充视为无效，主要用于判断是否为闲聊
    car_time_is_effective = True
    if time_period != "":
        list1 = ['签单', '签单日期']
        for i in list1:
            if i in word_list:
                data[tag_id1] = time_period
        list2 = ['入账', '入账日期']
        for i in list2:
            if i in word_list:
                data[tag_id2] = time_period
        list3 = ['起保', '起保日期', '投保', '投保日期']
        for i in list3:
            if i in word_list:
                data[tag_id3] = time_period
        list4 = ['止期', '止期日期', '截止日期', '到期', '到期日期']
        for i in list4:
            if i in word_list:
                data[tag_id4] = time_period
        if not data:
            data[tag_id2] = time_period
    else:
        car_time_is_effective = False
        current_year = str(datetime.now().year)
        data[tag_id2] = current_year + "/01/01," + current_year + "/12/31"
    return data, car_time_is_effective


# 提前签单天数
# 提前签单天数维度
def get_advance_sign_days(query):
    time_dict = {'一天': 1, '两天': 2, '三天': 3, '四天': 4, '五天': 5, '十天': 10, '十五天': 15,
                 '半个月': 15, '一个月': 30, '两个月': 60, '三个月': 90, '半年': 180}
    num_mark = 0
    final_list = []
    list_word = re.findall(r'提前.*签单', query)
    if list_word:
        word_list_dev = jieba.lcut(list_word[0])
        # 储存'- 到'包含的数值下标，防止区间重复填充
        list_dev = []
        num_list = []
        for i in word_list_dev:
            if len(get_number(i)) > 0:
                if i == get_number(i)[0]:
                    num_list.append(i)
        for index, i in enumerate(word_list_dev):
            num_min = ''
            num_max = ''
            index_number1 = ''
            index_number2 = ''
            if i == '-' or i == '到':
                if index - 2 >= 0:
                    word = word_list_dev[index - 1]
                    if word in time_dict.keys():
                        num_min = time_dict[i]
                        index_number1 = index - 1
                    elif word in num_list:
                        num_min = word
                        index_number1 = index - 1
                    elif word == '天':
                        if word_list_dev[index - 2] in num_list:
                            num_min = word_list_dev[index - 2]
                            index_number1 = index - 2
                if index + 2 < len(word_list_dev):
                    word = word_list_dev[index + 1]
                    if word in time_dict.keys():
                        num_min = time_dict[i]
                        index_number2 = index + 1
                    elif word in num_list:
                        num_max = word
                        index_number2 = index + 1
                if num_min and num_max:
                    final_list.append(str(num_min) + '-' + str(num_max))
                    list_dev.append(index_number1)
                    list_dev.append(index_number2)
        for index, i in enumerate(word_list_dev):
            num_min = ''
            num_max = ''
            if index not in list_dev:
                if i in time_dict.keys():
                    num_min = time_dict[i]
                    num_max = time_dict[i]
                if index + 1 < len(word_list_dev):
                    if i in num_list and word_list_dev[index + 1] == '天':
                        num_min = i
                        num_max = i
                if num_min and num_max:
                    final_list.append(num_min + '-' + str(num_max))
        if not final_list:
            # list1 = ['多少天']
            # for i in list1:
            #     if i in list_word[0]:
            num_mark = 1
    return final_list, num_mark


# 投保人省份
# 省份中不会引起歧义的简称
province_list = ['沪', '滇', '内蒙', '蜀', '宁夏', '皖', '鲁', '晋', '粤', '桂', '新疆',
                 '赣', '冀', '豫', '琼', '鄂', '湘', '陇', '闽', '黔', '渝', '秦', '浙', '江', '苏']
# 全称判断
province_list1 = ['上海市', '云南省', '内蒙古自治区', '北京市', '吉林省', '四川省', '天津市', '宁夏回族自治区', '安徽省', '山东省', '山西省', '广东省', '广西壮族自治区',
                  '新疆维吾尔自治区', '江苏省', '江西省', '河北省', '河南省', '浙江省', '海南省', '湖北省', '湖南省', '甘肃省', '福建省', '西藏自治区', '贵州省',
                  '辽宁省', '重庆市', '陕西省', '青海省', '黑龙江省', '东三省', '东北三省', '上海', '云南', '内蒙古', '北京', '吉林', '四川', '天津', '宁夏',
                  '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西',
                  '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江']

# 根据简称判断
dict_dev = {'云': '云南', '江': '江苏', '川': '四川', '蒙': '内蒙', '京': '北京', '吉': '吉林', '津': '天津', '宁': '宁夏', '苏': '江苏',
            '浙': '浙江', '甘': '甘肃', '藏': '西藏',
            '贵': '贵州', '辽': '辽宁', '陕': '陕西', '青': '青海', '黑': '黑龙江'}


#
# list_dev = ['上海', '云南', '内蒙古', '北京', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西',
#             '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江']

def identify_provinces(words_list, query, tag_id, dictionary):
    data = {}
    site_list = []
    site_dict = dictionary["noncar_identify_provinces"]
    target_list = []

    # 不会引起歧义的简称
    for i in province_list:
        if i in query and (i + '分') not in query:
            site_list.append(i)

    # 全称判断
    for j in province_list:
        if j in words_list:
            if '省' in query or '市' in query:
                site_list.append(j)

    # 可能会冲突的简称
    for key in dict_dev.keys():
        if key in query:
            if '省' in query or '市' in query:
                site_list.append(key)

    for _ in site_list:
        province = site_dict[_]
        target_list.append(province)

    data[tag_id] = ",".join(target_list)
    # print(data)
    return data


# 被保人省份
def identify_provinces_by(words_list, query, tag_id, dictionary):
    data = {}
    site_list = []
    site_dict = dictionary["noncar_identify_provinces"]
    target_list = []
    if '被保' in words_list or '被投保' in words_list:
        for i in province_list:
            if i in query:
                site_list.append(i)

    for _ in site_list:
        province = site_dict[_]
        # print(province)
        target_list.append(province)
        # print(target_list)

    data[tag_id] = ", ".join(target_list)
    # print(data)
    return data


# 提前签单天数
def advance_sign_day(words_list, query, tag_id):
    data = {}
    day_dict = {
        '半个月': '15', '一个月': '30', '一个半月': '45', '两个月': '60', '三个月': '90', '四个月': '120',
        '五个月': '150', '半年': '180', '一年': '360'
    }
    if '提前' in words_list:
        sign_day = re.findall(r"\d+\.?\d*", query)

        if len(sign_day) != 0:
            advance_day = sign_day[0]
            data[tag_id] = ",".join([advance_day, '#'])

        else:
            for k in day_dict:
                if k in words_list:
                    advance_day = day_dict[k]
                    data[tag_id] = ",".join([advance_day, '#'])
    return data


# 非车险险种
def notCar_insurance(words_list, query, tag_id, dictionary):
    dict1122 = {'一、家庭财产保险': 1, '二、人身意外保险': 2,
                '三、短期健康保险': 3, '四、责任保险': 4, '五、个信保': 5,
                '（一）常规家财险': '101', '（二）个人抵押贷款房屋综合保险': '102', '（三）储金类业务': '103', '（四）个人账户损失险': '104',
                '（一）个意险类': '201', '（二）交通人意类': '202',
                '（三）旅游人意类': '203', '（四）借款人意类': '204', '（五）特定人员意外类': '205', '（六）学生幼儿意外伤害综合保险': '206',
                '（七）其他类': '207', '（二）医疗险': '302',
                '（三）疾病类': '303', '（一）其他': '401'}
    dict1123 = {'常规家财险': '（一）常规家财险', '个人抵押贷款房屋综合保险': '（二）个人抵押贷款房屋综合保险', '储金类业务': '（三）储金类业务', '个人账户损失险': '（四）个人账户损失险',
                '个意险类': '（一）个意险类', '交通人意类': '（二）交通人意类', '旅游人意类': '（三）旅游人意类', '借款人意类': '（四）借款人意类',
                '特定人员意外类': '（五）特定人员意外类',
                '学生幼儿意外伤害综合保险': '（六）学生幼儿意外伤害综合保险', '其他类': '（七）其他类', '医疗险': '（二）医疗险', '疾病类': '（三）疾病类', '其他': '（一）其他'}

    insurance_is_effective = True
    short_dict = dictionary["short_dict"]
    data = {}
    insurance_dict = dictionary["notCar_insurance_type"]
    final_list = []
    final_list1 = []
    for key in dict1123.keys():
        if key in words_list and '（' in words_list:
            value1123 = dict1123[key]
            final_list.append(dict1122[value1123])
    for key in insurance_dict.keys():
        if key in words_list:
            final_list.append(insurance_dict[key])
    for k in short_dict:
        if k in words_list:
            # print(k)
            short_list = short_dict[k]
            # print("11111", short_list)
            for i in short_list:
                if i in insurance_dict:
                    # print(insurance_dict[i])
                    final_list.append(insurance_dict[i])
            break
    if not final_list:
        final_list = [1, 2, 3, 4]
        insurance_is_effective = False
    final_list = list(set(final_list))
    for _ in final_list:
        final_list1.append(str(_))
    data[tag_id] = ",".join(final_list1)
    # print(data)

    return data, insurance_is_effective


# 特殊业务语料非车规则处理
def get_non_car_special_words(query, data_dev, not_car_time_is_effective, insurance_is_effective):
    data = {}
    insured_word = ["被保", "被投保"]
    list1 = ["承保分析", "承保情况", "投保情况", "日报", "出单情况", "分布情况", "销售情况"]
    list1_dev = ["统计", "查询", "日报"]
    for i in list1:
        if i in query:
            if not get_include_dimension(data_dev):
                # 如果筛选是二级则变为三级，如果筛选是三级则变为四级
                data["notCar_organization_2"] = "1"
                data["channel_group"] = "1"
                data["insurance_type_details_group"] = "1"
                data["interval"] = "BNDJY_CHINA"
            data["non_car_index_customer"] = "-1"
            # 如果日期没选入账日期，则要变成保费和
            data["non_car_index_record_fee"] = "-1"
            data["non_car_index_policy_pieces"] = "-1"
    for i in list1_dev:
        if i in query and not get_include_target(data_dev):
            if not get_include_dimension(data_dev):
                # 如果筛选是二级则变为三级，如果筛选是三级则变为四级
                data["notCar_organization_2"] = "1"
                data["channel_group"] = "1"
                data["insurance_type_details_group"] = "1"
                data["interval"] = "BNDJY_CHINA"
            data["non_car_index_customer"] = "-1"
            # 如果日期没选入账日期，则要变成保费和
            data["non_car_index_record_fee"] = "-1"
            data["non_car_index_policy_pieces"] = "-1"
    list2 = ["客户分析", "客户情况", "投保人情况", "脸谱分析"]
    for i in list2:
        if i in query:
            if not get_include_dimension(data_dev):
                data["notCar_organization_2"] = "1"
                data["channel_group"] = "1"
                data["interval"] = "BNDJY_CHINA"
                for j in insured_word:
                    if j in query:
                        data["insured_gender_group"] = "1"
                        data["start_insured_age_group"] = "0-25,26-35,36-45,46-55,56-#"
                    else:
                        data["gender_group"] = "1"
                        data["start_insure_age_group"] = "0-25,26-35,36-45,46-55,56-#"
    list3 = ["赔付分析", "赔付情况"]
    for i in list3:
        if i in query:
            if not get_include_dimension(data_dev):
                data["notCar_organization_2"] = "1"
                data["insurance_type_details_group"] = "1"
                data["channel_group"] = "1"
    list4 = ["续保分析", "续保情况"]
    for i in list4:
        if i in query:
            if not get_include_dimension(data_dev):
                data["notCar_organization_2"] = "1"
                data["channel_group"] = "1"
                data["insurance_type_details_group"] = "1"
            data["non_car_index_customer"] = "-1"
            data["non_car_index_policy_pieces"] = "-1"

    return data


# 非车删去多余误填充方法
def non_car_del_extra_fill(data):
    list_keys = data.keys()
    if "insurance_type_group" in list_keys and "insurance_type_details_group" in list_keys:
        data.pop("insurance_type_group", 0)
    return data


# 非车未加识别功能的字段
def non_car_get_undefined_field(query, word_list, non_car_total):
    data = {}
    message_list = []
    list1 = ["代理点"]
    for i in list1:
        if i in word_list:
            message_list.append("代理点")
    list2 = ["合作伙伴代码"]
    for i in list2:
        if i in word_list:
            if 5000200 not in non_car_total.keys():
                message_list.append("合作伙伴代码")
    list3 = ['加保']
    for i in list3:
        if i in word_list:
            message_list.append('非车加保')
    if len(message_list) != 0:
        message = ("NLP未拓展" + ','.join(message_list) + "识别功能")
    else:
        message = ""
    data["message"] = message
    return data


# 非车出单工具(词典中为字典格式)
def get_non_car_issue_tool(words_list, query, tag_id, dictionary):
    data = {}
    list_dev = []
    common_dict = dictionary[tag_id]
    for word in words_list:
        if word in common_dict:
            if '出单' in query:
                list_dev.append(str(common_dict[word]))
    if list_dev:
        str_dev = ','.join(list_dev)
        data[tag_id] = str_dev
    if data:
        print(data)
    return data
