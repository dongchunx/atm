# -*- coding: UTF-8 -*-
import json

from common import get_common_dict, get_number_class_detail, to_insured, get_true_or_false, get_common_list, \
    get_field_attribute, get_filter_field, change_field_format, get_undefined_field, change_field_tag_id, get_interval,\
    get_number_in_group
from life_common import get_customer_status, get_others, get_status, get_policy_status, \
    life_cross_class, insurance_srceen, get_life_time_mode
from car_common import get_car_organization, get_car_time_code, get_local_car, get_car_gender, get_risk_level, \
    filter_using_nature, get_taibao_risk_level, insurance_time_limit, car_vehicle_type, \
    get_car_policy_type, get_car_policy_type_car, education_background, filter_motor_tractor
from noncar_common import get_not_car_gender, get_new_customer, \
    get_current_year_new_customer, get_gender_group, get_not_car_organization, get_not_car_channel, \
    get_not_car_time_code, identify_provinces, identify_provinces_by, advance_sign_day, notCar_insurance


def get_noncar(query, words_list, body, dictionary):
    data = {}
    # 险种
    data.update(notCar_insurance(words_list, query, "notCar_insurance", dictionary))
    # 非车机构(多选)
    data.update(get_not_car_organization(words_list, query, 'notCar_organization', dictionary))
    # 非车渠道
    data.update(get_not_car_channel(words_list, query, 'notCar_channel', dictionary))
    # 非车出单工具
    data.update(get_common_dict(words_list, "notCar_issue_tool", dictionary))
    # 投保人起保年龄
    # 投保人起保时年龄-维度
    num_mark = get_field_attribute(words_list, query, ['年龄', '年龄段', '起保年龄'])
    if num_mark == 0:
        data.update(
            get_number_class_detail(words_list, query, ["起保年龄"], "start_insure_age_min", "start_insure_age_max",
                                    "start_insure_age"))
    elif num_mark == 1:
        start_insure_age_group, number_mark = get_number_in_group(words_list, query, ['年龄', '年龄段'],
                                                                  "start_insure_age_group")
        if number_mark == 0:
            if '学平险' in data["insurance_name"]:
                data["start_insure_age_group"] = "0-6,7-13,14-17,18-25"
            else:
                data["start_insure_age_group"] = "0-25,26-35,36-45,46-55,56-#"
        elif number_mark == 1:
            data["start_insure_age_group"] = start_insure_age_group
    # 投保人当前年龄
    # 投保人当前年龄-维度
    num_mark = get_field_attribute(words_list, query, ['当前年龄'])
    if num_mark == 0:
        data.update(
            get_number_class_detail(words_list, query, ["起保年龄"], "start_insure_age_min", "start_insure_age_max",
                                    "start_insure_age"))
    elif num_mark == 1:
        start_insure_age_group, number_mark = get_number_in_group(words_list, query, ['年龄', '年龄段'],
                                                                  "start_insure_age_group")
        if number_mark == 0:
            data["start_insure_age_group"] = "0-25,26-35,36-45,46-55,56-#"
        elif number_mark == 1:
            data["start_insure_age_group"] = start_insure_age_group
    data.update(get_number_class_detail(words_list, query, ["当前年龄"], "now_age_min", "now_age_max", "now_age"))
    # 投保人星座
    data.update(get_common_dict(words_list, "notCar_constellation", dictionary))
    # 被保人起保时年龄
    to_insured(query, "start_insure_age_min", "start_insured_age_min", data)
    to_insured(query, "start_insure_age_max", "start_insured_age_max", data)
    # 被保人当前年龄
    to_insured(query, "now_age_min", "insured_now_age_min", data)
    to_insured(query, "now_age_max", "insured_now_age_max", data)
    # 被保人星座
    to_insured(query, "notCar_constellation", "notCar_insured_constellation", data)
    # # 非车险种
    # data.update(get_common_dict(words_list, "notCar_insurance_type", dictionary))
    # 非车保险期限
    data.update(get_common_list(words_list, "notCar_insurance_period", dictionary))
    # 保单状态
    data.update(get_common_dict(words_list, "notCar_policy_status", dictionary))
    # 承保天数
    data.update(get_number_class_detail(words_list, query, ["承包天数"], "accept_insurance_min", "accept_insurance_max",
                                        "accept_insurance"))
    # 保单保费
    data.update(get_number_class_detail(words_list, query, ["保费"], "insurance_premiums_min", "insurance_premiums_max",
                                        "insurance_premiums"))
    # 保单保额

    data.update(get_number_class_detail(words_list, query, ["保额"], "insurance_account_min", "insurance_account_max",
                                        "insurance_account"))
    # 个团单标识
    data.update(get_common_dict(words_list, "notCar_personal_group", dictionary))
    # 非车投保人性别
    data.update(get_not_car_gender(query))
    # 非车被投保人性别
    to_insured(query, "notCar_gender", "notCar_insurance_gender", data)
    # 投保人是否新客户
    data.update(get_new_customer(words_list, 'notCar_new_customer'))
    # 是否当年新客户
    data.update(get_current_year_new_customer(words_list, 'notCar_new_customer', 'current_year_customer', data))
    # 投保人省份
    data.update(identify_provinces(words_list, query, "notCar_province", dictionary))
    # 被保人省份
    data.update(identify_provinces_by(words_list, query, "notCar_insured_province", dictionary))
    # 提前签单天数
    # 需改动 数值抓取
    data.update(advance_sign_day(words_list, query, "advance_sign_day"))
    # 展业方式分组
    acquisition_way_code = get_field_attribute(words_list, query, ['展业方式'])
    if acquisition_way_code == 1:
        data['acquisition_way_group'] = 1
    # 渠道分组
    channel_code = get_field_attribute(words_list, query, ['渠道'])
    if channel_code == 1:
        data['channel_group'] = 1
    # 出单工具分组
    issue_tool_code = get_field_attribute(words_list, query, ['出单'])
    if issue_tool_code == 1:
        data['issue_tool_group'] = 1
    # 投保人性别分组
    data.update(get_gender_group(words_list, query, 'gender_group'))
    # 投保人星座分组
    constellation_code = get_field_attribute(words_list, query, ['星座'])
    if constellation_code == 1:
        data['constellation_group'] = 1
    # 投保人省份分组
    province_code = get_field_attribute(words_list, query, ['省份'])
    if province_code == 1:
        data['province_group'] = 1
    # 被保人性别分组
    to_insured(query, 'gender_group', 'insured_gender_group', data)
    # 被保人星座分组
    to_insured(query, 'constellation_group', 'insured_constellation_group', data)
    # 被保人省份分组
    to_insured(query, 'province_group', 'insured_province_group', data)
    # 投保人是否新客户
    notCar_new_customer_group = get_field_attribute(words_list, query, ['新客户', '老客户', '新老客户', '新老'])
    if notCar_new_customer_group == 1:
        data['notCar_new_customer_group'] = 1
        # 投保人是否当年新客户
        if "当年" in query:
            data['current_year_customer_group'] = 1
    # 险种大类
    insurance_type_code = get_field_attribute(words_list, query, ['险种'])
    if insurance_type_code == 1:
        data['insurance_type_group'] = 1
    # 二类险种
    insurance_type_one_code = get_field_attribute(words_list, query, ['二类险种'])
    if insurance_type_one_code == 1:
        data['insurance_type_one_group'] = 1
    # 三类险种
    insurance_type_two_code = get_field_attribute(words_list, query, ['三类险种'])
    if insurance_type_two_code == 1:
        data['insurance_type_two_group'] = 1
    # 险种明细
    insurance_type_details_code = get_field_attribute(words_list, query, ['险种明细'])
    if insurance_type_details_code == 1:
        data['insurance_type_details_group'] = 1
    # 保单状态
    policy_status_code = get_field_attribute(words_list, query, ['保单状态'])
    if policy_status_code == 1:
        data['policy_status_group'] = 1
    # 合作伙伴代码
    partner_code = get_field_attribute(words_list, query, ['合作伙伴代码'])
    if partner_code == 1:
        data['partner_group'] = 1
    # 二级机构
    notCar_organization_2 = get_field_attribute(words_list, query, ['分公司'])
    if notCar_organization_2 == 1:
        data['notCar_organization_2'] = 1
    # 三级机构
    notCar_organization_3 = get_field_attribute(words_list, query, ['部门组', '三级机构'])
    if notCar_organization_3 == 1:
        data['notCar_organization_3'] = 1
    # 四级机构
    notCar_organization_4 = get_field_attribute(words_list, query, ['部门', '四级机构'])
    if notCar_organization_4 == 1:
        data['notCar_organization_4'] = 1

    # source = get_noncardim_source(query)
    # print(source)
    # cross = noncar_cross_class(query)
    # print(cross)
    # noncar_insu = get_not_car_insurance(query, dictionary)
    # print(noncar_insu)
    # tools = get_noncar_tools(query, dictionary)
    # print(tools)

    # 指标
    # 投保客户数
    change_field_format(body, "iATM_non_car_index_customer", "non_car_index_customer", data)
    # 被保客户数
    change_field_format(body, "iATM_non_car_index_insured_customer", "non_car_index_insured_customer", data)
    # 保费和

    # 入账保费和
    change_field_format(body, "iATM_non_car_index_record_fee", "non_car_index_record_fee", data)
    # 客均保费
    change_field_format(body, "iATM_non_car_index_average_fee", "non_car_index_average_fee", data)
    # 保额和
    change_field_format(body, "iATM_non_car_index_insured_amount", "non_car_index_insured_amount", data)
    # 客均保额
    change_field_format(body, "iATM_non_car_index_average_insured_amount", "non_car_index_average_insured_amount", data)
    # 保单件数
    change_field_format(body, "iATM_non_car_index_policy_pieces", "non_car_index_policy_pieces", data)
    # 客均保单件数
    change_field_format(body, "iATM_non_car_index_average_policy_pieces", "non_car_index_average_policy_pieces", data)
    # 已赚保费
    change_field_format(body, "iATM_non_car_index_premium", "non_car_index_premium", data)
    # 投保人平均年龄
    change_field_format(body, "iATM_non_car_customer_average_age", "non_car_customer_average_age", data)
    # 被保人平均年龄
    change_field_format(body, "iATM_non_car_insured_customer_average_age", "non_car_insured_customer_average_age", data)

    # data.update(tools)
    # data.update(noncar_insu)
    # data.update(cross)
    # data.update(source)

    null_list = []
    for i in data:
        if data[i] == {} or data[i] == [] or data[i] == "":
            null_list.append(i)
    for i in null_list:
        data.pop(i, 0)
    # if
    return data


