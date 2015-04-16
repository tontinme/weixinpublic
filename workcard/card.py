# --*-- coding: utf-8 --*--

"""
处理具体的打卡逻辑
"""

import time
from datetime import datetime as DT
from datetime import timedelta
import kvdb, joke, weather, stock, baiduhot

def work_card(msg):
    wel_content = u"""欢迎关注vuurwerke!
	1. 回复'1'或者'打卡', 记录今天的上班时间
	2. 回复'2'或者'下班', 记录今天的下班时间
	3. 回复'3'查看今天的打卡记录
	4. 回复'joke'查看今天的糗事百科
	5. 回复'weather'查看今天天气
	6. 回复'stock CTRP'查看股票信息(仅支持美股)
	7. 回复'hot'查看百度热词榜
	.. 'h'|'help', 随时查看帮助
	"""
    # 设置返回数据模板
    # 纯文本格式
    #textTpl = """&lt;xml&gt;
    #    &lt;ToUserName&gt;&lt;![CDATA[%s]]&gt;&lt;/ToUserName&gt;
    #    &lt;FromUserName&gt;&lt;![CDATA[%s]]&gt;&lt;/FromUserName&gt;
    #    &lt;CreateTime&gt;%s&lt;/CreateTime&gt;
    #    &lt;MsgType&gt;&lt;![CDATA[text]]&gt;&lt;/MsgType&gt;
    #    &lt;Content&gt;&lt;![CDATA[%s]]&gt;&lt;/Content&gt;
    #    &lt;FuncFlag&gt;0&lt;/FuncFlag&gt;
    #    &lt;/xml&gt;"""
    textTpl = """<xml>
	    <ToUserName><![CDATA[%s]]></ToUserName>
	    <FromUserName><![CDATA[%s]]></FromUserName>
	    <CreateTime>%s</CreateTime>
	    <MsgType><![CDATA[text]]></MsgType>
	    <Content><![CDATA[%s]]></Content>
	    <FuncFlag>0</FuncFlag>
	    </xml>"""
    # 图文格式
    pictextTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
            <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>
            </Articles>
            <FuncFlag>1</FuncFlag>
            </xml> """
    # 判断MsgType内容，如果是一条“subscribe”的event，表明是一个新关注用户，如果不是，就判断内容
    if msg["MsgType"] == "event":
	if msg["Event"] == "CLICK":
	    if msg["EventKey"] in [u'onwork', u'offwork', u'worklist']:
		Content = deal_with_action(msg['EventKey'], msg['FromUserName'])
		echostr = textTpl % (
		    msg['FromUserName'], msg['ToUserName'], str(int(time.time())),Content)
	    if msg["EventKey"] == "joke":
		echostr = joke.fetchJoke(msg)
	    if msg["EventKey"] == "hot":
		echostr = baiduhot.fetchBaiduHot(msg)
	    if msg["EventKey"] == "weather":
		echostr = weather.fetchWeather(msg)
	    if msg["EventKey"] == "xiache":
		echostr = xiache.fetchzhihuXiache(msg)
	    if msg["EventKey"] == "stock":
		tmpstr = "目前尚不支持点击操作，请手动输入'stock STOCK_NAME'处理"
		echostr = textTpl % (
		    msg['FromUserName'], msg['ToUserName'], str(int(time.time())),tmpstr)
	    if msg["EventKey"] == "help":
		echostr = textTpl % (
		    msg['FromUserName'], msg['ToUserName'], str(int(time.time())),wel_content)
	else:
	    echostr = textTpl % (
        	msg['FromUserName'], msg['ToUserName'], str(int(time.time())),wel_content)
        return echostr
    else:
	if msg['Content'].lower() in ['h', 'H', 'Help', 'help', u'帮助']:
            echostr = textTpl % (
        	msg['FromUserName'], msg['ToUserName'], str(int(time.time())),wel_content)
	    #return echostr
	elif msg['Content'].lower() in ['joke', 'Joke', u'笑话', u'开心']:
	    echostr = joke.fetchJoke(msg)
	    #return echostr
	elif msg['Content'].lower() in ['weather', 'Weather', u'天气']:
	    echostr = weather.fetchWeather(msg)
	elif msg['Content'].lower() in ['hot', 'baidu', u'百度', u'热点', u'新闻']:
	    echostr = baiduhot.fetchBaiduHot(msg)
	elif msg['Content'].lower() in ['xiache', 'zhihu', u'知乎', u'tucao', u'吐槽', u'瞎扯']:
	    echostr = xiache.fetchzhihuXiache(msg)
	elif msg['Content'].strip().lower().startswith('stock'):
	    echostr = stock.fetchStock(msg)
	else:
            Content = deal_with_action(msg['Content'], msg['FromUserName'])
            echostr = textTpl % (
		msg['FromUserName'], msg['ToUserName'], str(int(time.time())),Content)
            #return echostr
	return echostr

def deal_with_action(content, clientUserID):
    idTime = time.time()
    if content in [u'1', u'上班', u'打卡', u'报道', u'我来了', u'onwork']:
	echostr = kvdb.onWork(idTime, clientUserID)
    elif content in [u'2', u'下班', u'回家', 'offwork']:
	echostr = kvdb.afterWork(idTime, clientUserID)
    elif content in [u'3', u'测试', u'worklist']:
	echostr = kvdb.traverseCard(idTime, clientUserID)
    elif content.strip().startswith('set'):
	echostr = kvdb.setCard(idTime, clientUserID, content.strip())
    elif content.strip().startswith('cancel'):
	echostr = kvdb.cancelCard(idTime, clientUserID, content.strip())
    else:
	echostr = content
    return echostr
