#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
#from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#import time
#import pymysql


# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('serviceAccount.json')


# 初始化firebase，注意不能重複初始化
#firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()



for num in range(1,86,4):
    if num < 10:
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-'+'00'+str(num) +'?Authorization=CWB-DB626D4A-61AC-493B-867C-69290345C159&format=JSON'
    else:
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-'+'0'+str(num) +'?Authorization=CWB-DB626D4A-61AC-493B-867C-69290345C159&format=JSON'
    print(url)
    

    data = requests.get(url)
    data_json = data.json()
    datatest = json.loads(data.text)
#縣
    location = datatest["records"]["locations"][0]["locationsName"]

#鄉鎮
    locations = datatest["records"]["locations"][0]["location"]#[1]["locationName"]

#天氣預報綜合描述:2022-06-14 06:00:00(3)、(11)
    times = datatest["records"]["locations"][0]["location"][1]["weatherElement"][6]['time'][11]['endTime']

#print(locations)
#天氣預報綜合描述:晴。降雨機率 20%。溫度攝氏27度。舒適。偏南風 平均風速2-3級(每秒4公尺)。相對濕度90%。
    cilm = datatest["records"]["locations"][0]["location"][1]["weatherElement"][6]['time'][3]['elementValue'][0]['value']
#天氣預報綜合描述
    #print(location)

    for i in range(len(locations)):
      name = locations[i]['locationName']  #全部鄉鎮名
      time1 = locations[i]["weatherElement"][6]['time'][3]['endTime'] #日期時間
      time2 = locations[i]["weatherElement"][6]['time'][11]['endTime'] #日期時間
          
      cilm1 = locations[i]["weatherElement"][6]['time'][3]['elementValue'][0]['value'] #天氣預報綜合描述 
      cilm2 = locations[i]["weatherElement"][6]['time'][11]['elementValue'][0]['value'] #天氣預報綜合描述
           
      doc ={
            'location':location,
            'name':name,
            'time_today':time1,
            'cilm_today':cilm1,
            'time_tomorrow':time2,
            'cilm_tomorrow':cilm2
            }
          # 建立文件 必須給定 集合名稱 文件id
          # 即使 集合一開始不存在 都可以直接使用

          # 語法
          # doc_ref = db.collection("集合名稱").document("文件id")
      location_name=location + name
      doc_ref = db.collection("exam").document(location_name)
          # doc_ref提供一個set的方法，input必須是dictionary
      doc_ref.set(doc)
      print(doc)

