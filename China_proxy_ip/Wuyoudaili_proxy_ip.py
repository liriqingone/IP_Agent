# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Wuyoudaili_proxy_ip(object):


    def parser_data(self,url):
        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

        }
        proxy=[]
        parser_reques=requests.get(url,headers=headers)
        parser_soup = BeautifulSoup(parser_reques.content, 'html.parser')
        tr_node=parser_soup.find('li',style="text-align:center;").find_all('ul')
        for tr in tr_node:
            if u"高匿" in tr.get_text().strip():
                tds = tr.find_all('li')
                ip = tds[0].get_text().strip()
                logging.info(ip)
                port = tds[1].get_text().strip()
                anonymous_degrees = tds[2].get_text().strip()  # 匿名度
                country = tds[4].get_text().strip()  # 国家
                location = tds[5].get_text().strip()  # 位置
                connection_time = tds[7].get_text().strip()  # 连接时间
                validation_time = tds[8].get_text().strip()  # 验证时间

            else:
                continue

    def start(self):

        for page in range(1,21):
            page_url="http://www.data5u.com/free/country/%E7%BE%8E%E5%9B%BD/"+"index%s.html"%page
            self.parser_data(page_url)



if __name__ == "__main__":
    spider = Wuyoudaili_proxy_ip()
    spider.start()
