import configparser
import pandas as pd
from NaverSA import fetch_campaign_list_data, fetch_campaign_performance, write_campaign_performance_data
from GoogleAds import fetch_gads_campaign_performance_data, write_gads_camapaign_performance_data

config = configparser.ConfigParser()
config.read(r'config/info.ini')

gads_cid = "7694228249"
naver_id = config['naver_sa']['aminotree_CUSTOMER_ID']

year = input("조회하실 연도? ")
month = input("조회하실 월? ")
from_day = input("언제부터 조회? ")
to_day = input("언제까지 조회? ")

# 모든 매체의 성과 담기
ads_performance = []

# 네이버 캠페인별 성과 가져오기
campaign_list_data = fetch_campaign_list_data(naver_id)
fetch_campaign_performance = fetch_campaign_performance(naver_id, campaign_list_data, year, month, from_day, to_day)
write_campaign_performance_data = write_campaign_performance_data(ads_performance, fetch_campaign_performance)


# Google Ads
fetch_gads_campaign_performance_data = fetch_gads_campaign_performance_data(gads_cid, year, month, from_day, to_day)
write_gads_camapaign_performance_data = write_gads_camapaign_performance_data(ads_performance, fetch_gads_campaign_performance_data)
print(ads_performance)


df = pd.DataFrame(ads_performance)

output_file = 'output.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')


