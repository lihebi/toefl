#!/usr/bin/env python2
from tools import *
import pickle

content = open('output.html').read()
infos = getInfo(content)

print len(infos)
