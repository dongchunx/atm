import jieba
import re


def token(string):
    return re.findall(r'[\d|\w]+', string)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


def get_number(string):
    return re.findall(r"\d+\.?\d*", string)


# life_insurance = ['金佑', '金诺', '利赢', '爱无忧', '爱无忧', '安行宝', '安贷宝', '学平险', '健康险']
# car_insurance = ['交强险', '商业险', '商业保险', '车辆损失险', '车辆自燃险', '第三方责任保险', '不计免赔', '三责险']
# non_car_insurance = ['驾意险', '人意险', '人身意外保险', '交通人意险', '旅游人意险', '借款人意险', '特定人员意外险', '学生幼儿意外伤害综合保险', '家财险', '家庭财产保险',
#                     '常规家财险', '个人抵押贷款房屋综合保险', '储金类业务', '个人账户损失险', '交通意外险']
#
# car_insurance_sim = {}
# car_insurance_sim["交强险"] = ['交通强制险']
# car_insurance_sim['商业险'] = ['商业保险', '车辆损失险', '车辆自燃险', '第三方责任保险', '不计免赔']
#
# life_period = ['极短险', '短险', '一年期', '长险', '极短期']
#
# life_agencys = ['宁夏', '重庆', '吉林', '云南', '山东', '无锡', '宁波', '广西', '苏州', '黑龙江', '甘肃', '上海', '辽宁', '福建', '常州', '河北', '浙江',
#                 '安徽', '贵州', '厦门', '湖南', '内蒙古', '广东', '四川', '山西', '天津', '陕西', '豫东', '江西', '豫西', '新疆', '青岛', '豫南', '江苏',
#                 '青海', '海南', '大连', '豫北', '湖北', '深圳', '北京']
# car_agencys = ['吉林', '温州', '厦门', '海南', '大连', '河北', '四川', '广西', '云南', '湖南', '东莞', '苏州', '江西', '河南', '青海', '广东', '上海',
#                '陕西', '北京', '重庆', '甘肃', '天津', '山东', '深圳', '浙江', '辽宁', '无锡', '新疆', '山西', '黑龙江', '宁夏', '西藏', '青岛', '安徽',
#                '湖北', '江苏', '常州', '内蒙古', '宁波', '福建', '贵州']
# non_car_agencys = ['贵州', '海南', '浙江', '湖南', '江西', '青岛', '河北', '湖北', '常州', '温州', '安徽', '辽宁', '陕西', '大连', '广东', '福建', '青海',
#                    '山西', '广西', '天津', '四川', '云南', '东莞', '山东', '上海', '深圳', '河南', '宁夏', '黑龙江', '重庆', '新疆', '北京', '苏州',
#                    '西藏', '吉林', '甘肃', '厦门', '江苏', '内蒙古', '宁波', '无锡']
#
# life_agencys_expand = {}
# life_agencys_expand['七大区'] = ['华东', '华北', '西北', '华中', '华南', '东北', '西南']
# life_agencys_expand['华北'] = ['内蒙古分公司', '北京分公司', '山西分公司', '河北分公司', '天津分公司']
# life_agencys_expand['华北地区'] = ['内蒙古分公司', '北京分公司', '山西分公司', '河北分公司', '天津分公司']
# life_agencys_expand['华南'] = ['广西分公司', '东莞分公司', '深圳分公司', '海南分公司', '广东分公司', '华南运营中心']
# life_agencys_expand['华南地区'] = ['广西分公司', '东莞分公司', '深圳分公司', '海南分公司', '广东分公司', '华南运营中心']
# life_agencys_expand['华中'] = ['河南分公司', '豫北分公司', '豫西分公司', '河南分公司法人渠道业务中心', '湖南分公司', '豫东分公司', '豫南分公司', '湖北分公司']
# life_agencys_expand['华中地区'] = ['河南分公司', '豫北分公司', '豫西分公司', '河南分公司法人渠道业务中心', '湖南分公司', '豫东分公司', '豫南分公司', '湖北分公司']
# life_agencys_expand['西南'] = ['云南分公司', '重庆分公司', '四川分公司', '贵州分公司']
# life_agencys_expand['东北'] = ['大连分公司', '黑龙江分公司', '吉林省分公司', '辽宁分公司']
# life_agencys_expand['东北地区'] = ['大连分公司', '黑龙江分公司', '吉林省分公司', '辽宁分公司']
# life_agencys_expand['西南地区'] = ['云南分公司', '重庆分公司', '四川分公司', '贵州分公司']
# life_agencys_expand['西北'] = ['陕西分公司', '西藏分公司', '新疆分公司', '青海分公司', '宁夏分公司', '甘肃分公司']
# life_agencys_expand['西北地区'] = ['陕西分公司', '西藏分公司', '新疆分公司', '青海分公司', '宁夏分公司', '甘肃分公司']
# life_agencys_expand['华东'] = ['苏州分公司', '青岛分公司', '无锡分公司', '山东分公司', '安徽分公司', '上海运营中心', '航运保险事业营运中心', '福建分公司', '上海分公司',
#                              '宁波分公司', '浙江分公司', '厦门分公司', '江苏分公司',
#                              '常州分公司,江西分公司,无锡分公司,安徽分公司,厦门分公司,江苏分公司,江西分公司,温州分公司,宁波分公司,苏州分公司', '常州分公司']
# life_agencys_expand['华东地区'] = ['苏州分公司', '青岛分公司', '无锡分公司', '山东分公司', '安徽分公司', '上海运营中心', '航运保险事业营运中心', '福建分公司', '上海分公司',
#                                '宁波分公司', '浙江分公司', '厦门分公司', '江苏分公司',
#                                '常州分公司,江西分公司,无锡分公司,安徽分公司,厦门分公司,江苏分公司,江西分公司,温州分公司,宁波分公司,苏州分公司', '常州分公司']
# life_agencys_expand['云贵川'] = ['云南', '贵州', '四川']
# life_agencys_expand['京津冀'] = ['北京', '天津', '河北']
# life_agencys_expand['东三省'] = ['辽宁', '吉林', '黑龙江']
#
# life_second_agencys = ['二级机构', '分公司']
# life_third_agencys = ['三级机构', '中支公司']
# car_second_agencys = ['二级机构', '分公司']
# car_third_agencys = ['三级机构', '部门', '部门组']
# non_car_second_agencys = ['二级机构', '分公司']
# non_car_third_agencys = ['三级机构']
#
# life_channels = ['金玉兰财富管理（直销)', '中介销售（兼业）', '医保合作', '内勤业务', '银邮代理', '自营电销外包', '顾问营销', '个人业务', '网销（第三方）', '产代法-银保',
#                  '客服专员（服劳营销）', '个人客户经营(代理）', '保险经纪公司', '渠道直销', '网销（经纪）', '健养专业代理', '金玉兰财富管理（代理)', '传统营销', '保险代理公司',
#                  '团体直销', '个人客户经营(直销）', '团体业务', '产代个', '中介销售（专业）', '企业员福', '新渠道经营', '一级渠道', '兼业代理', '机构合作', '服劳营销',
#                  '产代法-机构', '健养经纪业务', '产代法-团险', '独立代理人', '客服专员(渠道客经）', '三级渠道', '中介渠道', '区域拓展（顾问营销）', '网销（自营）', '二级渠道',
#                  '互联网业务', '健养兼业代理', '营销（传统营销）', '网销（代理）', '金融合作', '网销渠道', '中介销售渠道']
# car_channels = ['个人代理', '电网销', '门店', '车商渠道', '一级渠道', '直拓', '普通兼代', '其他', '专业中介', '交叉销售']
# non_car_channels = ['网销', '车商', '个代', '其他', '银邮', '电销', '交叉']


