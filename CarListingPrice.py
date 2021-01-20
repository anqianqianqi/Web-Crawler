#author: Anqi Luo
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import re

#This class scrape car listings from the website of CarGurus, which uses Json file to store data
class Cargurus:
	
	#initialize class member data from the user input
    def __init__(self,zipcode,distance,year,mileage,make):
        self.zipcode = zipcode
        self.distance = distance
        self.year = year
        self.mileage = mileage
        self.make = make
        self.baby_urls = set()

	# construct url with user input
    def getBaseUrl(self):
        return"https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?"\
            "zip={0}&inventorySearchWidgetType=PRICE&maxMileage={1}&showNegotiable=true&sortDir=ASC&sourceContext=cargurus&"\
            "distance={2}&minPrice=0&sortType=PRICE&startYear={3}".format(self.zipcode,self.mileage,self.distance,self.year)
	
	#get all detail page/url of the listing cars 
    def getBaby(self, url):
        headers = ({'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
            /537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        page = requests.get(url,headers = headers)
        soup = BS(page.text, 'html.parser')
        content_list = soup.find_all('a')
        baby_urls = set()
        for line in content_list:
            line = line.get('href')
            pattern = '#listing'
            result = re.match(pattern,line)
            if result:
                ls = line.split("=")
                ls = ls[1].split("_")
                ls = ls[0]
                baby_urls.add(ls)
        return baby_urls
	
	#open details pages and scrape car info
    def getDetails(self,baby,result):
        url = 'https://www.cargurus.com/Cars/detailListingJson.action?inventoryListing={0}&searchZip={1}&searchDistance={2}&inclusionType=undefined'.format(
           baby,self.zipcode,self.distance )
        headers = ({'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
            /537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        page = requests.get(url, headers=headers)
        soup = page.json()["listing"]
        rIndex,cIndex = result.shape
        for key, value in soup.items():
            try:
                result.loc[rIndex,key] = value
            except:
                if len(value) ==1:
                    result.insert(column=key,loc=rIndex,value = value)
        result.loc[rIndex,"Web"] = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?#listing={0}_isFeatured".format(baby)
        result.loc[rIndex, "WebName"] = "CarGurus"
        
    #run all scrapping functions in this class and reshape data in a desirable dataframe
    def run(self):
        instance = Cargurus(self.zipcode, self.distance,self.year,self.mileage,self.make)
        url = instance.getBaseUrl()
        for i in range(1, 10):
            self.baby_urls.update(instance.getBaby((url + str(i))))
        result = pd.DataFrame(columns=["Web","WebName"])

        for baby in self.baby_urls:
            instance.getDetails(baby, result)
        r1 = result[result.makeName.eq(self.make)]
        r2 = r1.loc[:,["WebName","year","makeName","modelName","postalCode","mileageString","vin","price","localizedExteriorColor","localizedInteriorColor","localizedTransmission","localizedDriveTrain","localizedFuelType","description","Web"]]
        r2 = r2.rename(columns={"year":"Year","makeName":"Brand","modelName":"Model","postalCode":"Location","vin":"VIN","price":"Price","localizedExteriorColor":"Exterior Color","localizedInteriorColor":"Interior Color","localizedTransmission":"Transmission","localizedDriveTrain":"Drive Type","localizedFuelType":"Fuel Type","description":"Other Features","Web":"Website Link","mileageString":"Mileage","WebName":"Website Name"})
        zipcode = r2.loc[:, "Location"]
        for i,j in zip(r2.index.values,range(len(zipcode))):
            r2.loc[i, "Location"] = instance.getlocation(zipcode.iloc[j])
        price_sort = r2.loc[:,"Price"].sort_values(ascending=True)
        if len(price_sort) > 10:
            price_sort_index = price_sort[:10].index.values
        else:
            price_sort_index = price_sort.index.values
        r3 = r2.loc[price_sort_index]
        return r3
	
	#translate zipcode into its corresponding city and state
    def getlocation(self,zipcode):
        headers = ({
            'User-Agent': 'Catalina/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        web_url = "https://www.unitedstateszipcodes.org/" + str(zipcode) + "/"
        html_text = requests.get(web_url, headers=headers)
        b_soup = BS(html_text.text, 'html.parser')
        city_state = b_soup.find('dl', attrs={'class': 'dl-horizontal'})
        if city_state:
            city_state = b_soup.find('dl', attrs={'class': 'dl-horizontal'}).text.split("\n")[2]
            return city_state
        return None




