# coding=utf-8
import requests
import re
import execjs
from bs4 import BeautifulSoup

url = "http://spys.one/en/http-proxy-list/"  # 该网站为国外网站,需要设置代理才访问
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
ip_list=[]
for a in range(2, len(tr_node)):
    td_node = tr_node[a].find('font', class_="spy14")
    if td_node is None:
        continue
    else:
        ip_list.append(re.search(r'(.*?)document',td_node.get_text()).group(1))

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
for a in range(0,len(ip_list)):
    print ip_list[a]
    print port[a]
