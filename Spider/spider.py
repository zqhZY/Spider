#-*- coding:utf-8 -*-

'''
	filename: spider.py
	describe: 指定书名在亚马逊中检索，获取与此书相似书目，以书名为文件名，保存图片到指定目录下
	date: 2016-2-2
	author: zqh
'''

import urllib
import urllib2
import re
import os


class FileTools:
	"""Tools used by spider class"""
	def __init__(self):
		pass

	'''
		替换创建文件、路径名中非法字符编码
	'''
	def subSpecialChar(self, filepath):
		filepath = re.sub(r':' , '-' , filepath)
		filepath = re.sub(r'/' , '-' , filepath)
		filepath = re.sub(r'"' , '' , filepath)
		return filepath
		


class MySpider:
	"""spider www.amazon.cn for needed book infomation"""
	def __init__(self, savepath = "BookInfo"):
		self.savepath = savepath
		self.Tools = FileTools()
		self.mkDir(savepath)
		pass
	
	'''
		获取完整的html代码
	'''
	def getAllHtml(self , url):
		try:
			print 'Loading...'
			page = urllib.urlopen(url)

		except IOError, e:
			html = ''
			print e
			print "Please Check Net Connection!"
		else:
			html = page.read()
		return html

	'''
		返回相似书目信息的代码块列表，后续处理信息只要从该列表中获取即可
	'''
	def getNeedHtmlBlock_likes(self, html):
		reg = r'<a class="a-link-normal" target="_blank"(.+?)class="a-dynamic-image"'
		myre = re.compile(reg)
		infolist = re.findall(myre, html)
		return infolist

	'''
		返回搜索书目信息的代码块列表，后续处理信息只要从该列表中获取即可
	'''
	def getNeedHtmlBlock_items(self , html):
		reg = r'<a class="a-link-normal s-access-detail-page  a-text-normal"(.+?)>'
		myre = re.compile(reg)
		infolist = re.findall(myre, html)
		return infolist

	'''
		获取html代码块中匹配到的书目链接
	'''
	def getBookUrl(self , htmlblock):
		reg = r'href="(.+?)"'
		myre = re.compile(reg)
		hreflist = re.findall(myre , htmlblock)#返回list
		href = hreflist[0]
		if href[0:7] == 'http://':
			return href
		else:
			return 'http://www.amazon.cn' + href#拼接成完整url

		
	'''
		获取html代码块中匹配到的书名
	'''
	def getItemsBookName(self, htmlblock):
		reg = r'title="(.+?)"'
		myre = re.compile(reg)
		name = re.findall(myre , htmlblock)
		return name[0]


	'''
		获取html代码块中匹配到的相似书目书名
	'''
	def getSamebookName(self, htmlblock):
		reg = r'<img alt="(.+?)"'
		myre = re.compile(reg)
		name = re.findall(myre , htmlblock)
		return name[0]


	'''
		获取html代码块中匹配到的相似书目封面图片路径
	'''
	def getSamebookImgUrl(self , htmlblock):
		reg = r'src="(.+?)"'
		myre = re.compile(reg)
		src = re.findall(myre , htmlblock)
		return src[0]

	'''
		创建目录
	'''
	def mkDir(self, savepath):
		savepath = self.Tools.subSpecialChar(savepath)#替换路径中的':' 为'-',否则Windowserror[123]文件名语法不正确
		if not os.path.exists(savepath):
			os.makedirs(savepath)
			print "file created", savepath
			return True
		else:
			#print "dir already exist"
			return False

	'''
		指定路径、文件名，保存图书封面
	'''
	def saveImg(self, imgurl, filepath , filename):
		self.mkDir(os.path.join(self.savepath, filepath))#创建被查书目目录文件夹
		imgpath = os.path.join(self.savepath, filepath, filename)#图片文件路径
		img = urllib.urlopen(imgurl)
		data = img.read()
		imgpath = self.Tools.subSpecialChar(imgpath)#替换非法字符
		imgfile = open(imgpath, 'wb')
		print "save img " , filename
		imgfile.write(data)
		imgfile.close()










