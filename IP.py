# coding=utf-8
import requests
import re
import execjs

ti = """请选择提取的数量: 
0.30个代理IP
1.50个代理IP
2.100个代理IP
3.200个代理IP
4.300个代理IP
5.500个代理IP
请输入你要提取数量的编号>>> """
while True:
    shu = input(ti)
    if shu not in ['0', '1', '2', '3', '4', '5']:
        print("\n%s" % "输入有误,请重新输入!\n")
    else:
        break

url = "http://spys.one/en/http-proxy-list/"  # 该网站为国外网站,需要设置代理才访问
data = {
    'xf1': "0",
    'xf2': "0",
    'xf4': "0",
    'xf5': "0",
    'xpp': str(shu),
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
ip_list= re.findall("\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", hh)  # 获取IP列表

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

# =====验证代理=====
url = "https://www.baidu.com"
for a in ip_list:

    print a
