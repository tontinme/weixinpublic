# --*-- coding: utf-8 --*-- import feedparser
import re
import feedparser
import random, time

def fetchBaiduHot(msg):

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

    top10_url = "http://top.baidu.com/rss/top10.xml"
    top10_content = feedparser.parse(top10_url)
    content = top10_content['entries'][0]['summary']
    
    p = re.compile(r'<th>\d+</th>[\n ]*<td>[\n ]*<a href="(.*?)" target="_blank">(.*?)</a>', re.DOTALL)
    result = [item for item in p.findall(content)]
    
    conList = []
    for i in range(len(result)):
      conList.append(list(result[i]))
      #conList[i][0] = (conList[i][0].replace(r'amp;', '')).encode('utf-8', 'ignore')
      conList[i][0] = (conList[i][0].replace(r'amp;', ''))
      #conList[i][1] = (conList[i][1]).encode('utf-8', 'ignore')
      #conList[i][1] = (conList[i][1]).encode('utf-8', 'ignore')
    newCon = random.sample(conList, 5)

    pictextTpl1 = ""
    for index in range(len(newCon)):
    	pictextTpl1 = pictextTpl1 + pictextItem %(newCon[index][1], newCon[index][1], newCon[index][0])
    echostr = pictextTpl %(msg['FromUserName'], msg['ToUserName'], str(int(time.time()))) + pictextTpl1 + pictextTpl2
    
    return echostr
    
