import requests
import configparser
import json


## https://developers.criteo.com/marketing-solutions/reference/getadsetreport


url = "https://api.criteo.com/oauth2/token"

payload = "grant_type=client_credentials&client_id=fe0f29cd2f524f7b8b076e5246fd2da2&client_secret=TgGf8oD%2ByhrdZnESp3biYWvBB9NQGlGC9b9cKgaoWzFV"

auth_headers = {
    "Accept": "text/plain",
    "Content-Type": "application/x-www-form-urlencoded"
}

auth_response = requests.post(url, data=payload, headers=auth_headers)

auth_res_result = auth_response.json()
criteo_auth_token = auth_res_result["access_token"]
print(criteo_auth_token)

report_url = "https://api.criteo.com/2022-04/statistics/report"

payload =  ""

report_headers = {
    "Accept": "text/plain",
    "Content-Type": "application/*+json",
    "Authorization": "Bearer " + criteo_auth_token
}

report_response = requests.post(report_url, data=payload, headers=report_headers)
        
print(report_response.text)

