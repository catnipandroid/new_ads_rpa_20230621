import requests
import time
from .utils import signaturehelper
import configparser
from datetime import datetime, timedelta
import json


# API info 가져오기
config = configparser.ConfigParser()
config.read(r"config/info.ini")

# uri method 세팅
BASE_URL = "https://api.searchad.naver.com"


def naver_SA_auth(uri, method, CUSTOMER_ID):
    # API 등 정보
    API_KEY = config["naver_sa"]["API_KEY"]
    SECRET_KEY = config["naver_sa"]["SECRET_KEY"]
    CUSTOMER_ID = CUSTOMER_ID

    # 인증 및 헤더 세팅
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)

    return {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Timestamp": timestamp,
        "X-API-KEY": API_KEY,
        "X-Customer": str(CUSTOMER_ID),
        "X-Signature": signature,
    }


def fetch_campaign_list_data(CUSTOMER_ID):
    r = requests.get(
        BASE_URL + "/ncc/campaigns",
        params={"type": "MYCLIENTS"},
        headers=naver_SA_auth("/ncc/campaigns", "GET", CUSTOMER_ID),
    )
    data = r.json()

    campaign_info_data = []
    for i in data:
        campaign_info_data.append(
            {
                "campaign_status": i["status"],
                "campaign_id": i["nccCampaignId"],
                "campaign_name": i["name"],
                "campaign_tp": i["campaignTp"],
            }
        )

    # print(campaign_info_data)

    return campaign_info_data


def fetch_adgroup_list_data(CUSTOMER_ID):
    nccAdgroupId = []

    r = requests.get(
        BASE_URL + "/ncc/adgroups",
        params={"targetTp": "PC_MOBILE_TARGET"},
        headers=naver_SA_auth("/ncc/adgroups", "GET", CUSTOMER_ID),
    )
    data = r.json()

    for i in data:
        nccAdgroupId.append(i["nccAdgroupId"])

    return nccAdgroupId


def fetch_adgroup_targeting(CUSTOMER_ID, list):
    data = []

    for i in list:
        r = requests.get(
            BASE_URL + f"/ncc/adgroups/{i}",
            params={"targetTp": "PC_MOBILE_TARGET"},
            headers=naver_SA_auth(f"/ncc/adgroups/{i}", "GET", CUSTOMER_ID),
        )
        data.append(r.json())

    json_data = json.dumps(data, ensure_ascii=False)

    output_file = "output_adgroup_data.json"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_data)


def fetch_report_list(CUSTOMER_ID):
    r = requests.get(
        BASE_URL + "/stat-reports",
        params={"targetTp": "PC_MOBILE_TARGET"},
        headers=naver_SA_auth("/stat-reports", "GET", CUSTOMER_ID),
    )
    data = r.json()

    json_data = json.dumps(data, ensure_ascii=False)

    output_file = "output.json"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_data)


def fetch_master_report_list(CUSTOMER_ID):
    r = requests.get(
        BASE_URL + "/master-reports",
        params={"breakdown": "pcMblTp", "targetTp": "PC_MOBILE_TARGET"},
        headers=naver_SA_auth("/master-reports", "GET", CUSTOMER_ID),
    )
    data = r.json()

    json_data = json.dumps(data, ensure_ascii=False)

    output_file = "output.json"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_data)


def fetch_campaign_performance(CUSTOMER_ID, campaign_list, from_date, to_date):
    campaign_performance_data = []

    current_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        print(date_str)

        for idx, j in enumerate(campaign_list):
            reportDate = json.dumps(
                {
                    "since": date_str,
                    "until": date_str,
                }
            )

            r = requests.get(
                BASE_URL + "/stats",
                params={
                    "ids": [j["campaign_id"]],
                    "fields": '["impCnt", "clkCnt", "ctr", "avgRnk", "crto", "ror", "cpConv", "salesAmt", "ccnt", "convAmt", "pcNxAvgRnk", "mblNxAvgRnk"]',
                    "timeRange": reportDate,
                },
                headers=naver_SA_auth("/stats", "GET", CUSTOMER_ID),
            )

            if r.status_code == 200:
                data = r.json()

                data["date"] = date_str
                data["campaign_tp"] = campaign_list[idx]["campaign_tp"]
                data["campaign_status"] = campaign_list[idx]["campaign_status"]
                data["campaign_name"] = campaign_list[idx]["campaign_name"]

                campaign_performance_data.append(data)

        current_date += timedelta(days=1)

    return campaign_performance_data


def write_campaign_performance_data(ads_performance, naverSA_performance_data):
    for i in naverSA_performance_data:
        if i["data"]:
            campaign_tp = {
                "WEB_SITE": "파워링크",
                "SHOPPING": "쇼핑검색",
                "BRAND_SEARCH": "브랜드검색",
            }.get(i["campaign_tp"], None)

            campaign_status = {"PAUSED": "정지", "ELIGIBLE": "운영중"}.get(
                i["campaign_status"], None
            )

            campaign_name = i["campaign_name"]

            ads_performance.append(
                {
                    "매체명": "네이버 검색광고",
                    "기기": "네이버 API에서 안줌...",
                    "캠페인유형": campaign_tp,
                    "캠페인상태": campaign_status,
                    "날짜": i["date"],
                    "캠페인ID": i["data"][0]["id"],
                    "캠페인명": campaign_name,
                    "노출수": i["data"][0]["impCnt"] if i["data"] else 0,
                    "클릭수": i["data"][0]["clkCnt"] if i["data"] else 0,
                    "클릭률": int(i["data"][0]["clkCnt"]) / int(i["data"][0]["impCnt"])
                    if i["data"] and int(i["data"][0]["clkCnt"]) > 0
                    else 0,
                    "비용": i["data"][0]["salesAmt"] if i["data"] else 0,
                    "전환수": i["data"][0]["ccnt"] if i["data"] else 0,
                    "전환률": (
                        int(i["data"][0]["ccnt"] if i["data"] else 0)
                        / int(i["data"][0]["clkCnt"] if i["data"] else 0)
                    )
                    if i["data"] and int(i["data"][0]["clkCnt"]) > 0
                    else 0,
                    "전환가치": i["data"][0]["convAmt"] if i["data"] else 0,
                    "ROAS": (
                        int(i["data"][0]["convAmt"]) / int(i["data"][0]["salesAmt"])
                    )
                    if i["data"][0]["salesAmt"] > 0
                    else 0,
                    "PC평균순위": i["data"][0]["pcNxAvgRnk"] if i["data"] else 0,
                    "MO평균순위": i["data"][0]["mblNxAvgRnk"] if i["data"] else 0,
                }
            )

    return ads_performance
