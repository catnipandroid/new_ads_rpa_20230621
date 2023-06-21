from NaverSA import NaverSA_API
from excelCreate import Create_Excel
from GoogleAds import GoogleAdsAPI, GoogleAdsPerform
import configparser

config = configparser.ConfigParser()
config.read('config\info.ini')

################### ################### ###################
################### Naver Search Ads 캠페인별 #############
################### ################### ###################

# Excel
incase_wb = Create_Excel(r'static\exist_excel\인케이스 리포트.xlsx')

# Day by Day Data를 담을 배열
incase_brand_search_pc_data = []
incase_brand_search_mob_data = []
incase_powerlink_pc_data = []
incase_powerlink_mob_data = []

# 브랜드검색 캠페인
incaseBrandAdCampaign = {
    'nccCampaignIdPC': 'cmp-a001-04-000000003086886',
    'nccCampaignIdMob': 'cmp-a001-04-000000003086868',
}

# 파워링크 캠페인
incasePlAdCampaign = {
    'nccCampaignIdPC': 'cmp-a001-01-000000005045511',
    'nccCampaignIdMob': 'cmp-a001-01-000000005045521',
}

# config 파일 필요함
naver_sa_api = NaverSA_API(config['naver_sa']['API_KEY'], config['naver_sa']['SECRET_KEY'], config['naver_sa']['multipop_CUSTOMER_ID'])

# 브랜드검색 호출
naver_sa_api.naverSearch_API_Get(
    incaseBrandAdCampaign['nccCampaignIdPC'], incase_brand_search_pc_data)
naver_sa_api.naverSearch_API_Get(
    incaseBrandAdCampaign['nccCampaignIdMob'], incase_brand_search_mob_data)

# 파워링크 호출
naver_sa_api.naverSearch_API_Get(incasePlAdCampaign['nccCampaignIdPC'], incase_powerlink_pc_data)
naver_sa_api.naverSearch_API_Get(incasePlAdCampaign['nccCampaignIdMob'], incase_powerlink_mob_data)

# 브랜드검색
incase_wb.naver_brand_sa_write(
    '네이버 브랜드검색', incase_brand_search_pc_data, 56, 18333)
incase_wb.naver_brand_sa_write(
    '네이버 브랜드검색', incase_brand_search_mob_data, 91, 80667)

# 파워링크
incase_wb.naver_sa_write('파워링크', incase_powerlink_pc_data, 56)
incase_wb.naver_sa_write('파워링크', incase_powerlink_mob_data, 91)    


################### ################### ###################
################### Google Ads 캠페인별 ###################
################### ################### ###################

# Google Conversion DA
# CID 및 캠페인 아이디 전달 (CID, Ads Account ID)
googleads_da_api = GoogleAdsAPI('8370773952', 19590351322)
# DB 쿼리 실행 (batch api)
googleads_da_api.get_data()
# 데이터 가져오기
googleAds_Perform = GoogleAdsPerform()
# Google DA
incase_wb.google_ads_write('구글애즈DA', googleAds_Perform.pc_data, 77)
incase_wb.google_ads_write('구글애즈DA', googleAds_Perform.mob_data, 112)
incase_wb.google_ads_write('구글애즈DA', googleAds_Perform.tablet_data, 147)
incase_wb.google_ads_write('구글애즈DA', googleAds_Perform.others_data, 182)
googleAds_Perform.clear_data()


# Google SA
# CID 및 캠페인 아이디 전달
googleads_sa_api = GoogleAdsAPI('8370773952', 13230191890)
# DB 쿼리 실행 (batch api)
googleads_sa_api.get_data()
# 데이터 가져오기
googleAds_Perform = GoogleAdsPerform()
# Google SA
incase_wb.google_ads_write('구글애즈SA', googleAds_Perform.pc_data, 58)
incase_wb.google_ads_write('구글애즈SA', googleAds_Perform.mob_data, 93)
incase_wb.google_ads_write('구글애즈SA', googleAds_Perform.tablet_data, 128)
incase_wb.google_ads_write('구글애즈SA', googleAds_Perform.others_data, 163)
googleAds_Perform.clear_data()


# Google PM
# CID 및 캠페인 아이디 전달
googleads_PM_api = GoogleAdsAPI('8370773952', 18000614330)
# DB 쿼리 실행 (batch api)
googleads_PM_api.get_data()
# 데이터 가져오기
googleAds_Perform = GoogleAdsPerform()
# Google PM
incase_wb.google_ads_write('구글애즈-스마트쇼핑', googleAds_Perform.pc_data, 58)
incase_wb.google_ads_write('구글애즈-스마트쇼핑', googleAds_Perform.mob_data, 93)
incase_wb.google_ads_write('구글애즈-스마트쇼핑', googleAds_Perform.tablet_data, 128)
incase_wb.google_ads_write('구글애즈-스마트쇼핑', googleAds_Perform.others_data, 163)
incase_wb.save('static\completed_excel\인케이스 리포트.xlsx')
googleAds_Perform.clear_data()

# 저장
incase_wb.save('static\completed_excel/인케이스 리포트.xlsx')