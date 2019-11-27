# -*- coding: UTF-8 -*-
import re
from datetime import datetime

import jieba
from jieba import posseg

from common import judge_utils, get_key, get_include_target, get_include_condition, get_include_dimension


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


# 首次投保车险客户数
def get_first_insure(word_list, tag_id, slot):
    data = {}
    first_dict = {'否': '0', '是': '1'}
    first_insure_list = ["首次", "第一次"]
    for key_word in first_insure_list:
        if key_word in word_list and "投保" in slot:
            data[tag_id] = '是'
            data = judge_utils(word_list, key_word, data, tag_id)
    if data:
        data[tag_id] = first_dict[data[tag_id]]
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
    car_organization_1100 = dictionary['car_organization']
    for j in car_organization_1100.keys():
        if j in query:
            data[tag_id] = dictionary['car_organization'][j]
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


# 车险时间日期值
def get_car_time_code(query, word_list, tag_id1, tag_id2, tag_id3, tag_id4, tag_id5, tag_id6, time_period):
    data = {}
    car_time_is_effective = True
    if time_period != "":
        list1 = ['起保', '起保日期', '投保', '投保日期']
        for i in list1:
            if i in word_list:
                data[tag_id1] = time_period
        if not data:
            list2 = ['终保', '终保日期']
            for i in list2:
                if i in word_list:
                    data[tag_id2] = time_period
        if not data:
            list3 = ['录入', '录入日期']
            for i in list3:
                if i in word_list:
                    data[tag_id3] = time_period
        if not data:
            list4 = ['签单', '签单日期']
            for i in list4:
                if i in word_list:
                    data[tag_id4] = time_period
        if not data:
            list5 = ['生效', '生效保单', '签发', '签发日期']
            for i in list5:
                if i in word_list:
                    data[tag_id5] = time_period
        if not data:
            data[tag_id1] = time_period
        list6 = ['保费入账日期', '保费入账', '入账', '入账日期']
        for j in list6:
            if j in query:
                data[tag_id6] = time_period
    else:
        car_time_is_effective = False
        current_year = str(datetime.now().year)
        data[tag_id1] = current_year + "/01/01," + current_year + "/12/31"
    return data, car_time_is_effective


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
def get_car_gender(words_list, query):
    data = {}
    gender_list = ['男', '女', '男性', '女性', '男生', '女生', '男人', '女人']
    gender_dict = {
        '男': '1010050001', '女': '1010050002', '男性': '1010050001', '女性': '1010050002',
        '男生': '1010050001', '女生': '1010050002', '男人': '1010050001', '女人': '1010050002'}
    for i in words_list:
        if i in gender_list:
            gender_index = words_list.index(i)
            target_list = words_list[0:gender_index]
            if '子' not in target_list:
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
    type_list = ['交强险', '商业险', '城市公交', '出租、租赁用车', '党政机关、事业团体用车', '非营业挂车', '非营业货车', '公路客运车', '家庭自用车',
                 '兼用型拖拉机', '摩托车', '企业用车', '特种车', '营业挂车', '营运货车', '运输型拖拉机', '城市公交',
                 '出租车', '党政机关用车', '非营业摩托车', '非营业特种车', '公路客运', '家庭自用车', '兼用型拖拉机', '企业非营业用车',
                 '事业团体用车', '营业货车', '营业摩托车', '营业特种车', '运输型拖拉机', '租赁车']
    code_list1 = []
    for k in code_dict:
        type_list.append(k)
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
        data[tag_id] = 1 if '去除' in words_list else 0

    if '去除' in words_list:
        key_index = words_list.index('去除')
        # location_list = words_list[key_index, len(words_list)-1]
        if '摩托车' in words_list or '拖拉机' in words_list:
            data[tag_id] = 1

    if data:
        data[tag_id] = str(data[tag_id])

    return data


