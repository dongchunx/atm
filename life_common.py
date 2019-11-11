# -*- coding: UTF-8 -*-


# life_target  = {}
#
# life_target['投保人客户数'] = ['投保人客户数', '投保客户数', '客户数']
# life_target['投保长险客户数'] = ['投保长险客户数', '长险客户数']
# life_target['投保长险有效客户数'] = ['投保长险有效客户数', '长险有效客户数']
# life_target['被保险人客户数'] = ['被保险人客户数', '被保人客户数']
# life_target['被保险长险客户数'] = ['被保险长险客户数', '被保长险客户数', '长险被保客户数']
# life_target['保费和'] = ['保费和', '保费收入', '保费情况']
# life_target['有效长险保费和'] = ['有效长险保费和', '长险有效客户保费情况', '长险有效保和']

# get targets
def get_life_targets(words_list):
    # targets = []
    # targets_dict = life_target
    #
    # for key in targets_dict.keys():
    #     for item in targets_dict[key]:
    #         if item in words_list:
    #             targets.append(key)
    #
    # print(target)
    # return list(set(targets))
    return


# customer_status = ['年龄', '收入', '学历']

def get_customer_status(words_list, dictionary):
    result = []
    for status in dictionary['customer_status']:
        if status in words_list:
            result.append(status)
    return result


# insured_type
# insured_type = [ '传统寿险', '医疗费用', '重疾', '医疗补贴', '意外', '教育金', '养老金', '财富管理' ]

def get_others(query, dictionary):
    data = {}
    data['compose'] = None
    data['net_source'] = None
    data['e_source'] = None
    data['insured'] = []

    if '组合保单' in query:
        data['compose'] = "是"

    if '微店' in query or '二维码' in query:
        data['net_source'] = "是"

    if 'e锦囊' in query:
        data['e_source'] = "是"

    for item in dictionary['insured_type']:
        key_word1 = item + '保额'
        key_word2 = item + '保障'

        if key_word1 in query or key_word2 in query:
            data['insured'].append(item)

    print(data)
    return data


# 筛选类 -- 客户状态类
def get_status(query):
    data = {}
    data['new_customer'] = None
    data['new_long'] = None
    data['silver'] = None

    if '长险新客户' in query:
        data['new_long'] = '是'
    elif '新客户' in query:
        data['new_customer'] = '是'

    if '银保客户' in query or '银保' in query:
        data['silver'] = '是'

    print(data)
    return data


##筛选类---保单状态类
# life_status = ['有效', '失效', '满期', '退保', '给付期', '融通退保', '理赔中', '变更中', '责任终止', '豁免', '终止']
# life_freq = ['趸交', '3年缴', '5年缴', '20年缴', '30年缴']
# life_method = ['趸交', '年缴']


def get_policy_status(query, dictionary):
    data = {}
    data['life_status'] = []
    data['pay_method'] = []
    data['pay_freq'] = []

    for item in dictionary['life_status']:
        if item in query:
            data['life_status'].append(item)

    for item in dictionary['life_freq']:
        if item in query:
            data['pay_freq'].append(item)

    for item in dictionary['life_method']:
        if item in query:
            data['pay_method'].append(item)
    print(data)
    return data


# 这里输入的query是需要判断过类别的,且将原来的类别排除掉
def life_cross_class(query):
    data = {}
    data['is_car'] = None
    data['is_non_car'] = None
    data['is_health'] = None

    if "寿险" in query:
        if "车险" in query:
            data['is_car'] = '是'
        if '非车' in query:
            data['is_non_car'] = '是'
        if '不是健康险' in query:
            data['is_health'] = '否'
        elif '健康险' in query:
            data['is_health'] = '是'

    print(data)
    return data


def insurance_srceen(query):
    data = {}
    data['main'] = None
    if '主险' in query:
        data['main'] = '主险'
    elif '附加险' in query:
        data['main'] = '附加险'

    data['year_money'] = None
    if '年缴保费' in query:
        data['year_money'] = '年缴保费'

    data['rule'] = None

    print(data)
    return data


# life time mode
def get_life_time_mode(query, time_period):
    data = {}
    message = ""
    if time_period != "":
        if '起保' in query:
            data['life_start_time'] = time_period

        elif '签单' in query:
            data['life_sign_time'] = time_period

        elif '生效' in query or '签发' in query:
            data['life_effect_time'] = time_period

        elif '录入' in query:
            data['life_record_time'] = time_period

        elif '终保' in query:
            data['life_end_time'] = time_period

        else:
            data['life_start_time'] = time_period
    else:
        message = "未识别到日期值！"
    print(data, message)
    return data, message
