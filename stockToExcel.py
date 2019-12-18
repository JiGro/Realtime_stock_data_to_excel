import time
import locale
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Correct values for further use
def cell_2_float(cell):
    cell=cell.replace("-","")
    if (cell!=""):
        result=locale.atof(cell)
    else:
        result=0.0
    return result

# Open browser
def open_browser():
    chromeOptions = webdriver.ChromeOptions()
    adBlocker = r'C:\Users\Jimmy\AppData\Local\Google\Chrome\User Data\Default\Extensions\cfhdojbkjhnklbpkdaibdccddilifddb\3.7_0'
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument('load-extension=' + adBlocker)
    prefs = {"profile.managed_default_content_settings.images": 2}
    driver = webdriver.Chrome(executable_path=r"C:\Users\Jimmy\AppData\Local\Programs\Python\Python37\chromedriver.exe",chrome_options=chromeOptions)
    return (driver)

# Page has loaded
def page_has_loaded(driver):
    pageState = driver.execute_script('return document.readyState;')
    return pageState == 'complete'

# Wait for xpath element
def wait_for_xpath_element(driver,xpathstr):
    loaded = False
    test = (not loaded)
    trial = 0
    while not(loaded) and (trial<100):
        try:
            el = driver.find_element_by_xpath(xpathstr)
            fertig=True
        except:
            trial = trial + 1
            if (trial > 60):
                raise Exception('Timeout waiting for: ' + xpathstr)
            loaded = False
        time.sleep(1)
    return (el)

# 3.2b) Get real time stock data from boerse online "function"
def get_stock_realtime_data():
    urls = ["http://www.boerse-online.de/aktien/realtimekurse/Dow_Jones", "http://www.boerse-online.de/aktien/realtimekurse/Euro_Stoxx_50", "http://www.boerse-online.de/aktien/realtimekurse/TecDAX", "http://www.boerse-online.de/aktien/realtimekurse/SDAX", "http://www.boerse-online.de/aktien/realtimekurse/MDAX", "http://www.boerse-online.de/aktien/realtimekurse/DAX"]
    writer = pd.ExcelWriter('output.xlsx')
        for url in urls:
            StockMarket = url[49:]
            aktienIsinLst, aktienNameLst, aktienIndexLst, aktienBidLst, aktienAskLst, kursDatumLst = ([] for i in range(6))
            df = pd.DataFrame()
            print ("*** Get stock data from "+url+" ***")
            locale.setlocale(locale.LC_ALL, 'deu_deu')
            driver = open_browser()
            driver.get(url)
            cookiesXpath = '// *[ @ id = "cookie-overlay"] / div / button'
            findCookiesXpath = driver.find_element_by_xpath(cookiesXpath)
            findCookiesXpath.click()
            while not(page_has_loaded(driver)):
                time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            for row in soup.find_all("tr"):
                aktien_isin=""
                cols = row.find_all("td")
                if (len(cols) == 8):
                    stockIndex=url[49:]
                    stockName = cols[0].text.strip()
                    stockIsin = cols[1].text.strip()
                    stockBid = cell_2_float(cols[3].text)
                    stockAsk = cell_2_float(cols[4].text)
                    if (stockAsk==0.0):
                        stockAsk=cell_2_float(cols[2].text)
                    stockDatum = time.strftime("%Y-%m-%d")
                if (aktien_isin!="") and (aktien_bid>0.0):
                    print(stockIsin, stockName, stockIndex, stockBid, stockAsk, stockDatum)
                    aktienIsinLst.append(aktien_isin)
                    aktienNameLst.append(aktien_name)
                    aktienIndexLst.append(aktien_index)
                    aktienBidLst.append(aktien_bid)
                    aktienAskLst.append(aktien_ask)
                    kursDatumLst.append(kurs_datum)
            df['aktien_isin'] = aktien_isin_lst
            df['aktien_name'] = aktien_name_lst
            df['aktien_index'] = aktien_index_lst
            df['aktien_bid'] = aktien_bid_lst
            df['aktien_ask'] = aktien_ask_lst
            df['kurs_datum'] = kurs_datum_lst
            df.to_excel(writer, StockMarket)
            writer.save()
            print('DataFrame is written successfully to Excel Sheet.')
            driver.quit()

get_stock_realtime_data()
