# coding=utf-8
from bs4 import BeautifulSoup
import logging
import sys
import os
import re
import MySQLdb

sys.path.append(os.path.pardir + os.sep + os.path.pardir)

from selenium import webdriver
from common import config
import time


reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)

class One(object):
    def start(self):
        conn = MySQLdb.Connect(
            host="localhost",
            user="root",
            passwd="asd123",
            db="li",
            port=3306,
            charset="utf8",
        )
        cur = conn.cursor()
        try:
            # 插入正式库
            sql = 'SELECT * FROM url LIMIT 10,1'
            cur.execute(sql)
            results = cur.fetchall()
            self.parser(results,conn,cur)

        except MySQLdb.Error as e:  # ignore mysql error: Duplicate entry。
            logger.debug(e)
    def parser(self,results,conn,cur):
        for row in results:
            id = row[0]
            province = row[1]
            city = row[2]
            county = row[3]
            url = row[4]
            options = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\'}
            options.add_experimental_option('prefs', prefs)
            options.add_argument(
                'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)
            driver.find_element_by_xpath('//div[@class="pb30 position-rel"]/input').send_keys('18588644240')
            driver.find_element_by_xpath('//div[@class="pb40 position-rel"]/input').send_keys('asd5601023')
            driver.find_element_by_xpath('//div[@class="modulein modulein1 mobile_box pl30 pr30 f14 collapse in"]/div[5]').click()
            print driver.window_handles
            driver.switch_to.window(driver.window_handles[0])
            print driver.page_source
            a_links=driver.find_elements_by_xpath('//a[@class="name" and @href]')
            for a in a_links:
                a.click()







if __name__ == "__main__":
    spider = One()
    spider.start()