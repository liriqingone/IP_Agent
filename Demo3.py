# coding=utf-8

import psutil
import os
from subprocess import PIPE
file_name="Demo1"
def kill_processByFile_name():
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            if "phantomjs.exe" in p.name():

                cmd="Tskill %s"%pid
                os.system(cmd)
        except:
            continue
kill_processByFile_name()