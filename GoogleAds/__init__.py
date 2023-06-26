from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
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

googleads_client = GoogleAdsClient.load_from_storage(version="v14")


def fetch_gads_campaign_performance_data(cid, year, month, from_day, to_day):
    ga_service = googleads_client.get_service("GoogleAdsService")

    campaign_performance_data = []

    # 기기는 enum 데이터이며, PC => 모바일 => 태블릿 => 기타 순
    query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                segments.device,
                segments.date,
                metrics.average_cpc,
                metrics.average_cost,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_by_conversion_date,
                metrics.conversions_value,
                metrics.conversions_value_by_conversion_date
            FROM campaign
            WHERE
                segments.date BETWEEN '{from_day}' AND '{to_day}'
            """
    search_request = googleads_client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = cid
    search_request.query = query

    stream = ga_service.search_stream(search_request)

    for batch in stream:
        for row in batch.results:
            campaign = row.campaign
            date = row.segments.date
            device = row.segments.device
            campaign_id = campaign.id
            campaign_name = campaign.name
            metrics = row.metrics

            campaign_performance_data.append(
                {
                    "date": date,
                    "campaign_id": campaign_id,
                    "campaign_device": device,
                    "campaign_status": campaign.status,
                    "campaign_channel_type": campaign.advertising_channel_type,
                    "campaign_name": campaign_name,
                    "cost": int(metrics.cost_micros / 1000000.0),
                    "impCnt": metrics.impressions,
                    "clkCnt": metrics.clicks,
                    "ctr": (metrics.clicks / metrics.impressions)
                    if not metrics.impressions == 0
                    else 0,
                    "ccnt": int(metrics.conversions),
                    "crto": (metrics.conversions / metrics.clicks)
                    if not metrics.clicks == 0
                    else 0,
                    "convAmt": int(metrics.conversions_value),
                }
            )

    return campaign_performance_data


def write_gads_camapaign_performance_data(ads_performance, data):
    for i in data:
        device_type = {
            0: "TV",
            1: "PC",
            2: "모바일",
            3: "기타",
            4: "태블릿",
            5: "알수없음",
            6: "명시되지않음",
        }.get(i["campaign_device"], None)

        campaign_status = {
            0: "명시되지않음",
            1: "알수없음",
            2: "운영중",
            3: "중지",
            4: "삭제됨",
        }.get(i["campaign_status"], None)

        campaign_type = {
            0: "명시되지않음",
            1: "알수없음",
            2: "검색",
            3: "디스플레이",
            4: "쇼핑",
            5: "호텔",
            6: "비디오",
            7: "멀티채널",
            8: "로컬",
            9: "스마트",
            10: "성과최대화",
            11: "로컬서비스",
            12: "디스커버리",
            13: "여행",
        }.get(i["campaign_channel_type"], None)

        ads_performance.append(
            {
                "매체명": "구글애즈",
                "기기": device_type,
                "캠페인유형": campaign_type,
                "캠페인상태": campaign_status,
                "날짜": i["date"],
                "캠페인ID": i["campaign_id"],
                "캠페인명": i["campaign_name"],
                "노출수": int(i["impCnt"]),
                "클릭수": int(i["clkCnt"]),
                "클릭률": i["ctr"],
                "비용": int(i["cost"]),
                "전환수": int(i["ccnt"]),
                "전환률": i["crto"],
                "전환가치": int(i["convAmt"]),
                "PC평균순위": 0,
                "MO평균순위": 0,
            }
        )

    return ads_performance
