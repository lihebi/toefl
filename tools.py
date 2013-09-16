#!/usr/bin/env python2
#coding: utf8
import urllib2
import urllib
import cookielib
import re
import time
from Tkinter import Tk, Label, Frame, Button, LEFT, Text, StringVar, Entry
import ImageTk
from bs4 import BeautifulSoup
import cPickle
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.data = ''
	self.grid()
        self.label = Label(self, text='not ready', fg='red')
        self.label.grid()
        self.img = ImageTk.PhotoImage(file='a.bmp')
        #Label(self, image=self.img).grid(side='top')
        Label(self, image=self.img).grid()
        self.content = StringVar()
        self.entry = Entry(self)
        self.entry.grid()
        self.entry.config(textvariable=self.content)
        self.entry.bind('<Key-Return>', self.post)
    def post(self, event):
        self.data = self.content.get()
        self.label['text']='ready'
        self.label['fg'] = 'green'
        self.quit()
    def getdata(self):
        return self.data
class App2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.label = Label(self, text='aaa')
        self.label.pack()
    def yes(self):
        self.label['fg'] = 'green'
        self.label['text'] = 'yes'
    def no(self):
        self.label['fg'] = 'red'
        self.label['text'] = 'no'
def getOpenerAndImgurl(cookie):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    url = 'http://toefl.etest.net.cn/cn/CityAdminTable'
    req = urllib2.Request(url)
    req.add_header('Cookie',cookie)
    try:
    	response = opener.open(req)
    except urllib2.HTTPError as e:
	    print e.reason
	    return (opener, '')
    content = response.read()
    pattern = re.compile('/.*\.bmp')
    try:
	    bmp = pattern.findall(content)[0]
    except:
	    print 'please relogin!'
	    return (opener, '')
    bmp = 'http://toefl.etest.net.cn'+bmp
    return (opener, bmp)
def getImgAndSave(url):
    response = urllib2.urlopen(url)
    content = response.read()
    writer = open('a.bmp','w')
    writer.write(content)
    writer.close()

def finalRequest(code, opener, date, province):
    data = {}
    data['whichFirst']='AS'
    data['afCalcResult']=code
    data['__act']='__id.34.AdminsSelected.adp.actListSelected'
    url_values1 = urllib.urlencode(data)
    url_date=''
    url_province=''
    for i in range(len(date)):
	    url_date += 'mvfAdminMonths='+date[i]+'&'
    for i in range(len(province)):
	    url_province += 'mvfSiteProvinces='+province[i]+'&'
    url_values = url_date + url_province + '&' + url_values1
    url = 'http://toefl.etest.net.cn/cn/SeatsQuery'
    full_url = url + '?' + url_values
    print full_url
    try:
    	response = opener.open(full_url)
    except urllib2.HTTPError as e:
	    print e.reason
	    return ''
    content = response.read()
    return content
def savehtml(content):
	writer = open('output.html','w')
	writer.write(content)
	writer.close()
def getInfo(content):
	soup = BeautifulSoup(content)
	forms = soup.find_all('form')
	infos = []
	if len(forms) == 0:
		return 0
	elif len(forms) == 1:
		return 1
	for form in forms:
		if not form.input.input.input.has_attr('disabled'):
			tds = form.find_all('td')
			school = tds[2].string
			cost = tds[3].string
			state = tds[4].string
			date = tds[5].input.get('value')[4:8]
			date = date[:2]+u'月'+date[2:]
			infos.append((date, school))
	return infos
def check(content):
	infos = getInfo(content)
	if infos == 0:
		print 'forms = 0'
		return
	elif infos == 1:
		print 'code incorrect'
		return
	print '='*30
	print '='*30
	tmp = ''
	for info in infos:
		if tmp!=info[0]:
			print '-'*20
			tmp = info[0]
		print info[0], info[1]
	curtime = time.localtime()
	print 'time: %d:%d'%(curtime.tm_hour, curtime.tm_min)
	print 'total: %d'%len(infos)
def checkAndGenHtml(content):
	infos = getInfo(content)
	html = '<html><body>'
	curtime = time.localtime()
	html += '<p>time: %d:%d</p>'%(curtime.tm_hour, curtime.tm_min)
	if infos == 0:
		html += '<p>forms=0</p></html></body>'
	elif infos == 1:
		html += '<p>code incorrect</p></html></body>'
	else:
		tmp = ''
		infos = sortbydate(infos)
		for info in infos:
			if tmp!=info[0]:
				html+='<p>----------------</p>'
				tmp = info[0]
			html+='<p>'+info[0]+' '+info[1]+'</p>'
		html += '</html></body>'
	return html
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
def getcookiefromfile():
	try:
		cookie = cPickle.load(open('cookie.cpickle','rb'))
	except:
		cookie=''
	return cookie
def dumpcookie(cookie):
	cPickle.dump(cookie, open('cookie.cpickle','wb'))
