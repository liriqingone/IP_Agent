# coding=utf-8
import re
import requests
import sys
import os
from bs4 import BeautifulSoup
import logging
sys.path.append(os.path.pardir + os.sep + os.path.pardir)
reload(sys)
# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
class Mayi_proxy_ip(object):

    def downloader_url(self,url):
        index_reques=requests.get(url)
        index_soup=BeautifulSoup(index_reques.content,'html.parser')
        total_node=index_soup.find('ul',class_="pagination").find_all('li')
        total_number=int(total_node[9].get_text())
        for page in range(1,total_number+1):
            page_url="http://www.mayidaili.com/free/location/美国-2-6252001/"+"%s"%page
            self.parser_data(page_url)
    def parser_data(self,url):

        parser_reques=requests.get(url)

        parser_soup = BeautifulSoup(parser_reques.content, 'html.parser')
        tr_node=parser_soup.find('table',class_="table table-hover table-bordered table-striped").find_all('tr')
        for tr in tr_node:
            if u"美国" in tr.get_text().strip() and tr.find('span',class_="label label-success") is not None and u"高匿" in tr.get_text().strip():

               tds=tr.find_all('td')
               ip=tds[0].get_text().strip()
               logger.debug(tr.get_text().strip())
               logger.info(ip)
               port=""
               anonymous_degrees=tds[2].get_text().strip()  #匿名度
               country=tds[3].get_text().strip() #国家
               location=tds[4].get_text().strip() #位置
               connection_time = re.search(r'(\d+)', tds[5].get_text().strip()).group(1) + 'ms'  # 连接时间
               validation_time=tds[6].get_text().strip() #验证时间

            else:
                continue

    def start(self):
        print "2"
        logging.debug("1")
        print  "3"
        url="http://www.mayidaili.com/free/location/%E7%BE%8E%E5%9B%BD-2-6252001/1"
        self.downloader_url(url)


if __name__ == "__main__":
    spider = Mayi_proxy_ip()

    spider.start()
