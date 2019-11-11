# -*- coding: UTF-8 -*-
import re

import jieba
from jieba import posseg

from common import judge_utils, get_key


# car_target = {}
#
# car_target['投保人客户数'] = ['投保人客户数', '投保客户数', '客户数']
# car_target['保费和'] = ['保费和', '保费收入', '保费情况']
# car_target['保单件数'] = ['保单件数', '保单数']
# car_target['车辆数'] = ['车辆数', '车辆数（纯车）']


def get_car_chetargets(words_list):
    #     targets = []
    #     targets_dict = car_target
    #
    #     for key in targets_dict.keys():
    #         for item in targets_dict[key]:
    #             if item in words_list:
    #                 targets.append(key)
    #
    #     print(targets)
    #     return list(set(targets))
    return


# 获取车险维度字段中险种类信息
def get_cardim_insurance(query):
    pass


# 获取车险维度字段中来源类信息
def get_cardim_source(query):
    data = {}
    data['channel_1'] = None
    data['channel_2'] = None
    data['channel_3'] = None
    data['group'] = None
    data['depart'] = None
    data['branch'] = None

    if '一级渠道' in query:
        data['channel_1'] = '一级渠道'
    if '二级渠道' in query:
        data['channel_2'] = '二级渠道'
    if '三级渠道' in query:
        data['channel_3'] = '三级渠道'

    if '各分公司' in query:
        data['branch'] = '分公司'
    if '部门组' in query:
        data['group'] = '部门组'
    if '部门' in query:
        data['depart'] = '部门'

    print(data)
    return data


# 获取车险筛选字段中的交叉类字段信息

def car_cross_class(query):
    data = {}
    data['is_life'] = None
    data['is_non_car'] = None
    data['is_health'] = None

    if "车险" in query:

        if "寿险" in query:
            data['is_life'] = '是'
        if '非车' in query:
            data['is_non_car'] = '是'
        if '不是健康险' in query:
            data['is_health'] = '否'
        elif '健康险' in query:
            data['is_health'] = '是'

    print(data)
    return data


# car_screen_insu = ['交强险', '商业险']
# car_screen_mark = ['个人', '团体']


# 获取车险筛选字段中的保单类类字段信息
def get_car_insurance(query, dictionary):
    data = {}
    data['person_or_group'] = []
    data['car_insurance_type'] = []

    for item in dictionary['car_screen_insu']:
        if item in query:
            data['car_insurance_type'].append(item)

    for item in dictionary['car_screen_mark']:
        if item in query:
            data['person_or_group'].append(item)

    print(data)
    return data


# 车险筛选字段车辆信息
def get_car_info(query):
    data = {}
    if '非次新车' in query or '不是次新车' in query:
        data['sub_new_car'] = '0'
    elif "次新车" in query:
        data['sub_new_car'] = '1'
    if '非新车' in query or '不是新车' in query:
        data['new_car'] = '0'
    elif '新车' in query:
        data['new_car'] = '1'
    if '非家庭自用车' in query or '不是家庭自用车' in query:
        data['self_car'] = '0'
    elif '家庭自用车' in query:
        data['self_car'] = '1'
    # print(data)
    return data


def get_car_common(data, word_list, slot):
    # 多个关键词
    data = {}
    first_dict = {'否': '0', '是': '1'}
    first_insure_list = ["首次", "第一次"]
    for key_word in first_insure_list:
        if key_word in word_list and "投保" in slot and "车险" in slot:
            data["first_insure"] = '是'
            data = judge_utils(word_list, key_word, data, "first_insure")
    if data:
        data["first_insure"] = first_dict[data["first_insure"]]
    return data


# new_channel = ['个代团队', '普通个代', '电销协作', '网销协作', '车商中口径']


# 统保代码
def get_blanket_insurance(query, words_list, dictionary):
    data = {}
    list1 = []
    if "统保代码" in query:
        for word in words_list:
            if word in dictionary["blanket_insurance"]:
                list1.append(word)
    data["blanket_insurance"] = ",".join(list1)


