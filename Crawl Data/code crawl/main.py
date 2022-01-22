from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
class Crawl():
    def crawldata(MaCK,sotrang):
        #Them 1 so option cho trinh duyet gia lap
        chrome_option=Options()
        #chrome_option.add_argument("--incognito") #An danh
        # chrome_option.add_argument("--headless") #khong hien thi UI

        #Khai bao bien browser
        browser = webdriver.Chrome(chrome_options=chrome_option,executable_path="chromedriver.exe")

        #Mo trang web
        browser.get("https://s.cafef.vn/Lich-su-giao-dich-"+str(MaCK)+"-1.chn")
        sleep(3)
        #Lay du lieu
        datacrawl=[]
        i=1
        while i<(sotrang+1):
            counter=0
            load= 1
            try:
                pagenum = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//strong')))
                print(pagenum.text)
                print(i)
                print(pagenum.text == str(i))
                while(pagenum.text != str(i)):
                    sleep(0.2)
                    pagenum = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//strong')))
                    counter+=1
                    if(counter==5):
                        nextpage = browser.find_element(By.XPATH, "(//a[contains(text(),'>')])[2]")  # nut chuyen trang
                        nextpage.click()  # Trang ke tiep
                        counter=0
                a=pagenum.text
            except:
                print("error load page"+str(i))
            stonks =browser.find_elements(By.XPATH, '//tr[starts-with(@id,"ctl00_ContentPlaceHolder1_ctl03_rptData")]') # lay duong dan cua cac du lieu
            for stonk in stonks:
                try:
                    print(stonk.text)
                    data=stonk.find_elements(By.XPATH,'td')
                    datastonk= {'Ngày':            data[0].text,
                                'Giá điều chỉnh':  data[1].text,
                                'Giá đóng cửa':    data[2].text,
                                'thay đổi':        data[3].text,
                                'KL1':             data[5].text,
                                'GT1':             data[6].text,
                                'KL2':             data[7].text,
                                'GT2':             data[8].text,
                                'Giá mở cửa':      data[9].text,
                                'Giá cao nhất':    data[10].text,
                                'Giá thấp nhất':   data[11].text
                                }
                except:
                    load=0
                if(str(a)==str(i) and load==1):
                    datacrawl.append(datastonk)
            if (str(a) == str(i) and load == 1):
                i+=1
            #nextpage
            try:
                nextpage = browser.find_element(By.XPATH, "(//a[contains(text(),'>')])[2]")  # nut chuyen trang
                nextpage.click()  # Trang ke tiep
                sleep(1)  # Dung de load du lieu

            except:
                 print("error load page"+str(i+1))
        #Ghi du lieu
        print(datacrawl)
        df= pd.DataFrame(datacrawl)
        df.to_csv(str(MaCK)+'.csv')

        #dong trinh duyet
        sleep(3)
        browser.close()
# Điền mã chứng khoán và số trang cần crawl
Crawl.crawldata("SAM",230)
# cài thư viện selenium,pandas
# pip install selenium
# pip install pandas