# -*- coding: UTF-8 -*-

# noncar_target  = {}
#
# noncar_target['投保人客户数']  = ['投保人客户数', '投保客户数', '客户数']
# noncar_target['被保险人客户数'] = ['被保险人客户数', '被保人客户数']
# noncar_target['保费和'] = ['保费和', '保费收入', '保费情况']
# noncar_target['入账保费和'] = ['入账保费和', '入账保费收入', '入账保费情况']
# noncar_target['客均保费'] = ['客均保费']
import re

import jieba
from jieba import posseg

from common import judge_utils, get_true_or_false, get_field_attribute


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
    print(data)
    return data


def get_not_car_gender(query):
    data = {'notCar_gender': []}
    gender_list = ['男', '女']
    gender_dict = {'男': '1', '女': '2'}
    for i in gender_list:
        if i in query:
            data['notCar_gender'].append(i)
    if data['notCar_gender']:
        for _ in data['notCar_gender']:
            data['notCar_gender'] = gender_dict[_]
    return data


def get_new_customer(word_list, tag_id):
    data = {tag_id: ''}
    if '新客户' in word_list:
        data[tag_id] = '1'
        data = judge_utils(word_list, '新客户', data, tag_id)
    elif '老客户' in word_list:
        data[tag_id] = '0'
    return data


def get_current_year_new_customer(word_list, old_tag_id, current_tag_id, data):
    if data[old_tag_id] == '1':
        dict_current = get_true_or_false(word_list, '当年', 'current_year')
        data[current_tag_id] = dict_current['current_year']
    return data


def get_gender_group(word_list, query, tag_id):
    data = {}
    gender_list = ['女', '男', '性别']
    for i in gender_list:
        for j in word_list:
            if i in j:
                gender_code = get_field_attribute(word_list, query, j)
                if gender_code == 1:
                    data[tag_id] = 1
    return data


# 机构(需改善)
def get_not_car_organization(word_list, query, tag_id, dictionary):
    data = {tag_id: []}
    organization_2 = ['青海', '山西', '湖南', '苏州', '北京', '辽宁', '安徽', '云南', '温州', '广西', '福建', '甘肃', '无锡', '西藏', '海南', '常州',
                      '浙江', '贵州', '青岛', '上海', '四川', '吉林', '重庆', '宁波', '新疆', '东莞', '江苏', '深圳', '宁夏', '大连', '江西', '厦门',
                      '河南', '山东', '广东', '湖北', '内蒙古', '黑龙江', '陕西', '河北', '天津']
    notCar_organization_list = posseg.lcut(query)
    for word, flag in notCar_organization_list:
        if flag == 'ns':
            if word in organization_2:
                organization = word + "分公司"
                data[tag_id].append(dictionary['notCar_organization'][organization])
            else:
                for i in dictionary['notCar_organization']:
                    if word in i:
                        data[tag_id].append(dictionary['notCar_organization'][i])
    return data


# 渠道
def get_not_car_channel(word_list, query, tag_id, dictionary):
    # 非车渠道
    dict_dev = {'车商': '1', '车商兼代': '28', '车商兼业代理（网销）': '43', '车商经纪': '39', '车商经纪（网销）': '46', '车商专代': '37',
                '车商专业代理（网销）': '44',
                '电销': '2', '电销呼出': '16', '电销呼入': '13', '网电融合（电网）': '10', '个人': '3', '个人营销（网销）': '55', '个人营销非便利店': '23',
                '交叉': '4', '个代产': '32, 26, 34', '个代产（网销）': '53', '寿险营销便利店': '36', '寿险营销便利店（网销）': '54', '银团代产': '25, 35',
                '银团代产（网销）': '52', '其他': '7', '产险营销便利店': '38', '公司直营门店': '11', '普通经纪': '31', '普通专代': '21', '其他代理类': '0',
                '其他兼业兼代（不含车商）': '22, 24', '运输业务': '29', '直拓': '12, 15', '网销': '5', '第三方网销': '19', '普通兼业代理（网销）': '42',
                '普通经纪（网销）': '47', '普通专业代理（网销）': '45', '其他网销': '18', '网电融合（网电）': '51', '银行兼业代理（网销）': '41', '自营网销': '14',
                '银邮': '6', '银保通': '33', '银行代理': '27', '邮局业务': '40'}
    data = {}
    for word in word_list:
        for i in dictionary['notCar_channel']:
            if i == word:
                value = dict_dev[i]
                data[tag_id] = value
    return data


def get_not_car_time_code(query, tag_id1, tag_id2, tag_id3, tag_id4, time_period):
    data = {}
    message = ""
    if time_period != "":
        if '签单' in query:
            data[tag_id1] = time_period
        elif '入账' in query:
            data[tag_id2] = time_period
        elif '起保' in query or '投保' in query:
            data[tag_id3] = time_period
        elif '止期' in query or '截止' in query or '到期' in query:
            data[tag_id4] = time_period
        else:
            data[tag_id2] = time_period
    else:
        message = "未识别到日期值"
    return data, message


# 提前签单天数维度
def get_advance_sign_days(word_list, query, tag_id):
    data = {}
    return data


# 投保人省份
province_list = ['沪', '云', '江', '滇', '内蒙', '蒙', '京', '吉', '川', '蜀', '津', '宁', '宁夏', '皖', '鲁', '晋', '粤', '桂', '新', '新疆',
                 '苏', '赣',
                 '冀', '豫', '浙', '琼', '鄂', '湘', '甘', '陇', '闽', '藏', '贵', '黔', '辽', '渝', '陕', '秦', '青', '黑',
                 '上海', '云南', '内蒙古', '北京', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西',
                 '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江',
                 '上海市', '云南省', '内蒙古自治区', '北京市', '吉林省', '四川省', '天津市', '宁夏回族自治区', '安徽省', '山东省', '山西省', '广东省', '广西壮族自治区',
                 '新疆维吾尔自治区', '江苏省', '江西省', '河北省', '河南省', '浙江省', '海南省', '湖北省', '湖南省', '甘肃省', '福建省', '西藏自治区', '贵州省',
                 '辽宁省',
                 '重庆市', '陕西省', '青海省', '黑龙江省']


def identify_provinces(words_list, query, tag_id, dictionary):
    data = {}
    site_list = []
    site_dict = dictionary["noncar_identify_provinces"]
    target_list = []
    if '投保' in words_list or '投保人' in words_list:
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
    short_dict = dictionary["short_dict"]
    data = {}
    insurance_dict = dictionary["notCar_insurance_type"]
    final_list = []
    final_list1 = []
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
    for _ in final_list:
        final_list1.append(str(_))
    data[tag_id] = ",".join(final_list1)
    # print(data)
    return data