# 机构
def get_car_organization(word_list, query, tag_id, dictionary):
    data = {}
    organization_1 = ['陕西', '甘肃', '广东', '温州', '厦门', '深圳', '山西', '重庆', '青岛', '青海', '北京', '山东', '宁波', '河北', '云南', '安徽',
                      '内蒙古', '海南', '江苏', '辽宁', '吉林省', '无锡', '广西', '新疆', '湖北', '常州', '天津', '河南', '江西', '大连', '贵州',
                      '西藏', '浙江', '福建', '苏州', '四川', '宁夏', '湖南', '黑龙江', '上海', '东莞']
    car_organization_list = posseg.lcut(query)
    for word, flag in car_organization_list:
        if flag == 'ns':
            if word in organization_1:
                organization = word + "分公司"
                data[tag_id] = dictionary['car_organization'][organization]
            else:
                for i in dictionary['car_organization']:
                    if word in i:
                        data[tag_id] = dictionary['car_organization'][i]
    return data


def get_car_time_code(query, tag_id1, tag_id2, tag_id3, tag_id4, tag_id5, tag_id6, time_period):
    data = {}
    message = ""
    if time_period != "":
        if '起保' in query or '投保' in query:
            data[tag_id1] = time_period
        elif '终保' in query:
            data[tag_id2] = time_period
        elif '录入' in query:
            data[tag_id3] = time_period
        elif '签单' in query:
            data[tag_id4] = time_period
        elif '生效' in query:
            data[tag_id5] = time_period
        else:
            data[tag_id1] = time_period
        if '入账' in query:
            data[tag_id6] = time_period
    else:
        message = "未识别到日期值"
    return data, message


# 车牌标示 comobox
def get_local_car(word_list, query, tag_id, dictionary):
    data = {}
    local_dict = {
        '本地牌照': '1', '本地车牌': '1', '非本地车牌': '2', '非本地车牌照': '2',
        '异地车': '2', '非本地': '2', '临时牌照': '0'
    }
    local_list = ["本地牌照", "本地车牌", "临时牌照"]
    not_local_host = ["非本地牌照", "非本地车牌", "异地车", "非本地"]
    for i in local_list:
        if i in query:
            data[tag_id] = i
    for j in not_local_host:
        if j in query:
            data[tag_id] = j

    if data:
        code_str = local_dict[data[tag_id]]
        data[tag_id] = code_str
    return data


# 性别 comobox
def get_car_gender(query):
    data = {}
    gender_list = ['男', '女']
    gender_dict = {'男': '1010050001', '女': '1010050002'}
    for i in gender_list:
        if i in query:
            data['car_gender'] = i
        if data:
            data['car_gender'] = gender_dict[i]
    return data


# 车型风险等级 comotree
def get_risk_level(words_list, query, tag_id):
    # target_point:目标索引位
    data = {}
    risk_list = ['1', '2', '3']
    get_list = []
    if '车型' in words_list and '风险' in words_list and '等级' in words_list:
        target_point = words_list.index('等级')
        # print('标识的index位置>>', words_list.index('等级'))
        for i in range(target_point - 3, target_point + 8):
            if words_list[i] in risk_list:
                get_list.append(words_list[i])
    data[tag_id] = get_list
    if data:
        data[tag_id] = ",".join(get_list)
    # print(data)
    return data


# 太保车型风险等级 comobox
def get_taibao_risk_level(words_list, query, tag_id):
    data = {}
    risk_list = ['A', 'B', 'C', 'D', 'E', '其他']
    if '风险' in words_list and '标识' in words_list:
        target_point = words_list.index('标识')
        # print('标识的index位置>>', word_list.index('标识'))
        for i in range(target_point - 2, target_point + 3):
            if words_list[i] in risk_list:
                data[tag_id] = words_list[i]

    # print(data)
    return data


# 投保期限未完善
def number_section(num):
    limit_list = [0, 30, 180, 360]
    if len(num) >= 2:
        num = list(map(int, num))
        # print('num2222', num)
        for i in limit_list:
            if num[0] <= i:
                num[0] = i
                break
        for i in limit_list:
            if num[1] <= i:
                num[1] = i
                break

    if len(num) == 1:
        num = list(map(int, num))
        # print('num1111', num)
        for i in limit_list:
            if num[0] == i:
                num.append(limit_list[limit_list.index(i) + 1])
                break
            if num[0] < i:
                num.append(i)
                # print('num[0]>>', num[0])
                if limit_list.index(i) - 1 >= 0:
                    num[0] = limit_list[limit_list.index(i) - 1]
                    break
            if num[0] >= 360:
                num[0] = 360
                num.append("+")
                break
    # print(num)
    # return num
    # print('A函数>>>>', list(map(str, num)))
    return list(map(str, num))


