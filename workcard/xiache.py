# --*-- coding: utf-8 --*-- import feedparser
import re
import feedparser
import random, time
from BeautifulSoup import BeautifulSoup

def fetchzhihuXiache(msg):

    #图文格式
    pictextTpl = """<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>5</ArticleCount>
        <Articles> """
    pictextTpl2 = """</Articles>
        </xml> """
    pictextItem = """<item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item> """

    xiache_url = "http://zhihurss.miantiao.me/section/id/2"
    xiache_content = feedparser.parse(xiache_url)
    content = xiache_content['entries'][0]['summary']
    #ranNum = random.randint(0, len(xiache_content['entries']))
    #content = top10_content['entries'][ranNum]['summary']
    soup = BeautifulSoup(''.join(content))
    question = soup.findAll("h2", "question-title")
    answer = soup.findAll("div", "content")
    viewMore = soup.findAll("div", "view-more")
    viewUrl = []
    for view in viewMore:
        for vm in view.findAll('a', href=True):
            viewUrl.append(vm['href'])

    newCon = []
    for conIndex in range(len(question)):
        newCon.append(question[conIndex].text + "\n" + answer[conIndex].text)

    pictextTpl1 = ""
    for index in range(len(question)):
    	pictextTpl1 = pictextTpl1 + pictextItem %(newCon[index], newCon[index], viewUrl[index])
    echostr = pictextTpl %(msg['FromUserName'], msg['ToUserName'], str(int(time.time()))) + pictextTpl1 + pictextTpl2
    
    return echostr
