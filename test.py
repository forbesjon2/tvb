from selenium import webdriver
from TradingView import TradingView as tv
import pandas as pd
import os


########### You need to change username & password ###############
###########  to your accounts username & password  ###############
username = "example username"
password = "example password"
########## Dont touch anything below this line  ##################


scriptName = input("whats the name of the script that youre testing (keep it short): ")

#initialization
tv = tv()
stockList = tv.csvToList()
driver = tv.initialize(username, password)
df = pd.DataFrame()

dateDict = {0:"30m", 1:"45m", 2:"1h", 3:"2h", 4:"3h", 5:"4h",6:"1d"}
print("this might take a while...")

# for each stock
for stock in stockList:
    tv.changeStock(driver, stock)
    for i in range(0,6):
        tv.changeDate(driver, i)
        dictt = tv.saveBacktest(scriptName, stock, driver, i)
        df = pd.concat([dictt, df])
    print("updating output.csv")
    try:
        os.remove("output.xlsx")
    except:
        pass
    df.to_excel("output.xlsx")
driver.close()

