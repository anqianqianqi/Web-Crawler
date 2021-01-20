#@Author: Anqi Luo
import requests
from bs4 import BeautifulSoup as BS
import re

url = 'https://www.censtatd.gov.hk/hkstat/quicklink/index.jsp'
html = "https://www.censtatd.gov.hk"

#get all the directory link in the homepage
def get_link_first_step(url):
    page = requests.get(url)
    soup = BS(page.content, 'html.parser')
    html = "https://www.censtatd.gov.hk"
    pattern = '^/hkstat/'
    link_first_step = []
    for link in soup.find_all('li'):
        for link1 in link.find_all('a'):
            object = link1.get('href')
            result = re.match(pattern,object)
            if result:
                link_first_step.append(html+object)
    return link_first_step

#extract the accompany files in one html
#based on two types of web interfaces, see the attached text file for further indications

def get_accompany_files1(url):
    page = requests.get(url)
    soup = BS(page.content, 'html.parser')
    link_second_step = []
    class_ = ["productaccompanyfiles","producttitle"] #both title and accompany files share the same links
    if soup.find_all('div',{"class":class_[0]}) != []: #we see the accompany files as priority
        target = soup.find_all('div', {"class": class_[0]})
    else:
        target = soup.find_all('div', {"class": class_[1]})
    html = "https://www.censtatd.gov.hk"
    for targets in target:
        for name in targets.find_all('a'):
            result = name.get('href')
            link_second_step.append(html + result)
    if not link_second_step:
        return
    else:
        return link_second_step




def get_accompany_files2_excel(url):
    page = requests.get(url)
    soup = BS(page.content, 'html.parser')
    link_second_step = []
    target = soup.find_all('a', attrs={'id': 'downExcel'})
    html = "https://www.censtatd.gov.hk"
    for targets in target:
        result = targets.get('href')
        link_second_step.append(html + result)
    return link_second_step

def get_accompany_files2_cvs(url):
    page = requests.get(url)
    soup = BS(page.content, 'html.parser')
    link_second_step = []
    target = soup.find_all('a', attrs={'id': 'downcsv'})
    html = "https://www.censtatd.gov.hk"
    for targets in target:
        result = targets.get('href')
        link_second_step.append(html + result)
    if not link_second_step:
        return
    else:
        return link_second_step

#get the names of the files
def get_names(url):
    page = requests.get(url)
    soup = BS(page.content, 'html.parser')
    target = soup.find_all('div', {"id": "cam2A"})
    sub_target = soup.find_all('div',{"class":"productaccompanyfiles"})
    name =[]
    for targets in target:
        for result in targets.find_all('h2'):
            title = result.get_text()
    if sub_target != []:
        for sub_targets in sub_target:
            for result in sub_targets.find_all('a'):
                name.append(title + " - " + result.get_text())
    else:
        name.append(title)
    return name


def get_everything(url):
    master_links = []
    master_names = []
    link_first_step = get_link_first_step(url)
    for i in link_first_step:
        if get_accompany_files1(i) is not None:
            master_links.extend(get_accompany_files1(i))
            master_names.extend(get_names(i))
        if get_accompany_files2_cvs(i) is not None:
            master_links.extend(get_accompany_files2_cvs(i))
            master_names.extend(get_names(i))
    return master_links, master_names

#store links in an excel file
from pandas import DataFrame
def store_in_excel(master_names,master_links):
    df = DataFrame({'Title': master_names, 'Links': master_links})
    df.to_excel('links_from_Census_and_Statistics_Department.xlsx', sheet_name='url', index=False)
    return

#f= open("result.txt","w+")
#f.write(soup.prettify())
#f.close()
