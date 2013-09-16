#!/usr/bin/env python2
from tools import *
import pickle

content = open('output.html').read()
infos = getInfo(content)


def sortbydate(infos):
	i=0
	while(i<len(infos)-1):
		j=0
		while(j<len(infos)-i-1):
			month1 = infos[j][0][:2]
			day1 = infos[j][0][-2:]
			month2 = infos[j+1][0][:2]
			day2 = infos[j+1][0][-2:]
			if compp(month1, day1, month2, day2):
				tmp = infos[j]
				infos[j] = infos[j+1]
				infos[j+1]=tmp
			j+=1
			
		i+=1
	return infos
def compp(month1, day1, month2, day2):
	if month1>month2: return True
	elif month1<month2: return False
	else:
		if  day1>day2: return True
		else: return False
infos = sortbydate(infos)
for info in infos:
	print info[0]

print len(infos)
