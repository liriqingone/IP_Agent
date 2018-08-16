# coding=utf-8
import re
import requests
import sys
import os
from bs4 import BeautifulSoup
import logging
import time
import execjs
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
class Spys_proxy_ip(object):

    def downloader_url(self,url):
        data = {
            'xf1': "4",
            'xf2': "0",
            'xf4': "0",
            'xf5': "1",
            'xpp': str('5'),
        }
        # xpp:4代表提取300个代理;0:30,1:50,2:100,3:200,4:300,5:500
        print("正在获取代理网站内容...")
        try:
            h1 = requests.post(url=url, data=data)
        except requests.exceptions.ConnectionError:
            exit("注意: 需要设置国外代理才能提取!")
        if h1.status_code == 200:
            print("获取成功!\n\n正在解密代理IP...")
        else:
            exit("获取失败!")
        hh = h1.text
        print hh
        index_soup = BeautifulSoup(hh, 'html.parser')
        total_node = index_soup.find_all('td', colspan="10")[0].find('table')
        tr_node = total_node.find_all('tr')
        ip_list = []
        http_list=[]
        anonymous_degrees_list=[]
        country_list=[]
        for a in range(2, len(tr_node)):

            if tr_node[a].find('font', class_="spy14") is None:
                continue
            else:
                td_node=tr_node[a].find_all('td')
                ip_list.append(re.search(r'(.*?)document',td_node[0].get_text()).group(1))
                http_list.append(td_node[1].get_text())
                anonymous_degrees_list.append(td_node[2].get_text())
                country_list.append(td_node[3].get_text())


                # ====获取加密算法规则====
        m1 = re.findall(r'</table><script type="text/javascript">.*;</script>', hh)
        m2 = re.sub(r'</table><script type="text/javascript">', "", m1[0])
        m3 = re.sub(r'</script>', "", m2)
        m4 = re.sub(r';', ';\n', m3)
        # =====================

        # ====获取加密内容====
        h3 = hh.split("onmouseover")
        del h3[0]
        u = []
        for h33 in h3:
            h4 = re.findall(r'\+.*\)</script>', h33)
            h5 = re.sub("\+", "", h4[0])
            h6 = re.sub("\)</script>", "", h5)
            h7 = "port = String" + h6
            h8 = h7.replace(")(", ")+String(")
            u.append(h8)
        # ==================

        # =======解密=======
        ctx = """
        function port()
        {
        %s
        return port;
        }
        """
        port = []
        for s in u:
            s1 = m4 + s  # 完整js代码
            s2 = ctx % (str(s1))
            s3 = execjs.compile(s2)
            p = s3.call("port")
            port.append(p)
        # =================
        for a in range(0, len(ip_list)):
            print ip_list[a]
            print port[a]





    def start(self):

        url="http://spys.one/en/http-proxy-list/"
        self.downloader_url(url)


if __name__ == "__main__":
    spider = Spys_proxy_ip()

    spider.start()
