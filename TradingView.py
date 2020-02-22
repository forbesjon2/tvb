from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.keys import Keys


class TradingView:
    def __init__(self):
        pass
    def csvToList(self):
        """
        Reads zacks custom screen csv and returns it as a list
        """
        dataFrame = pd.read_csv("zacks_custom_screen.csv")
        res = []
        for item in dataFrame:
            res.append(item)
        return res


    def initialize(self, username, password):
        """
        Signs you in, opens the main chart, will return an instance of chromedriver
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        driver = webdriver.Chrome(options=options)
        driver.get('https://tradingview.com/#signin')
        
        # sign in, open chart
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_class_name("tv-button--loader").click()
        time.sleep(2)
        driver.get("https://www.tradingview.com/chart/G3QqB8yo/")
        time.sleep(3)
        return driver


    def changeStock(self, driver, stockName):
        """
        changes current stock to a different one
        """
        for i in range(0,20):
            driver.find_element_by_class_name("input-3lfOzLDc").send_keys(Keys.BACK_SPACE)
        driver.find_element_by_class_name("input-3lfOzLDc").send_keys(stockName)
        driver.find_element_by_class_name("input-3lfOzLDc").send_keys(Keys.ENTER)
        time.sleep(1)

    def changeDate(self, driver, dateID):
        """
        changes the time interval to any of the following

        30 minutes (index 0)
        45 minutes (index 1)
        1 hour (index 2)
        2 hours (index 3)
        3 hours (index 4)
        4 hours (index 5)
        1 day (index 6)
        """
        dateID += 4
        driver.find_element_by_id("header-toolbar-intervals").click()
        time.sleep(1)
        dropdowns = driver.find_elements_by_class_name("item-2xPVYue0")
        dropdowns[dateID].click()
        time.sleep(1)

    def saveBacktest(self, name, stock, driver, dateID):
        """
        saves backtest results in a dictionary. Returns a pandas dataframe with the following properties

        params:
        name = <script name>
        driver = instance of chromeDriver
        dateID: 0-6
        """
        dateDict = {0:"30m", 1:"45m", 2:"1h", 3:"2h", 4:"3h", 5:"4h",6:"1d"}
        interval = dateDict[dateID]
        content = {"Name":[name, name, name], "Stock":[stock, stock, stock],"Time Interval":[interval, interval, interval], "Type":["All", "Long", "Short"], 
            "Net Profit":[], "Gross Profit":[], "Gross Loss":[], "Max Drawdown":[], "Buy & Hold Return":[], "Sharpe Ratio":[], 
            "Profit Factor":[], "Max Contracts Held":[], "Open PL":[], "Commission Paid":[], "Total Closed Trades":[], "Total Open Trades":[],
            "Number Winning Trades":[], "Number Losing Trades":[], "Percent Profitable":[], "Avg Trade":[], "Avg Win Trade":[], "Avg Los Trade":[],
            "Ratio Avg Win / Avg Loss":[], "Largest Win Trade":[], "Largest Losing Trade":[], "Avg # Bars in Trades":[], "Avg # Bars in Winning Trades":[], 
            "Avg # Bars in Losing Trades":[]}
        htmlContent = driver.find_element_by_class_name("report-data").get_attribute('innerHTML')
        keys = list(content)
        soups = BeautifulSoup(htmlContent, features="lxml")
        table = soups.find("table")
        contentIndex = ""
        contentIndexCount = 3
        contentIndex = str(keys[contentIndexCount])

        for row in table.find_all('tr')[1:]:
            col = row.find_all('td')
            for i in col:
                percent = i.find("span",{"class":"additional_percent_value"})
                if percent is not None and len(content[contentIndex]) < 3:
                    negative = len(percent.find_all({"span":{"class":"neg"}})) > 0
                    percent = re.sub(r'[^0-9\.]',"", percent.string)
                    if(negative):
                        content[contentIndex].append("-" + percent)
                    else:
                        content[contentIndex].append(percent)
                else:
                    if i.string in content or len(content[contentIndex]) > 3:
                        while len(content[contentIndex]) < 3:
                            content[contentIndex].append(str(content[contentIndex][0]))
                        contentIndexCount += 1
                        contentIndex = str(keys[contentIndexCount])
                    else:
                        if i.string is not None:
                            content[contentIndex].append(re.sub(r'[^0-9\.]',"", i.string))
                        else:
                            content[contentIndex].append("")
        return pd.DataFrame(content, index=[0,1,2])

