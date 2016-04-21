#coding=utf-8

'''
	filename:get.py
	describle:python http get方法提交表单,实现应用逻辑
	date:2016-2-4
	author:zqh
'''

import urllib
import urllib2
import HTMLParser

import spider

spider = spider.MySpider()
parser = HTMLParser.HTMLParser()

if __name__ == '__main__':
        
        getmethod_key = "field-keywords"

        while True:
                getmethod_value = raw_input("您要输入相关书名：")
                url = "https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=亚马逊网站&url=search-alias%3Daps&"  + getmethod_key + "=" + getmethod_value
                #get方法提交数据可以直接写在url路径中

                page = spider.getAllHtml(url)
                if page == '':
                        
                        continue
                blocklist = spider.getNeedHtmlBlock_items(page)
        
                i = 1
                for block in blocklist:
                        name = parser.unescape(spider.getItemsBookName(block))
                        url = spider.getBookUrl(block)
                        print i , "、" , name
                        i+=1
                print i , ":" , 'Exit'
                
                try:
                        index = int(raw_input("请选择数目序号[1-"+str(i)+"]:"))
                except ValueError, e:
                        print 'Input error'
                        continue
                
                if i == index:
                        break
                else:
                        choosen_bookname = parser.unescape(spider.getItemsBookName(blocklist[index-1]))
                        print "你选择了：", choosen_bookname
                        print "看这本书的同志一般也会看："

                        url = spider.getBookUrl(blocklist[index-1])
                        page = spider.getAllHtml(url)
                        blocklist = spider.getNeedHtmlBlock_likes (page)
                        #print blocklist

                        num = 0
                        for block in blocklist:
                                bookname = parser.unescape(spider.getSamebookName(block))
                                booklink = spider.getBookUrl(block)
                                imgurl = spider.getSamebookImgUrl(block)
                                print bookname
                                spider.saveImg(imgurl, choosen_bookname ,bookname + '.jpg' )
                                #print parser.unescape(imgurl)
                                #print parser.unescape(booklink)


        print "Program Ended!"





