import requests
import time
from .utils import signaturehelper
import configparser
from datetime import datetime
import json

# 날짜 정보를 저장
days31 = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
]

# API info 가져오기
config = configparser.ConfigParser()
config.read(r'config\info.ini')

# uri method 세팅
BASE_URL = 'https://api.searchad.naver.com'

def naver_SA_auth(uri, method, CUSTOMER_ID):

    # API 등 정보
    API_KEY = config['naver_sa']['API_KEY']
    SECRET_KEY = config['naver_sa']['SECRET_KEY']
    CUSTOMER_ID = CUSTOMER_ID
    
    # 인증 및 헤더 세팅
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

def fetch_campaign_list_data(CUSTOMER_ID):
    r = requests.get(BASE_URL + '/ncc/campaigns', params={'type': 'MYCLIENTS'}, headers=naver_SA_auth('/ncc/campaigns', 'GET', CUSTOMER_ID))
    data = r.json()

    campaign_info_data = []

    for i in data:
        if not i['status'] == 'PAUSED':
            campaign_info_data.append({"campaign_id":i['nccCampaignId'], "campaign_tp":i["campaignTp"]})

    return campaign_info_data

def fetch_campaign_performance(CUSTOMER_ID, campaign_list, year, month, from_day, to_day):

    campaign_performance_data = []

    from_date = year + '-' + month + '-' + from_day
    to_date = year + '-' + month + '-' + to_day

    _from_date = datetime.strptime(from_date, "%Y-%m-%d")
    _to_date = datetime.strptime(to_date, "%Y-%m-%d")

    formatted_from_date = _from_date.strftime("%Y-%m-%d")

    for i in days31[0:int(to_day)]:
        reportDate = json.dumps({ "since": formatted_from_date, "until": year + "-" + month + "-" + str(i) })
        for j in campaign_list:
            r = requests.get(BASE_URL + '/stats', params={'ids': [j["campaign_id"]], 'fields': '["impCnt", "clkCnt", "salesAmt", "ccnt", "convAmt"]','timeRange': reportDate} , headers=naver_SA_auth('/stats', 'GET', CUSTOMER_ID))
            data = r.json()
            campaign_performance_data.append(data)

    return campaign_performance_data
                                   