def get_insurance_type(words_list, dictionary):
    """
     params:words_list which is tokend used jieba
     output:tuple(insurance_type, insurnace_name)
    """

    insurance_list = []
    insurance_type = "CX001"
    print(words_list)
    # only support insurance name is exact
    for item in dictionary['life_insurance']:
        if item in words_list:
            insurance_list.append(item)

    for item in dictionary['car_insurance']:
        if item in words_list:
            insurance_type = "CX001"
            insurance_list.append(item)

    for item in dictionary['non_car_insurance']:
        if item in words_list:
            insurance_type = "FC001"
            insurance_list.append(item)

    if "非车" not in words_list and "车险" in words_list or "车辆" in words_list:
        insurance_type = "CX001"
    if "非车" in words_list:
        insurance_type = "FC001"

    return insurance_type, insurance_list


def get_agencys(locations, insurance_type, dictionary):
    agencys = []
    filter_agencys = []
    life_expand_keys = []
    for key in dictionary['life_agencys_expand'].keys():
        life_expand_keys.append(key)
    if insurance_type == 0:
        agencys = dictionary['life_agencys'] + life_expand_keys
    elif insurance_type == 1:
        agencys = dictionary['car_agencys']
    elif insurance_type == 2:
        agencys = dictionary['non_car_agencys']
    else:
        # print("insurance_type {} is illegal".format(insurace_type))
        # return None
        agencys = list(set(
            dictionary['life_agencys'] + life_expand_keys + dictionary['car_agencys'] + dictionary['non_car_agencys']))
    for loc in locations:
        if loc in agencys:
            if loc in dictionary['life_agencys_expand'].keys():
                filter_agencys = filter_agencys + dictionary['life_agencys_expand'][loc]
            else:
                filter_agencys.append(loc)
    return filter_agencys


def get_channels(words_list, insurance_type, dictionary):
    filter_channels = []
    channels = []

    if insurance_type == 0:
        filter_channels = dictionary['life_channels']
    elif insurance_type == 1:
        filter_channels = dictionary['car_channels']
    elif insurance_type == 2:
        filter_channels = dictionary['non_car_channels']
    else:
        filter_channels = dictionary['life_channels'] + dictionary['car_channels'] + dictionary['non_car_channels']
        # print("insurance_type {} is illegal".format(insurace_type))
        # return None

    for channel in filter_channels:
        for word in words_list:
            if channel in word:
                channels.append(channel)

            if channel in word:
                # if channel in word or word in channel:
                channels.append(channel)
    return list(set(channels))


# def get_targets(words_list, insurance_type):
#     targets = []
#     targets_dict = target_sim
#
#     if insurance_type == 1:
#         targets_dict.update(target_car)
#     elif insurance_type == 2:
#         targets_dict.update(target_non_car)
#
#     for key in targets_dict.keys():
#         if key in words_list:
#             targets.append(key)
#         for item in targets_dict[key]:
#             if item in words_list:
#                 targets.append(key)
#         for word in words_list:
#             if word in key:
#                 targets.append(key)
#
#     return list(set(targets))


def get_life_period(words_list, dictionary):
    periods = []

    for item in dictionary['life_period']:
        if item in words_list:
            periods.append(item)
    return periods


# 筛选通用枚举字段(词典中为字典格式)
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


# 筛选通用枚举字段(词典中为列表格式)
def get_common_list(word_list, tag_id, dictionary):
    data = {}
    list_common_list = []
    common_list = dictionary[tag_id]
    for word in word_list:
        if word in common_list:
            list_common_list.append(str(word))
    if list_common_list:
        str_common_list = ','.join(list_common_list)
        data[tag_id] = str_common_list
    if data:
        print(data)
    return data


# 用于单个关键字的是否判断（只能传单个关键字）
# 需改造成列表传参形式，方便加别名
def get_true_or_false(word_list, key_word_list, tag_id):
    data = {}
    for key_word in key_word_list:
        if key_word in word_list:
            data[tag_id] = '1'
            data = judge_utils(word_list, key_word, data, tag_id)
    return data


# 判断是否为否定词
def judge_utils(word_list, key_word, data, tag_id):
    index = word_list.index(key_word)
    # 否定词集合
    negative_word = ["不", "非", "没", "无", "否"]
    min_index = index - 2
    max_index = index + 3
    if min_index < 0:
        min_index = 0
    if max_index > 0:
        max_index = len(word_list)
    for i in range(min_index, max_index):
        if 0 <= i < len(word_list):
            if word_list[i]:
                for j in negative_word:
                    if j in word_list[i]:
                        data[tag_id] = '0'
                        break
    return data


