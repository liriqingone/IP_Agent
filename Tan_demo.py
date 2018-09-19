# coding=utf-8
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.action_chains import ActionChains

class Tan():

    def Recognition_method(self,driver,identify_type,user_name,password,url,select_type_bny,keyword_bny,issuer_name_bny,deal_name_bny,shelf_type_citimortgage,data_type_citimortgage,file_name,issuer): #根据爬虫项目名称,识别调用对应的接口
        try:
            if "db" in identify_type:
                self.Popup_window_Db(driver,url)
            elif "usbank" in identify_type:
                self.Popup_window_Usbank(user_name, password,url)
            elif "bny" in identify_type:
                self.Popup_window_Bny(driver,user_name,password,select_type_bny,keyword_bny,issuer_name_bny,deal_name_bny)
            elif "wf" in identify_type:
                self.Popup_window_Wf(user_name, password,url)
            elif "ocwen" in identify_type:
                self.Popup_window_Ocwen(user_name, password,file_name)
            elif "citidirect" in identify_type:
                self.Popup_window_Citidirect(file_name,issuer)
            elif "citimortgage" in identify_type:
                self.Popup_window_Citimortgage(user_name,password,shelf_type_citimortgage,data_type_citimortgage,file_name)
            else:
                print ("待扩展的方法")
        except Exception as e:
            print (e)

    def Popup_window_Db(self,url):  # Db爬虫弹窗接口
        path='D:\\Download-file\DB'
        driver = self.driver(path)
        driver.maximize_window()  # 最大化浏览器
        driver.get(url)

        driver.close()
    def Popup_window_Usbank(self,user_name, password,url): #usbank爬虫弹窗接口
        driver = self.driver()
        driver.maximize_window()  # 最大化浏览器
        driver.get("https://usbtrustgateway.usbank.com/portal/home.do")
        try:
            elem_user = driver.find_element_by_id("uname")
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_id("pword")
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        try:
            driver.find_element_by_xpath('//input[@class="form-action-button rounded"]').click()
        except:
            print ("提交按钮定位失败")
        driver.get(url)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()

    def Popup_window_Citimortgage(self, user_name,password,shelf_type,data_type,file_name):#citimortgage爬虫弹窗接口
        driver = self.driver()
        driver.maximize_window()  # 最大化浏览器
        driver.get("https://www2.citimortgage.com/Remic/login.do")
        try:
            elem_user = driver.find_element_by_id("login_USER_ID")
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_id("login_PASSWORD")
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        try:
            driver.find_element_by_xpath('//input[@name="SUBMIT"]').click()
        except:
            print ("提交按钮定位失败")
        try:
            Select(driver.find_element_by_id('securitydata_SHELF')).select_by_value(shelf_type)
        except:
            print ("标签查找失败或shelf_type参数不在下拉列表")
        try:
            Select(driver.find_element_by_id('data_selectionId')).select_by_value(data_type)
        except:
            print ("标签查找失败或data_type参数不在下拉列表")
        driver.find_element_by_xpath('//td[@width="37"]/a').click()
        tds= driver.find_elements_by_xpath('//td[@width="40%"]')
        for td in tds:
            if td.text==file_name:
                driver.execute_script("arguments[0].scrollIntoView();", td)
                break
            else:
                continue

    def Popup_window_Citidirect(self,file_name,issuer):#Citidirect爬虫弹窗接口
        driver = self.driver()
        driver.maximize_window()  # 最大化浏览器
        driver.get("https://sf.citidirect.com/")
        driver.implicitly_wait(8)
        driver.switch_to.frame("left")
        driver.find_element_by_id("MBS").click()
        time.sleep(3)
        driver.switch_to.default_content()
        driver.switch_to.frame("mainFrame")
        if driver.find_element_by_xpath('//table[@class="tableborder"]').is_displayed():
            trs=driver.find_elements_by_xpath('//table[@class="tableborder"]/tbody/tr[position()>1]')
            for tr in trs:
                text=tr.text
                if "MBS" in text and "Public" in text:
                    if file_name in text and issuer in text:
                       tr.find_element_by_class_name('nodec1').click()
                       break
                    else:
                        continue
                else:
                    continue
        else:
            print ("页面未加载完成")

    def Popup_window_Wf(self,user_name,password,url):#WF爬虫弹窗接口
        driver = self.driver()
        driver.get(url)
        driver.find_elements_by_xpath('//td[@class="fltNone"]/a')[0].click()
        user_name_node = "user_id"  # 用户名文本框的网页标签
        password_node = "password"  # 密码文本框的网页标签
        submit_node = '//button[@id="loginButton"]'  # 提交按钮的网页标签
        try:
            elem_user = driver.find_element_by_id(user_name_node)
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_id(password_node)
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        try:
            driver.find_element_by_xpath(submit_node).click()
        except:
            print ("提交按钮定位失败")

    def Popup_window_Ocwen(self,user_name, password,file_name):#pcwen爬虫弹窗接口
        login_url = "https://www.realportal.com/realportalweb/home"  # bny登录页面
        user_name_node = '//input[@name="j_username"]'  # 用户名文本框的网页标签
        password_node = '//input[@name="j_password"]'  # 密码文本框的网页标签
        submit_node = '//input[@id="login-button"]'  # 提交按钮的网页标签
        driver = self.driver()
        driver.maximize_window()  # 最大化浏览器
        driver.get(login_url)
        try:
            elem_user = driver.find_element_by_xpath(user_name_node)
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_xpath(password_node)
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        driver.find_element_by_xpath('//input[@id="agreed-check"]').click()
        driver.find_element_by_xpath(submit_node).click()
        if "Saved Queries" not in driver.page_source:
            time.sleep(4)
            driver.find_element_by_xpath('//a[@href="../queries/display"]').click()
        else:
            driver.find_element_by_xpath('//a[@href="../queries/display"]').click()
        if "linkedToQuery" not in driver.page_source:
            driver.implicitly_wait(5)
            scroll_add_crowd_button = driver.find_element_by_link_text(file_name)
            driver.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
        else:
            scroll_add_crowd_button = driver.find_element_by_link_text(file_name)
            driver.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
    def driver(self,path):
        try:
            options = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
            options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(chrome_options=options)

        except:
            try:
                driver = webdriver.Firefox()
            except:
                try:
                    driver = webdriver.Ie()
                except Exception as e:
                    print ("启动失败,请先安装谷歌或火狐或IE浏览器:%s" % e)
        return driver
    def Popup_window_Bny(self,user_name,password,select_type,keyword,issuer_name,deal_name):#bny爬虫弹窗接口
        driver=self.driver()
        login_url = "https://gctinvestorreporting.bnymellon.com/GCTIRServices"  # bny登录页面
        driver.maximize_window()  # 最大化浏览器
        driver.get(login_url)
        try:
            elem_user = driver.find_element_by_id('txtUserLogin')
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_id('txtUserPassword')
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        try:
            driver.find_element_by_xpath('//a[@id="signin"]').click()
        except:
            print ("提交按钮定位失败")
        Select(driver.find_element_by_name('lb_product_type')).select_by_value(select_type)
        Select(driver.find_element_by_id('QuickLookup')).select_by_value(keyword)
        driver.find_element_by_link_text(issuer_name).click()
        driver.find_element_by_link_text(deal_name).click()
        trs=driver.find_elements_by_xpath('//table[@id="FirstLevelDataTable"]/tbody/tr')
        for tr in trs:
            if "Loan" in tr.text:
                tr.find_element_by_xpath('//td[5]/a[1]').click()
                break
            else:
                continue

    def Popup_window_FeddieMac(self, user_name, password):
        login_url="https://freddiemac.embs.com/FhlDiscl/Data/download.php?ds=1"

        driver = self.driver()
        driver.maximize_window()  # 最大化浏览器
        driver.get(login_url)
        try:
            elem_user = driver.find_element_by_id('username')
            elem_user.clear()
            elem_user.send_keys(user_name)
        except:
            print ("用户名文本框定位失败")
        try:
            elem_pwd = driver.find_element_by_id('password')
            elem_pwd.clear()
            elem_pwd.send_keys(password)
        except:
            print ("密码文本框定位失败")
        try:
            driver.find_element_by_xpath("//input[@class='fmSubmit']").click()
        except:
            print ("提交按钮定位失败")


