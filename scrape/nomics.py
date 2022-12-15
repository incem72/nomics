import requests
from bs4 import BeautifulSoup
import time
import constants
import pandas as pd
import datetime
import sys

URL = constants.url
HEADERS = constants.headers

# pip install requests
# pip install beautifulsoup4
# pip install pandas

def extract_currency_urls(page_data):
    page_tr = page_data.findAll("tr", {"class": "bb b--black-10 bn-last-tr n-table-ph n-bg-table-row tp-bc td-1 dash-row-visibility"})
    list_urls=[]

    for i in page_tr:
        dic_url={}
        url = "https://nomics.com" + i.find("a")["href"]
        if url:
            dic_url = {"url":url}
            list_urls.append(dic_url)
        else:
            print("Some error on :")
            print(i)
            continue

    return list_urls

def extract_data_points(soup, dict):
    dict["about_currency"] =""
    dict["Currency_Name"] = ""
    dict["Symbol"] = ""
    dict["Contract_Address"] = ""
    dict["Website"] = ""
    dict["Whitepaper"] = ""
    dict["Symbol"] = ""
    dict["Block_Explorer"] = ""
    dict["Github"] = ""
    dict["Twitter"] = ""
    dict["Facebook"] = ""
    dict["Reddit"] = ""
    dict["Telegram"] = ""
    dict["Discord"] = ""
    dict["BitcoinTalk"] = ""
    dict["Medium"] = ""
    dict["Blog"] = ""
    dict["Youtube"] = ""
    dict["LinkedIn"] = ""

    overview = soup.find("div",{"class":"overview_about__t1xA4"})

    if overview:
        overview_about = overview.find("div",{"class":"relative"})

        if overview_about:
            #Check and get text if exist

            #about_currency = overview_about.find("div",{"class":"flex flex-column n-flex-row-540 flex-row-l justify-between relative w-100 n-pv18 n-ph18 n-pt18-l n-pb30-l n-ph30-l n-gray lh-copy f5"})

            overview_about_p = overview_about.findAll("p",{"class":"n-mt12 n-mb18"})

            if overview_about_p:
                about_currency =""

                for p in overview_about_p:
                    about_currency = about_currency + p.text.replace("\n", "").replace("\r", " ")

                dict["about_currency"] = about_currency

            #get curency details
            details_ul = overview_about.find("ul").findAll("li")

            if details_ul:
                for li in details_ul:
                    title = li.find("div", {"class":"f6 fw5 self-start w-25 n-ph0 n-dark-gray"}).text.replace("\n", "")
                    value = li.find("div", {"class":"f6 f5-ns fw3 n-gray self-end self-start-ns w-75 n-ph12"}).text.replace("\n", "")
                    if title and value:
                        if title == "Currency Name":
                            dict["Currency_Name"] = value
                        elif title == "Symbol":
                            dict["Symbol"] = value
                        elif title == "Contract Address":
                            dict["Contract_Address"] = value
                        elif title == "Website":
                            dict["Website"] = value
                        elif title == "Whitepaper":
                            dict["Whitepaper"] = value
                        elif title == "Symbol":
                            dict["Symbol"] = value
                        elif title == "Block Explorer":
                            dict["Block_Explorer"] = value
                        elif title == "Github":
                            dict["Github"] = value
                        elif title == "Twitter":
                            dict["Twitter"] = value
                        elif title == "Facebook":
                            dict["Facebook"] = value
                        elif title == "Reddit":
                            dict["Reddit"] = value
                        elif title == "Telegram":
                            dict["Telegram"] = value
                        elif title == "Discord":
                            dict["Discord"] = value
                        elif title == "BitcoinTalk":
                            dict["BitcoinTalk"] = value
                        elif title == "Medium":
                            dict["Medium"] = value
                        elif title == "Blog":
                            dict["Blog"] = value
                        elif title == "Youtube":
                            dict["Youtube"] = value
                        elif title == "LinkedIn":
                            dict["LinkedIn"] = value
                        # else:
                        #     print("***********************")
                        #     print ("WARNING ! Unmatched Title...:", title, " - ", value )
                        #     print("***********************")


    return dict

list_output = []
for page_num in range(1,2):

    # if page_num>1:
    #     time.sleep(30)

    data = []
    new_url = URL + "?page=" + str(page_num)
    try:
        print("URL :", new_url)
        print("--------------------------------------------")

        r = requests.get(new_url, headers=HEADERS)
        if not r.status_code == 200:
            print(f"Status code: {r.status_code} - {URL}")

        soup = BeautifulSoup(r.text, 'html.parser')


        page_data = soup.find("div", {"class": "n-ph18-ns n-ph30-l n-ph0-xl"}
                      ).find("table", {"class": "w-100"}
                             ).find("tbody", {"class": "f7-s"})

        currency_urls = []
        currency_urls = extract_currency_urls(page_data)

        for currency_url in currency_urls:
            #*********************
            #time.sleep(3)
            #*********************

            dict_crawled ={}
            # Extracting Data Points
            r_datapoints = requests.get(currency_url["url"], headers=HEADERS)
            if not r_datapoints.status_code == 200:
                print(f"Status code: {r_datapoints.status_code} - {currency_url['url']}")


            soup_datapoints = BeautifulSoup(r_datapoints.text, 'html.parser')

            if soup_datapoints:
                dict_crawled = extract_data_points(soup_datapoints, dict_crawled)

                if dict_crawled:
                    list_output.append(dict_crawled)

    except:
        print("*********************** Excepption *********************** : ", currency_url)
        print("excepppp!", sys.exc_info())
        print("excepppp!", sys.exc_info()[0], ".......")
        print("excepppp!", sys.exc_info()[1], ".......")
        break

day_mont_year = datetime.datetime.now()
day = day_mont_year.day
month = day_mont_year.month
year = day_mont_year.year

df = pd.DataFrame(list_output)
df.to_csv(f"{day}_{month}_{year}_nomics.csv", index=False)

# *****************************
# SINGLE URL TESTING...
# *****************************
# list_output = []
# dict_crawled ={}
# r_datapoints = requests.get("https://nomics.com/assets/usdd2-usdd", headers=HEADERS)
# soup_datapoints = BeautifulSoup(r_datapoints.text, 'html.parser')
# dict_crawled = extract_data_points(soup_datapoints, dict_crawled)
# print(dict_crawled)
#
# list_output.append(dict_crawled)
# df = pd.DataFrame(list_output)
# df.to_csv("xxx.csv", index=False)