# 车辆种类
def car_vehicle_type(words_list, query, tag_id, dictionary):
    car_vehicle_type_words_list = ['交强险', '商业险', '功率小于等于14.7KW的低速载货汽车', '三轮汽车（2缸以上）', '50CC', '手扶拖拉机', '250CC(含)',
                                   '功率大于14.7KW小于等于17.6KW的三轮汽车', '36座及36座以上客车', '三轮汽车', '功率大于17.6KW小于等于50KW的超标变拖',
                                   '三轮汽车（2缸及2缸以下）', '功率大于17.6KW小于等于50KW的三轮汽车', '250CC(含)以上及侧三轮', '10吨及10吨以上挂车',
                                   '20130201前14.7KW以下运输型拖拉机', '250CC', '20座及36座以下客车', '50CC及以下摩托车', '低速载货汽车',
                                   '整体式拖拉机（2缸以上）', '250CC以上摩托车及侧三轮', '特种车一挂车', '整体式拖拉机（2缸及2缸以下）', '低速载货汽车（2缸以上）',
                                   '功率小于等于14.7KW的超标变拖', '低速载货汽车（2缸及2缸以下）', '6座及10座以下客车',
                                   '功率大于14.7KW小于等于17.6KW的低速载货汽车', '特种车三挂车', '三缸不超标', '功率大于80KW的低速载货汽车', '6座以下客车',
                                   '特种车二挂车',
                                   '250CC(含)摩托车', '特种车一', '14.7KW以上拖拉机', '特种车三', '五缸及以上',
                                   '10吨及10吨以上货车', '14.7KW以下拖拉机', '5吨及10吨以下货车', '2吨以下挂车', '10座及20座以下客车',
                                   '20130201前14.7KW以上运输型拖拉机', '功率大于80KW的超标变拖', '2吨以下货车', '功率小于等于14.7KW的符合规范的变型拖拉机',
                                   '特种车二', '5吨及10吨以下挂车', '单缸拖拉机', '功率大于50KW小于等于80KW的超标变拖', '2吨及5吨以下挂车', '2吨及5吨以下货车',
                                   '盘式拖拉机（含手扶变型运输机）', '功率大于17.6KW小于等于50KW的低速载货汽车',
                                   '三缸超标或四缸', '功率大于14.7KW小于等于17.6KW的符合规范的变型拖拉机', '功率大于50KW小于等于80KW的低速载货汽车',
                                   '功率大于14.7KW小于等于17.6KW的超标变拖', '功率小于等于14.7KW的三轮汽车', '250CC以上及侧三轮',
                                   '三缸拖拉机', '四缸拖拉机', '特种车四', '功率大于50KW小于等于80KW的三轮汽车', '双缸拖拉机']

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


# 投保人证件类型
def id_filter(words_list, query, tag_id, dictionary):
    data = {}
    list_dev1 = []
    common_dict = dictionary[tag_id]
    id_list = []
    value_list = []
    for key in common_dict.keys():
        id_list.append(key)
    for value in common_dict.values():
        value_list.append(value)
        value_list = list(set(value_list))
    for word in words_list:
        if word in id_list:
            list_dev1.append(str(common_dict[word]))
            word_index = words_list.index(word)
            fei_index = word_index - 1
            if words_list[fei_index] == '非':
                value_list.remove(common_dict[word])
                list_dev1 = value_list

    if list_dev1:
        list_dev = [str(x) for x in list_dev1]
        str_dev = ','.join(list_dev)
        data[tag_id] = str_dev
    if data:
        print(data)
    return data


