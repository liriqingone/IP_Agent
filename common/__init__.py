import logging
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_logger = logging.getLogger()
logger = logging.getLogger(__name__)
root_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s -%(filename)s:%(lineno)s- %(levelname)s: %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')

fh = logging.FileHandler(os.path.join(BASE_DIR, '../bid_run.log'))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

root_logger.addHandler(ch)
root_logger.addHandler(fh)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("common.downloader").setLevel(logging.INFO)