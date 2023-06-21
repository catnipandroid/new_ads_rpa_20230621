import configparser
from NaverSA import fetch_campaign_list_data,fetch_campaign_performance

config = configparser.ConfigParser()
config.read(r'config\info.ini')

year = input("조회하실 연도? ")
month = input("조회하실 월? ")
from_day = input("언제부터 조회? ")
to_day = input("언제까지 조회? ")

campaign_list_data = fetch_campaign_list_data(config['naver_sa']['aminotree_CUSTOMER_ID'])

# 예시 return 값 
# [{'cmp-a001-01-000000004140839': 'WEB_SITE'}, 
# {'cmp-a001-01-000000004140843': 'WEB_SITE'}, 
# {'cmp-a001-02-000000006599217': 'SHOPPING'}, 
# {'cmp-a001-04-000000001172425': 'BRAND_SEARCH'}]

fetch_naverSA_performance_data = fetch_campaign_performance(config['naver_sa']['aminotree_CUSTOMER_ID'], campaign_list_data, year, month, from_day, to_day)

print(fetch_naverSA_performance_data)