def get_numbers_common(word_list, query, key_word_list):
    """
    :param word_list:
    :param query:
    :param key_word_list:
    :return:
    """
    num_list = []
    final_list = []
    for key_word in key_word_list:
        if key_word in word_list:
            list_word = re.findall(r'{}.*'.format(key_word), query)
            if list_word:
                word_list_dev = jieba.lcut(list_word[0])
                for i in word_list_dev:
                    if len(get_number(i)) > 0:
                        if i == get_number(i)[0]:
                            num_list.append(i)
                for index, i in enumerate(word_list_dev):
                    num_min = ''
                    num_max = ''
                    if i == '-' or i == '到':
                        if index - 2 >= 0:
                            word = word_list_dev[index - 1]
                            if word in num_list:
                                num_min = word
                            elif word == '天':
                                if word_list_dev[index - 2] in num_list:
                                    num_min = word_list_dev[index - 2]
                            elif word == '万':
                                if word_list_dev[index - 2] in num_list:
                                    num_min = str(float(word_list_dev[index - 2]) * 10000)
                        if index + 2 < len(word_list_dev):
                            word = word_list_dev[index + 1]
                            if word in num_list:
                                if word_list_dev[index + 2] == '万':
                                    num_max = str(float(word) * 10000)
                                else:
                                    num_max = word
                        if num_min and num_max:
                            final_list.append(str(num_min) + '-' + str(num_max))
                for index, i in enumerate(word_list_dev):
                    num_min = ''
                    num_max = ''
                    if i == '以上' and index - 2 >= 0:
                        if word_list_dev[index - 2] == '万':
                            if word_list_dev[index - 1] in num_list:
                                num_min = str(float(word_list_dev[index - 1]) * 10000)
                                num_max = '#'
                        else:
                            if word_list_dev[index - 1] in num_list:
                                num_min = word_list_dev[index - 1]
                                num_max = '#'
                        if num_min and num_max:
                            final_list.append(str(num_min) + '-' + str(num_max))
    return final_list


# 获取数值类字段详细信息
def get_number_class_detail(word_list, query, key_word_list, tag_id_1, tag_id_2, tag_id):
    """
    :param key_word_list: 关键字列表
    :param word_list:
    :param query:
    :param tag_id_1: 较小值
    :param tag_id_2: 较大值
    :param tag_id: tag_id值
    :return:
    """
    num_list = []
    data = {}
    for i in word_list:
        if len(get_number(i)) > 0:
            if i == get_number(i)[0]:
                num_list.append(i)
    for key_word in key_word_list:

        if key_word in word_list:
            data[tag_id_1] = '*'
            data[tag_id_2] = '#'
            index_word = word_list.index(key_word)
            num_min = index_word - 3
            num_max = index_word + 7
            if num_min < 0:
                num_min = 0
            if num_max >= len(word_list):
                num_max = len(word_list) - 1
            list_range = word_list[num_min:num_max]

            # 多种规则匹配
            if '-' in list_range:
                index1 = list_range.index('-')
                for j in range(1, 3):
                    if index1 - j >= 0:
                        if list_range[index1 - j] in num_list:
                            data[tag_id_1] = list_range[index1 - j]
                    if index1 + j < len(list_range):
                        if list_range[index1 + j] in num_list:
                            data[tag_id_2] = list_range[index1 + j]
            elif '到' in list_range:
                index1 = list_range.index('到')
                for i in range(0, 3):
                    if index1 - i >= 0:
                        if list_range[index1 - i] in num_list:
                            data[tag_id_1] = list_range[index1 - i]
                    if index1 + i < len(list_range):
                        if list_range[index1 + i] in num_list:
                            data[tag_id_2] = list_range[index1 + i]

            # 其后会跟最小值的词汇
            list_min_value = ['超过', '大于', '多于']
            for j in list_min_value:
                if j in list_range:
                    index2 = list_range.index(j)
                    if index2 + 1 <= len(list_range):
                        if list_range[index2 + 1] in num_list:
                            data[tag_id_1] = list_range[index2 + 1]

            # 后面会跟最大值的词汇
            list_max_value = ['低于', '小于']
            for j in list_max_value:
                if j in list_range:
                    index3 = list_range.index(j)
                    if index3 + 1 <= len(list_range):
                        if list_range[index3 + 1] in num_list:
                            data[tag_id_2] = list_range[index3 + 1]
            # 出现在最小值前面的词汇
            list1 = ["以上"]
            for j in list1:
                if j in list_range:
                    index5 = list_range.index(j)
                    for z in range(1, 3):
                        if index5 - z >= 0:
                            if list_range[index5 - z] in num_list:
                                data[tag_id_1] = list_range[index5 - z]
            list2 = ["以下"]
            for j in list2:
                if j in list_range:
                    index6 = list_range.index(j)
                    for z in range(1, 3):
                        if index6 - z >= 0:
                            if list_range[index6 - z] in num_list:
                                data[tag_id_2] = list_range[index6 - z]
            is_wan = False
            if data != {}:
                for x, y in data.items():
                    if y != '*' and y != '#':
                        index4 = word_list.index(y)
                        if word_list[index4 + 1] == '万':
                            is_wan = True
                            # data[x] = float(y) * 10000
            value_min = data[tag_id_1]
            value_max = data[tag_id_2]
            if is_wan:
                if value_min != '*':
                    value_min = float(data[tag_id_1]) * 10000
                if value_max != '#':
                    value_max = float(data[tag_id_2]) * 10000
            data[tag_id] = str(value_min) + ',' + str(value_max)
            data.pop(tag_id_1, 0)
            data.pop(tag_id_2, 0)
    # special handle for 吨位 and 车重
    if "吨" in key_word_list and "车重" in query:
        data.clear()
    return data


# 将投保人转为被投保人
def to_insured(query, old_tag_id, new_tag_id, data):
    """
    :param query:
    :param old_tag_id: 投保人tag_id
    :param new_tag_id: 被保人tag_id
    :param data:
    :return:
    """
    insured_list = ['被投保', '被保']
    for i in insured_list:
        if i in query:
            if old_tag_id in data.keys():
                data[new_tag_id] = data[old_tag_id]
                data.pop(old_tag_id, 0)


# 判断字段属性是维度还是筛选
def get_field_attribute(word_list, query, key_word_list):
    """
    :param key_word_list: 关键字列表
    :param word_list:
    :param query:
    :return:  0： 筛选； 1： 维度；
    """
    field_attribute = 0
    for key_word in key_word_list:
        if key_word in word_list:
            # print("有维度或筛选字段")
            index = word_list.index(key_word)
            # 需考虑多种表示分组词汇
            list1 = re.findall(r'按[\u2E80-\u9FFF]+分组', query)
            if list1:
                for i in list1:
                    if key_word in i:
                        field_attribute = 1
            list1 = re.findall(r'按[\u2E80-\u9FFF|\d]+分步', query)
            if list1:
                for i in list1:
                    if key_word in i:
                        field_attribute = 1
            list1 = re.findall(r'按[\u2E80-\u9FFF|\d]+看', query)
            if list1:
                for i in list1:
                    if key_word in i:
                        field_attribute = 1
            list1 = re.findall(r'按[\u2E80-\u9FFF|\d]+统计', query)
            if list1:
                for i in list1:
                    if key_word in i:
                        field_attribute = 1
            # 表维度的关键字
            dimensionality_list = ["所有", "哪", "什么", "多少", "各", "每", "分"]
            for i in dimensionality_list:
                index1 = index - 4
                if index1 <= 0:
                    index1 = 0
                for j in range(index1, index):
                    if i in word_list[j]:
                        field_attribute = 1
            # 表维度的关键字
            dimensionality_list2 = ["占比", "比例", "分布", "分别", "多少", "各自"]
            for i in dimensionality_list2:
                index2 = index + 4
                if index2 >= len(word_list):
                    index2 = len(word_list) - 1
                for j in range(index, index2 + 1):
                    if i in word_list[j]:
                        field_attribute = 1
    return field_attribute


