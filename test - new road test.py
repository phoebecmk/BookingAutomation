from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
from selenium.webdriver.support.ui import Select
from tkinter import messagebox
from datetime import datetime
import time
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

import pandas as pd

Email = '' 
LicenseNum = ''
ExpiryDate = ''
#input desired exam center code here
locations = ""
month = ['JULY 2021','AUGUST 2021','SEPTEMBER 2021']
MaxMonthAhead = 6
#chrome operate in headless mode
options = Options()
options.headless = False

maxrun = 5
count = 0


while count <= maxrun:
    result = {k: [] for k in month}
    driver = webdriver.Chrome('C:/.../chromedriver.exe', chrome_options=options)
    #action = ActionChains(driver)
    driver.get("https://drivetest.ca/book-a-road-test/booking.html#/validate-driver-email")
    driver.find_element_by_id('emailAddress').send_keys(Email)
    driver.find_element_by_id('confirmEmailAddress').send_keys(Email)
    driver.find_element_by_id('licenceNumber').send_keys(LicenseNum)
    driver.find_element_by_id('licenceExpiryDate').send_keys(ExpiryDate)
    driver.find_element_by_id('regSubmitBtn').click()
    # driver.implicitly_wait
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'G2btn')))
    driver.find_element_by_id('G2btn').click()
    driver.find_element_by_xpath('//button[normalize-space()="Continue"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, locations)))
    driver.find_element_by_id(locations).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Continue"]')))
    driver.find_element_by_xpath('//button[normalize-space()="Continue"]').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//h3[@class="ng-binding"]')))
    
    for i in range(MaxMonthAhead):
        mon = driver.find_element_by_xpath('//h3[@class="ng-binding"]').text
        # print(mon)
        if mon in month:
            DatesAvailable = driver.find_elements_by_xpath('//div[@class="date-cell-contents"]')
            # print(DatesAvailable)
            if len(DatesAvailable) != 0:
                for date in DatesAvailable:
                    result[mon].append(date.text)    
        driver.find_element_by_xpath('//a[@title="next month"]').click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="date-cell-contents disabled"]')))
        driver.implicitly_wait(5)
        #WebDriverWait(driver, 5).until(mon !=driver.find_element_by_xpath('//h3[@class="ng-binding"]').text)    
    messagebox.showinfo(title="Updated: " + datetime.now().strftime('%m/%d/%y %H:%M'), message = result) 
    # count += 1
    driver.close()   
    time.sleep(300)
