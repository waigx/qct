#!/usr/bin/python

__author__ = "Yigong Wang"
__license__ = "GPL"

__email__ = "yigwang@cs.stonybrook.edu"


import random


def randHexChar():
	return chr( random.randint(ord('A'), ord('F')) )


def getRandMAC():
	macAddress = "DE:AD:BE:EF:"
	macAddress += randHexChar() + randHexChar() + ':' + randHexChar() + randHexChar() 
	return macAddress
