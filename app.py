from selenium import webdriver
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
import time
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

import re
from threading import Thread
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import calendar

class search():
   def __init__(self):
      d = DesiredCapabilities.CHROME 
      d["goog:loggingPrefs"] = {"browser": "INFO"}
      options = webdriver.ChromeOptions()
      options.add_argument(f"--headless={True}")
      self.driver = webdriver.Chrome(options=options)
      self.driver.maximize_window()
      
   def invoke(self,year,month,day):
      try:
         self.tableList = []
         self.bblList = []
         self.year = year
         self.month = month
         self.dayfrom = day
         self.dayt = calendar.monthrange(self.year, self.month)[1]
         self.driver.get("https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType")
         documentTypeEl = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='combox_doc_doctype']")))
         selectVar = Select(documentTypeEl)
         selectVar.select_by_value("AGMT")
         dateRangeEl = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='cmb_date']")))
         selectDateVar = Select(dateRangeEl)
         selectDateVar.select_by_value("DR")
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromm']"))).send_keys(self.month)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromd']"))).send_keys(self.dayfrom)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_fromy']"))).send_keys(self.year)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_tom']"))).send_keys(self.month)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_tod']"))).send_keys(self.dayfrom)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='edt_toy']"))).send_keys(self.year)
         WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Search']"))).click()
         drop_max_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//select[@name='com_maxrows']")))
         drop_max_list = Select(drop_max_element)
         drop_max_list.select_by_value("99")
      except:
          pass
   def ftable(self,element):
      tmpData = {}
      td = WebDriverWait(element, 10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::td]")))
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
            i_index+=1
            self.tmpDataList.append(tmpData)
         self.detSearch()
         self.tableList += self.tmpDataList
         self.bblSearch()
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
   def bblSearch(self):
      num_iterations = len(self.tableList)
      max_threads = 4
      for i in range(0, num_iterations, max_threads):
         threads = []
         for j in range(i, min(i+max_threads, num_iterations)):
            thread = Thread(target=self.bblThread, args=(j,))
            threads.append(thread)
            thread.start()
         for thread in threads:
            thread.join()
   def bblThread(self,index):
      try:
         d = DesiredCapabilities.CHROME 
         d["goog:loggingPrefs"] = {"browser": "INFO"}
         options = uc.ChromeOptions()
         options.add_argument(f"--headless={True}")
         driver = webdriver.Chrome(options=options)
         driver.get("https://a836-acris.nyc.gov/DS/DocumentSearch/BBL")
         borough = self.tableList[index]["Borough"]
         block = self.tableList[index]["Block"]
         lot = self.tableList[index]["LOT"]
         borough_mapping = {'BROOKLYN': '3', 'MANHATTAN': '1',
                           'BRONX': '2', 'QUEENS': '4', 'SI': '5'}
         dropelement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[@name='borough']")))
         droplist = Select(dropelement)
         droplist.select_by_value(borough_mapping[borough])
         time.sleep(1)
         WebDriverWait(driver, 10).until(EC.presence_of_element_located(
               (By.XPATH, "//input[@name='edt_block']"))).send_keys(block)
         time.sleep(.7)
         
         WebDriverWait(driver, 10).until(EC.presence_of_element_located(
               (By.XPATH, "//input[@name='edt_lot']"))).send_keys(lot)
         WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//input[@value='Search']"))).click()
         drop_max_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='com_maxrows']")))
         drop_max_list = Select(drop_max_element)
         drop_max_list.select_by_value("99")
         nextCheck = True
         while nextCheck:
            tableBody = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody/tr[2]/td/table/tbody")))
            detidList = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@name='DET']")))
            tableTR = WebDriverWait(tableBody,10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::tr]")))
            i_index = 0
            for i in tableTR:
               if i_index==0:
                  i_index+=1
                  continue
               tableTD = WebDriverWait(i, 10).until(EC.presence_of_all_elements_located((By.XPATH, "./*[self::td]")))
               checkText = tableTD[7].text
               print(checkText)
               if checkText == "SATISFACTION OF MORTGAGE" or checkText == "UCC3 TERMINATION":
                  tmpData = {}
                  for j_index, j in enumerate(tableTD):
                     if j_index == 2:
                        tmpData["CRFN"] = j.text
                     if j_index == 3:
                        tmpData["Lot"] = j.text
                     if j_index == 4:
                        tmpData["Partial"] = j.text
                     if j_index == 5:
                        tmpData["Doc Date"] = j.text
                     if j_index == 7:
                        tmpData["Document Type"] = j.text
                     if j_index == 9:
                        tmpData["Party1"] = j.text
                     if j_index == 10:
                        tmpData["Party2"] = j.text
                     if j_index == 14:
                        tmpData["Doc Amount"] = j.text
                  detid = detidList[i_index].get_attribute("onClick")
                  print(detid)
                  match = re.search(r'"([^"]+)"', detid)
                  if match:
                     desired_value = match.group(1)
                     detUrl = f"https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentDetail?doc_id={desired_value}"
                     print(detUrl)
                     tmpData["REFERENCES-CRFN"] = self.refId(detUrl)
                  self.bblList.append(tmpData)
               i_index+=1
            try:
               checkNextTd = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody/tr[1]/td")))
               nextAtag = WebDriverWait(checkNextTd, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
               nextCheck = False
               for j in nextAtag:
                  if 'next' == j.text:
                     j.click()
                     nextCheck = True
            except:
               pass
         driver.quit()
      except:
         pass
   def refId(self,id):
      d = DesiredCapabilities.CHROME 
      d["goog:loggingPrefs"] = {"browser": "INFO"}
      options = uc.ChromeOptions()
      options.add_argument(f"--headless={True}")
      driver = webdriver.Chrome(options=options)
      driver.get(id)
      try:
         ref = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[4]/tbody/tr/td/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]"))).text
         driver.quit()
         return ref
      except:
         driver.quit()
         return ''
   def fetchData(self):

      while self.loadTable():
         print(f"{self.year}/{self.month}/{self.dayfrom}")
      df = pd.DataFrame(self.tableList)
      dfBbl = pd.DataFrame(self.bblList)
      try:
         if os.path.exists("MORTGAGE OR AGREEMENT.csv") and os.path.exists("SATISFACTION AND TERMINATION.csv"):
            old_df = pd.read_csv("MORTGAGE OR AGREEMENT.csv")
            old_dff = pd.DataFrame(old_df)
            combind_data = pd.concat([df, old_dff], ignore_index=True)
            combind_data.to_csv("MORTGAGE OR AGREEMENT.csv",index=False)

            old_bbl = pd.read_csv("SATISFACTION AND TERMINATION.csv")
            old_bblf = pd.DataFrame(old_bbl)
            combind_bbl_data = pd.concat([dfBbl, old_bblf], ignore_index=True)
            combind_bbl_data.to_csv("SATISFACTION AND TERMINATION.csv",index=False)
            
         else:
            if len(self.tableList) !=0:
               df.to_csv("MORTGAGE OR AGREEMENT.csv", index=False, quoting=1)
            if len(self.bblList) !=0:
               dfBbl.to_csv("SATISFACTION AND TERMINATION.csv", index=False, quoting=1)
         if self.dayfrom == self.dayt:
               save_day = 1
               if self.month ==12:
                  save_month = 1
                  save_year = self.year +1
               elif self.month < 12:
                  save_month = self.month
                  save_year = self.year
         if self.dayfrom < self.dayt:
            save_month = self.month
            save_year = self.year
            save_day = self.dayfrom + 1
         my_data = np.array([save_year, save_month, save_day])
         np.save("save.npy", my_data)
      except:
         pass
      
   def detSearch(self):
      num_iterations = len(self.detList)
      max_threads = 4
      for i in range(0, num_iterations, max_threads):
         threads = []
         for j in range(i, min(i+max_threads, num_iterations)):
            thread = Thread(target=self.detThread, args=(j,))
            threads.append(thread)
            thread.start()
         for thread in threads:
            thread.join()
   def detThread(self,index):
      try:
         d = DesiredCapabilities.CHROME 
         d["goog:loggingPrefs"] = {"browser": "INFO"}
         options = uc.ChromeOptions()
         options.add_argument(f"--headless={True}")
         driver = webdriver.Chrome(options=options)
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
ins = search()
year=2013
month = 1
day = 1
if os.path.exists("save.npy"):
   my_array = np.load("save.npy")
   year = my_array[0]
   month = my_array[1]
   day = my_array[2]

dayto = calendar.monthrange(year, month)[1]
for i in range(year,2024):
   year = i
   for j in range(month,13):
      for k in range(day, dayto+1):
         monthfrom = j
         ins.invoke(year,monthfrom, k)
         ins.fetchData()