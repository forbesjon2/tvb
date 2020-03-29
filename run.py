from selenium import webdriver
from TradingView import TradingView as tv
import pandas as pd
import re
import os


########### You need to change username & password ###############
###########  to your accounts username & password  ###############
username = "markermal3@gmail.com"
password = "8!zc4rmAtSDcjBx"
#username = "forbesjon2@gmail.com"
#password = "giXky6-caqnuj-bebdas"
########## Dont touch anything below this line  ##################


scriptName = input("whats the name of the script that youre testing (keep it short): ")

#initialization
tv = tv()
stockList = tv.csvToList()
driver = tv.initialize(username, password)
df = pd.DataFrame()
skts = re.sub(r'[^A-Z]','',input("skip to stock (leave blank if N/A): "))

dateDict = {0:"30m", 1:"45m", 2:"1h", 3:"2h", 4:"3h", 5:"4h",6:"1d"}
print("this might take a while...")


def logic(stock, skts, driver, df):
    tv.changeStock(driver, stock)
    for i in range(0,6):
        tv.changeDate(driver, i)
        dictt = tv.saveBacktest(scriptName, stock, driver, i)
        df = pd.concat([dictt, df])
    return df

# for each stock
for stock in stockList:
    if len(skts) != 0:
        if skts != re.sub(r'[^A-Z]','', stock):
            print("skipping " + str(stock))
            continue
        else:
            skts = ""
    try:
        df = logic(stock, skts, driver, df)
        print("updating output.csv")
        try:
            os.remove("output.xlsx")
        except:
            pass
        df.to_excel("output.xlsx")
    except:
        print("error at " + str(stock))
driver.close()

