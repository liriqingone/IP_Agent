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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
)
class One(object):
    def start(self):
        conn = config.connection()
        cur = conn.cursor()
        try:
            # 插入正式库
            sql = 'SELECT * FROM url LIMIT 10,60'
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
            key = re.search(r'key=(.*)', url).group(1)
            for a in range(1, 6):
                page_url = "https://sjz.tianyancha.com/search/p%s?key=" % a + key
                logger.debug(page_url)
                driver = webdriver.PhantomJS(
                    executable_path='D:/phantomjs-2.1.1/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                    desired_capabilities=dcap)
                driver.get(page_url)
                # 等待5秒,更据动态网页加载耗时自定义
                time.sleep(5)
                # 获取网页内容
                content = driver.page_source.encode('utf-8')
                print content
                driver.close()
                soup = BeautifulSoup(content, 'html.parser')
                a_node = soup.find_all('a', class_="name")
                i = 0
                for b in range(0, len(a_node)):
                    print a_node[b]['href']





if __name__ == "__main__":
    spider = One()
    spider.start()