# 职业 待改
def find_policyholder_industry(words_list, query, tag_id, dictionary):
    data = {}
    key_word = ['从事', '属于']
    profession_dict = dictionary[tag_id]
    profession_list = []
    final_list = []
    industry_name = []
    for key in profession_dict.keys():
        profession_list.append(key)
        profession_list = list(set(profession_list))  # 去重
    for i in key_word:
        if i in query:
            for j in profession_list:
                if j in query:
                    final_list.append(profession_dict[j])
                    industry_name.append(j)
    data[tag_id] = final_list
    # key_index = words_list.index(i)
    # profession_index = key_index + 3
    # if profession_index > len(words_list):
    #     profession_index = len(words_list)
    # else:
    #     profession_index = key_index + 3
    # for j in profession_list:
    #     if j in words_list[key_index:profession_index]:
    #         j = j + "业"
    #         final_list.append(profession_dict[j])
    if data:
        data[tag_id] = ",".join(final_list) + '$$$' + ",".join(industry_name)
    # print("data_____", data)
    return data


# 投保人职业 待改
def find_policyholder_profession(words_list, query, tag_id, dictionary):
    key_word = ['是', '职业']
    data = {}
    profession_dict = dictionary[tag_id]
    profession_list = []
    final_list = []
    profession_name = []
    for key in profession_dict.keys():
        profession_list.append(key)
        profession_list = list(set(profession_list))  # 去重
    for i in key_word:
        if i in query:
            for j in profession_list:
                if j in query:
                    final_list.append(profession_dict[j])
                    profession_name.append(j)
    data[tag_id] = final_list
    if data:
        data[tag_id] = ",".join(final_list) + '$$$' + ",".join(profession_name)
    # print("data_____", data)
    return data


# 民族,待改
def find_policyholder_nation(words_list, query, tag_id, dictionary):
    data = {}
    nation_list = []
    nation_name = []
    nation_dict = dictionary[tag_id]
    nation_dict1 = {'景颇族': '1010120028', '高山族': '1010120023', '俄罗斯族': '1010120044', '黎族': '1010120019',
                    '壮族': '1010120008', '彝族': '1010120007', '佤族': '1010120021', '拉祜族': '1010120024',
                    '苗族': '1010120006', '撒拉族': '1010120035', '畲族': '1010120022', '满族': '1010120011',
                    '锡伯族': '1010120038', '达斡尔族': '1010120031', '瑶族': '1010120013', '柯尔克孜族': '1010120029',
                    '布朗族': '1010120034', '傈僳族': '1010120020', '裕固族': '1010120048', '仡佬族': '1010120037',
                    '毛南族': '1010120036', '蒙古族': '1010120002', '白族': '1010120014', '鄂温克族': '1010120045',
                    '朝鲜族': '1010120010', '阿昌族': '1010120039', '京族': '1010120049', '纳西族': '1010120027', '未知': '9999',
                    '赫哲族': '1010120053', '鄂伦春族': '1010120052',
                    '哈尼族': '1010120016', '傣族': '1010120018', '哈萨克族': '1010120017', '土族': '1010120030',
                    '普米族': '1010120040', '侗族': '1010120012', '水族': '1010120025', '东乡族': '1010120026',
                    '仫佬族': '1010120032', '回族': '1010120003', '乌孜别克族': '1010120043', '藏族': '1010120004',
                    '土家族': '1010120015', '羌族': '1010120033', '0000019999': '0000019999',
                    '布依族': '1010120009', '维吾尔族': '1010120005', '塔吉克族': '1010120041'}
    final_list = []
    # if "少数民族" in query:
    #     print("21111+++++++++++++++++")
    #     for key in nation_dict1.keys():
    #         nation_name.append(key)
    #     for value in nation_dict1.values():
    #         nation_list.append(value)
    #     data[tag_id] = final_list
    #
    # else:
    for key in nation_dict.keys():
        nation_list.append(key)
        nation_list = list(set(nation_list))
    for i in nation_list:
        if i in query:
            final_list.append(nation_dict[i])
            nation_name.append(i)
    data[tag_id] = final_list

    if data:
        data[tag_id] = ",".join(final_list) + '$$$' + ",".join(nation_name)
    # print("data_____", data)
    return data


