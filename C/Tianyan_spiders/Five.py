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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
)
class Five(object):
    def start(self):
        conn = config.connection()
        cur = conn.cursor()
        try:
            # 插入正式库
            sql = 'SELECT * FROM url LIMIT 242,60'
            cur.execute(sql)
            results = cur.fetchall()
            self.parser(results,conn,cur)

        except MySQLdb.Error as e:  # ignore mysql error: Duplicate entry。
            logger.debug(e)

    def parser(self, results, conn, cur):
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
                driver.close()
                soup = BeautifulSoup(content, 'html.parser')
                a_node = soup.find_all('a', class_="name")
                i = 0
                for b in range(0, len(a_node)):
                    try:
                        parser_url = a_node[b]['href']
                        driver_parser = webdriver.PhantomJS(
                            executable_path='D:/phantomjs-2.1.1/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                            desired_capabilities=dcap)
                        driver_parser.get(parser_url)
                        # 等待5秒,更据动态网页加载耗时自定义
                        time.sleep(5)
                        # 获取网页内容
                        sc_content = driver_parser.page_source.encode('utf-8')
                        driver_parser.close()
                        sc_soup = BeautifulSoup(sc_content, 'html.parser')
                        try:
                            company_name = sc_soup.find('h1').get_text()
                        except:
                            company_name = ""
                        logger.debug(company_name)
                        detail_node = sc_soup.find('div', class_="detail")
                        sc = detail_node.find_all('div', class_="in-block")
                        logger.debug(len(sc))
                        if u"查看更多" in sc[0].get_text():
                            script_node = sc[0].find('script')
                            mobile_number = re.search(r'\"(.*?)\"', script_node.get_text().strip()).group(1)

                        else:
                            mobile_number = ""
                        if u"查看更多" in sc[1].get_text():
                            script_one_node = sc[1].find('script')

                            email = re.search(r'\"(.*?)\"', script_one_node.get_text().strip()).group(1)

                        else:
                            email = ""
                        if u"详情" in sc[3].get_text():
                            script_two_node = sc[3].find('script')

                            company_address = re.search(r'\"(.*?)\"', script_two_node.get_text().strip()).group(1)

                        else:
                            company_address = re.search(ur'地址：(.*)', sc[3].get_text()).group(1)
                        try:
                            # 插入正式库
                            sql = 'insert into tianyan_xian(url,company_name,mobile_number,company_address,email,province,city,county) values ( %s, %s,%s, %s,%s,%s,%s,%s)'
                            item = (
                            parser_url, company_name, mobile_number, company_address, email, province, city, county)
                            cur.execute(sql, item)
                            conn.commit()
                            i += 1
                            logger.debug(
                                "现在爬取id为%s%s %s %s的url : %s  已爬取到第%s页第%d个" % (id, province, city, county, url, a, i))
                        except MySQLdb.Error as e:  # ignore mysql error: Duplicate entry。
                            logger.debug(e)
                    except:
                        continue
if __name__ == "__main__":
    spider = Five()
    spider.start()