# 转换时间格式
def get_time_detail(time_slot):
    start_year = time_slot[0][:4]
    start_month = time_slot[0][4:6]
    start_day = time_slot[0][6:8]
    end_year = time_slot[1][:4]
    end_month = time_slot[1][4:6]
    end_day = time_slot[1][6:8]
    start_time = start_year + '/' + start_month + '/' + start_day
    end_time = end_year + '/' + end_month + '/' + end_day
    return start_year, start_month, start_day, end_year, end_month, end_day, start_time, end_time


# 转换筛选字段格式
def get_filter_field(body, old_field_name, tag_id, data):
    if old_field_name in body.keys():
        if body[old_field_name] != "":
            data[tag_id] = body[old_field_name]


# 转换指标字段格式
def change_field_format(body, old_field_name, tag_id, data):
    if old_field_name in body.keys():
        if body[old_field_name] != "":
            data[tag_id] = "-1"
            # print("test")
            # print(data)


# 获取维度字段中需要返回的数值
# def get_number_in_group(word_list, query, key_word_list, tag_id):
#     num_list = []
#     result_list = []
#     number_mark = 0
#     for i in word_list:
#         if len(get_number(i)) > 0:
#             if i == get_number(i)[0]:
#                 num_list.append(i)
#     for key_word in key_word_list:
#
#         value_list = []
#         if key_word in word_list:
#             index = word_list.index(key_word)
#             for j in range(index, len(word_list)):
#                 if word_list[j] == '-' or word_list[j] == '到':
#                     if word_list[j - 1] in num_list and word_list[j + 1] in num_list:
#                         if word_list[j + 2] == '万':
#                             value_list.append([int(word_list[j - 1]) * 10000, int(word_list[j + 1]) * 10000])
#                         else:
#                             value_list.append([word_list[j - 1], word_list[j + 1]])
#             result_list = value_list
#             list_final = []
#             if result_list:
#                 number_mark = 1
#                 for i in result_list:
#                     list_final.append(str(i[0]) + '-' + str(i[1]))
#                     result_list = ','.join(list_final)
#                 print(result_list)
#     return result_list, number_mark


# # 未加识别功能的字段
# def get_undefined_field(query):
#     data = {}
#     message_list = []
#     list1 = ["品牌"]
#     for i in list1:
#         if i in query:
#             message_list.append("品牌")
#     list2 = ["车系"]
#     for i in list2:
#         if i in query:
#             message_list.append("车系")
#     list3 = ["车型"]
#     for i in list3:
#         if i in query:
#             if "精友车型" not in query:
#                 message_list.append("车型")
#     list4 = ["经办人"]
#     for i in list4:
#         if i in query:
#             message_list.append("经办人")
#     list5 = ["代理点"]
#     for i in list5:
#         if i in query:
#             message_list.append("代理点")
#     list6 = ["精友车型编码", "精友车型"]
#     for i in list6:
#         if i in query:
#             message_list.append("精友车型编码")
#     list7 = ["渠道合作代码"]
#     for i in list7:
#         if i in query:
#             message_list.append("渠道合作代码")
#     list8 = ["合作企业"]
#     for i in list8:
#         if i in query:
#             message_list.append("合作企业")
#     list9 = ["合作伙伴代码"]
#     for i in list9:
#         if i in query:
#             message_list.append("合作伙伴代码")
#     if len(message_list) != 0:
#         message = ("未拓展" + ','.join(message_list) + "识别功能,需手动添加")
#     else:
#         message = ""
#     data["message"] = message
#     return data


