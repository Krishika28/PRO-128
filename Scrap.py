from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import requests


url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("./chromeDriver/chromedriver")
browser.get(url)
time.sleep(15)

stars_data = []
new_stars_data = []

def scraper():

    headers = ["Name","Distance","Mass","Radius","Hyperlink"]

    stars_data = []

    soup = BeautifulSoup(browser.page_source, "html.parser" )    
    star_table = soup.find("table")
    rows = star_table.find_all("tr")

    for i in rows:
        td = i.find_all("td")
        stars_data.append([j.text.rstrip() for j in td ])
    
    print(stars_data[0:5])
    name = []
    distance = []
    mass = []
    radius = []
    
    for i in range(1,len(stars_data)):
        name.append(stars_data[i][1])
        distance.append(stars_data[i][3])
        mass.append(stars_data[i][5])
        radius.append(stars_data[i][6])
  
    df = pd.DataFrame(list(zip(name, distance, mass, radius)), columns = headers)
    df.to_csv("stars.csv")
    
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(browser.page_source, "html.parser" )
        temp_list = []

        for tr_row in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_row.find_all("td")
            for td in td_tags:
                try:
                    temp_list.append(td.find_all("div", attrs={"class": "values"})[0].contents[0])
                except: 
                    temp_list.append("")

        new_stars_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scraper()

for index,data in enumerate(stars_data):
        scrape_more_data(data[5])

        
final_data = []
for index,data in enumerate(stars_data):
    new_stars_element = new_stars_data[index]
    new_stars_element = [i.replace("\n", "") for i in new_stars_element]
    new_stars_element = new_stars_element[:7]
    final_data.append(data+new_stars_element)