def get_car(query, words_list, body, dictionary):
    data = {}
    # 车险机构
    data.update(get_car_organization(words_list, query, 'car_organization', dictionary))
    # 是否车险在保客户
    data.update(get_true_or_false(words_list, "在保客户", "car_under_warranty_customer"))
    # 车险渠道
    data.update(get_common_dict(words_list, "car_channels", dictionary))
    # 车险新渠道大类名称
    data.update(get_common_list(words_list, "new_channel", dictionary))
    # 统保代码
    data.update(get_common_list(words_list, "blanket_insurance", dictionary))
    # 业务来源
    data.update(get_common_dict(words_list, "business_origin", dictionary))
    # 单程提车险
    data.update(get_true_or_false(words_list, "单程提车险", "one_way_car_insurance"))
    # 车险险种
    data.update(get_common_dict(words_list, "car_insurance_type", dictionary))
    # 车龄
    data.update(get_number_class_detail(words_list, query, ["车龄"], "car_age_min", "car_age_max", "car_age"))
    # 新车购置价
    data.update(get_number_class_detail(words_list, query, ["购置价"], "purchase_price_min", "purchase_price_max",
                                        "purchase_price"))
    # 吨位
    data.update(get_number_class_detail(words_list, query, ["吨"], "ton_min", "ton_max", "ton"))
    # 核定载客量
    data.update(
        get_number_class_detail(words_list, query, ["核定载客量"], "passenger_capacity_min", "passenger_capacity_max",
                                "passenger_capacity"))
    # 多年贷款投保标志
    data.update(get_true_or_false(words_list, "多年贷款", "years_loan"))
    # 自卸挂车分类
    data.update(get_common_dict(words_list, "dump_trailer", dictionary))
    # 特种车分类
    data.update(get_common_list(words_list, "special_vehicle", dictionary))
    # 排量
    data.update(
        get_number_class_detail(words_list, query, ["排量"], "displacement_min", "displacement_max", "displacement"))
    # 车重
    data.update(get_number_class_detail(words_list, query, ["车重"], "car_weight_min", "car_weight_max", "car_weight"))
    # 投保人性别
    data.update(get_car_gender(query))
    # 投保人投保时年龄
    data.update(get_number_class_detail(words_list, query, ["投保年龄"], "issue_age_min", "issue_age_max", "issue_age"))
    # 投保证件类型
    data.update(get_common_dict(words_list, "id_type", dictionary))
    # 投保人婚姻状况
    data.update(get_common_dict(words_list, "marital_status", dictionary))
    # 投保人年收入金额
    data.update(
        get_number_class_detail(words_list, query, ["年收入"], "annual_income_min", "annual_income_max", "annual_income"))
    # 被投保人性别
    to_insured(query, "car_gender", "car_insured_gender", data)
    # 被投保人投保时年龄
    to_insured(query, "issue_age_min", "issued_age_min", data)
    to_insured(query, "issue_age_max", "issued_age_max", data)
    # 新转续
    data.update(get_common_list(words_list, "car_new_renew", dictionary))
    # 渠道核保系数
    data_coefficient = get_number_class_detail(words_list, query, ["渠道核保系数"], "channel_underwriting_coefficient_min",
                                               "channel_underwriting_coefficient_max",
                                               "channel_underwriting_coefficient")
    if "渠道核保系数" in words_list:
        value1 = data_coefficient["channel_underwriting_coefficient_min"]
        value2 = data_coefficient["channel_underwriting_coefficient_max"]
        if value1 == "*":
            data_coefficient["channel_underwriting_coefficient_min"] = "0.6375"
        elif int(value1) < 0.6375:
            data_coefficient["channel_underwriting_coefficient_min"] = "0.6375"
        if value2 == "#":
            data_coefficient["channel_underwriting_coefficient_max"] = "1.4375"
        elif int(value2) > 1.4375:
            data_coefficient["channel_underwriting_coefficient_max"] = "1.4375"
    data.update(data_coefficient)
    # 太保分
    data_insurance_point = get_number_class_detail(words_list, query, ["太保分"], "insurance_point_min",
                                                   "insurance_point_max", "insurance_point")
    if "太保分" in words_list:
        value1 = data_coefficient["insurance_point_min"]
        value2 = data_coefficient["insurance_point_max"]
        if value1 == "*":
            data_coefficient["insurance_point_min"] = "0"
        if value2 == "#":
            data_coefficient["insurance_point_max"] = "100"
        elif int(value2) > 100:
            data_coefficient["insurance_point_max"] = "100"
    data.update(data_insurance_point)
    # 业务渠道
    data.update(get_common_list(words_list, "business_channel", dictionary))
    # 总保费
    data.update(
        get_number_class_detail(words_list, query, ["总保费"], "total_premium_min", "total_premium_max", "total_premium"))
    # 商业险保费
    data.update(get_number_class_detail(words_list, query, ["商业险保费"], "commercial_insurance_premium_min",
                                        "commercial_insurance_premium_max", "commercial_insurance_premium"))
    # 交强险保费
    data.update(get_number_class_detail(words_list, query, ["交强险保费"], "vehicle_insurance_premium_min",
                                        "vehicle_insurance_premium_max", "vehicle_insurance_premium"))
    # 车损险保费
    data.update(get_number_class_detail(words_list, query, ["车损险保费"], "car_damage_insurance_premium_min",
                                        "car_damage_insurance_premium_max", "car_damage_insurance_premium"))
    # 车损险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["车损险不计免赔保费"], "car_damage_insu_no_deductible_min",
                                        "car_damage_insu_no_deductible_max", "car_damage_insu_no_deductible"))
    # 三责险保费
    data.update(get_number_class_detail(words_list, query, ["三责险保费"], "three_liability_insurance_premium_min",
                                        "three_liability_insurance_premium_max", "three_liability_insurance_premium"))
    # 三责险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["三责险不计免赔保费"], "three_liability_insu_no_deductible_min",
                                        "three_liability_insu_no_deductible_max", "three_liability_insu_no_deductible"))
    # 玻璃破碎险保费
    data.update(get_number_class_detail(words_list, query, ["玻璃破碎险保费"], "glass_break_insu_premium_min",
                                        "glass_break_insu_premium_max", "glass_break_insu_premium"))
    # 车责险保费
    data.update(
        get_number_class_detail(words_list, query, ["车责险保费"], "car_duty_insu_premium_min", "car_duty_insu_premium_max",
                                "car_duty_insu_premium"))
    # 车责险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["车责险不计免赔保费"], "car_duty_insu_no_deductible_premium_min",
                                        "car_duty_insu_no_deductible_premium_max",
                                        "car_duty_insu_no_deductible_premium"))
    # 盗抢险保费
    data.update(
        get_number_class_detail(words_list, query, ["盗抢险保费"], "robbery_insu_premium_min", "robbery_insu_premium_max",
                                "robbery_insu_premium"))
    # 盗抢险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["盗抢险不计免赔保费"], "robbery_insu_no_deductible_premium_min",
                                        "robbery_insu_no_deductible_premium_max", "robbery_insu_no_deductible_premium"))
    # 划痕险保费
    data.update(
        get_number_class_detail(words_list, query, ["划痕险保费"], "scratch_insu_premium_min", "scratch_insu_premium_max",
                                "scratch_insu_premium"))
    # 划痕险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["划痕险不计免赔保费"], "scratch_insu_no_deductible_premium_min",
                                        "scratch_insu_no_deductible_premium_max", "scratch_insu_no_deductible_premium"))
    # 涉水险保费
    data.update(
        get_number_class_detail(words_list, query, ["涉水险保费"], "wading_insu_premium_min", "wading_insu_premium_max",
                                "wading_insu_premium"))
    # 自燃险保费
    data.update(
        get_number_class_detail(words_list, query, ["自燃险保费"], "self_ignite_premium_min", "self_ignite_premium_max",
                                "self_ignite_premium"))
    # 自燃险不计免赔保费
    data.update(get_number_class_detail(words_list, query, ["自燃险不计免赔保费"], "self_ignite_no_deductible_premium_min",
                                        "self_ignite_no_deductible_premium_max", "self_ignite_no_deductible_premium"))
    # 不计免赔保费
    data.update(
        get_number_class_detail(words_list, query, ["不计免赔保费"], "no_deductible_premium_min",
                                "no_deductible_premium_max", "no_deductible_premium"))
    # 签单保费
    data.update(get_number_class_detail(words_list, query, ["签单保费"], "written_premium_min", "written_premium_max",
                                        "written_premium"))
    # 总保额
    data.update(get_number_class_detail(words_list, query, ["总保额"], "total_sum_min", "total_sum_max", "total_sum"))
    # 商业险总保额
    data.update(get_number_class_detail(words_list, query, ["商业险总保额"], "commercial_insu_total_sum_min",
                                        "commercial_insu_total_sum_max", "commercial_insu_total_sum"))
    # 交强险保额
    data.update(get_number_class_detail(words_list, query, ["交强险保额"], "vehicle_insu_sum_min", "vehicle_insu_sum_max",
                                        "vehicle_insu_sum"))
    # 车损险保额
    data.update(
        get_number_class_detail(words_list, query, ["车损险保额"], "car_damage_insu_sum_min", "car_damage_insu_sum_max",
                                "car_damage_insu_sum"))
    # 三责险保额
    data.update(get_number_class_detail(words_list, query, ["三责险保额"], "three_liability_insu_sum_min",
                                        "three_liability_insu_sum_max", "three_liability_insu_sum"))
    # 车责险保额
    data.update(get_number_class_detail(words_list, query, ["车责险保额"], "car_duty_insu_sum_min", "car_duty_insu_sum_max",
                                        "car_duty_insu_sum"))
    # 划痕险保额
    data.update(get_number_class_detail(words_list, query, ["划痕险保额"], "vehicle_insu_sum_min", "vehicle_insu_sum_max",
                                        "vehicle_insu_sum"))
    # 平台返回NCD系数
    data.update(get_number_class_detail(words_list, query, ["NCD系数"], "NCD_coefficient_min", "NCD_coefficient_max",
                                        "NCD_coefficient"))
    # 平台返回商业险NCD系数（从车辆）
    data.update(get_number_class_detail(words_list, query, ["商业险NCD系数"], "commercial_insu_NCD_coefficient_min",
                                        "commercial_insu_NCD_coefficient_max", "commercial_insu_NCD_coefficient"))
    # 平台返回交强险NCD系数（从车辆）
    data.update(get_number_class_detail(words_list, query, ["交强险NCD系数"], "vehicle_insu_NCD_coefficient_min",
                                        "vehicle_insu_NCD_coefficient_max", "vehicle_insu_NCD_coefficient"))
    # 出险次数
    data.update(get_number_class_detail(words_list, query, ["出险"], "accident_account_min", "accident_account_max",
                                        "accident_account"))
    # 是否出险
    data.update(get_true_or_false(words_list, "出险", "accident"))
    # 本地车标识
    data.update(get_local_car(words_list, query, "local_car", dictionary))

    # 车型风险等级
    data.update(get_risk_level(words_list, query, "risk_level"))
    # 太保车型风险等级
    data.update(get_taibao_risk_level(words_list, query, "tai_risk_level"))
    # 投保期限未完成 "insurance_time_limit"
    data.update(insurance_time_limit(words_list, query, "insurance_time_limit"))
    # 筛选摩托车，拖拉机
    data.update(filter_motor_tractor(words_list, query, "filter_motor_tractor"))
    # 使用性质
    data.update(filter_using_nature(words_list, query, "using_nature", dictionary))
    # 车辆种类
    data.update(car_vehicle_type(words_list, query, "vehicle_type", dictionary))
    # 保单类型
    data.update(get_car_policy_type(words_list, query, 'car_policy_type'))
    # 投保类型（人车）
    data.update(get_car_policy_type_car(words_list, query, 'car_insurance_type'))

    # 维度
    # 个团单标示分组
    car_personal_or_group_group = get_field_attribute(words_list, query, ['个单', '团单', '个团单'])
    if car_personal_or_group_group == 1:
        data['car_personal_or_group_group'] = 1
    # 是否车险在保客户
    car_under_warranty_customer_group = get_field_attribute(words_list, query, ['在保'])
    if car_under_warranty_customer_group == 1:
        data['car_under_warranty_customer_group'] = 1
    # 时间间隔

    # 分公司
    car_organization_2_group = get_field_attribute(words_list, query, ['分公司'])
    if car_organization_2_group == 1:
        data['car_organization_2_group'] = 1
    # 部门组
    car_organization_3_group = get_field_attribute(words_list, query, ['部门组'])
    if car_organization_3_group == 1:
        data['car_organization_3_group'] = 1
    # 部门
    car_organization_4_group = get_field_attribute(words_list, query, ['部门'])
    if car_organization_4_group == 1:
        data['car_organization_4_group'] = 1
    # 一级渠道
    car_channel_1_group = get_field_attribute(words_list, query, ['渠道', '一级渠道'])
    if car_channel_1_group == 1:
        data['car_channel_1_group'] = 1
    # 二级渠道
    car_channel_2_group = get_field_attribute(words_list, query, ['二级渠道'])
    if car_channel_2_group == 1:
        data['car_channel_2_group'] = 1
    # 三级渠道
    car_channel_3_group = get_field_attribute(words_list, query, ['三级渠道'])
    if car_channel_3_group == 1:
        data['car_channel_3_group'] = 1
    # 渠道大类
    new_channel_channel_group = get_field_attribute(words_list, query, ['渠道大类', '新渠道', '新渠道大类'])
    if new_channel_channel_group == 1:
        data['new_channel_channel_group'] = 1
    # 统保代码
    blanket_insurance_group = get_field_attribute(words_list, query, ['统保代码'])
    if blanket_insurance_group == 1:
        data['blanket_insurance_group'] = 1
    # 业务来源
    business_origin_group = get_field_attribute(words_list, query, ['业务来源'])
    if business_origin_group == 1:
        data['business_origin_group'] = 1
    # 异地车标示
    local_car_group = get_field_attribute(words_list, query, ['异地车', '本地车'])
    if local_car_group == 1:
        data['local_car_group'] = 1
    # 使用性质
    using_properties_group = get_field_attribute(words_list, query, ['使用性质'])
    if using_properties_group == 1:
        data['using_properties_group'] = 1
    # 车辆种类
    car_kind_group = get_field_attribute(words_list, query, ['车辆种类'])
    if car_kind_group == 1:
        data['car_kind_group'] = 1
    # 险种
    car_insurance_type_group = get_field_attribute(words_list, query, ['险种'])
    if car_insurance_type_group == 1:
        data['car_insurance_type_group'] = 1
    # 品牌
    car_brand_group = get_field_attribute(words_list, query, ['品牌'])
    if car_brand_group == 1:
        data['car_brand_group'] = 1
    # 车系
    car_series_group = get_field_attribute(words_list, query, ['车系'])
    if car_series_group == 1:
        data['car_series_group'] = 1
    # 特种车分类
    special_vehicle_group = get_field_attribute(words_list, query, ['特种车', '特种车辆'])
    if special_vehicle_group == 1:
        data['special_vehicle_group'] = 1
    # 去除摩托车、拖拉机等车辆
    filter_motor_tractor_group = get_field_attribute(words_list, query, ['摩托车', '拖拉机'])
    if filter_motor_tractor_group == 1:
        data['filter_motor_tractor_group'] = 1
    # 家庭自用车分组
    self_car_group = get_field_attribute(words_list, query, ['家庭', '家庭用车', '家庭自用车'])
    if self_car_group == 1:
        data['self_car_group'] = 1
    # 是新车分组
    new_car_group = get_field_attribute(words_list, query, ['新车'])
    if new_car_group == 1:
        data['new_car_group'] = 1
    # 是次新车分组
    sub_new_car_group = get_field_attribute(words_list, query, ['次新车'])
    if sub_new_car_group == 1:
        data['sub_new_car_group'] = 1
    # 投保人性别分组
    car_gender_group = get_field_attribute(words_list, query, ['男性', '女性', '男女'])
    if car_gender_group == 1:
        data['car_gender_group'] = 1
    # 投保人是否首次在太保投保车险客户分组
    first_insure_group = get_field_attribute(words_list, query, ['投保'])
    if first_insure_group == 1:
        if '首次' in query:
            data['first_insure_group'] = 1
    # 投保证件类型分组
    id_type_group = get_field_attribute(words_list, query, ['证件', '证件类型'])
    if id_type_group == 1:
        data['id_type_group'] = 1
    # 投保人婚姻状况分组
    marital_status_group = get_field_attribute(words_list, query, ['婚姻', '婚姻状况', '婚姻情况'])
    if marital_status_group == 1:
        data['marital_status_group'] = 1
    # 投保人行业分组
    policyholder_industry_group = get_field_attribute(words_list, query, ['行业', '工作'])
    if policyholder_industry_group == 1:
        data['policyholder_industry_group'] = 1
    # 投保人最高学历分组
    policyholder_edu_group = get_field_attribute(words_list, query, ['学历', '最高学历', '文凭'])
    if policyholder_edu_group == 1:
        data['policyholder_edu_group'] = 1
    # 投保人职业分组
    policyholder_profession_group = get_field_attribute(words_list, query, ['职业'])
    if policyholder_profession_group == 1:
        data['policyholder_profession_group'] = 1
    # 被保人性别分组
    to_insured(query, 'car_gender_group', 'car_insured_gender_group', data)
    # 投保类型（人车）分组
    car_insurance_type_group = get_field_attribute(words_list, query, ['类型', '投保类型'])
    if car_insurance_type_group == 1:
        if '投保' in query:
            data['car_insurance_type_group'] = 1
    # 保单类型分组
    car_policy_type_group = get_field_attribute(words_list, query, ['保单类型', '商业', '交强', '商业险', '交强险'])
    if car_policy_type_group == 1:
        data['car_policy_type_group'] = 1
    # 新转续（产分）分组
    car_new_renew_group = get_field_attribute(words_list, query, ['新转续', '新保', '转保', '续保'])
    if car_new_renew_group == 1:
        data['car_new_renew_group'] = 1
    # 业务渠道分组
    business_channel_group = get_field_attribute(words_list, query, ['业务渠道', '渠道'])
    if business_channel_group == 1:
        data['business_channel_group'] = 1
    # 是否出险分组
    accident_group = get_field_attribute(words_list, query, ['出险', '出险情况'])
    if accident_group == 1:
        data['accident_group'] = 1

    # source = get_cardim_source(query)
    # print(source)
    # cross = car_cross_class(query)
    # print(cross)
    # car_insu = get_car_insurance(query, dictionary)
    # print(car_insu)
    # car_info = get_car_info(query)
    # print(car_info)
    # new_channel = get_car_newchannel(query, dictionary)
    # print(new_channel)
    # car_channel = get_car_channel(query, dictionary)
    # data = get_car_common(data, words_list, query)

    # data.update(source)
    # data.update(car_insu)
    # data.update(cross)
    # data.update(car_info)
    # 最高学历
    education_background(body, "iATM_highest_degree", "highest_degree", data, dictionary)
    # 指标
    # 车辆数（纯车）
    change_field_format(body, "iATM_car_index_vehicle_numbers", "car_index_vehicle_numbers", data)
    # 保单件数
    change_field_format(body, "iATM_car_index_policy_pieces", "car_index_policy_pieces", data)
    # 保费和
    # 附加险保费和
    change_field_format(body, "iATM_car_additional_premium_sum", "car_additional_premium_sum", data)
    # 总保额
    change_field_format(body, "iATM_car_insured_amount_sum", "car_insured_amount_sum", data)
    # 附加险保额和
    change_field_format(body, "iATM_car_additional_insured_amount_sum", "car_additional_insured_amount_sum", data)
    # 车均保费（投保人）
    change_field_format(body, "iATM_car_average_premium", "car_average_premium", data)
    # 商业险件均保费
    change_field_format(body, "iATM_car_commercial_average_premium", "car_commercial_average_premium", data)
    # 投保人客户数
    change_field_format(body, "iATM_car_index_clients", "car_index_clients", data)
    # 客均保费（投保人）
    change_field_format(body, "iATM_car_customer_average_premium", "car_customer_average_premium", data)
    # 签单保费之和
    change_field_format(body, "iATM_car_sign_premium_sum", "car_sign_premium_sum", data)

    # 个团单标识
    get_filter_field(body, "iATM_car_personal_or_group", "car_personal_or_group", data)
    null_list = []
    print("test")
    print(data)
    for i in data:
        if data[i] == {} or data[i] == [] or data[i] == "":
            null_list.append(i)
    for i in null_list:
        data.pop(i, 0)
    return data