# 将字段名转换为tag_id
def change_field_tag_id(data_dev):
    dict_field = {'car_start_time': 200001, 'car_end_time': 200081, 'car_record_time': 200501, 'car_sign_time': 200179,
                  'car_effect_time': 200180, 'car_entry_time': 200182, 'car_personal_or_group': 200022,
                  'car_under_warranty_customer': 200677, 'car_organization': 200003, 'car_channels': 200004,
                  'new_channel': 200613, 'car_partner_code': 200082, 'channel_partner_code': 200083,
                  'channel_partner_firm_name': 200593, 'blanket_insurance': 200084, 'car_agent_point': 200085,
                  'car_agent_person': 200086, 'business_origin': 200186, 'one_way_car_insurance': 200006,
                  'filter_motor_tractor': 200007,
                  'car_insurance_type': 200099, 'self_car': 200008, 'new_car': 200009, 'sub_new_car': 200010,
                  'local_car': 200188, 'car_age': 200189, 'purchase_price': 200013, 'using_properties': 200093,
                  'car_kind': 200191, 'risk_level': 200094, 'tai_risk_level': 200014, 'car_type_name': 200015,
                  'car_barnd': 200097, 'car_series': 200192, 'car_type': 200193, 'car_type_code': 200194,
                  'ton': 200017, 'passenger_capacity': 200195, 'years_loan': 200198, 'dump_trailer': 200199,
                  'special_vehicle': 200200, 'displacement': 200204, 'car_weight': 200594,
                  'first_insure': 200209, 'car_gender': 200502, 'issue_age': 200503,
                  'policyholder_birth_day': 200225, 'id_type': 200224, 'marital_status': 200227,
                  'annual_income': 200228, 'policyholder_industry': 200229, 'policyholder_edu': 200231,
                  'policyholder_profession': 200232, 'policyholder_nation': 200233, 'car_insured_gender': 200213,
                  'issued_age': 200214, 'car_policy_type': 200098, 'car_new_renew': 200586,
                  'insurance_time_limit': 200100, 'channel_underwriting_coefficient': 200102,
                  'insurance_point': 200704, 'business_channel': 200603, 'total_premium': 200025,
                  'commercial_insurance_premium': 200026, 'vehicle_insurance_premium': 200027,
                  'car_damage_insurance_premium': 200103, 'car_damage_insurance_premium_1': 200263,
                  'car_damage_insu_no_deductible': 200104, 'three_liability_insurance_premium': 200105,
                  'three_liability_insu_no_deductible': 200106, 'glass_break_insu_premium': 200107,
                  'car_duty_insu_premium': 200108, 'car_duty_insu_no_deductible_premium': 200109,
                  'robbery_insu_premium': 200110, 'robbery_insu_no_deductible_premium': 200111,
                  'scratch_insu_premium': 200112, 'scratch_insu_no_deductible_premium': 200113,
                  'wading_insu_premium': 200114, 'self_ignite_premium': 200115,
                  'self_ignite_no_deductible_premium': 200116, 'no_deductible_premium': 200264,
                  'written_premium': 200266, 'total_sum': 200029, 'commercial_insu_total_sum': 200030,
                  'vehicle_insu_sum': 200120, 'car_damage_insu_sum': 200117,
                  'three_liability_insu_sum': 200118, 'car_duty_insu_sum': 200119,
                  'NCD_coefficient': 200277, 'commercial_insu_NCD_coefficient': 200278,
                  'vehicle_insu_NCD_coefficient': 200279, 'accident': 200033, 'accident_account': 200034,
                  'car_personal_or_group_group': 200329, 'car_under_warranty_customer_group': 200682,
                  'car_interval_group': 200330, 'car_organization_2_group': 200073, 'car_organization_3_group': 200074,
                  'car_organization_4_group': 200075, 'car_channel_1_group': 200077, 'car_channel_2_group': 200078,
                  'car_channel_3_group': 200079, 'new_channel_channel': 200649, 'blanket_insurance_group': 200128,
                  'business_origin_group': 200331, 'local_car_group': 200332, 'car_age_group': 200333,
                  'purchase_price_group': 200041, 'using_properties_group': 200137, 'car_kind_group': 200335,
                  'car_insurance_type_group': 200141, 'car_brand_group': 200337, 'car_series_group': 200338,
                  'special_vehicle_group': 200346, 'filter_motor_tractor_group': 200623, 'self_car_group': 200624,
                  'new_car_group': 200625, 'sub_new_car_group': 200626, 'car_gender_group': 200358,
                  'issue_age_min_group': 200359, 'first_insure_group': 200355, 'policyholder_birth_day_group': 200373,
                  'id_type_group': 200372, 'marital_status_group': 200375, 'policyholder_industry_group': 200377,
                  'policyholder_edu_group': 200379, 'policyholder_profession_group': 200380,
                  'car_insured_gender_group': 200361, 'issued_age__group': 200362, 'car_policy_type_group': 200627,
                  'car_new_renew_group': 200628, 'insurance_point_group': 200705, 'business_channel_group': 200639,
                  'accident_group': 200060, 'car_index_vehicle_numbers': 200504, 'car_index_policy_pieces': 200507,
                  'car_premium_sum': 200510, 'car_additional_premium_sum': 200721, 'car_insured_amount_sum': 200711,
                  'car_additional_insured_amount_sum': 200722, 'car_average_premium': 200480,
                  'car_commercial_average_premium': 200511, 'car_index_clients': 200512,
                  'car_customer_average_premium': 200487, 'car_sign_premium_sum': 200551, 'notCar_sign_time': 5000001,
                  'notCar_record_time': 5000002, 'notCar_start_time': 5000003, 'notCar_end_time': 5000004,
                  'notCar_organization': 5000006, 'notCar_channel': 5000069, 'notCar_issue_tool': 5000009,
                  'notCar_gender': 5000012, 'start_insure_age': 5000013, 'now_age': 5000014,
                  'notCar_constellation': 5000070, 'notCar_province': 5000015, 'notCar_insurance_gender': 5000016,
                  'start_insured_age': 5000017, 'insured_now_age': 5000018, 'notCar_insured_constellation': 5000071,
                  'notCar_insured_province': 5000019, 'notCar_new_customer': 5000021, 'current_year_customer': 5000176,
                  'notCar_insurance': 5000072, 'notCar_insurance_period': 5000026, 'notCar_policy_status': 5000027,
                  'accept_insurance': 5000193, 'insurance_premiums': 5000168, 'insurance_account': 5000189,
                  'advance_sign_day': 5000203, 'notCar_personal_group': 5000196, 'notCar_agent_point': 5000204,
                  'notCar_partner_code': 5000199, 'interval': 5000030, 'notCar_organization_2': 5000032,
                  'notCar_organization_3': 5000033, 'notCar_organization_4': 5000034, 'acquisition_way_group': 5000035,
                  'channel_group': 5000036, 'issue_tool_group': 5000037, 'gender_group': 5000040,
                  'start_insure_age_group': 5000041, 'now_age_group': 5000042, 'constellation_group': 5000090,
                  'province_group': 5000043, 'insured_gender_group': 5000044, 'start_insured_age_group': 5000045,
                  'now_insured_age_group': 5000046, 'insured_constellation_group': 5000091,
                  'insured_province_group': 5000047, 'notCar_new_customer_group': 5000049,
                  'current_year_customer_group': 5000179, 'insurance_type_group': 5000053,
                  'insurance_type_one_group': 5000092, 'insurance_type_two_group': 5000093,
                  'insurance_type_details_group': 5000094, 'policy_status_group': 5000056,
                  'accept_insurance_group': 5000195, 'insurance_premiums_group': 5000171,
                  'insurance_account_group': 5000190, 'advance_sign_day_group': 5000208,
                  'notCar_personal_group_group': 5000197, 'partner_group': 5000200,
                  'non_car_index_customer': 5000058, 'non_car_index_insured_customer': 5000059,
                  'non_car_index_fee': 5000122, 'non_car_index_record_fee': 5000060,
                  'non_car_index_average_fee': 5000061, 'non_car_index_insured_amount': 5000062,
                  'non_car_index_average_insured_amount': 5000063, 'non_car_index_policy_pieces': 5000064,
                  'non_car_index_average_policy_pieces': 5000065, 'non_car_index_premium': 5000142,
                  'non_car_customer_average_age': 5000220, 'non_car_insured_customer_average_age': 5000221}
    data = {}
    if data_dev != {}:
        for i in data_dev:
            if i in dict_field:
                data[dict_field[i]] = data_dev[i]
    return data


