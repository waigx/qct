#!/usr/bin/python

__author__ = "Yigong Wang"
__license__ = "GPL"

__email__ = "yigwang@cs.stonybrook.edu"


import subprocess as sp
import sys
from module.getConf import getVMInfo, getTopoInfo, getExisitingTopo


def callCMD(cmd, user, ipAddr):
	sp.call(['ssh', user + '@' + ipAddr, cmd])
	return


ipbase = getVMInfo()['vmnet']['ipbase']
existingTopo = getExisitingTopo();


def sendCMD(cmd):
	for machineNo in existingTopo:
		print "running " + cmd + " on machine No:" + machineNo
		callCMD(cmd, 'root', ipbase + machineNo)
	return


cmd = ' '.join(sys.argv[1:])
print cmd
sendCMD(cmd)