# 特种车分类
def find_special_vehicle(words_list, query, tag_id, dictionary):
    data = {}
    special_vehicle_list = dictionary[tag_id]
    final_list = []
    for i in special_vehicle_list:
        if i in query:
            final_list.append(i)
            data[tag_id] = final_list
    if '特种车' in words_list:
        final_list.append('特种车二其它')
        final_list.append('特种车三其它')

    if '排气量' in words_list and 'cc' in query:
        # type_list = ['排气量(50cc及以下)', '排气量(50cc－100cc含)', '排气量(100cc－250cc含)', '排气量(250cc以上)']
        # key_index = words_list.index('排气量')
        if '50' in query and "cc以下" in query:
            final_list.append('排气量(50cc及以下)')
        if '50' in query and '100' in query:
            final_list.append('排气量(50cc－100cc含)')
        if '100' in query and '250' in query:
            final_list.append('排气量(100cc－250cc含)')
        if '250' in query and "cc以上" in query:
            final_list.append('排气量(250cc以上)')
        data[tag_id] = final_list
    if data:
        data[tag_id] = ','.join(final_list) + '$$$' + ','.join(final_list)
    return data


# 特殊业务语料车规则处理
def get_car_special_words(query, data_dev, car_time_is_effective):
    data = {}
    insured_word = ["被保", "被投保"]
    list1 = ["承包分析", "承包情况", "投保情况", "出单情况", "分布情况", "销售情况"]
    list1_dev = ["统计", "查询", "日报"]
    for i in list1:
        if i in query:
            # 如果筛选是二级则变为三级，如果筛选是三级则变为四级
            if not get_include_dimension(data_dev):
                data["car_organization_2_group"] = "1"
                data["new_channel_channel"] = "1"
                data["car_personal_or_group_group"] = "1"
                data["car_interval_group"] = "BNDJY_CHINA"
            data["car_index_clients"] = "-1"
            data["car_index_policy_pieces"] = "-1"
            data["car_premium_sum"] = "-1"
            data["car_index_vehicle_numbers"] = "-1"
    for i in list1_dev:
        if i in query and not get_include_target(data_dev):
            if not get_include_dimension(data_dev):
                # 如果筛选是二级则变为三级，如果筛选是三级则变为四级
                data["car_organization_2_group"] = "1"
                data["new_channel_channel"] = "1"
                data["car_personal_or_group_group"] = "1"
                data["car_interval_group"] = "BNDJY_CHINA"
            data["car_index_clients"] = "-1"
            data["car_index_policy_pieces"] = "-1"
            data["car_premium_sum"] = "-1"
            data["car_index_vehicle_numbers"] = "-1"
    list2 = ["客户分析", "客户情况", "投保人情况", "脸谱分析"]
    for i in list2:
        if i in query:
            if not get_include_dimension(data_dev):
                data["car_organization_2_group"] = "1"
                data["new_channel_channel"] = "1"
                data["car_personal_or_group_group"] = "1"
                data["car_interval_group"] = "BNDJY_CHINA"
                for j in insured_word:
                    if j in query:
                        data["car_gender_group"] = "1"
                        data["issue_age_min_group"] = "0-25,26-35,36-45,46-55,56-#"
                    else:
                        data["car_insured_gender_group"] = "1"
                        data["issued_age__group"] = "0-25,26-35,36-45,46-55,56-#"
            data["car_index_clients"] = "-1"
    list3 = ["渗透率", "搭售率"]
    for i in list3:
        if i in query:
            data["car_index_clients"] = "-1"
    list4 = ["赔付分析", "赔付情况"]
    for i in list4:
        if i in query:
            if not get_include_dimension(data_dev):
                data["car_organization_2_group"] = "1"
                data["new_channel_channel"] = "1"
                data["car_personal_or_group_group"] = "1"
    list5 = ["续保分析", "续保情况"]
    for i in list5:
        if i in query:
            if not get_include_dimension(data_dev):
                data["car_organization_2_group"] = "1"
                data["new_channel_channel"] = "1"
                data["car_personal_or_group_group"] = "1"
            data["car_index_clients"] = "-1"
            data["car_index_vehicle_numbers"] = "-1"
    return data


