from selenium import webdriver
import pandas as pd
import time
import locale
from bs4 import BeautifulSoup

def open_browser():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=r"C:\Users\Jimmy\AppData\Local\Programs\Python\Python37\chromedriver.exe",chrome_options=chromeOptions)
    return (driver)

def page_status(driver):
    pageStatus = driver.execute_script('return document.readyState;')
    return pageStatus == 'complete'

def wait_for_xpath(driver,xpath):
    loaded = True
    i = 0
    while loaded and i<100:
        try:
            el = driver.find_element_by_xpath(xpath)
        except:
            i += 1
            if (i > 50):
                raise Exception('Timeout waiting for: ' + xpath)
            loaded = False
        time.sleep(1)
    return el

# Get real time stock data from boerse online
def get_stock_realtime_data():
    urls = ["http://www.boerse-online.de/aktien/realtimekurse/Dow_Jones", "http://www.boerse-online.de/aktien/realtimekurse/Euro_Stoxx_50", "http://www.boerse-online.de/aktien/realtimekurse/TecDAX", "http://www.boerse-online.de/aktien/realtimekurse/SDAX", "http://www.boerse-online.de/aktien/realtimekurse/MDAX", "http://www.boerse-online.de/aktien/realtimekurse/DAX"]
    writer = pd.ExcelWriter('output.xlsx')
    for url in urls:
        StockMarket = url[49:]
        stockIsinLst, stockNameLst, stockIndexLst, stockBidLst, stockAskLst, stockDateLst = ([] for i in range(6))
        df = pd.DataFrame()
        print ("*** Get stock data from "+url+" ***")
        locale.setlocale(locale.LC_ALL, 'deu_deu')
        driver = open_browser()
        driver.get(url)
        while not(page_status(driver)):
            time.sleep(1)
        findCookiesXpath = driver.find_element_by_xpath('// *[ @ id = "cookie-overlay"] / div / button')
        findCookiesXpath.click()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for row in soup.find_all("tr"):
            stockIsin=""
            cols = row.find_all("td")
            if (len(cols) == 8):
                stockIndex=url[49:]
                stockName = cols[0].text.strip()
                stockIsin = cols[1].text.strip()
                stockBid = float(cols[3].text.strip().replace(',','.'))
                stockAsk = float(cols[4].text.strip().replace(',','.'))
                if (stockAsk == '0.0'):
                    stockAsk = float(cols[2].text.strip().replace(',','.'))
                stockDate = time.strftime("%Y-%m-%d")
            if (stockIsin!="") and (stockBid > 0.0):
                print(stockIsin, stockName, stockIndex, stockBid, stockAsk, stockDate)
                stockIsinLst.append(stockIsin)
                stockNameLst.append(stockName)
                stockIndexLst.append(stockIndex)
                stockBidLst.append(stockBid)
                stockAskLst.append(stockAsk)
                stockDateLst.append(stockDate)
        df['aktien_isin'] = stockIsinLst
        df['aktien_name'] = stockNameLst
        df['aktien_index'] = stockIndexLst
        df['aktien_bid'] = stockBidLst
        df['aktien_ask'] = stockAskLst
        df['kurs_date'] = stockDateLst
        df.to_excel(writer, StockMarket)
        writer.save()
        if df.empty:
            print('Layout has changed, please check.')
        else:
            print('DataFrame is written successfully to Excel Sheet.')
        driver.quit()

get_stock_realtime_data()
print('***Finished***')
