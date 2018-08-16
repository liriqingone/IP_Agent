# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

class Yundaili_proxy_ip(object):

    def downloader_url(self,url):
        index_reques=requests.get(url)
        index_soup=BeautifulSoup(index_reques.content,'html.parser')
        total_node=index_soup.find_all('div',class_="ipportlink")
        text=total_node[1].get_text().strip()
        print text
        total_number=int(re.search(r'\(of(.*?)ones',text).group(1))
        page_total=int(re.search(r'(.*?)proxies',text).group(1))+1
        if total_number%page_total==0:
            number=total_number/page_total+1
        else:
            number = total_number/page_total+2
        for page in range(1,number+1):
            page_url="https://premproxy.com/list/0%s.htm"%page
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
        tr_node=parser_soup.find('table',id="proxylistt").find_all('tr')
        for tr in tr_node:
            if "elite" in tr.get_text().strip() and "United States" in tr.get_text().strip():
               tds=tr.find_all('td')
               ip=tds[0].get_text().strip()
               port=""
               anonymous_degrees=tds[1].get_text().strip()  #匿名度
               country=tds[3].get_text().strip() #国家
               location=tds[4].get_text().strip() #位置
               connection_time =""  # 连接时间
               validation_time="" #验证时间
               print ip
            else:
                continue

    def start(self):
        url="https://premproxy.com/list/"
        self.downloader_url(url)


if __name__ == "__main__":
    spider = Yundaili_proxy_ip()
    spider.start()
