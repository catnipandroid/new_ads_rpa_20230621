import requests
import configparser
from datetime import datetime, timedelta
import json
from datetime import datetime

# conversion_test = "https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=conversion&targetDate=20230614&userId=godomall&apiKey=TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM"
# https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=ad&targetDate=20230201&userId=godomall&apiKey=TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM

config = configparser.ConfigParser()
config.read(r"config/info.ini")

token = config["Mobon"]["token"]
userId = config["Mobon"]["userId"]

ad_url = "https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=conversion&targetDate=20230614&userId=godomall&apiKey=TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM"
conversion_url = ""


# Mobon은 전체 광고주의 데이터를 받은 후, json 파일로 파싱 후 다운로드 -> 그 뒤 json파일 다시 딕셔너리로 파싱해서 광고주별로 데이터 가져오기
def fetch_mobon_performance(from_date, to_date):
    current_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        date_str_replace = date_str.replace("-", "")

        ad_url = f"https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=ad&targetDate={date_str_replace}&userId=godomall&apiKey={token}"

        r = requests.get(ad_url)

        data = r.json()

        json_data = json.dumps(data, ensure_ascii=False)

        output_file = f"mobon_ad_{from_date}_{to_date}.json"

        with open("Mobon/data/" + output_file, "w", encoding="utf-8") as file:
            file.write(json_data)

        current_date += timedelta(days=1)


def fetch_mobon_conversion(from_date, to_date):
    current_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        date_str_replace = date_str.replace("-", "")

        ad_url = f"https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=conversion&targetDate={date_str_replace}&userId=godomall&apiKey={token}"

        r = requests.get(ad_url)

        data = r.json()

        json_data = json.dumps(data, ensure_ascii=False)

        output_file = f"mobon_conversion_{from_date}_{to_date}.json"

        with open("Mobon/data/" + output_file, "w", encoding="utf-8") as file:
            file.write(json_data)

        current_date += timedelta(days=1)


def write_mobon_ad_data(from_date, to_date, userId, ads_performance):
    impCnt = 0
    clkCnt = 0
    CTR = 0
    cost = 0
    ccnt = 0
    CVR = 0
    convAmt = 0
    ROAS = 0

    file_name = f"mobon_ad_{from_date}_{to_date}.json"

    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    performance_data = data

    if data["result_code"] == 200:
        for i in performance_data["data"]:
            if i["userId"] == userId:
                ads_performance.append({})


def write_mobon_conversion_data(from_date, to_date, userId):
    json_file = f"mobon_conversion_{from_date}_{to_date}.json"