# 统保代码识别
# def find_blanket_insurance(words_list, query, tag_id, dictionray):
#     data = {}
#     final_list = []
#     code_list = ['A', 'B', 'C', 'D']
#     if '统保' in words_list and '代码' in words_list:
#         key_index = words_list.index('代码')
#         # location = words_list[key_index, len(words_list)]
#         for i in code_list:
#             if i in query:
#                 final_list.append(i)
#             data[tag_id] = final_list
#     if data:
#         data[tag_id] = ','.join(final_list)
#     return data


# 车险险种
def filter_car_insurance_type(words_list, tag_id, dictionary):
    # '子女教育安家保险': '34P00600, 34P00300', '子女教育婚嫁': '34S00100'， '子女教育安家-镇江': '34914000'
    data = {}
    final_list = []
    name_list = []
    common_dict = dictionary[tag_id]
    for word in words_list:
        if word in common_dict:
            final_list.append(str(common_dict[word]))
            name_list.append(word)
    if '子女教育' in words_list:
        final_list = ['34P00600', '34P00300', '34S00100', '34914000']
        name_list = ['子女教育安家保险', '子女教育安家保险', '子女教育婚嫁', '子女教育安家-镇江']
    if final_list:
        str_dev = ','.join(final_list) + '$$$' + ','.join(name_list)
        data[tag_id] = str_dev
    # if data:
    #     # print(data)
    return data


def get_common_dict(words_list, tag_id, dictionary):
    data = {}
    list_dev = []
    common_dict = dictionary[tag_id]
    for word in words_list:
        if word in common_dict:
            list_dev.append(str(common_dict[word]))
    if list_dev:
        str_dev = ','.join(list_dev)
        data[tag_id] = str_dev
    if data:
        print(data)
    return data


# 车险删去多余误填充方法
def car_del_extra_fill(data):
    list_keys = data.keys()
    if "car_premium_sum" in list_keys and "car_additional_premium_sum" in list_keys:
        data.pop("car_premium_sum", 0)
    if "sub_new_car" in list_keys and "new_car" in list_keys:
        data.pop("new_car", 0)
    return data


# 车险未加识别功能的字段
def car_get_undefined_field(query, word_list):
    data = {}
    message_list = []
    list1 = ["品牌"]
    for i in list1:
        if i in word_list:
            message_list.append("品牌")
    list2 = ["车系"]
    for i in list2:
        if i in word_list:
            message_list.append("车系")
    list3 = ["车型"]
    for i in list3:
        if i in word_list:
            if "精友车型" not in query:
                message_list.append("车型")
    list4 = ["经办人"]
    for i in list4:
        if i in word_list:
            message_list.append("经办人")
    list5 = ["代理点"]
    for i in list5:
        if i in word_list:
            message_list.append("代理点")
    list6 = ["精友车型编码", "精友车型"]
    for i in list6:
        if i in word_list:
            message_list.append("精友车型编码")
    list7 = ["渠道合作代码"]
    for i in list7:
        if i in word_list:
            message_list.append("渠道合作代码")
    list8 = ["合作企业", "渠道合作企业名称"]
    for i in list8:
        if i in word_list:
            message_list.append("渠道合作企业名称")
    list9 = ["合作伙伴代码"]
    for i in list9:
        if i in word_list:
            message_list.append("合作伙伴代码")
    list10 = ["精友车型名称"]
    for i in list10:
        if i in word_list:
            message_list.append("精友车型分类名称")
    if len(message_list) != 0:
        message = ("未拓展" + ','.join(message_list) + "识别功能,需手动添加")
    else:
        message = ""
    data["message"] = message
    return data