def insurance_time_limit(words_list, query, tag_id):
    data = {}
    num = []
    if '投保' in words_list and '期限' in words_list:
        num = re.findall(r"\d+\.?\d*", query)
        num = number_section(num)

    key_words1 = ['大于', '高于']
    for i in words_list:
        if i in key_words1:
            target_index = words_list.index(i)
            target_location = words_list[target_index:]
            if '一年' in target_location:
                num = [360]
            if '半年' in target_location:
                num = [180]
            if '三个月' in target_location:
                num = [90]
            if '一个月' in target_location:
                num = [30]
            num = number_section(num)

    key_words2 = ['小于', '低于']
    for i in words_list:
        if i in key_words2:
            target_index = words_list.index(i)
            target_location = words_list[target_index:]
            if '一年' in target_location:
                num = [180, 360]
            if '半年' in target_location:
                num = [30, 180]
            if '三个月' in target_location:
                num = [0, 30]
            if '一个月' in target_location:
                num = [0, 30]
            num = number_section(num)

    key_words3 = ['以上', '往后']
    for i in words_list:
        if i in key_words3:
            target_index = words_list.index(i)
            target_location = words_list[0:target_index]
            if '一年' in target_location:
                num = [360]
            if '半年' in target_location:
                num = [180, 360]
            if '一个月' in target_location:
                num = [30, 180]
            num = number_section(num)
    data[tag_id] = num
    return data


# # 车险中车辆使用性质
def filter_using_nature(words_list, query, tag_id, dictionary):
    code_dict = dictionary["Car_using_property"]
    type_list = []
    code_list1 = []
    for k in code_dict:
        type_list.append(k)
    # init_slot(type_list)
    data = {}
    code_list = []
    if '交强险' in words_list:
        for i in words_list:
            if i in type_list[2:]:
                search_tag = '交强险-' + i
                if search_tag in type_list:
                    data[tag_id] = code_dict[search_tag]

    if '商业险' in words_list:
        for i in words_list:
            if i in type_list[2:]:
                search_tag = '商业险-' + i
                if search_tag in type_list:
                    data[tag_id] = code_dict[search_tag]

    else:
        for i in words_list:
            if i in type_list[2:]:
                search_tag1 = '商业险-' + i
                search_tag2 = '交强险-' + i
                if search_tag1 in type_list:
                    code_list.append(code_dict[search_tag1])
                if search_tag2 in type_list:
                    code_list.append(code_dict[search_tag2])
        data[tag_id] = code_list
        if data:
            for _ in code_list:
                _ = str(_)
                code_list1.append(_)
        data[tag_id] = ",".join(code_list1)

    # print("1111111", data)
    return data


# 筛选摩托车，拖拉机 combobox
def filter_motor_tractor(words_list, query, tag_id):
    data = {}
    if '摩托车' in words_list and '拖拉机' in words_list:
        data[tag_id] = 1 if '去除' in words_list else 2
    if data:
        data[tag_id] = str(data[tag_id])

    return data


# 车辆种类
car_vehicle_type_words_list = ['交强险', '商业险', '功率小于等于14.7KW的低速载货汽车', '三轮汽车（2缸以上）', '50CC', '手扶拖拉机', '250CC(含)',
                               '功率大于14.7KW小于等于17.6KW的三轮汽车', '36座及36座以上客车', '三轮汽车', '功率大于17.6KW小于等于50KW的超标变拖',
                               '三轮汽车（2缸及2缸以下）', '功率大于17.6KW小于等于50KW的三轮汽车', '250CC(含)以上及侧三轮', '10吨及10吨以上挂车',
                               '20130201前14.7KW以下运输型拖拉机', '250CC', '20座及36座以下客车', '50CC及以下摩托车', '低速载货汽车',
                               '整体式拖拉机（2缸以上）', '250CC以上摩托车及侧三轮', '特种车一挂车', '整体式拖拉机（2缸及2缸以下）', '低速载货汽车（2缸以上）',
                               '功率小于等于14.7KW的超标变拖', '低速载货汽车（2缸及2缸以下）', '6座及10座以下客车',
                               '功率大于14.7KW小于等于17.6KW的低速载货汽车', '特种车三挂车', '三缸不超标', '功率大于80KW的低速载货汽车', '6座以下客车', '特种车二挂车',
                               '250CC(含)摩托车', '特种车一', '14.7KW以上拖拉机', '特种车三', '五缸及以上',
                               '10吨及10吨以上货车', '14.7KW以下拖拉机', '5吨及10吨以下货车', '2吨以下挂车', '10座及20座以下客车',
                               '20130201前14.7KW以上运输型拖拉机', '功率大于80KW的超标变拖', '2吨以下货车', '功率小于等于14.7KW的符合规范的变型拖拉机',
                               '特种车二', '5吨及10吨以下挂车', '单缸拖拉机', '功率大于50KW小于等于80KW的超标变拖', '2吨及5吨以下挂车', '2吨及5吨以下货车',
                               '盘式拖拉机（含手扶变型运输机）', '功率大于17.6KW小于等于50KW的低速载货汽车',
                               '三缸超标或四缸', '功率大于14.7KW小于等于17.6KW的符合规范的变型拖拉机', '功率大于50KW小于等于80KW的低速载货汽车',
                               '功率大于14.7KW小于等于17.6KW的超标变拖', '功率小于等于14.7KW的三轮汽车', '250CC以上及侧三轮',
                               '三缸拖拉机', '四缸拖拉机', '特种车四', '功率大于50KW小于等于80KW的三轮汽车', '双缸拖拉机']


