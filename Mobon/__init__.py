import requests
import json
from datetime import datetime

# conversion_test = "https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=conversion&targetDate=20230614&userId=godomall&apiKey=TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM"
# https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType=ad&targetDate=20230201&userId=godomall&apiKey=TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM

inquire_year = input("조회하실 년도? ")
inquire_month = input("조회하실 월? ")
inquire_day = int(input("일자를 언제까지 조회? "))

targetDate = inquire_year + inquire_month
apiKey = "TWpBeU1URXhNamt4TURJeU5USXdYMmR2Wkc5dFlXeHM"
userId = "godomall"


def fetch_ads_performance_data(statsType, view_userId):
    url = f"https://www.mediacategory.com/servlet/API/ver2.1/JSON/sNo/0/STATS?type=AD&statsType={statsType}\
            &userId={userId}&apiKey={apiKey}"

    data_arry = []

    for i in range(1, int(inquire_day + 1)):
        date = datetime.strptime(str(i), "%d")
        api_url = (
            url
            + "&targetDate="
            + inquire_year
            + inquire_month
            + str(date.strftime("%dd"))
        )

        response = requests.get(api_url)

        json_data = response.json()

        if json_data["result_code"] == 200:
            for j in json_data["data"]:
                if j["userId"] == view_userId:
                    j["date"] = inquire_year + inquire_month + str(date.strftime("%d"))
                    data_arry.append(j)
        else:
            data_arry.append(
                {
                    "date": inquire_year + inquire_month + str(date.strftime("%d")),
                    "serviceGubun": "noData",
                    "siteCode": "e7d9193d36474d229e351a3007e13073",
                    "userId": view_userId,
                    "siteName": "noData",
                    "adGubun": "noData",
                    "adGubunName": "noData",
                    "viewCnt1": 0,
                    "clickCnt": 0,
                    "point": 0,
                }
            )

    return data_arry


# conversion_api = fetch_ads_performance_data("conversion", "trdst")
ads_api = fetch_ads_performance_data("ad", "trdst")

print(ads_api)
