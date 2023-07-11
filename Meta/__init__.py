from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from datetime import datetime, timedelta
import configparser
import time

config = configparser.ConfigParser()
config.read(r"config/info.ini")

# Meta Access Token
META_ACCESS_TOKEN = config["META"]["META_ACCESS_TOKEN"]
META_APP_ID = config["META"]["META_APP_ID"]
META_APP_SECRET = config["META"]["META_APP_SECRET"]


# 요청 횟수가 넘어가니 요청하는 부분을 따로 나눠서 쿼리를 쪼개서 데이터를 받아야할 듯
def fetch_meta_campaign_data(account_id, from_date, to_date, ads_performance):
    try:
        access_token = META_ACCESS_TOKEN
        app_id = META_APP_ID
        app_secret = META_APP_SECRET
        FacebookAdsApi.init(app_id, app_secret, access_token=access_token)

        # 필요한 필드 설정
        fields = [
            "campaign_name",
            "campaign_id",
            "account_name",
            "impressions",
            "clicks",
            "spend",
            "actions",
            "action_values",
        ]

        # 필터링 설정
        params = {
            "level": "campaign",
            "breakdowns": ["device_platform"],
            "action_breakdowns": ["action_type"],
            "action_type": ["offsite_conversion.fb_pixel_purchase"],
        }

        data = {}

        ad_account = AdAccount("act_" + account_id)

        # 날짜 범위 반복
        current_date = datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.strptime(to_date, "%Y-%m-%d")

        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            params["time_range"] = {"since": date_str, "until": date_str}

            # time.sleep(2)

            insights = ad_account.get_insights(fields=fields, params=params)

            for insight in insights:
                insight_data = insight.export_all_data()

                if date_str not in data:
                    data[date_str] = []

                data[date_str].append(insight_data)

            current_date += timedelta(days=1)

        # print(data)

        for date, insights in data.items():
            for insight in insights:
                actions_value_total = 0
                actions_total = 0

                # print(insight)

                if "action_values" in insight:
                    action_values = insight["action_values"]
                    for action_value in action_values:
                        if (
                            action_value["action_type"]
                            == "offsite_conversion.fb_pixel_purchase"
                        ):
                            actions_value_total += int(action_value["value"])

                if "actions" in insight:
                    actions = insight["actions"]
                    for action in actions:
                        if (
                            action["action_type"]
                            == "offsite_conversion.fb_pixel_purchase"
                        ):
                            actions_total += int(action["value"])

                device_type = {
                    "desktop": "PC",
                    "mobile_app": "모바일",
                    "mobile_web": "모바일",
                    "unknown": "모바일",
                }.get(insight["device_platform"], None)

                impressions = insight.get("impressions", 0)
                clicks = int(insight.get("clicks", 0))
                spend = insight.get("spend", 0)

                ads_performance.append(
                    {
                        "매체명": "META",
                        "기기": device_type,
                        "캠페인유형": "SNS",
                        "캠페인상태": "운영중",
                        "날짜": insight["date_start"],
                        "캠페인ID": insight["campaign_id"],
                        "캠페인명": insight["campaign_name"],
                        "노출수": int(float(insight.get("impressions", 0))),
                        "클릭수": clicks,
                        "클릭률": (clicks / int(float(insight.get("impressions", 1))))
                        if int(insight.get("impressions", 1)) > 0
                        else 0,
                        "비용": int(float(insight.get("spend", 0))),
                        "전환수": actions_total,
                        "전환률": (actions_total / clicks)
                        if actions_total > 0 and clicks > 0
                        else 0,
                        "전환가치": actions_value_total,
                        "ROAS": (
                            int(float(actions_value_total))
                            / int(float(insight.get("spend", 0)))
                        )
                        if int(actions_value_total) > 0 and int(actions_value_total) > 0
                        else 0,
                        "PC평균순위": 0,
                        "MO평균순위": 0,
                    }
                )
        return ads_performance

    except Exception as e:
        print(e)
