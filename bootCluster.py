#!/usr/bin/python

__author__ = "Yigong Wang"
__license__ = "GPL"

__email__ = "yigwang@cs.stonybrook.edu"


import subprocess as sp
import sys
import random
from module.getConf import getVMInfo, getTopoInfo
from module.randMAC import getRandMAC


def iptablesReset():
	print "Clean up iptables..."
	sp.call(['iptables', '-F'])
	sp.call(['iptables', '-X'])
	sp.call(['iptables', '-t', 'nat', '-F'])
	sp.call(['iptables', '-t', 'nat', '-X'])
	sp.call(['iptables', '-t', 'mangle', '-F'])
	sp.call(['iptables', '-t', 'mangle', '-X'])
	sp.call(['iptables', '-P', 'INPUT', 'ACCEPT'])
	sp.call(['iptables', '-P', 'FORWARD', 'ACCEPT'])
	sp.call(['iptables', '-P', 'OUTPUT', 'ACCEPT'])
	return;


def extraTAPOpt(TAPname):
	vlan = str(random.randint(0, 100))
	return ['-net', 'nic,vlan='+vlan+',macaddr='+getRandMAC(), '-net', 'tap,vlan='+vlan+',ifname='+TAPname+',script=no,downscript=no']


def getIMGOpt(machineName):
	imgNameArr = baseName.split('.')
	imgNameArr[0] += machineName
	return ['-hda', basePath + '.'.join(imgNameArr)]


def createTAP(tapName):
	sp.call(['tunctl', '-d', tapName]);
	sp.call(['tunctl', '-t', tapName]);
	sp.call(['ifconfig', tapName, 'up']);
	return;


def createBridge(brName):
	isTAPExists = True
	try:
		output = sp.check_output(['ifconfig', brName])
	except sp.CalledProcessError as output:
		isTAPExists = False
	if isTAPExists:
		sp.call(['ifconfig', brName, 'down'])
		sp.call(['brctl', 'delbr', brName])
	sp.call(['brctl', 'addbr', brName])
	return;


def addToBridge(brName, tapName):
	sp.call(['brctl', 'addif', brName, tapName])
	return;


def addIptablePolicy(outlet, brName):
	sp.call(['sysctl', 'net.ipv4.ip_forward=1'])
	sp.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', outlet, '-j', 'MASQUERADE'])
	sp.call(['iptables', '-I', 'FORWARD', '1', '-i', brName, '-j', 'ACCEPT'])
	sp.call(['iptables', '-I', 'FORWARD', '1', '-o', brName, '-m', 'state', '--state', 'RELATED,ESTABLISHED', '-j', 'ACCEPT'])
	return;


def bootQEMU(qemuCommand):
	sp.Popen(qemuCommand);
	return;


tapPrefix = '_tap'

VMInfo = getVMInfo()
basePath = VMInfo['hdaimg']['path']
if basePath[-1] is not '/':
	basePath += '/'
baseName = VMInfo['hdaimg']['base']

baseCommand = ['qemu-system-x86_64']
for key, value in VMInfo['vmconfig'].iteritems():
	baseCommand.append(key)
	if value is not None:
		baseCommand.append(value)

topoInfo = getTopoInfo()
if topoInfo == {}:
	for machine in sys.argv[1:]:
		topoInfo[machine] = ['br0']

bridgeLst = []
for machine, brs in topoInfo.iteritems():
	qemuCommand = baseCommand + getIMGOpt(machine)
	for br in brs:
		tapName = tapPrefix + '_' + br + '_' + machine
		createTAP(tapName)
		if br in bridgeLst:
			addToBridge(br, tapName)
			print br
		else:
			createBridge(br)
			addToBridge(br, tapName)
			bridgeLst.append(br)
		qemuCommand += extraTAPOpt(tapName)
	print ' '.join(qemuCommand)
	bootQEMU(qemuCommand);

sp.call(['ifconfig', 'br0', VMInfo['br0']['ip'], 'netmask', VMInfo['br0']['mask']])
iptablesReset();
addIptablePolicy('eth0', 'br0');
