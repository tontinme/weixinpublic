# --*-- coding: utf-8 --*--

import feedparser
import re, time

def fetchJoke(msg):
    #图文格式
    pictextTpl = """<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>%s</ArticleCount>
	<Articles> """
    pictextTpl2 = """</Articles>
	</xml> """
    pictextItem = """<item>
	<Title><![CDATA[%s]]></Title> 
	<Description><![CDATA[%s]]></Description>
	<PicUrl><![CDATA[%s]]></PicUrl>
	<Url><![CDATA[%s]]></Url>
	</item> """


    qiubai_url = "http://feed.qiushibaike.com/rss"
    qiubai_content = feedparser.parse(qiubai_url)
    content = qiubai_content['entries'][0]['summary']
    p = re.compile(r'<p>(.*?)<\/p>', re.DOTALL)
    result = [item.strip() for item in p.findall(content)]
    q_url = []
    q_con = {}
    q_img = {}
    for k in result[1::2]:
        m = re.compile(r'<a href="(http.*)">')
        q_url.append(m.findall(k))
    num1 = 0
    for k in result[::2]:
        res_img = re.findall(r'<img src="(http.*)" />',k)
        res_con = re.findall(r'(.*)<br \/>',k)
        q_con[str(q_url[num1][0])] = res_con
        q_img[str(q_url[num1][0])] = res_img
        num1 += 1
    
    articleCount = len(q_url)
    pictextTpl1 = ""
    for key in q_con.keys():
	if not q_img[key]:
	    pic_url = "http://ww1.sinaimg.cn/mw690/74eb8f35gw1eleai8yqkwj208c08c74l.jpg"
	else:
	    pic_url = q_img[key][0]
	con_des = q_con[key][0]
	pictextTpl1 = pictextTpl1 + pictextItem %(con_des, con_des, pic_url, key)
    echostr = pictextTpl % (
	msg['FromUserName'], msg['ToUserName'], str(int(time.time())), articleCount) + pictextTpl1 + pictextTpl2

    return echostr
