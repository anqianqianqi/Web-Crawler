#@Author: Anqi Luo
import json
import pandas as pd
import urllib.request
import requests
import time
import numpy as np

#    default max num of row = 100
# input url shall be in format of "http://...offset="


update_date = "20190716"

url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/money/supply-unadjusted-fc?segment=old&offset="
data_file = "Unadjusted_for_foreign_currency_swap_deposits_tab_old"


def get_statistics(data_file,url): ##This is the new one remember to import the requests package     
    r = requests.get(url) 
    r.encoding = 'utf-8'
    JSON_object = r.json()
    df = pd.DataFrame(JSON_object['result']['records'])
    df.to_csv(data_file + "_" + update_date +".csv")
    return df


def get_statistics_old(data_file, url):
    req = urllib.request.urlopen (url)
    data = req.read()
    encoding = req.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    df = pd.DataFrame(JSON_object['result']['records'])
    #time.sleep(np.random.rand(1))
    return df


    
def get_cvs(data_file,url):
    data_file1 = data_file + str(0)
    to_combine = []
    i = 0
    j = 100 * i
    url_next = url + str(j)
    while get_statistics(data_file1,url_next).empty is False:
        data_file1 = data_file + str(i)
        to_combine.append(get_statistics(data_file1,url_next))
        i = i + 1
        j = 100 * i
        url_next = url + str(j)
       
    combine = pd.concat(to_combine)
    combine.to_csv(data_file + "_" + update_date +".csv")
    
    return

import openpyxl 
  
from openpyxl import load_workbook
wb = load_workbook('result.xlsx') #double the backslashes to avoid syntaxError
ws = wb.get_active_sheet()
for row in ws.values:
   if row != ('data_file', 'url'):
      data_file = row[0]
      url = str(row[1])
      get_cvs(data_file,url)
      get_statistics(data_file,url)