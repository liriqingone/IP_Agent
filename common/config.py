#coding=utf-8
import MySQLdb
import logging
logger = logging.getLogger(__name__)
try:
    conn = MySQLdb.Connect(
        host="localhost",
        user="root",
        passwd="asd123",
        db="li",
        port=3306,
        charset="utf8",
    )
    cur = conn.cursor()

except Exception as e:
    logger.info(e)

def insert_ip(ip,port,anonymous_degrees,country,location,connection_time,validation_time):
    try:
        # 插入正式库
        sql = 'insert into tianyan_xian(url,company_name,mobile_number,company_address,email,province,city,county) values ( %s, %s,%s, %s,%s,%s,%s,%s)'
        a = (ip,port,anonymous_degrees,country,location,connection_time,validation_time)
        cur.execute(sql, a)
        conn.commit()
    except MySQLdb.Error as e:  # ignore mysql error: Duplicate entry。
        logger.debug(e)