if __name__ == '__main__':

    spider = Tan()
    url="https://tss.sfs.db.com/investpublic/servlet/web/Web?document=viewhistory&link=&producttype=RMBS&issueid=AS894&displayScreen=R&FromBackUrl=true&year=2018&OWASP_CSRFTOKEN=AJ37-Z2XR-S29I-K0Q9-DIHM-BZFS-0BY1-2EY4"
    spider.Popup_window_Db(url)
    # user_name = "2632423486@qq.com"
    # password = "{lfufeQ3"
    # spider.Popup_window_FeddieMac(user_name,password)
    # identify_type = "bny" #对应爬虫项目的接口,全小写
    # user_name = "caiping99"  # 用户名
    # password = "Hua_yu_123"  # 密码
    # url = ""  # 下载url
    # #bny赛选关键词列表
    # select_type_bny = "RMBS"
    # keyword_bny = "C"
    # issuer_name_bny = "C-BASS"
    # deal_name_bny = "C-BASS Mortgage Loan Asset-Backed Certificates, Series 2002-CB1"
    # #citimortgage关键词列表
    # shelf_type_citimortgage = "CMSI"
    # data_type_citimortgage = "summary"
    # file_name = "Loan Level - Apr 2008 Payment Date"  #下载的文件名
    # #citidirect关键词
    # issuer=""
    # spider.Recognition_method(identify_type,user_name,password,url,select_type_bny,keyword_bny,issuer_name_bny,deal_name_bny,shelf_type_citimortgage,data_type_citimortgage,file_name,issuer)

    #citidirect
    #file_name = "AHMA 2006-3"  # 下载的文件名
    #issuer = "American Home Mortgage Assets LLC"
    #usbank
    #user_name = "caicai@sub"  # 用户名
    #password = "Xiao_ma_234"  # 密码
    #url = "https://trustinvestorreporting.usbank.com/TIR/public/deals/detail/11535/a-best-seven-srl?layout=layout&issuerName=A-BEST+Seven"  # 下载url

    # citimortgage
    #user_name = "christe1"  # 用户名
    #password = "aftgo07"  # 密码
    #shelf_type_citimortgage = "CMSI"
    #data_type_citimortgage = "summary"
    #file_name = "Loan Level - Apr 2008 Payment Date"  # 下载的文件名
    #WF
    #url = "https://www.ctslink.com/a/shelfdocs.html?shelfId=AMIT"
    #https://www.ctslink.com/a/seriesdocs.html?shelfId=AMIT&seriesId=20061
    #user_name = "liang99"  # 用户名
    #password = "Wf-201808"  # 密码
    #user_name_node = "user_id"  # 用户名文本框的网页标签
    #password_node = "password"  # 密码文本框的网页标签
    #submit_node = '//button[@id="loginButton"]'  # 提交按钮的网页标签
    #db
    #url="https://tss.sfs.db.com/investpublic/servlet/web/Web?document=viewhistory&link=&producttype=RMBS&issueid=AS894&displayScreen=R&FromBackUrl=true&year=2018&OWASP_CSRFTOKEN=AJ37-Z2XR-S29I-K0Q9-DIHM-BZFS-0BY1-2EY4"
    #bny
    #  user_name = "caiping99"  # 用户名
    # password = "Hua_yu_123"  # 密码
    #select_type_bny = "RMBS"
    #keyword_bny = "C"
    #issuer_name_bny = "C-BASS"
    #deal_name_bny = "C-BASS Mortgage Loan Asset-Backed Certificates, Series 2002-CB1"
    #usbank
    #login_url = "https://usbtrustgateway.usbank.com/portal/home.do" #登录页面的url
    #user_name = "caicai@sub"   #密码文本框的网页标签
    #password = "Xiao_ma_234"  #密码文本框的网页标签
    #submit_node = '//input[@class="form-action-button rounded"]' #提交按钮的网页标签
    #url = "https://trustinvestorreporting.usbank.com/TIR/public/deals/detail/3444/abn-amro-2002-9"#要下载的url
    #spider.Popup_window_One(url)
    #spider.Popup_window_Three(login_url,user_name, password,login_url,user_name_node,password_node,submit_node,url)
