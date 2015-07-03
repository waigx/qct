#!/usr/bin/python

__author__ = "Yigong Wang"
__license__ = "GPL"

__email__ = "yigwang@cs.stonybrook.edu"


import json


def getVMInfo():
	jsonFile = open("conf/vminfo.json", 'r')
	VMInfo = json.load(jsonFile)
	jsonFile.close()
	return VMInfo


def getTopoInfo():
	brIndex = 1;
	topoDict = dict()
	topoFile = open("conf/topo.conf", 'r')
	existTopoFile = open("conf/existTopo.json", 'w')
	for tempLine in topoFile:
		brName = 'br' + str(brIndex)
		pair = tempLine[:-1].split(' ')
		for i in pair:
			if i in topoDict:
				topoDict[i].append(brName)
			else:
				topoDict[i] = ['br0', brName]
		brIndex += 1
	json.dump(topoDict, existTopoFile)
	existTopoFile.close();
	topoFile.close();
	return topoDict
