# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

class Ip_adress_proxy_ip(object):





    def start(self):
        url = "https://www.ip-adress.com/proxy-list"
        index_request = requests.get(url)
        soup = BeautifulSoup(index_request.content, 'html.parser')
        tr_node = soup.find('table', class_="htable proxylist").find_all('tr')
        for a in range(1, len(tr_node)):
            td_node = tr_node[a].find_all('td')
            ip = re.search(r'(.*?):', td_node[0].get_text()).group(1)
            port = re.search(r':(.*)', td_node[0].get_text()).group(1)


if __name__ == "__main__":
    spider = Ip_adress_proxy_ip()
    spider.start()
