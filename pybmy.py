#!/usr/bin/env python
#encoding=utf-8
#title:pybmy
#author:deepurple
#mail:junyuanleng@gmail.com

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib,urllib2,json,re
from BeautifulSoup import BeautifulSoup

BMY='http://bbs.xjtu.edu.cn'

def getUrl(token,suffix,**params):
    lst=[BMY,str(token),str(suffix)]
    url=''.join(lst)
    params=urllib.urlencode(params)
    request=urllib2.Request(url,params)
    response=urllib2.urlopen(request).read()
    return response
    
#获取登录token
def login(user,passwd):
    response=getUrl('','/BMY/bbslogin',id=user,pw=passwd)
    soup=BeautifulSoup(response)
    url=soup('meta')[1]['content']
    token=str(url)[7:]
    #擦，蛋疼
    return token

#退出登录
def logout(token):
    getUrl(token,'bbslogout')
    print '成功登出'

#用户信息查询
def getUserInfo(token,user):
    response=getUrl(token,'bbsqry',userid=str(user))
    soup=BeautifulSoup(response)
    info=soup.findAll('font')
    for i in info:
	print i.string

#获取好友列表
def listFriend(token):
    response=getUrl(token,'bbsfall')
    soup=BeautifulSoup(response)
    print soup.prettify()

#添加好友
def addFriend(token,user,expression):
    getUrl(token,'bbsfadd',userid=str(user),exp=str(expression))
    print '好友%s添加成功！' %user

#删除好友
def removeFriend(token,user):
    getUrl(token,'bbsfdel',userid=str(user))
    print '好友%s删除成功！' %user
    

#十大贴，需要知道每个主题贴的第一个帖子编号
#获取本日十大
def getTop10(token):
    response=getUrl(token,'bbstop10')
    soup=BeautifuSoup(response)
    
#获取版面主题帖
def getTheme(token,board):
    response=getUrl(token,'tdoc',B=str(board))
    html=unicode(response,'GB2312','ignore').encode('utf-8','ignore')
    soup=BeautifulSoup(html)
    author=soup.findAll('td',{'class':'tduser'},limit=21)
    IDs=list()
    for i in author[1:]:
	IDs.append(i.contents[0].string)
    print '帖子作者',IDs
    #获取发帖时间、帖子链接等信息
    post=soup.findAll('td',{'class':'tdborder'},limit=100)
    posts=list()
    for i in post:
	posts.append(i.contents[0].string)
    numbers=posts[0::5]
    states=posts[1::5]
    times=posts[2::5]
    titles=posts[3::5]
    print '帖子编号',numbers
    print '帖子状态',states
    print '发帖时间',times 
    print '帖子标题',titles
    hrefs=list()
    for i in post[3::5]:
	hrefs.append(i.contents[0]['href'])
    print '帖子链接',hrefs

#获取某版面大版主和小版主
def getBoss(token,board):
    response=getUrl(token,'tdoc',B=str(board))
    html=unicode(response,'GB2312','ignore').encode('utf-8','ignore')
    soup=BeautifulSoup(html)

    try:
	bigBoss_list=soup('table')[3]('tr')[0]('a')
	if len(bigBoss_list)!=0:
	    for i in range(0,len(bigBoss_list)):
		print bigBoss_list[i].string
	else:
	    print '诚征版主中'
    except:
	print '啊哦出错了'
    try:
	smallBoss_list=soup('table')[3]('tr')[1]('a')
	len_list=len(smallBoss_list)
	if len_list!=0:
	    for i in range(0,len_list):
		print smallBoss_list[i].string
    except:
	print '该版无小版主'

#获取版面所有帖
def getPost(token,board):
    response=getUrl(token,'bbsdoc',board=str(board))
    soup=BeautifulSoup(response)

    #获取置底帖子的数目 
    doctop=soup.findAll('tr',{'class':'doctop'})
    #获取所有发帖人ID
    author=soup.findAll('td',{'class':'tduser'},limit=21)
    IDs=list()
    for i in author[1:]:
	IDs.append(i.contents[0].string)
    print '帖子作者',IDs
    #获取发帖时间、帖子链接等信息
    post=soup.findAll('td',{'class':'tdborder'},limit=120)
    posts=list()
    for i in post:
	posts.append(i.contents[0].string)
    numbers=posts[0::6]
    states=posts[1::6]
    times=posts[2::6]
    titles=posts[3::6]
    print '帖子编号',numbers
    print '帖子状态',states
    print '发帖时间',times 
    print '帖子标题',titles
    hrefs=list()
    for i in post[3::6]:
	hrefs.append(i.contents[0]['href'])
    print '帖子链接',hrefs
	    
    

#获取收藏夹版面
def getFavorite(token):
    url=BMY+token+'boa?secstr=*'+'&sortmode=2/3'
    response=getUrl(token,'boa',secstr='*',sortmode='')

#搜索相关版面
def searchBoard(token,keyword):
    response=getUrl(token,'bbssbs',keyword=str(keyword))
    soup=BeautifulSoup(response)
    print soup.prettify()

#在版面发布主题帖
def post(token,board,title,signature,text):
    post_signature=str(signature)
    post_title=title.decode('utf-8').encode('GB2312')
    post_text=text.decode('utf-8').encode('GB2312')
    response=getUrl(token,'bbssnd',board=str(board),th='-1',title=post_title,signature=post_signature,text=post_text)


