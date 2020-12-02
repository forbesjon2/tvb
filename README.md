# About
The purpose of this was, instead of learning pinescript & wrtiting my own script, scraping & recording the performance of some of the many public scripts listed on tradingview. The goal is to find a script that can provide relatively accurate & profitable stock alerts based on its past performance. I ended up with some decent candidates but [the ability for scripts to repaint](https://youtu.be/dAzhR0Ve3PI) made things more difficult in finding whether or not a particular script should work or not. I stopped near the end where I was going to manually track some scripts and measure them up against the backtests. 

*about allScripts.py*
Tradingview has a feature where people can upload their own buy / sell strategies written in pinescript. This code can scrape the [individual performance metrics](https://www.tradingview.com/script/G228N3DK-Sequential-Up-Down/) (see the sequential up/down report section) for the [scripts listed on a search page](https://www.tradingview.com/scripts/search/SEQUENTIAL) with only   [a part of the URL path](https://github.com/forbesjon2/tvb/blob/4b396261535737442b93595b808e02bc3d7cd7c7/allScripts.py#L42) provided in a list in allScripts.py. 

*about main.py*
Once you find a few good candidates in the results from allScripts.py (filter out the fake ones, read the comments), the next step is to get a list of stocks that you want to test this against. A good script should perform well regardless of the ticker / time or well in some & decent in others. The list I used is in zacks_custom_screen.csv. [This is what it's getting the performance data from](https://backtest-rookies.com/wp-content/uploads/2018/07/Performance-Summary.png). 



# Getting started
download python

## 1. Add chromedriver to path

#### Download chromedriver
https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/

once downloaded, place it in the parent directory

#### Run command
```bash 
export PYTHONPATH="../"
```


## 2. add username and password where directed in run.py


## 3. Run the following command
```bash
pip3 install -r requirements.txt
```

## 4. run the program
```bash
python3 run.py
```