def get_life(query, words_list, body, dictionary):
    data = {}

    customer_status = get_customer_status(query, dictionary)
    # print(customer_status)
    others = get_others(query, dictionary)
    # print(others)
    cross_class = life_cross_class(query)
    # print(cross_class)
    status = get_status(query)
    # print(status)
    policy_status = get_policy_status(query, dictionary)
    # print(policy_status)
    screen = insurance_srceen(query)

    data.update(screen)
    data.update(customer_status)
    data.update(others)
    data.update(status)
    data.update(cross_class)
    data.update(policy_status)
    print(data)
    return data


# def get_targets(query, insurance_type):
#     if insurance_type == 0:
#         return get_life_targets()
#     if insurance_type == 1:
#         return get_car_targets()
#     if insurance_type == 2:
#         return get_noncar_targets()


def process_total(words_list, query, body, insurance_type, time_period, dictionary):
    data = {
        "fail_reason": "",
        "fail_code": ""
    }
    print("process start")

    if insurance_type == 0:
        print("~~~寿险~~~")
        life_total = get_life(query, words_list, body, dictionary)
        life_time_dict, time_message = get_life_time_mode(query, time_period)
        life_total.update(life_time_dict)
        # print(life_total)
        data["fail_reason"] = time_message
        life_total = change_field_tag_id(life_total)
        data["life"] = life_total.replace("\"", "\\\"")
    if insurance_type == 1:
        print("~~~车险~~~")
        car_total = get_car(query, words_list, body, dictionary)
        car_time_dict, time_message = get_car_time_code(query, 'car_start_time', 'car_end_time', 'car_record_time',
                                                        'car_sign_time', 'car_effect_time', 'car_entry_time',
                                                        time_period)
        car_interval_group = get_interval(query, dictionary)
        if car_interval_group:
            car_total['car_interval_group'] = car_interval_group
        car_total.update(car_time_dict)
        if time_message != "":
            if "car_organization" not in car_total.keys():
                data["fail_reason"] = "未识别到时间机构"
                data["fail_code"] = 11
            else:
                data["fail_reason"] = "未识别到时间"
                data["fail_code"] = 10
        car_total = change_field_tag_id(car_total)
        data["car"] = json.dumps(car_total).replace("\"", "\\\"")
    if insurance_type == 2:
        print("~~~非车险~~~")
        non_car_total = get_noncar(query, words_list, body, dictionary)
        not_car_time_dict, time_message = get_not_car_time_code(query, 'notCar_sign_time', 'notCar_record_time',
                                                                'notCar_start_time',
                                                                'notCar_end_time', time_period)
        noncar_interval = get_interval(query, dictionary)
        if noncar_interval:
            non_car_total['interval'] = noncar_interval
        non_car_total.update(not_car_time_dict)
        if time_message != "":
            if "notCar_organization" not in non_car_total.keys():
                if "notCar_insurance" not in non_car_total.keys():
                    data["fail_reason"] = "未识别到时间机构险种"
                    data["fail_code"] = 222
            else:
                if "notCar_insurance" not in non_car_total:
                    data["fail_reason"] = "未识别到时间险种"
                    data["fail_code"] = 21
        else:
            if "notCar_organization" not in non_car_total.keys():
                if "notCar_insurance" not in non_car_total.keys():
                    data["fail_reason"] = "未识别到险种机构"
                    data["fail_code"] = 22
            else:
                if "notCar_insurance" not in non_car_total:
                    data["fail_reason"] = "未识别到险种"
                    data["fail_code"] = 23
        non_car_total = change_field_tag_id(non_car_total)
        data["noncar"] = json.dumps(non_car_total).replace("\"", "\\\"")
    # 模糊搜索或枚举值过多
    data.update(get_undefined_field(query))
    print('process_data is {}'.format(data))
    return data
