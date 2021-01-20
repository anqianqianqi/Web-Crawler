import datetime
import requests
import toExcelCopy

#This class scrape listing prices in Beijing, HongKong, London and New York from Agoda
#Listing price will be displayed with local currency
class Agoda:
    def __init__(self,page,days_from_now,city):
        cityID = {"London": ["233","GBP"],"HongKong":["16808","HKD"],"Beijing":["1569","CNY"],"NewYork":["318","USD"],"Guangzhou":["10112","CNY"]}
        self.page = page
        self.today = datetime.date.today()
        self.checkin = str(self.today + datetime.timedelta(days=days_from_now))
        self.checkout = str(self.today + datetime.timedelta(days=(days_from_now+1)))
        self.today = str(self.today)
        self.city = city
        self.cityID = cityID[city][0]
        self.cityCurrency = cityID[city][1]
        cookies = {
            'agoda.vuser': 'UserId=0261b4da-47f7-43eb-b080-b59c4deb4712',
            'agoda.user.03': 'UserId=b732096d-b560-4941-b952-d5aa4a73b9cf',
            'agoda.prius': 'PriusID=0&PointsMaxTraffic=Agoda',
            'akamai.guid': 'ceffdcac-b8d8-4d64-9a17-ec9340df4799',
            'tealiumEnable': 'true',
            '_ab50group': 'GroupB',
            '_40-40-20Split': 'Group40B',
            '_ga': 'GA1.2.230483728.1592167963',
            '_gid': 'GA1.2.803677626.1592167963',
            '_fbp': 'fb.1.1592167962994.1954473256',
            'agoda.familyMode': 'Mode=0',
            'deviceId': '9baf9e5a-5f26-483b-a688-61730c6c2622',
            'agoda.lastclicks': '1744603||948fa426-9b1b-7d50-bc56-4a4be86624a5||2020-06-15T21:57:47||yprq4fzcjll04katdbm0jhed||{"IsPaid":true,"gclid":"","Type":""}',
            '__gads': 'ID=0df08933515d294e:T=1592234824:S=ALNI_MZ5hVKdDedNBNlnVRQZgF8RqT6T2w',
            'dc': 'wg',
            'UserSession': 'b732096d-b560-4941-b952-d5aa4a73b9cf',
            'ASP.NET_SessionId': 'khb1uawfgdmikvsylgzdb1fd',
            'agoda.firstclicks': '-1||||2020-06-16T18:54:04||khb1uawfgdmikvsylgzdb1fd||{"IsPaid":false,"gclid":"","Type":""}',
            'session_cache': '{"Cache":"as4","Time":"637279052449691242","SessionID":"khb1uawfgdmikvsylgzdb1fd","CheckID":"2e53052381fcdd994aa4c2cd8c852a05f8ec850e","CType":"N"}',
            'ak_geo': 'US',
            'agoda.banner': 'OverlayBanner=1',
            'agoda.price.01': 'PriceView=1',
            'agoda.search.01': 'SHist=4$108189$7111$1$1$2$0$0$$|4$6126$7111$1$1$2$0$0$$|4$8671$7111$1$1$2$0$0$$|3$59113$7111$1$1$2$0$0$$|1$1569$7111$1$1$2$0$0$$|3$1449450$7111$1$1$2$0$0$$|1$318$7111$1$1$2$0$0$$|1$16808$7111$1$1$2$0$0$$|1$233$7110$1$1$2$0$0$$|4$738603$7110$1$1$2$0$0$$|4$49676$7110$1$1$2$0$0$$|4$11062$7111$1$1$2$0$0$$|4$267505$7111$1$1$2$0$0$$|4$5009$7111$1$1$2$0$0$$|4$1632447$7111$1$1$2$0$0$$|4$8899251$7111$1$1$2$0$0$$|1$233$7111$1$1$2$0$0$$&H=7106|1$108189$6126$8671$738603$49676$11062|0$267505$5009$1632447$8899251',
            'agoda.attr.03': 'CookieId=5e5e42a3-3368-46db-bef9-5ddf8be67578&ATItems=1744603$06-15-2020 21:57$948fa426-9b1b-7d50-bc56-4a4be86624a5|-1$06-16-2020 18:54$|1743908$06-16-2020 20:23$',
            'agoda.landings': '-1|||khb1uawfgdmikvsylgzdb1fd|2020-06-16T18:54:04|False|19----1744603|948fa426-9b1b-7d50-bc56-4a4be86624a5||yprq4fzcjll04katdbm0jhed|2020-06-15T21:57:47|True|20----1743908|||khb1uawfgdmikvsylgzdb1fd|2020-06-16T20:23:40|False|99',
            'ABSTATIC': '1',
            'agoda.version.03': 'CookieId=b793dbbe-cc3c-4b60-aa3b-8bf0a364897b&AllocId=b6102bc8f8acc92d7a62190377c6fc11d3cc66ca8dccdd964c26e1cc51d4f9c036e2fc6194133a4826f36448d5db8a575463ab76456014d031fa37a2d0c35f5d084a0640517173f2e944e8fd675b46fa9a8ee41930b793dbbecc3cb60a3b8bf0a364897b&DLang=en-us&CurLabel='+self.cityCurrency+'&DPN=1&Alloc=&FEBuildVersion=&TItems=2$-1$06-16-2020 18:54$07-16-2020 18:54$&CulCd=&UrlV=&CuCur=2&MobSeeRed=1',
            'utag_main': 'v_id:0172b49b0a64001935be55f17c760307801390700093c$_sn:8$_se:14$_ss:0$_st:1592315916199$ses_id:1592308446018%3Bexp-session$_pn:13%3Bexp-session',
            '_uetsid': '72acabb5-c498-c921-9b34-e21555223775',
            '_uetvid': '99bd1d4e-0412-24a6-dd99-02c1311b37df',
            '_uetmsclkid': '_uet16a8a5e4a84117da9e53fb0226515b08',
            'agoda.analytics': 'Id=499719296507742098&Signature=5441335218633263491&Expiry=1592317870504',
            'PricingCookie': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJjaWQiOi0xLCJleHAiOjE1OTIzMjg2NzQsInR0bCI6MTQ0MDB9.mBSUiplG5MqeJqMB21v3id8fov-FPfoufmX3Rb7k_V9ItEBy2p5jeHzUaFoc0Xjk',
        }

        headers = {
            'authority': 'www.agoda.com',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.agoda.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.agoda.com/search?city='+self.cityID+'&checkIn=' + self.checkin +'&los=1&rooms=1&adults=2&children=0&cid=1743908&languageId=1&userId=b732096d-b560-4941-b952-d5aa4a73b9cf&sessionId=khb1uawfgdmikvsylgzdb1fd&pageTypeId=1&origin=US&locale=en-US&aid=82172&currencyCode='+self.cityCurrency+'&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=b732096d-b560-4941-b952-d5aa4a73b9cf&prid=0&checkOut='+self.checkout+'&priceCur='+self.cityCurrency+'&textToSearch='+self.city+'&travellerType=1&familyMode=off&productType=-1&sort=agodaRecommended',
            'accept-language': 'en-US,en;q=0.9',
        }
        data = '{"SearchMessageID":"e80de120-bd28-4826-ab5b-c5e727e6330e","IsPollDmc":false,"SearchType":1,"ObjectID":0,"HashId":null,"Filters":{"PriceRange":{"HasPriceFilterQueryParameter":false,"Min":0,"Max":0},"ProductType":[-1],"HotelName":""},"SelectedColumnTypes":{"ProductType":[-1]},"RateplanIDs":null,"TotalHotels":2668,"PlatformID":1001,"CurrentDate":"2020-06-16T20:31:10.5340309+07:00","SearchID":991110616203110500,"CityId":'+self.cityID+',"Latitude":0,"Longitude":0,"Radius":0,"RectangleSearchParams":null,"PageNumber":' + self.page + ',"PageSize":45,"SortOrder":1,"SortField":0,"PointsMaxProgramId":0,"PollTimes":4,"RequestedDataStatus":0,"MaxPollTimes":4,"CityName":"'+self.city+'","ObjectName":"'+self.city+'","AddressName":null,"CountryName":"United Kingdom","CountryId":107,"IsAllowYesterdaySearch":false,"CultureInfo":"en-US","CurrencyCode":"'+self.cityCurrency+'","UnavailableHotelId":0,"IsEnableAPS":false,"SelectedHotelId":0,"IsComparisonMode":false,"HasFilter":false,"LandingParameters":{"SelectedHotelId":0,"LandingCityId":0},"NewSSRSearchType":0,"IsWysiwyp":false,"RequestPriceView":1,"FinalPriceView":1,"MapType":1,"IsShowMobileAppPrice":false,"IsApsPeek":false,"IsRetina":false,"IsCriteriaDatesChanged":false,"TotalHotelsFormatted":"2,668","PreviewRoomFinalPrice":null,"ReferrerUrl":null,"CountryEnglishName":"United Kingdom","CityEnglishName":"'+self.city+'","Cid":1743908,"Tag":null,"ProductType":-1,"NumberOfBedrooms":[],"ShouldHideSoldOutProperty":false,"FamilyMode":false,"FlightSearchCriteria":{"originCode":null,"originType":null,"originText":null,"originCity":null,"destinationCode":null,"destinationType":null,"destinationText":null,"destinationCity":null,"destinationCountry":null,"departDate":null,"returnDate":null,"departDateString":null,"returnDateString":null,"occupancy":{"adults":0,"children":0,"infants":0},"searchType":null,"cabinType":0,"itineraryId":null,"token":null},"PackageToken":null,"isAgMse":false,"ccallout":false,"defdate":false,"BankCid":null,"BankClpId":null,"ShouldShowHomesFirst":false,"PropertyMatchResults":null,"RequiredPropertyMatch":false,"Adults":2,"Children":0,"Rooms":1,"MaxRooms":9,"RoomOccupancy":null,"CheckIn":"'+ self.checkin + 'T00:00:00","LengthOfStay":1,"ChildAges":[],"DefaultChildAge":8,"ChildAgesStr":null,"CheckOut":"'+self.checkout+'T00:00:00","Text":"'+self.city+'","IsDateless":false,"CheckboxType":0,"TravellerType":1}'

        response = requests.post('https://www.agoda.com/api/en-us/Main/GetSearchResultList', headers=headers,
                                 cookies=cookies, data=data)

        self.response = response


    def getTotalPages(self):
        #print(self.response.json())
        responseInJson = self.response.json()
        totalnumber = responseInJson['TotalFilteredHotels']
        numberOfHotelsOnePage = len(responseInJson['ResultList'])
        totalpages = totalnumber // numberOfHotelsOnePage + 1

        return totalpages


    def firstFetch(self):

        hotelsresult = self.response.json()['ResultList']

        hotels = []

        try:

            for i in hotelsresult:
                #item = [i['HotelID'], i['EnglishHotelName'], "https://www.agoda.com" + i['HotelUrl'], i['DisplayCurrency'], self.checkin,i['DisplayPrice']]
                item = [i['HotelID'], i['EnglishHotelName'], self.today,self.checkin, i['DisplayCurrency'], i['DisplayPrice']]
                hotels.append(item)

        except TypeError:
            print("TypeError")
            print("page number is " + self.page)

        return hotels

    def fetchAfterFirst(self,hotels):
        IDlist = []
        for item in hotels:
            ID = item[0]
            IDlist.append(ID)

        hotelsresult = self.response.json()['ResultList']

        try:

            for i in hotelsresult:
                if (i['HotelID'] in IDlist):
                    IDtoBeSearch = i['HotelID']
                    index = IDlist.index(IDtoBeSearch)
                    if ((self.checkin in hotels[index]) is False):
                        item = [self.checkin, i['DisplayCurrency'], i['DisplayPrice']]
                        hotels[index].extend(item)
                else:
                    # item = [i['HotelID'], i['EnglishHotelName'], "https://www.agoda.com" + i['HotelUrl'], i['DisplayCurrency'], self.checkin,i['DisplayPrice']]
                    item = [i['HotelID'], i['EnglishHotelName'], self.today,self.checkin, i['DisplayCurrency'], i['DisplayPrice']]
                    hotels.append(item)
        except TypeError:
            print("TypeError")
            print("page number is " + self.page)

        return hotels

    def run(self):
        LD = Agoda('1', 7, self.city)
        totalpages = LD.getTotalPages()
        print("Total pages are " + str(totalpages))
        self.hotels = []

        for page in range(totalpages):
            page = str(page+1)
            LD = Agoda(page, 7, self.city)
            hotelitem = LD.firstFetch()
            self.hotels.extend(hotelitem)

        for days in [30, 60]:
            for page in range(1, totalpages):
                page = str(page+1)
                LD = Agoda(page, days, self.city)
                self.hotels = LD.fetchAfterFirst(self.hotels)

        print("Total number of available hotels in "+ self.city + " is "+ str(len(self.hotels)))

        toExcelCopy.toExcel(self.hotels,self.city)


cities = ["London","NewYork","Beijing","HongKong"]

for city in cities:
    LD = Agoda('1', 0, city)
    LD.run()

