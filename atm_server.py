# -*- coding: UTF-8 -*-
import json
import jieba
import jieba.posseg as pseg
import datetime
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from common import init_slot, get_insurance_type, token, get_channels, get_agencys, get_time_detail
from common import get_life_period
from atm_api import process_total


# insurance_dict = {0: "寿险", 1: "车险", 2: "非车"}


# 初始化日志信息
def init_log():
    log_file = 'atm_log.txt'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = TimedRotatingFileHandler(log_file, when='D', interval=24, backupCount=7)
    datefmt = '%Y-%m-%d %H:%M:%S'
    # format_str = '%(asctime)s %(levelname)s\n%(message)s'
    format_str = '%(message)s'
    formatter = logging.Formatter(format_str, datefmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# 初始化
logger = init_log()


# define a httpserver class to handle bank data
class AtmServer(BaseHTTPRequestHandler):

    def get_logtime(self):
        time_stamp = int(time.time())
        time_array = time.localtime(time_stamp)
        logtime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return logtime

    def write_log(self, logInfo):
        try:
            logger.debug(logInfo)
        except:
            return

    def do_POST(self):
        print(self.path)
        method = self.path.strip('/')
        body = self.rfile.read(int(self.headers['content-length']))
        print(method, body, datetime.datetime.now())
        logtime = self.get_logtime()
        self.write_log(logtime + ":use method {}".format(method))
        self.write_log("recv body {}".format(body))
        getattr(self, method)(body)
        self.response()
        self.write_log("response {}".format(self.response_data))

    def atm_extract_time(self, body):

        # add decode for python3.4
        body = json.loads(body.decode('utf-8'))
        data = {}
        try:
            if '-' in body['time_slot']:
                time_slot = body["time_slot"].split('-')
                print(time_slot)
                start_year, start_month, start_day, end_year, end_month, end_day, start_time, end_time = get_time_detail(
                    time_slot)
                if start_year == end_year:
                    if int(start_month) == 1 and int(end_month) == 12:
                        start_month = end_month
                data["time_mode"] = start_year + '年' + str(int(start_month)) + '月'
                data["time_period"] = start_time + '-' + end_time
                data["status"] = 0
            else:
                data['status'] = 1
        except Exception as e:
            print(e)
            data['status'] = 1
            data['msg'] = 0
        self.response_data = json.dumps(data)

    def atm_extract_agency(self, body):
        dictionary = get_dict()
        body = json.loads(body.decode('utf-8'))
        data = {}
        if body:
            # try:
            query = body["slot"]
            cut_list = pseg.lcut(' '.join(token(query)))

            muliti_addr = []
            for word, flag in cut_list:
                if flag == 'ns' or word in list(dictionary['life_agencys_expand'].keys()):
                    muliti_addr.append(word)
            muliti_addr = get_agencys(muliti_addr, 3, dictionary)
            data["agencys"] = muliti_addr
            data["status"] = 0
        # except:
        # data["status"] = 1
        self.response_data = json.dumps(data)

    def atm_extract_channel(self, body):
        dictionary = get_dict()
        body = json.loads(body.decode('utf-8'))
        data = {}
        try:
            slot = body["slot"]
            cut_list = jieba.lcut(' '.join(token(slot)))

            channels = []
            print(cut_list)
            channels = channels + get_channels(cut_list, None, dictionary)
            print(channels)

            data["channels"] = channels
            data["status"] = 0
        except Exception as e:
            print(e)
            data["status"] = 1
        self.response_data = json.dumps(data)

    # 转换词槽抓取到的数据的格式
    def atm_change_format(self, body):
        pass

    def atm_extract_insurance(self, body):
        dictionary = get_dict()
        body = json.loads(body.decode('utf-8'))
        data = {}
        if body:
            # try:
            slot = body["slot"]

            cut_list = jieba.lcut(slot)
            print(cut_list)
            insurance_type, insurance_name = get_insurance_type(slot, dictionary)
            # print(body['time_slot'])
            print(dictionary['insurance_dict'])
            data["tag_types"] = dictionary["insurance_dict"]["{}".format(insurance_type)]
            data["insurance_name"] = list(set(insurance_name))

            data["status"] = 0
            data["periods"] = get_life_period(cut_list, dictionary)
            data["time_period"] = ''
            if '-' in body['time_slot']:
                time_slot = body["time_slot"].split('-')
                start_year, start_month, start_day, end_year, end_month, end_day, start_time, end_time = get_time_detail(
                    time_slot)
                data["time_mode"] = start_year + '年' + str(int(start_month)) + '月'
                data["time_period"] = start_time + '-' + end_time
                data["status"] = 0
            total = process_total(cut_list, slot, body, insurance_type, data['time_period'], dictionary)
            # print(insurance_type)
            # print(total)
            data.update(total)

            # sub_intent = ['保单件数', '保费和', '客户数']
            # father_intent = '销售情况'
            # if father_intent in slot:
            #     data['sales'] = sub_intent
            # else:
            #     intent_result = []
            #     for sub in sub_intent:
            #         if sub in slot:
            #             intent_result.append(sub)
            #     data['target'] = intent_result
            # except:
            # data["status"] = 1

            # print("final_data is {}".format(data))
            test_data = {
                "tag_types": "car",
                "car": {
                    "200001": "2019/01/01,2019/03/31",
                    "200003": "4010100410300",
                    "200084": "北京,上海",
                    "200359": "*-1,2-14,15-26,27-#",
                    "200191": "101,102,001,002$$$交强险-6座以下客车,交强险-6座及10座以下客车,商业险-6座以下客车,商业险-6座及10座以下客车",
                    "200097": "362397,364227,371275$$$东风日产奇骏,奇骏,日产奇骏",
                    "200689": "2019/10/01,2019/10/28",
                    "200472": "13940100$$$13941100$$$13942100$$$13943100$$$13944100$$$13945100$$$13946100$$$44150100$$$44151100$$$44152100$$$44153100$$$44154100$$$44155100$$$44156100$$$44157100",
                    "200693": "FC001,7020100,1030100"
                },
                "fail_reason": "",
                "fail_code": "",
                "message": ""
            }
            test_data1 = {
                "tag_types": "noncar",
                "noncar": "{\"5000001\": \"2019/01/01,2019/03/31\",\"5000014\": \"20,#\",}",
                    # "5000199": "BXSH,WYBXJJ,BXSPT,HZWY$$$杭州微易,杭州微易,杭州微易,杭州微易",
                    # "5000006": "170174526005040000",
                    # "5000091": "1",
                    # "5000072": "203,204",
                    # "5000195": "*-1,2-14,15-26,27-#",
                    # "5000062": "-1"

                "fail_reason": "",
                "fail_code": "",
                "message": ""
            }
            data.pop("insurance_name", 0)
            # data.pop("status", 0)
            data.pop("periods", 0)
        # self.response_data = json.dumps(test_data)
        self.response_data = json.dumps(data)

    def response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(self.response_data, encoding="utf8"))


def get_dict():
    with open('dictionary.txt', 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    return dictionary


dictionary1 = get_dict()
init_slot(dictionary1)


def run():
    port = 1558
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, AtmServer)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