# 时间间隔
# interval_dict = {}
# interval_dict['天'] = ['每天', '每日', '按天', '按日', '按照日', '按照天', '分天']
# interval_dict['周'] =['星期', '礼拜', '每周', '按周', '按照周', '分星期']
# interval_dict['月'] = [ '各月', '按照月', '按月', '分月', '每月']
# interval_dict['季度'] = ['按照季度', '按季', '分季', '各季度', '每季度']
# interval_dict['年'] = ['按年', '按照年', '分年', '每年']

# 时间间隔
def get_interval(query, dictionary):
    key_dict222 = {
        '年': 'BN_CHINA', '季度': 'BNDJJ_CHINA', '月': 'BNDJY_CHINA',
        '周': 'BZDYT_BZZHYT', '天': 'ZL_DATE'
    }
    for key in dictionary['interval_dict'].keys():
        for item in dictionary['interval_dict'][key]:
            if item in query:
                value = key_dict222[key]
                return value


# 获取字段属性
def get_field_kind(tag_id):
    kind_dict = {
        "condition": [5000001, 5000002, 5000003, 5000004, 5000006, 5000069, 5000009, 5000012, 5000013, 5000014, 5000070,
                      5000015, 5000016, 5000017, 5000018, 5000071, 5000019, 5000021, 5000176, 5000072, 5000026, 5000027,
                      5000193, 5000168, 5000189, 5000203, 5000196, 5000204, 5000199, 200001, 200081, 200501, 200179,
                      200180, 200182, 200022, 200677, 200003, 200004, 200613, 200082, 200083, 200593, 200084, 200085,
                      200086, 200186, 200006, 200007, 200187, 200008, 200009, 200010, 200188, 200189, 200013, 200093,
                      200191, 200094, 200014, 200015, 200097, 200192, 200193, 200194, 200017, 200195, 200198, 200199,
                      200200, 200204, 200594, 200209, 200502, 200503, 200225, 200224, 200227, 200228, 200229, 200231,
                      200232, 200233, 200213, 200214, 200098, 200099, 200586, 200100, 200102, 200704, 200603, 200025,
                      200026, 200027, 200103, 200263, 200104, 200105, 200106, 200107, 200108, 200109, 200110, 200111,
                      200112, 200113, 200114, 200115, 200116, 200264, 200266, 200029, 200030, 200031, 200117, 200118,
                      200119, 200120, 200277, 200278, 200279, 200033, 200034, 'car_start_time', 'car_end_time',
                      'car_record_time', 'car_sign_time', 'car_effect_time', 'car_entry_time', 'car_personal_or_group',
                      'car_under_warranty_customer', 'car_organization', 'car_channels', 'new_channel',
                      'car_partner_code', 'channel_partner_code', 'channel_partner_firm_name', 'blanket_insurance',
                      'car_agent_point', 'car_agent_person', 'business_origin', 'one_way_car_insurance',
                      'filter_motor_tractor', 'car_insurance_type', 'self_car', 'new_car', 'sub_new_car', 'local_car',
                      'car_age', 'purchase_price', 'using_properties', 'car_kind', 'risk_level', 'tai_risk_level',
                      'car_type_name', 'car_barnd', 'car_series', 'car_type', 'car_type_code', 'ton',
                      'passenger_capacity', 'years_loan', 'dump_trailer', 'special_vehicle', 'displacement',
                      'car_weight', 'first_insure', 'car_gender', 'issue_age', 'policyholder_birth_day', 'id_type',
                      'marital_status', 'annual_income', 'policyholder_industry', 'policyholder_edu',
                      'policyholder_profession', 'policyholder_nation', 'car_insured_gender', 'issued_age',
                      'car_policy_type', 'car_insurance_type', 'car_new_renew', 'insurance_time_limit',
                      'channel_underwriting_coefficient', 'insurance_point', 'business_channel', 'total_premium',
                      'commercial_insurance_premium', 'vehicle_insurance_premium', 'car_damage_insurance_premium',
                      'car_damage_insurance_premium_1', 'car_damage_insu_no_deductible',
                      'three_liability_insurance_premium', 'three_liability_insu_no_deductible',
                      'glass_break_insu_premium', 'car_duty_insu_premium', 'car_duty_insu_no_deductible_premium',
                      'robbery_insu_premium', 'robbery_insu_no_deductible_premium', 'scratch_insu_premium',
                      'scratch_insu_no_deductible_premium', 'wading_insu_premium', 'self_ignite_premium',
                      'self_ignite_no_deductible_premium', 'no_deductible_premium', 'written_premium', 'total_sum',
                      'commercial_insu_total_sum', 'vehicle_insu_sum', 'car_damage_insu_sum',
                      'three_liability_insu_sum', 'car_duty_insu_sum', 'vehicle_insu_sum', 'NCD_coefficient',
                      'commercial_insu_NCD_coefficient', 'vehicle_insu_NCD_coefficient', 'accident',
                      'accident_account', 'notCar_sign_time', 'notCar_record_time', 'notCar_start_time',
                      'notCar_end_time', 'notCar_organization', 'notCar_channel', 'notCar_issue_tool', 'notCar_gender',
                      'start_insure_age', 'now_age_min', 'notCar_constellation', 'notCar_province',
                      'notCar_insurance_gender', 'start_insured_age', 'insured_now_age', 'notCar_insured_constellation',
                      'notCar_insured_province', 'notCar_new_customer', 'current_year_customer', 'notCar_insurance',
                      'notCar_insurance_period', 'notCar_policy_status', 'accept_insurance', 'insurance_premiums',
                      'insurance_account', 'advance_sign_day', 'notCar_personal_group', 'notCar_agent_point',
                      'notCar_partner_code'],
        "dimension": [5000030, 5000032, 5000033, 5000034, 5000035, 5000036, 5000037, 5000040, 5000041, 5000042, 5000090,
                      5000043, 5000044, 5000045, 5000046, 5000091, 5000047, 5000049, 5000179, 5000053, 5000092, 5000093,
                      5000094, 5000056, 5000195, 5000171, 5000190, 5000208, 5000197, 5000200, 200329, 200682, 200330,
                      200073, 200074, 200075, 200077, 200078, 200079, 200649, 200128, 200331, 200332, 200333, 200041,
                      200137, 200335, 200336, 200337, 200338, 200346, 200623, 200624, 200625, 200626, 200358, 200359,
                      200355, 200373, 200372, 200375, 200377, 200379, 200380, 200361, 200362, 200141, 200627, 200628,
                      200705, 200639, 200060, 'car_personal_or_group_group', 'car_under_warranty_customer_group',
                      'car_interval_group', 'car_organization_2_group', 'car_organization_3_group',
                      'car_organization_4_group', 'car_channel_1_group', 'car_channel_2_group', 'car_channel_3_group',
                      'new_channel_channel', 'blanket_insurance_group', 'business_origin_group', 'local_car_group',
                      'car_age_group', 'purchase_price_group', 'using_properties_group', 'car_kind_group',
                      'car_insurance_type_group', 'car_brand_group', 'car_series_group', 'special_vehicle_group',
                      'filter_motor_tractor_group', 'self_car_group', 'new_car_group', 'sub_new_car_group',
                      'car_gender_group', 'issue_age_min_group', 'first_insure_group', 'policyholder_birth_day_group',
                      'id_type_group', 'marital_status_group', 'policyholder_industry_group', 'policyholder_edu_group',
                      'policyholder_profession_group', 'car_insured_gender_group', 'issued_age_group',
                      'car_insurance_type_group', 'car_policy_type_group', 'car_new_renew_group',
                      'insurance_point_group', 'business_channel_group', 'accident_group', 'interval',
                      'notCar_organization_2', 'notCar_organization_3', 'notCar_organization_4',
                      'acquisition_way_group', 'channel_group', 'issue_tool_group', 'gender_group',
                      'start_insure_age_group', 'now_age_group', 'constellation_group', 'province_group',
                      'insured_gender_group', 'start_insured_age_group', 'now_insured_age_group',
                      'insured_constellation_group', 'insured_province_group', 'notCar_new_customer_group',
                      'current_year_customer_group', 'insurance_type_group', 'insurance_type_one_group',
                      'insurance_type_two_group', 'insurance_type_details_group', 'policy_status_group',
                      'accept_insurance_group', 'insurance_premiums_group', 'insurance_account_group',
                      'advance_sign_day_group', 'notCar_personal_group_group', 'partner_group'],
        "target": [5000058, 5000059, 5000122, 5000060, 5000061, 5000062, 5000063, 5000064, 5000065, 5000142, 5000220,
                   5000221, 200504, 200507, 200510, 200721, 200711, 200722, 200480, 200511, 200512, 200487, 200551,
                   'car_index_vehicle_numbers', 'car_index_policy_pieces', 'car_premium_sum',
                   'car_additional_premium_sum', 'car_insured_amount_sum', 'car_additional_insured_amount_sum',
                   'car_average_premium', 'car_commercial_average_premium', 'car_index_clients',
                   'car_customer_average_premium', 'car_sign_premium_sum', 'non_car_index_customer',
                   'non_car_index_insured_customer', 'non_car_index_fee', 'non_car_index_record_fee',
                   'non_car_index_average_fee', 'non_car_index_insured_amount', 'non_car_index_average_insured_amount',
                   'non_car_index_policy_pieces', 'non_car_index_average_policy_pieces', 'non_car_index_premium',
                   'non_car_customer_average_age', 'non_car_insured_customer_average_age']}
    for i in kind_dict.keys():
        if tag_id in kind_dict[i]:
            return i


