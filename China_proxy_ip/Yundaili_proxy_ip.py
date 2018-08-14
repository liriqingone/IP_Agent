# coding=utf-8
import re
import requests
import logging
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Yundaili_proxy_ip(object):

    def downloader_url(self,url):
        index_reques=requests.get(url)
        index_soup=BeautifulSoup(index_reques.content,'html.parser')
        total_node=index_soup.find('div',id="listnav").get_text().strip()
        total_number=int(re.search(r'/(\d+)',total_node).group(1))
        for page in range(1,total_number+1):
            page_url="http://www.ip3366.net/free/?stype=3&page="+"%s"%page
            self.parser_data(page_url)
    def parser_data(self,url):
        headers = {
            'Host': 'tss.sfs.db.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://tss.sfs.db.com/investpublic/servlet/web/Web?document=report&producttype=RMBS&Series=1989-4&issueid=AS894&displayScreen=R',
            'Connection': 'keep-alive'
        }
        proxy=[]
        parser_reques=requests.get(url)
        parser_soup = BeautifulSoup(parser_reques.content, 'html.parser')
        tr_node=parser_soup.find('table',class_="table table-bordered table-striped").find_all('tr')
        for tr in tr_node:
            if u"美国" in tr.get_text().strip():
               tds=tr.find_all('td')
               ip=tds[0].get_text().strip()
               logging.info(ip)
               port=tds[1].get_text().strip()
               anonymous_degrees=tds[2].get_text().strip()  #匿名度
               country="" #国家
               location=tds[4].get_text().strip() #位置
               connection_time =tds[5].get_text().strip()  # 连接时间
               validation_time=tds[6].get_text().strip() #验证时间
               test_url="https://tss.sfs.db.com/investpublic/servlet/web/Web?document=viewhistory&link=&producttype=RMBS&issueid=AS894&displayScreen=R&FromBackUrl=true&year=2018&OWASP_CSRFTOKEN=AJ37-Z2XR-S29I-K0Q9-DIHM-BZFS-0BY1-2EY4"
               proxy.append(ip)
               test_reques=requests.get(test_url,proxies=proxy,headers=headers)
               if test_reques.status_code==200:
                   print(u'有效的ip: '+ip)
               else:
                   print "无效ip"
                   proxy.remove(ip)
            else:
                continue

    def start(self):
        url="http://www.ip3366.net/free/?stype=3"
        self.downloader_url(url)


if __name__ == "__main__":
    spider = Yundaili_proxy_ip()
    spider.start()
