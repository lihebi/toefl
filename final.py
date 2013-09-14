#!/usr/bin/env python2
import wx
import wx.html
import os, time
from tools import *
import threading

class myThread(threading.Thread):
	def __init__(self, frame):
		threading.Thread.__init__(self)
		self.frame = frame
		self.isrunning = True
		self.ispausing = False
	def run(self):
		while self.isrunning:
			if not self.ispausing:
				self.frame.mainprocess()
				time.sleep(60)
	def stop(self):
		self.isrunning = False
	def pause(self):
		self.ispausing = True
	def restart(self):
		self.ispausing = False
class Frame(wx.Frame):
	def __init__(self):
		self.date = ['201309','201310','201311']
		self.province = ['Anhui', 'Shandong', 'Jiangsu']
		self.cookie = getcookiefromfile()
		wx.Frame.__init__(self, None, -1, '', size=(500,600))
		self.panel = wx.Panel(self, -1)

		self.bimg = self.getImage()

		self.cookielabel = wx.StaticText(self.panel, -1, 'Enter Cookie:')
		self.cookietext = wx.TextCtrl(self.panel, -1, size=(175,30))
		self.cookietext.SetValue(self.cookie)
		cookiebutton = wx.Button(self.panel, label='Change')

		self.codelabel = wx.StaticText(self.panel, -1, 'Enter Code:')
		self.codetext = wx.TextCtrl(self.panel, -1, '', size=(175,30))
		codebutton = wx.Button(self.panel, label='Submit')

		startbutton = wx.Button(self.panel, label='Start')
		pausebutton = wx.Button(self.panel, label='Pause')
		stopbutton = wx.Button(self.panel, label='Stop')

		self.html = wx.html.HtmlWindow(self.panel, pos=(30,200), size=(300,300))

		sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
		sizer.AddMany((self.bimg,self.bimg,self.bimg,self.cookielabel, self.cookietext, cookiebutton, self.codelabel, self.codetext, codebutton, startbutton, pausebutton, stopbutton))
		self.panel.SetSizer(sizer)

		self.Bind(wx.EVT_BUTTON, self.OnCookieChange, cookiebutton)
		self.Bind(wx.EVT_BUTTON, self.OnCodeSubmit, codebutton)

		self.Bind(wx.EVT_BUTTON, self.MyQuit, stopbutton)
		self.Bind(wx.EVT_BUTTON, self.MyStart, startbutton)
		self.Bind(wx.EVT_BUTTON, self.MyPause, pausebutton)
		self.thread = myThread(self)
	def MyStart(self, event):
		if self.thread.ispausing:
			self.thread.restart()
		else:
			self.thread.start()
	def MyQuit(self, event):
		self.thread.stop()
		self.Destroy()
	def MyPause(self, event):
		self.thread.pause()
	def reloadImg(self):
		self.bimg = self.getImage()
	def mainprocess(self):
		cookie = 'WebBrokerSessionID='+self.cookie
		opener, url = getOpenerAndImgurl(cookie)
		self.opener = opener
		if url=='':
			return
		getImgAndSave(url)
		self.reloadImg()
		time.sleep(0.1)
		os.system('beep')
		time.sleep(0.1)
		os.system('beep')
		time.sleep(0.1)
		os.system('beep')
		time.sleep(0.1)
		os.system('beep')
	def getImage(self):
		img = wx.Image('a.bmp', wx.BITMAP_TYPE_ANY)
		bimg = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img))
		return bimg
	def OnCookieChange(self, event):
		self.cookie = self.cookietext.GetValue()
		dumpcookie(self.cookie)
		print 'cookie:', self.cookie
	def OnCodeSubmit(self, event):
		code = self.codetext.GetValue()
		print 'code:', code
		content = finalRequest(code, self.opener, self.date, self.province)
		savehtml(content)
		html = checkAndGenHtml(content)
		self.html.SetPage(html)
def main():
	app = wx.PySimpleApp()
	frame = Frame()
	frame.Show()
	app.MainLoop()
if __name__ == '__main__':
	main()
