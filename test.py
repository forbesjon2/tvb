from selenium import webdriver
from TradingView import TradingView as tv
import pandas as pd
import os


scriptName = input("whats the name of the script that youre testing (keep it short): ")

#initialization
tv = tv()
stockList = tv.csvToList()
driver = tv.initialize()
df = pd.DataFrame()

dateDict = {0:"30m", 1:"45m", 2:"1h", 3:"2h", 4:"3h", 5:"4h",6:"1d"}

count = 1
# for each stock
for stock in stockList:
    if count == 0:
        break
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
    count -= 1
driver.close()

