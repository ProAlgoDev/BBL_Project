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

class BBL():   
   def __init__(self,data,index):
      self.index= index
      self.tableList = []
      self.tableList = data[self.index:]
   def bblSearch(self):
         self.bblList = []
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
      self.bblList = []
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
         np.save("ranking.npy", index)
         print(index)
         dfBbl = pd.DataFrame(self.bblList)
         try:
            if os.path.exists("SATISFACTION AND TERMINATION.csv"):
               old_bbl = pd.read_csv("SATISFACTION AND TERMINATION.csv")
               old_bblf = pd.DataFrame(old_bbl)
               combind_bbl_data = pd.concat([dfBbl, old_bblf], ignore_index=True)
               combind_bbl_data.to_csv("SATISFACTION AND TERMINATION.csv",index=False)
            else:
               if len(self.bblList) !=0:
                  dfBbl.to_csv("SATISFACTION AND TERMINATION.csv", index=False, quoting=1)
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
      

init_file_path = "MORTGAGE OR AGREEMENT.csv"
save = "ranking.npy"
data = []
try:
   if os.path.exists(init_file_path):
      csv = pd.read_csv(init_file_path, header=None, chunksize=1, skiprows=1)
      for row_num, chunk in enumerate(csv, start=0):
         tmp = {}
         tmp["Borough"] = str(chunk.iloc[0, 0])
         tmp["Block"] = str(chunk.iloc[0, 1])
         tmp["LOT"] = str(chunk.iloc[0, 3])
         data.append(tmp)
      if os.path.exists(save):
         try:
            my_data = np.load(save)
            index = my_data
         except:
            pass
         
      index = 0

      instance = BBL(data,index)
      dataArray = []
      instance.bblSearch()
      
except:
   pass
