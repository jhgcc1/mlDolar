from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datas import get_dates
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import datetime
import re
import csv
import requests

def getData(NumberOfyears,whatToconsider):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options,executable_path=r'C:\Users\jh_gc\Desktop\doalr\chromedriver.exe')

    driver.get("https://www.investing.com/")
    dictall={"dxy": ["942611", "2067751", "US Dollar Index Historical Data"],"brent": ['8830','300004', 'Gold Futures Historical Data'],'gold': ['8833','300028', 'Brent Oil Futures Historical Data'],'bovespa': ['17920','2036142','Bovespa Historical Data'],'vix': ['44336', '2059974', 'CBOE Volatility Index Historical Data' ],'usd_jpy': ['3','106684', 'USD/JPY Historical Data'],'usd_cny':['2111','107259','USD/CNY Historical Data'],'usd_cop': ['2112','107260','USD/COP Historical Data'],'usd_mxn': ['39', '106701', 'USD/MXN Historical Data'],'usd_brl': ['2103', '107254', 'USD/BRL Historical Data']}
    

    initialDate, finalDate,dateRange = get_dates(NumberOfyears,"/")
    print(dateRange)
    print("dtae range")
    dataframe=pd.DataFrame()
    #tempDict={}
    for key in dictall:
        if key in whatToconsider:
            
            js_command_one = """$('body').html('')"""
            driver.execute_script(js_command_one)
            curr_id=dictall[key][0]
            smlID=dictall[key][1]
            header=dictall[key][2]
            # Request the data
            js_command_two = '$.ajax({type: "POST",url: "https://www.investing.com/instruments/HistoricalDataAjax",data: { "curr_id":'+curr_id+', "smlID":'+ smlID+', "header": "'+header+'", "st_date": "'+initialDate+'", "end_date": "'+finalDate+'", "interval_sec": "Daily", "sort_col": "date", "sort_ord": "DESC", "action": "historical_data" },success: function(dataString) {$("body").append(dataString);}});'
            driver.execute_script(js_command_two)
            wait = WebDriverWait(driver, 60)
            # Wait for the table to show up
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#curr_table')))
            soup=BeautifulSoup(driver.page_source,'html.parser')

            closePrices = soup.select("#curr_table tbody tr td:nth-of-type(2)")
            closeDates = soup.select("#curr_table tbody tr td:nth-of-type(1)")
            
            #Create Dictionary
            TempListPricesAndDates=dict(map(lambda args:(closeDates[args[0]].text,args[1].text),enumerate(closePrices)))

            print("Next")
            dataSeries = pd.Series(TempListPricesAndDates,index=dateRange)
            dataSeries= dataSeries.fillna(method="ffill")
            dataSeries= dataSeries.fillna(method="bfill")
            dataframe[key]=dataSeries.str.replace(",","").astype(float)
    

    dictall2={"Pib eua":["397881","375"],"Relacao divida/pib Brasil":["398221","763"],"Pib Brasil trimestral":["391420","858"],"Fed interest rate decisions":[ "391242", "168"],"Selic":[ "402978", "415"]}

    initialDate, finalDate,dateRange = get_dates(NumberOfyears,"-")
    print(dateRange)
    print("dtae range")

    for key in dictall2:
        if key in whatToconsider:
            id1=dictall2[key][0]
            id2=dictall2[key][1]
            dateAjax=finalDate
            print(finalDate)
            closePrices=[]
            closeDates=[]
            while dateAjax>initialDate:
                js_command_one = """$('body').html('')"""
                driver.execute_script(js_command_one)
                js_command_two = '$.ajax({type: "POST",url: "https://www.investing.com/economic-calendar/more-history" ,data:{"eventID":' +id1+',"event_attr_ID": ' +id2+',"event_timestamp":"' +dateAjax+'"},success: function(dataString) {$("body").append(dataString);$("body").append("<div id='+"'done'"+'</div>");}});'
                print(js_command_two)
                driver.execute_script(js_command_two)
                wait = WebDriverWait(driver, 60)
                # Wait for the table to show up
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#done')))
                soup=BeautifulSoup(driver.page_source,'html.parser')
                closePricesTemp = [item.text.replace("%<\\/span><\\/td>\\n","").strip() for item in soup.select(".takeover tr td:nth-of-type(3)")]
                
                closeDatesTemp = [re.sub(r'\(.+\)', '', item.text).replace("<\\/td>\\n","").strip() for item in soup.select(".takeover tr td:nth-of-type(1)")]
                print(closeDatesTemp)
                print(closePricesTemp)
                lastdateAjax=str(datetime.datetime.strptime(closeDatesTemp[-1], '%b %d, %Y').date())
                dateAjax=lastdateAjax
                closePrices=closePrices+closePricesTemp
                closeDates=closeDates+closeDatesTemp
            TempListPricesAndDates=dict(map(lambda args:(closeDates[args[0]],args[1]),enumerate(closePrices)))
            dataSeries = pd.Series(TempListPricesAndDates,index=dateRange)
            dataSeries= dataSeries.fillna(method="ffill")
            dataSeries= dataSeries.fillna(method="bfill")
            dataframe[key]=dataSeries.str.replace(",","").astype(float)
            print(dataframe[key])
    if "divida/pib eua" in whatToconsider:       
        CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1901&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GFDEGDQ188S&scale=left&cosd="+initialDate+"&coed=2020-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date="+finalDate+"&revision_date="+finalDate+"&nd="+initialDate
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)[1:]
        TempListPricesAndDates=dict(map(lambda x:(datetime.datetime.strptime(x[0],"%Y-%m-%d").strftime('%b %d, %Y'),x[1]),my_list))
        dataSeries = pd.Series(TempListPricesAndDates,index=dateRange)
        dataSeries= dataSeries.fillna(method="ffill")
        dataSeries= dataSeries.fillna(method="bfill")
        dataframe[key]=dataSeries.str.replace(",","").astype(float)
        driver.quit
        dataframe.index=(np.arange(start=0, stop=len(dataframe.index)))
    return dataframe