# 与上一个方法区别--字典中删去了含默认值的字段名，比如时间机构这些
# 此方法用来判断语料是否包含有效信息（除时间机构之外的），再结合时间机构是识别到的还是给的默认值来判断语料是否为闲聊
def get_effective_field(tag_id):
    kind_dict = {
        "condition": [5000069, 5000009, 5000012, 5000013, 5000014, 5000070,
                      5000015, 5000016, 5000017, 5000018, 5000071, 5000019, 5000021, 5000176, 5000026, 5000027,
                      5000193, 5000168, 5000189, 5000203, 5000196, 5000204, 5000199, 200182, 200022, 200677,
                      200004, 200613, 200082, 200083, 200593, 200084, 200085,
                      200086, 200186, 200006, 200007, 200187, 200008, 200009, 200010, 200188, 200189, 200013, 200093,
                      200191, 200094, 200014, 200015, 200097, 200192, 200193, 200194, 200017, 200195, 200198, 200199,
                      200200, 200204, 200594, 200209, 200502, 200503, 200225, 200224, 200227, 200228, 200229, 200231,
                      200232, 200233, 200213, 200214, 200098, 200099, 200586, 200100, 200102, 200704, 200603, 200025,
                      200026, 200027, 200103, 200263, 200104, 200105, 200106, 200107, 200108, 200109, 200110, 200111,
                      200112, 200113, 200114, 200115, 200116, 200264, 200266, 200029, 200030, 200031, 200117, 200118,
                      200119, 200120, 200277, 200278, 200279, 200033, 200034, 'car_entry_time', 'car_personal_or_group',
                      'car_under_warranty_customer', 'car_channels', 'new_channel',
                      'car_partner_code', 'channel_partner_code', 'channel_partner_firm_name', 'blanket_insurance',
                      'car_agent_point', 'car_agent_person', 'business_origin', 'one_way_car_insurance',
                      'filter_motor_tractor', 'car_insurance_type', 'self_car', 'new_car', 'sub_new_car', 'local_car',
                      'car_age', 'purchase_price', 'using_properties', 'car_kind', 'risk_level', 'tai_risk_level',
                      'car_type_name', 'car_barnd', 'car_series', 'car_type', 'car_type_code', 'ton',
                      'passenger_capacity', 'years_loan', 'dump_trailer', 'special_vehicle', 'displacement',
                      'car_weight', 'first_insure', 'car_gender', 'issue_age', 'policyholder_birth_day', 'id_type',
                      'marital_status', 'annual_income', 'policyholder_industry', 'policyholder_edu',
                      'policyholder_profession', 'policyholder_nation', 'car_insured_gender', 'issued_age',
                      'car_policy_type', 'car_insurance_type', 'car_new_renew', 'insurance_time_limit',
                      'channel_underwriting_coefficient', 'insurance_point', 'business_channel', 'total_premium',
                      'commercial_insurance_premium', 'vehicle_insurance_premium', 'car_damage_insurance_premium',
                      'car_damage_insurance_premium_1', 'car_damage_insu_no_deductible',
                      'three_liability_insurance_premium', 'three_liability_insu_no_deductible',
                      'glass_break_insu_premium', 'car_duty_insu_premium', 'car_duty_insu_no_deductible_premium',
                      'robbery_insu_premium', 'robbery_insu_no_deductible_premium', 'scratch_insu_premium',
                      'scratch_insu_no_deductible_premium', 'wading_insu_premium', 'self_ignite_premium',
                      'self_ignite_no_deductible_premium', 'no_deductible_premium', 'written_premium', 'total_sum',
                      'commercial_insu_total_sum', 'vehicle_insu_sum', 'car_damage_insu_sum',
                      'three_liability_insu_sum', 'car_duty_insu_sum', 'vehicle_insu_sum', 'NCD_coefficient',
                      'commercial_insu_NCD_coefficient', 'vehicle_insu_NCD_coefficient', 'accident',
                      'accident_account', 'notCar_channel', 'notCar_issue_tool', 'notCar_gender',
                      'start_insure_age', 'now_age_min', 'notCar_constellation', 'notCar_province',
                      'notCar_insurance_gender', 'start_insured_age', 'insured_now_age', 'notCar_insured_constellation',
                      'notCar_insured_province', 'notCar_new_customer', 'current_year_customer',
                      'notCar_insurance_period', 'notCar_policy_status', 'accept_insurance', 'insurance_premiums',
                      'insurance_account', 'advance_sign_day', 'notCar_personal_group', 'notCar_agent_point',
                      'notCar_partner_code'],
        "dimension": [5000030, 5000032, 5000033, 5000034, 5000035, 5000036, 5000037, 5000040, 5000041, 5000042, 5000090,
                      5000043, 5000044, 5000045, 5000046, 5000091, 5000047, 5000049, 5000179, 5000053, 5000092, 5000093,
                      5000094, 5000056, 5000195, 5000171, 5000190, 5000208, 5000197, 5000200, 200329, 200682, 200330,
                      200073, 200074, 200075, 200077, 200078, 200079, 200649, 200128, 200331, 200332, 200333, 200041,
                      200137, 200335, 200336, 200337, 200338, 200346, 200623, 200624, 200625, 200626, 200358, 200359,
                      200355, 200373, 200372, 200375, 200377, 200379, 200380, 200361, 200362, 200141, 200627, 200628,
                      200705, 200639, 200060, 'car_personal_or_group_group', 'car_under_warranty_customer_group',
                      'car_interval_group', 'car_organization_2_group', 'car_organization_3_group',
                      'car_organization_4_group', 'car_channel_1_group', 'car_channel_2_group', 'car_channel_3_group',
                      'new_channel_channel', 'blanket_insurance_group', 'business_origin_group', 'local_car_group',
                      'car_age_group', 'purchase_price_group', 'using_properties_group', 'car_kind_group',
                      'car_insurance_type_group', 'car_brand_group', 'car_series_group', 'special_vehicle_group',
                      'filter_motor_tractor_group', 'self_car_group', 'new_car_group', 'sub_new_car_group',
                      'car_gender_group', 'issue_age_min_group', 'first_insure_group', 'policyholder_birth_day_group',
                      'id_type_group', 'marital_status_group', 'policyholder_industry_group', 'policyholder_edu_group',
                      'policyholder_profession_group', 'car_insured_gender_group', 'issued_age_group',
                      'car_insurance_type_group', 'car_policy_type_group', 'car_new_renew_group',
                      'insurance_point_group', 'business_channel_group', 'accident_group', 'interval',
                      'notCar_organization_2', 'notCar_organization_3', 'notCar_organization_4',
                      'acquisition_way_group', 'channel_group', 'issue_tool_group', 'gender_group',
                      'start_insure_age_group', 'now_age_group', 'constellation_group', 'province_group',
                      'insured_gender_group', 'start_insured_age_group', 'now_insured_age_group',
                      'insured_constellation_group', 'insured_province_group', 'notCar_new_customer_group',
                      'current_year_customer_group', 'insurance_type_group', 'insurance_type_one_group',
                      'insurance_type_two_group', 'insurance_type_details_group', 'policy_status_group',
                      'accept_insurance_group', 'insurance_premiums_group', 'insurance_account_group',
                      'advance_sign_day_group', 'notCar_personal_group_group', 'partner_group'],
        "target": [5000058, 5000059, 5000122, 5000060, 5000061, 5000062, 5000063, 5000064, 5000065, 5000142, 5000220,
                   5000221, 200504, 200507, 200510, 200721, 200711, 200722, 200480, 200511, 200512, 200487, 200551,
                   'car_index_vehicle_numbers', 'car_index_policy_pieces', 'car_premium_sum',
                   'car_additional_premium_sum', 'car_insured_amount_sum', 'car_additional_insured_amount_sum',
                   'car_average_premium', 'car_commercial_average_premium', 'car_index_clients',
                   'car_customer_average_premium', 'car_sign_premium_sum', 'non_car_index_customer',
                   'non_car_index_insured_customer', 'non_car_index_fee', 'non_car_index_record_fee',
                   'non_car_index_average_fee', 'non_car_index_insured_amount', 'non_car_index_average_insured_amount',
                   'non_car_index_policy_pieces', 'non_car_index_average_policy_pieces', 'non_car_index_premium',
                   'non_car_customer_average_age', 'non_car_insured_customer_average_age']}
    for i in kind_dict.keys():
        if tag_id in kind_dict[i]:
            return i


