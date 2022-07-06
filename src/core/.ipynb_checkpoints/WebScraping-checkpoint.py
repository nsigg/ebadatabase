from bs4 import BeautifulSoup
import requests as req
import re
import datetime

def start_extraction(year = datetime.datetime.now().year):
    data_l = ["Credit risk", "Market risk", "Sovereign debt exposures", "Other templates", "Data dictionary", "Metadata"]
    soup = scrape_page(year)
    soup = soup.find_all("ul", {"class": "CrossLinks"})
    soup = soup[1]
    for tag in soup.find_all("a"):
            tag_t = tag.text
            if tag_t in data_l:
                print(tag_t)
                get_data(tag)
                

def scrape_page(year):
    year  = str(year)
    url = f"https://www.eba.europa.eu/risk-analysis-and-data/eu-wide-transparency-exercise/{year}"
    print(url)
    resp = req.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup
              
#Diese Funktion filtert nach den gewünschten Daten und führt die anderen Funtionen aus.
def get_data(tag):
    href_t = tag.attrs["href"]
    if href_t.__contains__(".csv") or href_t.__contains__(".xlsx"):
        url = write_url(href_t)
        f_name = getName(href_t)
        download_data(url, f_name)
        
    return href_t

#Diese Funktion erstellt aus dem Inhalten des Tags eine URL für den Download
def write_url(href):
    if href.__contains__("https:"):
        url = href
    else:
        url = "https://www.eba.europa.eu"+href
    return url

#Diese Frunktion läd die Daten von den Links herunter und speichert sie ab. 
def download_data(url, f_name):
    request = req.get(url)
    
    with open("data/RawData/"+f_name, 'wb') as f:
        f.write(request.content) 

#Diese Funktion legt die Namen für die Files fest. 
def getName(href_t):
    if href_t.__contains__("tr_cre"):
        name = "tr_cre.csv"
    elif href_t.__contains__("tr_mrk"):
        name = "tr_mrk.csv"
    elif href_t.__contains__("tr_oth"):
        name = "tr_oth.csv"
    elif href_t.__contains__("SDD"):
        name = "sdd.xlsx"
    elif href_t.__contains__("TR_Metadata"):
        name = "banks.xlsx"
    elif href_t.__contains__("tr_sov"):
        name = "tr_sov.csv"
    else:
        name ="no_name"
    return name