def car_vehicle_type(words_list, query, tag_id, dictionary):
    data = {}
    car_list = []
    code_list = []  # 多值使用列表
    code_list1 = []
    car_name = []
    code_dict = dictionary["Car_vehicle_type"]
    for k in code_dict:
        car_list.append(k)
    if '交强险' in words_list:
        for i in words_list:
            if i in car_vehicle_type_words_list[2:]:
                search_tag = '交强险-' + i
                if search_tag in car_list:
                    data[tag_id] = code_dict[search_tag]

    if '商业险' in words_list:
        for i in words_list:
            if i in car_vehicle_type_words_list[2:]:
                search_tag = '商业险-' + i
                if search_tag in car_list:
                    data[tag_id] = code_dict[search_tag]

    else:
        for i in words_list:
            if i in car_vehicle_type_words_list[2:]:
                search_tag1 = '商业险-' + i
                search_tag2 = '交强险-' + i
                if search_tag1 in car_list:
                    code_list.append(code_dict[search_tag1])
                if search_tag2 in car_list:
                    code_list.append(code_dict[search_tag2])
        data[tag_id] = code_list
    if data:
        for _ in code_list:
            car_name.append(get_key(code_dict, _)[0])
            code_list1.append(str(_))
        data[tag_id] = ",".join(code_list1) + '$$$' + ",".join(car_name)
    # print("data???", data)
    # print("22222", car_name)
    return data


def education_background(body, old_tag_id, new_tag_id, data, dictionary):
    if old_tag_id in body.keys():
        str1 = body[old_tag_id]
        dict_edu = dictionary["Car_education_background"]
        code_list = []
        list_rec = str1.split("、")
        print(list_rec)
        for j in list_rec:
            if j != "":
                code_list.append(dict_edu[j])
        code_str = ','.join(code_list)
        data[new_tag_id] = code_str
        # print(data)
    return data


# 保单类型
def get_car_policy_type(words_list, query, tag_id):
    data = {}
    if '投保' in words_list:
        if '交强险' in words_list:
            data[tag_id] = 1
        if '商业险' in words_list:
            data[tag_id] = 2
    if data:
        data[tag_id] = str(data[tag_id])
    return data


# 投保类型（人车）
# list3 = ["商业险", "交强险", "交强商业"]
# for i in list3:
#     jieba.add_word(i)
def get_car_policy_type_car(words_list, query, tag_id):
    data = {}
    if '仅' in words_list or '只' in words_list or '只有' in words_list:
        if '商业险' in words_list:
            data[tag_id] = 10
        if '交强险' in words_list:
            data[tag_id] = 1

    if '都' in words_list or '全' in words_list:
        if '交强险' in words_list and '商业险' in words_list:
            data[tag_id] = 11
        if '交强' in words_list and '商业' in words_list:
            data[tag_id] = 11
        if '交强' in words_list and '商业险' in words_list:
            data[tag_id] = 11
        if '交强险' in words_list and '商业' in words_list:
            data[tag_id] = 11
        if '交强商业' in words_list:
            data[tag_id] = 11

    if data:
        data[tag_id] = str(data[tag_id])
    return data
