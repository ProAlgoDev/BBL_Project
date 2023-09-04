from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from threading import Thread
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from bs4 import BeautifulSoup
import calendar
from multiprocessing import Process

class search():
   def __init__(self):
      self.driver = webdriver.Chrome()
      self.driver.maximize_window()
      
   def invoke(self,year,month):
      try:
         # self.detailChrome = detailSearch()
         self.tableList = []
         self.year = year
         self.month = month
         self.dayt = calendar.monthrange(self.year, self.month)[1]
         self.driver.get("https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType")
         documentTypeEl = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='combox_doc_doctype']")))
         selectVar = Select(documentTypeEl)
         selectVar.select_by_value("AGMT")
         dateRangeEl = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='cmb_date']")))
         selectDateVar = Select(dateRangeEl)
         selectDateVar.select_by_value("DR")
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromm']"))).send_keys(self.month)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromd']"))).send_keys("1")
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromy']"))).send_keys(self.year)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_tom']"))).send_keys(self.month)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_tod']"))).send_keys(self.dayt)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_toy']"))).send_keys(self.year)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Search']"))).click()
         drop_max_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//select[@name='com_maxrows']")))
         drop_max_list = Select(drop_max_element)
         drop_max_list.select_by_value("99")
      except:
          pass
   def ftable(self,element):
      print(element)
      tmpData = {}
      td = WebDriverWait(element, 10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::td]")))
      for m_index, m in enumerate(td):
         print(m_index)
         if m_index == 1:
            tmpData["Borough"] = m.text
         if m_index == 2:
            tmpData["Block"] = m.text
         if m_index == 4:
            tmpData["CRFN"] = m.text
         if m_index == 5:
            tmpData["LOT"] = m.text
         if m_index == 6:
            tmpData["Partial "] = m.text
         if m_index == 7:
            tmpData["Doc Date"] = m.text
         if m_index == 8:
            tmpData["Recorded / Filed"] = m.text
         if m_index == 15:
            tmpData["Doc Amount"] = m.text
            print(tmpData["Doc Amount"])
      self.tmpDataList.append(tmpData)
   def loadTable(self):
      try:
         self.detList = []
         self.tmpDataList = []
         table =  WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody/tr[2]/td/table/tbody")))
         tr = WebDriverWait(table,10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::tr]")))
         j_detailId = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@name='DET']")))
         for h in j_detailId:
            match = re.search(r'"([^"]+)"', h.get_attribute("onClick"))
            if match:
               desired_value = match.group(1)
               detUrl = f"https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentDetail?doc_id={desired_value}"
               self.detList.append(detUrl)
         i_index=0
         # for i in range(1, len(tr), 10):
         #    threads = []
         #    for g in range(i, min(i+10, len(tr))):
         #       thread = Thread(target=self.ftable, args=(tr[g],))
         #       threads.append(thread)
         #       thread.start()
         #    for thread in threads:
         #       thread.join()
         for i in tr:
            if i_index == 0:
               i_index +=1
               continue
            tmpData = {}
            td = WebDriverWait(i, 10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::td]")))
            for m_index, m in enumerate(td):
               if m_index == 1:
                  tmpData["Borough"] = m.text
               if m_index == 2:
                  tmpData["Block"] = m.text
               if m_index == 4:
                  tmpData["CRFN"] = m.text
               if m_index == 5:
                  tmpData["LOT"] = m.text
               if m_index == 6:
                  tmpData["Partial "] = m.text
               if m_index == 7:
                  tmpData["Doc Date"] = m.text
               if m_index == 8:
                  tmpData["Recorded / Filed"] = m.text
               if m_index == 15:
                  tmpData["Doc Amount"] = m.text
            # detailData = self.detailChrome.detThread(self.detList[i_index])
            # tmpData["Document ID"] = detailData["Document ID"]
            # tmpData["Party1-1 Name"] = detailData["Party1-1 Name"]
            # tmpData["Party1-1 ADDRESS1"] = detailData["Party1-1 ADDRESS1"]
            # tmpData["Party1-1 ADDRESS2"] = detailData["Party1-1 ADDRESS2"]
            # tmpData["Party1-1 CITY"] = detailData["Party1-1 CITY"]
            # tmpData["Party1-1 STATE"] = detailData["Party1-1 STATE"]
            # tmpData["Party1-1 ZIP"] = detailData["Party1-1 ZIP"]
            # tmpData["Party1-2 Name"] = detailData["Party1-2 Name"]
            # tmpData["Party1-2 ADDRESS1"] = detailData["Party1-2 ADDRESS1"]
            # tmpData["Party1-2 ADDRESS2"] = detailData["Party1-2 ADDRESS2"]
            # tmpData["Party1-2 CITY"] = detailData["Party1-2 CITY"]
            # tmpData["Party1-2 STATE"] = detailData["Party1-2 STATE"]
            # tmpData["Party1-2 ZIP"] = detailData["Party1-2 ZIP"]
            # tmpData["Party2-1 Name"] = detailData["Party2-1 Name"]
            # tmpData["Party2-1 ADDRESS1"] = detailData["Party2-1 ADDRESS1"]
            # tmpData["Party2-1 ADDRESS2"] = detailData["Party2-1 ADDRESS2"]
            # tmpData["Party2-1 CITY"] = detailData["Party2-1 CITY"]
            # tmpData["Party2-1 STATE"] = detailData["Party2-1 STATE"]
            # tmpData["Party2-1 ZIP"] = detailData["Party2-1 ZIP"]
            # tmpData["Party2-2 Name"] = detailData["Party2-2 Name"]
            # tmpData["Party2-2 ADDRESS1"] = detailData["Party2-2 ADDRESS1"]
            # tmpData["Party2-2 ADDRESS2"] = detailData["Party2-2 ADDRESS2"]
            # tmpData["Party2-2 CITY"] = detailData["Party2-2 CITY"]
            # tmpData["Party2-2 STATE"] = detailData["Party2-2 STATE"]
            # tmpData["Party2-2 ZIP"] = detailData["Party2-2 ZIP"]
            # tmpData["PROPERTY TYPE"] = detailData["PROPERTY TYPE"]
            # tmpData["PROPERTY ADDRESS"] = detailData["PROPERTY ADDRESS"]
            i_index+=1
            self.tmpDataList.append(tmpData)
         self.detSearch()
         self.tableList += self.tmpDataList
         try:
            checkNextTd = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody/tr[1]/td")))
            nextAtag = WebDriverWait(checkNextTd, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            for j in nextAtag:
               if 'next' == j.text:
                  j.click()
                  return True
            return False
         except:
            return False
      except:
         print("FALSE")
         return False
   def fetchData(self):
      while self.loadTable():
         print("processing")
      df = pd.DataFrame(self.tableList)
      print(df)
      if os.path.exists("MORTGAGE OR AGREEMENT.csv"):
         old_df = pd.read_csv("MORTGAGE OR AGREEMENT.csv")
         combind_data = old_df.append(df, ignore_index=True)
         combind_data.to_csv("MORTGAGE OR AGREEMENT.csv",index=False)
      else:
         df.to_csv("MORTGAGE OR AGREEMENT.csv", index=False, quoting=1)
      my_data = np.array([self.year, self.month])
      np.save("save.npy", my_data)
      

   def detSearch(self):
      num_iterations = len(self.detList)
      max_threads = 4
      for i in range(0, num_iterations, max_threads):
         threads = []
         for j in range(i, min(i+5, num_iterations)):
            thread = Thread(target=self.detThread, args=(j,))
            threads.append(thread)
            thread.start()
         for thread in threads:
            thread.join()
   def detThread(self,index):
      try:
         print(index)
         driver = webdriver.Chrome()

         url = self.detList[index]
         driver.get(url)
         documentId = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]"))).text
         self.tmpDataList[index]["Document ID"] = documentId
         party1 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[3]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody")))
         party1TR = WebDriverWait(party1, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
         for i_index, i in enumerate(party1TR):
            if i_index == 2:
               break
            td = i.find_elements(By.TAG_NAME, "td")
            for j_index, j in enumerate(td):
               if j_index == 0:
                  self.tmpDataList[index][f"Party1-{i_index+1} Name"] = j.text
               if j_index == 1:
                  self.tmpDataList[index][f"Party1-{i_index+1} ADDRESS1"] = j.text
               if j_index == 2:
                  self.tmpDataList[index][f"Party1-{i_index+1} ADDRESS2"] = j.text
               if j_index == 3:
                  self.tmpDataList[index][f"Party1-{i_index+1} CITY"] = j.text
               if j_index == 4:
                  self.tmpDataList[index][f"Party1-{i_index+1} STATE"] = j.text
               if j_index == 5:
                  self.tmpDataList[index][f"Party1-{i_index+1} ZIP"] = j.text
         Party2 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody")))
         Party2TR = WebDriverWait(Party2,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
         for i_index, i in enumerate(Party2TR):
            if i_index == 2:
               break
            td = WebDriverWait(i,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))
            for j_index, j in enumerate(td):
               if j_index == 0:
                  self.tmpDataList[index][f"Party2-{i_index+1} Name"] = j.text
               if j_index == 1:
                  self.tmpDataList[index][f"Party2-{i_index+1} ADDRESS1"] = j.text
               if j_index == 2:
                  self.tmpDataList[index][f"Party2-{i_index+1} ADDRESS2"] = j.text
               if j_index == 3:
                  self.tmpDataList[index][f"Party2-{i_index+1} CITY"] = j.text
               if j_index == 4:
                  self.tmpDataList[index][f"Party2-{i_index+1} STATE"] = j.text
               if j_index == 5:
                  self.tmpDataList[index][f"Party2-{i_index+1} ZIP"] = j.text
         
         type = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[4]/tbody/tr/td/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[5]"))).text
         address = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[4]/tbody/tr/td/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[9]"))).text
         self.tmpDataList[index]["PROPERTY TYPE"] = type
         self.tmpDataList[index]["PROPERTY ADDRESS"] = address
         driver.quit()
      except:
         pass
class detailSearch():
   def __init__(self):
      self.driver = webdriver.Chrome()
   def detThread(self,url):
      try:
         data ={}
         self.driver.get(url)
         documentId = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]"))).text
         data["Document ID"] = documentId
         party1 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[3]/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody")))
         party1TR = WebDriverWait(party1, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
         for i_index, i in enumerate(party1TR):
            if i_index == 2:
               break
            td = i.find_elements(By.TAG_NAME, "td")
            for j_index, j in enumerate(td):
               if j_index == 0:
                  data[f"Party1-{i_index+1} Name"] = j.text
               if j_index == 1:
                  data[f"Party1-{i_index+1} ADDRESS1"] = j.text
               if j_index == 2:
                  data[f"Party1-{i_index+1} ADDRESS2"] = j.text
               if j_index == 3:
                  data[f"Party1-{i_index+1} CITY"] = j.text
               if j_index == 4:
                  data[f"Party1-{i_index+1} STATE"] = j.text
               if j_index == 5:
                  data[f"Party1-{i_index+1} ZIP"] = j.text
         Party2 = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody")))
         Party2TR = WebDriverWait(Party2,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
         for i_index, i in enumerate(Party2TR):
            if i_index == 2:
               break
            td = WebDriverWait(i,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))
            for j_index, j in enumerate(td):
               if j_index == 0:
                  data[f"Party2-{i_index+1} Name"] = j.text
               if j_index == 1:
                  data[f"Party2-{i_index+1} ADDRESS1"] = j.text
               if j_index == 2:
                  data[f"Party2-{i_index+1} ADDRESS2"] = j.text
               if j_index == 3:
                  data[f"Party2-{i_index+1} CITY"] = j.text
               if j_index == 4:
                  data[f"Party2-{i_index+1} STATE"] = j.text
               if j_index == 5:
                  data[f"Party2-{i_index+1} ZIP"] = j.text
         
         type = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[4]/tbody/tr/td/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[5]"))).text
         address = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[4]/tbody/tr/td/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[9]"))).text
         data["PROPERTY TYPE"] = type
         data["PROPERTY ADDRESS"] = address
         return data
      except:
         return data
class searchBBL():
    def __init__(self):
      search_url = "https://a836-acris.nyc.gov/DS/DocumentSearch/BBL"
      op = uc.ChromeOptions()
   
      op.add_argument("--disable-blink-feature=AutomationControlled")
      self.driver = webdriver.Chrome(options=op)
      self.driver.maximize_window()
      self.driver.execute_script(
         "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
      time.sleep(1)

    def search(self, m_borough, m_block, m_lot, m_bbl):
        self.proc = True
        self.borough = m_borough
        self.block = m_block
        self.lot = m_lot
        self.bbl = m_bbl
        self.acris = ''
        self.zolaContent= ''
        self.bisweb = ''
        self.year = True
        search_url = "https://a836-acris.nyc.gov/DS/DocumentSearch/BBL"
        self.driver.get(search_url)
        borough_mapping = {'BK': '3', 'MN': '1',
                           'BX': '2', 'QN': '4', 'SI': '5'}
        try:
            dropelement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[@name='borough']")))
            if dropelement:
                droplist = Select(dropelement)
                droplist.select_by_value(borough_mapping[self.borough])
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='MT']/tbody/tr/td/form/table[1]/tbody/tr/td[2]/b/font/input"))).send_keys(self.block)
            time.sleep(.7)
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='MT']/tbody/tr/td/form/table[1]/tbody/tr/td[3]/b/font/input"))).send_keys(self.lot)
            dropelement = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//select[@name='cmb_date']")))
            Select(dropelement).select_by_value("5Y")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='MT']/tbody/tr/td/form/table[5]/tbody/tr[1]/td[1]/div/table/tbody/tr/td/input[1]"))).click()
            try:
                noData = ''
                noData = WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/b"))).text
            except:
                pass
            if noData =='':
                drop_max_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//select[@name='com_maxrows']")))
                if dropelement:
                    drop_max_list = Select(drop_max_element)
                    drop_max_list.select_by_value("99")
                    self.year= True
                return True
            elif noData !='':
                self.acris  = noData+"\n"
                self.year = False
                return True
        except:
            pass
      
ins = search()
year=2013
month = 1
if os.path.exists("save.npy"):
   my_array = np.load("save.npy")
   year = my_array[0]
   month = my_array[1]
for i in range(year,2024):
   year = i
   for j in range(month,13):
      month = j
      ins.invoke(year,month)
      ins.fetchData()