# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup
import logging
import sys
import os
reload(sys)
import pymssql
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s:%(lineno)s-%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
class Yundaili_proxy_ip(object):

    def insert_downloadfile(self,deal,issuer,date,ftype,url,abs_path,is_download,case_id):
        try:
            conn= pymssql.connect(host='92M5KAUIVPCUSPS', user='sa',
                                  password='sa123', database='WellDataDB', charset="utf8")
            cursor = conn.cursor()

            if not cursor:
                raise Exception('数据库连接失败！')
            sql = 'insert into welldata_downloadfile(deal,issuer,date,ftype,url,abs_path,is_download,case_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
            item = (deal,issuer,date,ftype,url,abs_path,is_download,case_id)
            cursor.execute(sql, item)
            conn.commit()

        except pymssql.Error as e:
            print e

    def li(self, deal, issuer, date, ftype, url, abs_path, is_download, case_id):
        try:
            conn = pymssql.connect(host='92M5KAUIVPCUSPS', user='sa',
                                   password='sa123', database='WellDataDB', charset="utf8")
            cursor = conn.cursor()

            if not cursor:
                raise Exception('数据库连接失败！')
            sql = 'insert into welldata_downloadfile(deal,issuer,date,ftype,url,abs_path,is_download,case_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
            item = (deal, issuer, date, ftype, url, abs_path, is_download, case_id)
            cursor.execute(sql, item)
            conn.commit()

        except pymssql.Error as e:
            print e
    def ri(self):
        conn = pymssql.connect(host='92M5KAUIVPCUSPS', user='sa',
                               password='sa123', database='WellDataDB', charset="utf8")
        cursor = conn.cursor()
        deal = "11"
        abs_path = "E:"
        issuer = ""
        ftype = "G"
        date = "201809"
        url = ""
        is_download = "True"
        case_id = "OcwenNew"
        sql = 'insert into welldata_downloadfile(deal,issuer,date,ftype,url,abs_path,is_download,case_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        item = (deal, issuer, date, ftype, url, abs_path, is_download, case_id)
        cursor.execute(sql, item)
        conn.commit()
    def start(self):

        rootdir = 'E:\OcwenDataDownload'
        i=0
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        print (len(list))
        conn = pymssql.connect(host='welldatadb.c9rukeih98lt.us-west-1.rds.amazonaws.com', user='welltitled',
                               password='Welltitled888', database='WellDataDB', charset="utf8")
        cursor = conn.cursor()

        if not cursor:
            raise Exception('数据库连接失败！')
        for i in range(0, len(list)):
            dir=list[i]
            if ".txt" in dir:
                continue
            ri= rootdir+"\\"+dir
            a_list = os.listdir(ri)
            for j in range(0,len(a_list)):
                deal = a_list[j]
                abs_path = os.path.join(rootdir, list[i])
                issuer = ""
                ftype = "G"
                date = "201809"
                url = ""
                is_download = "True"
                case_id = "OcwenNew"
                sql = 'insert into welldata_downloadfile(deal,issuer,date,ftype,url,abs_path,is_download,case_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
                item = (deal, issuer, date, ftype, url, abs_path, is_download, case_id)
                cursor.execute(sql, item)
                conn.commit()
                i += 1
                logger.info("已入库第%s个" % i)


if __name__ == "__main__":
    spider = Yundaili_proxy_ip()
    spider.ri()
