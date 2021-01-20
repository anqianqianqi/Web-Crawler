# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 10:47:33 2019

@author: Angel A Luo
"""

import requests # Python 3.6
import json
import pandas as pd
import os
import xlsxwriter
from openpyxl import load_workbook
import numpy as np
os.chdir(r"C:\Users\Angel A Luo\Desktop\test")

def get_database_id():
    url_dataflow = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    key = 'Dataflow'  
    series_list = requests.get(f'{url_dataflow}{key}').json()\
            ['Structure']['Dataflows']['Dataflow']
    Database_ID = []
    for series in series_list:
        Database_ID.append((f"{series['KeyFamilyRef']['KeyFamilyID']}"))
    return Database_ID

def get_compactdata_links_by_country(database_ID):
    url_dataset = "http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/"
    structure = requests.get(f'{url_dataset}{database_ID}').json()\
            ['Structure']['KeyFamilies']['KeyFamily']\
            ['Components']['Dimension']
    All_Dimension_ID = []        
    for dimension in structure:
        #print(dimension['@codelist'],dimension['@conceptRef'])
        All_Dimension_ID.append(dimension['@codelist'])
    #Find the codes for each dimensions
    url_codelist ='http://dataservices.imf.org/REST/SDMX_JSON.svc/CodeList/'
    indicator_list = requests.get(f'{url_codelist}{All_Dimension_ID[2]}').json()\
        	    ['Structure']['CodeLists']['CodeList']['Code']
    indicators = []
    for indi in indicator_list:
        indicators.append(indi['@value'])
    code_list = requests.get(f'{url_codelist}{All_Dimension_ID[1]}').json()\
        	    ['Structure']['CodeLists']['CodeList']['Code']
    country_ID = []
    country_ref = []
    for code in code_list:
            #print(code['Description']['#text'],code['@value'])
        country_ID.append(code['@value'])
        country_ref.append(code['Description']['#text'])
    url_get = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/'
    url_country = []
    for area in country_ID:
            url_country.append(f'{url_get}{database_ID}/M.{area}')
    return {"url_country":url_country,"indicators":indicators,"country_ref": country_ref}

def run_compactdata_links(url_country):
    all_indi = []
    for i in range(len(indicators)):
        all_indi.append([])
    for url in url_country:
        try:
            page = requests.get(url).json()['CompactData']['DataSet']['Series']
            df = pd.DataFrame(page)
            indicator_values = list(df['@INDICATOR'].values)
            for indi in indicator_values:
                index = indicators.index(indi)
                index1 = indicator_values.index(indi)
                element = [df['@REF_AREA'].values[index1],df['Obs'].values[index1]]
                all_indi[index].append(element)
        except:
            pass
    return all_indi

def create_excel(indicators,all_indi,database_ID):   
    for i in range(len(all_indi)):#goes into indicators
        for j in range(len(all_indi[i])): #going into country
            try: #vecasue some data looks like ["countryID",nan]     
                for z in range(len(all_indi[i][j][1])):
                    try:
                        all_indi[i][j][1][z].update({'country': all_indi[i][j][0]})
                    except:
                        pass
            except:
                pass
    for i in range(len(all_indi)):
        combine = []
        for j in range(len(all_indi[i])): 
            try:
                if type(all_indi[i][j][1]) is list:
                    combine.extend(all_indi[i][j][1])
            except:
                pass
        #writer = pd.ExcelWriter(f'r"C:\Users\Angel A Luo\Desktop\test\.xlsx", engine = 'xlsxwriter')
        df = pd.DataFrame(combine)
        df.to_excel(f'{database_ID}_{indicators[i]}_monthly.xlsx', sheet_name='data', index=False)
        #df.to_excel(writer, sheet_name = indicators[i])
    #writer.save()
    #writer.close()
    return


#dfall = pd.DataFrame(all_indi) 
#dfall.to_excel('monthly.xlsx')
database_ID = get_database_id()            
result = get_compactdata_links_by_country('PCTOT')
url_country = result["url_country"]
indicators = result['indicators']
country_ref = result['country_ref']         
all_indi = run_compactdata_links(url_country)
create_excel(indicators,all_indi,database_ID)              


test = ['http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/M.1C_440',
 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/M.1C_NANSA',
 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/M.1C_NASA','http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/M.AF',
 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/M.AL']
all_indi = run_compactdata_links(test)




