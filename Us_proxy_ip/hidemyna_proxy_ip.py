# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

class Hidemyna_proxy_ip(object):

    def downloader_url(self,url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'cookie': '__cfduid=d40c51831d43d1753bd190d9bae576eec1534775450; cf_clearance=01477a625da412c43597a76b03146966a75ea3fe-1534775455-86400-150; t=72789103; PAPVisitorId=b503d14f8ecb3d8cbb9a7ce5d9425qxl; _ga=GA1.2.1427663734.1534775470; _gid=GA1.2.1638014470.1534775470; _ym_uid=1534775472129271882; _ym_d=1534775472; _ym_isad=2; _ym_wasSynced=%7B%22time%22%3A1534775474029%2C%22params%22%3A%7B%22webvisor%22%3A%7B%22date%22%3A%222011-10-31%2016%3A20%3A50%22%7D%2C%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; jv_enter_ts_EBSrukxUuA=1534775474083; jv_visits_count_EBSrukxUuA=1; jv_refer_EBSrukxUuA=https%3A%2F%2Fhidemyna.me%2Fen%2Fproxy-list%2F; jv_utm_EBSrukxUuA=; _ym_visorc_42065329=w; _dc_gtm_UA-90263203-1=1; jv_pages_count_EBSrukxUuA=6; _gat_UA-90263203-1=1'
        }
        index_request = requests.get(url, headers=headers)
        soup = BeautifulSoup(index_request.content, 'html.parser')
        tr_nodes = soup.find('table', class_="proxy__t").find_all('tr')
        for a in range(1, len(tr_nodes)):
            td_node = tr_nodes[a].find_all('td')
            if "background:#e00000" not in str(td_node[3]):
                ip = td_node[0].get_text().strip()
                port = td_node[1].get_text().strip()
                http_type=td_node[4].get_text().strip()
                print http_type



    def start(self):
        url = "https://hidemyna.me/en/proxy-list/?country=US&anon=4"
        for a in range(1,8):
            if a==1:
                page_url=url
            else:
                start=(a-1)*64
                page_url="https://hidemyna.me/en/proxy-list/?country=US&amp;anon=4&amp;start=%s#list"%start
            self.downloader_url(page_url)


if __name__ == "__main__":
    spider = Hidemyna_proxy_ip()
    spider.start()