# 判断字段中是否包含指标字段
def get_include_target(tags):
    """
    :param tags: 包含键为字段名的字典
    :return: 是否包含指标字段
    """
    is_include = False
    if tags:
        for i in tags.keys():
            if get_field_kind(i) == "target":
                is_include = True
    return is_include


# 是否包含筛选（不包括时间机构险种这一类含默认值字段）
def get_include_condition(tags):
    is_include = False
    if tags:
        for i in tags.keys():
            if get_effective_field(i) == "condition":
                is_include = True
    return is_include


# 是否包含维度
def get_include_dimension(tags):
    is_include = False
    if tags:
        for i in tags.keys():
            if get_field_kind(i) == "dimension":
                is_include = True
    return is_include


# def get_interval(query, dictionary):
#     for key in dictionary['interval_dict'].keys():
#         for item in dictionary['interval_dict'][key]:
#             if item in query:
#                 return key


# 要修改成add_word参数中所有子字典和子列表中的元素
def add_word2jieba(words):
    if isinstance(words, dict):
        for key in words.keys():
            jieba.add_word(key)
            dict1 = words[key]
            if isinstance(dict1, dict):
                for key1 in dict1.keys():
                    jieba.add_word(key1)
                    for j in dict1[key1]:
                        jieba.add_word(j)
            elif isinstance(dict1, list):
                for x in dict1:
                    jieba.add_word(x)
    elif isinstance(words, list):
        for word in words:
            jieba.add_word(word)


def init_slot(dictionary):
    print("start init")
    for value in dictionary.values():
        add_word2jieba(value)
    del_list = ["万到", "各省", "出豫皖", "看豫皖", "网销渠道", "客车", "比及"]
    for i in del_list:
        jieba.del_word(i)
    print("end init")
