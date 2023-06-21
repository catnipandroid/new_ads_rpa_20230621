import requests
import time
import datetime
import json
from utils import signaturehelper

# 날짜 정보를 저장
days31 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
          '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

# 조회할 년,월 문의
Year = input('네이버검색광고 시작 년도를 입력해주세요. 형식: YYYY ')
Month = input('네이버검색광고 시작 월을 입력해주세요. 형식: MM ')
Day = int(input('네이버검색광고 언제까지의 데이터? 형식: DD '))

# Basic API Infos & Method to get the report
BASE_URL = 'https://api.naver.com'
uri = '/stats'
method = 'GET'

class NaverSA_API():
    
    # Naver API Client Info
    def __init__(self, API_KEY, SECRET_KEY, CUSTOMER_ID):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.CUSTOMER_ID = CUSTOMER_ID

    # 네이버 API를 사용하기 위한 헤더 세팅
    def get_header(self, method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
        timestamp = str(round(time.time() * 1000))
        signature = signaturehelper.Signature.generate(timestamp, method, uri, self.SECRET_KEY)
        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': self.API_KEY, 'X-Customer': self.CUSTOMER_ID, 'X-Signature': signature}
    
    # 네이버 SA API 호출
    def naverSearch_API_Get(self, campaign, arr):
    
        for i in days31[0:Day]:
            # json data로 변경한다.
            reportDate = json.dumps({
                                        "since": Year+"-"+Month+"-"+str(i), 
                                        "until": Year+"-"+Month+"-"+str(i)
                                    })

            api_get = requests.get(BASE_URL + uri, 
                                    params={
                                                'ids': campaign, 
                                                'fields': '["impCnt", "clkCnt", "salesAmt", "ccnt", "convAmt"]',
                                                'timeRange': reportDate
                                            }, 
                                    headers=self.get_header(method, uri, self.API_KEY, self.SECRET_KEY, self.CUSTOMER_ID))
            
            datas = api_get.json()
            
            if not datas['data']:
                arr.append({
                    'data': [{
                                'convAmt': 0, 
                                'clkCnt': 0, 
                                'ccnt': 0, 
                                'id': '0', 
                                'impCnt': 0, 
                                'salesAmt': 0
                            }], 
                    'compTm': '0', 
                    'cycleBaseTm': '0'
                })
            else: 
                arr.append(datas)
                
                
