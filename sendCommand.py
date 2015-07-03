#!/usr/bin/python

__author__ = "Yigong Wang"
__license__ = "GPL"

__email__ = "yigwang@cs.stonybrook.edu"


import subprocess as sp
import sys


def sendCMD(cmd):
	sp.call(['ssh', 'root@10.10.1.0', "\"" + cmd + "\""])
	sp.call(['ssh', 'root@10.10.1.1', "\"" + cmd + "\""])
	sp.call(['ssh', 'root@10.10.1.2', "\"" + cmd + "\""])
	sp.call(['ssh', 'root@10.10.1.3', "\"" + cmd + "\""])
	return;


cmd = ' '.join(sys.argv[1:])
sendCMD(cmd)
