#coding=utf-8
import MySQLdb
import logging
logger = logging.getLogger(__name__)
def connection():
    try:
        conn = MySQLdb.Connect(
            host="localhost",
            user="root",
            passwd="asd123",
            db="li",
            port=3306,
            charset="utf8",
        )
        return conn
    except:
        exit(0)