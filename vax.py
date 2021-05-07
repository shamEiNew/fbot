import requests
import json
import winsound
import datetime as dt
import time
from datetime import datetime, date
import pytz

def notify(district, DATE, frequency, duration, my_headers):
    data = []
    for d in district['districts']:
        District_id = d['district_id']
        url1 = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={District_id}&date={DATE}"
        res = requests.get(url1, headers = my_headers)
        try:
            res1 = res.json()['sessions']
        except:
            res1 = []
        if res1 != []:
            for p in res1:
                if p['min_age_limit']==18 and p['district_name']=="Mumbai":
                    data.append(f"{p['district_name']}-{p['name']}-{p['address']}-{p['pincode']}")

    return data

def vax_main():
    my_date = datetime.now(pytz.timezone('Asia/Kolkata')) 
    DATE = my_date+dt.timedelta(days=1)
    DATE = str(DATE)
    DATE = f"{DATE[8:10]}-{DATE[5:7]}-{DATE[0:4]}"
    n = 21
    frequency = 2500
    duration = 2000
    my_headers = {'accept':'application/json','Accept-Language': 'en_US','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url2 = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{n}"
    response = requests.get(url2, headers = my_headers)
    try:
        district = response.json()
    except:
        pass
    data = notify(district, DATE, frequency, duration, my_headers)
    return data