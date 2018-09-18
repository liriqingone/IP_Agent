# coding: utf-8
import os

import inspect
import Tianyan_spiders
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from multiprocessing.pool import Pool as ProcessPool


# 全量抓取类实例
full_spiders = []
all_spiders = [Tianyan_spiders]

def start(spider_cls):
    try:

        spider_cls().start()
    except Exception, e:
        # send_alert_email_to(['n@sequee.com'], [], name + '\n\n' + traceback.format_exc())
        print e


def main():
    spider_list = []
    for spiders in all_spiders:
        for name in dir(spiders):
            spider_instance = getattr(spiders, name)
            if inspect.isclass(spider_instance):
                spider_list.append(spider_instance)
    # pool = ThreadPool(8)
    pool = ProcessPool(4)
    pool.map(start, spider_list)
    pool.close()
    pool.join()
    print("ALL TASK DONE")


if __name__ == '__main__':
    main()
