from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# 날짜 정보를 저장
days31 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
          '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

Year = input('구글애즈 광고 시작 년도를 입력해주세요. 형식: YYYY ')
Month = input('구글애즈 광고 시작 월을 입력해주세요. 형식: MM ')
Day = int(input('구글애즈 광고 언제까지의 데이터? 형식: DD '))

googleads_client = GoogleAdsClient.load_from_storage(version="v10")

query_device_selector = ['DESKTOP', 'MOBILE', 'TABLET', 'OTHER']

pc_data = {
    'impCnt': [],
    'clkCnt': [],
    'salesAmt': [],
    'ccnt': [],
    'convAmt': [],
}
mob_data = {
    'impCnt': [],
    'clkCnt': [],
    'salesAmt': [],
    'ccnt': [],
    'convAmt': [],
}
tablet_data = {
    'impCnt': [],
    'clkCnt': [],
    'salesAmt': [],
    'ccnt': [],
    'convAmt': [],
}
others_data = {
    'impCnt': [],
    'clkCnt': [],
    'salesAmt': [],
    'ccnt': [],
    'convAmt': [],
}


class GoogleAdsAPI:

    def __init__(self, cid, campaign_id):
        self.cid = cid
        self.campaign_id = campaign_id
        self.pc_data = pc_data
        self.mob_data = mob_data
        self.tablet_data = tablet_data
        self.others_data = others_data

    def get_data(self):
        ga_service = googleads_client.get_service("GoogleAdsService")

        # 기기는 enum 데이터이며, PC => 모바일 => 태블릿 => 기타 순
        for idx, i in enumerate(query_device_selector):
            for j in days31[0:Day]:
                query = """
                        SELECT
                            campaign.id,
                            segments.device,
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
                            segments.device = {0}
                            AND segments.date BETWEEN '{1}-{2}-{3}' AND '{1}-{2}-{3}'
                        """.format(query_device_selector[idx], Year, Month, j)

                search_request = googleads_client.get_type(
                    "SearchGoogleAdsStreamRequest")
                search_request.customer_id = self.cid
                search_request.query = query

                stream = ga_service.search_stream(search_request)

                for batch in stream:
                    for row in batch.results:
                        campaign = row.campaign
                        ad_group = row.ad_group
                        metrics = row.metrics
                        campaign_id = campaign.id

                        if query_device_selector[idx] == 'DESKTOP' and campaign.id == self.campaign_id:
                            pc_data['impCnt'].append(metrics.impressions)
                            pc_data['clkCnt'].append(metrics.clicks)
                            pc_data['salesAmt'].append(
                                int(metrics.average_cpc*0.000001))
                            pc_data['ccnt'].append(metrics.conversions)
                            pc_data['convAmt'].append(
                                metrics.conversions_value)
                        elif query_device_selector[idx] == 'MOBILE' and campaign.id == self.campaign_id:
                            mob_data['impCnt'].append(metrics.impressions)
                            mob_data['clkCnt'].append(metrics.clicks)
                            mob_data['salesAmt'].append(
                                int(metrics.average_cpc*0.000001))
                            mob_data['ccnt'].append(metrics.conversions)
                            mob_data['convAmt'].append(
                                metrics.conversions_value)
                        elif query_device_selector[idx] == 'TABLET' and campaign.id == self.campaign_id:
                            tablet_data['impCnt'].append(metrics.impressions)
                            tablet_data['clkCnt'].append(metrics.clicks)
                            tablet_data['salesAmt'].append(
                                int(metrics.average_cpc*0.000001))
                            tablet_data['ccnt'].append(metrics.conversions)
                            tablet_data['convAmt'].append(
                                metrics.conversions_value)
                        elif query_device_selector[idx] == 'OTHERS' and campaign.id == self.campaign_id:
                            others_data['impCnt'].append(metrics.impressions)
                            others_data['clkCnt'].append(metrics.clicks)
                            others_data['salesAmt'].append(
                                int(metrics.average_cpc*0.000001))
                            others_data['ccnt'].append(metrics.conversions)
                            others_data['convAmt'].append(
                                metrics.conversions_value)


class GoogleAdsPerform(GoogleAdsAPI):

    def __init__(self):
        self.pc_data = pc_data
        self.mob_data = mob_data
        self.tablet_data = tablet_data
        self.others_data = others_data

    # Clear Datas
    def clear_data(self):

        self.pc_data['impCnt'].clear()
        self.pc_data['clkCnt'].clear()
        self.pc_data['salesAmt'].clear()
        self.pc_data['ccnt'].clear()
        self.pc_data['convAmt'].clear()

        self.mob_data['impCnt'].clear()
        self.mob_data['clkCnt'].clear()
        self.mob_data['salesAmt'].clear()
        self.mob_data['ccnt'].clear()
        self.mob_data['convAmt'].clear()

        self.tablet_data['impCnt'].clear()
        self.tablet_data['clkCnt'].clear()
        self.tablet_data['salesAmt'].clear()
        self.tablet_data['ccnt'].clear()
        self.tablet_data['convAmt'].clear()

        self.others_data['impCnt'].clear()
        self.others_data['clkCnt'].clear()
        self.others_data['salesAmt'].clear()
        self.others_data['ccnt'].clear()
        self.others_data['convAmt'].clear()
