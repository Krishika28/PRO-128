from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import requests


url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("./chromeDriver/chromedriver")
browser.get(url)
time.sleep(15)

def scraper():

    headers = ["Name","Distance","Mass","Radius"]

    stars_data = []

    soup = BeautifulSoup(browser.page_source, "html.parser" )    
    star_table = soup.find("table")
    rows = star_table.find_all("tr")

    for i in rows:
        td = i.find_all("td")
        stars_data.append([j.text.rstrip() for j in td ])
    
    name = []
    distance = []
    mass = []
    radius = []
    
    for i in range(1,len(stars_data)):
        name.append(stars_data[i][0])
        distance.append(stars_data[i][5])
        mass.append(stars_data[i][8])
        radius.append(stars_data[i][9])
  
    df = pd.DataFrame(list(zip(name, distance, mass, radius)), columns = headers)
    df.to_csv("dwarfs_stars.csv")
    
scraper()
