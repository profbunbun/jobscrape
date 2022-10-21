import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

HEADERS ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
    "Accept-Encoding":"gzip, deflate", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
}

def get_current_url(url, job_title, location):
    #updated for selenium depreciating find_element_by_XXXX
    driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="text-input-where"]').clear()
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="text-input-where"]').send_keys(location)
    time.sleep(3)
    driver.find_element(By.XPATH,'/html/body/div').click()
    time.sleep(3)
    try:
        driver.find_element(By.CLASS_NAME,'yosegi-InlineWhatWhere-primaryButton').click()
    except:
        driver.find_element(By.XPATH,'//*[@id="jobsearch"]/div[3]/button').click()
    current_url = driver.current_url
    time.sleep(3)
    time.sleep(3)
    return current_url 

current_url = get_current_url('https://indeed.com/','visa sponsorship available','')
print('output ' + current_url)


def scrape_job_details(url):
    
    resp = requests.get(url, headers=HEADERS)
    content = BeautifulSoup(resp.content, 'lxml')
   
    jobs_list = []    
    for post in content.select('.job_seen_beacon'):
        try:
            data = {
                "job_title":post.select('.jobTitle')[0].get_text().strip(),
                "company":post.select('.companyName')[0].get_text().strip(),
                "rating":post.select('.ratingNumber')[0].get_text().strip(),
                "location":post.select('.companyLocation')[0].get_text().strip(),
                "date":post.select('.date')[0].get_text().strip(),
                "job_desc":post.select('.job-snippet')[0].get_text().strip()
                
            }
        except IndexError:
            continue          
        jobs_list.append(data)
    dataframe = pd.DataFrame(jobs_list)
    
    return dataframe

scrape_job_details(current_url).to_csv('jobs.csv')