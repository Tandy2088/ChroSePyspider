# -*- encoding: utf-8 -*-
# Project: GooglePatent


from pyspider.libs.base_handler import *
from urllib import quote
from pymongo import MongoClient
import re
import time

#Modify the KEYWORDS
KEYWORDS='''LED Display'''
ASSIGNEE='''Samsung'''
MAX_PAGE=2
SORT_BY_NEW=True


class Handler(BaseHandler):
    
    mongo = MongoWriter()
    crawl_config = {
        'itag':'v225'
    }
    currentPage=1

    def on_start(self):
        self.crawl('https://patents.google.com/?q='+quote(KEYWORDS)+'&assignee='+quote(ASSIGNEE)+('&sort=new' if SORT_BY_NEW is True else ''), callback=self.index_page, fetch_type='js',js_script={'2':pend},timeout=60)
        
 
    @config(age=0)
    def index_page(self, response):
        for each in response.doc('#resultsContainer  article > state-modifier > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js',js_script={'2':pend2},timeout=60)
#            self.crawl(each.attr.href, callback=self.detail_page,timeout=60)
    
        if self.currentPage<MAX_PAGE :
            self.currentPage=self.currentPage+1
            self.crawl('https://patents.google.com/?q='+quote(KEYWORDS)+'&assignee='+quote(ASSIGNEE)+('&sort=new' if SORT_BY_NEW is True else '')+'&page='+str(self.currentPage-1), callback=self.index_page, fetch_type='js',js_script={'2':pend},timeout=60) 
    


        
    def detail_page(self, response):
        claim=''
        for item in response.doc('div section#claims section div[num]').items():
            claim=claim+'CLAIM#'+item.attr('num')+'.'+item.text()+'\n'
        return {
            "Title": response.doc('[id=title]').remove('user-comment-link').text(),
            "Link": response.url,
            "Abstract": response.doc('#text > abstract ').text(),
            "Inventors": response.doc('#wrapper dl.important-people>dd').text(),
            "Claims": claim,
            "_PARA":{
                "KEYWORDS":KEYWORDS,
                "MAX_PAGE":MAX_PAGE,
                "ASSIGNEE":ASSIGNEE,
                "SORT_BY_NEW":SORT_BY_NEW
            }
        }
    

# show the window to show the result
pend2='''
driver.set_window_size(200, 200)
driver.set_window_position(70,70)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div section#claims section div[num]')))
'''

# move mouse to every click to extract the href
pend='''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains    

wait = WebDriverWait(driver, 10)
driver.set_window_size(200, 200)
driver.set_window_position(70,70)
#driver.minimize_window()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#resultsContainer  article > state-modifier')))
for item in driver.find_elements_by_css_selector('#resultsContainer  article > state-modifier'):
    ActionChains(driver).move_to_element(item).perform()
#    print '##'
    time.sleep(1)

'''