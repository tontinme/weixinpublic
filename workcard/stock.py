#--*-- coding: utf-8 --*--

import urllib2, urllib
import re
import time
import json

def fetchStock(msg):

    #图文格式
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
        </xml> """
  

    con = msg['Content'].strip()
    try:
	stockCode = str(con.split()[1]).upper()
    except:
	echostr = msg['Content']
	return echostr
    #url = 'https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.quotes where symbol in ("%s")&format=json&diagnostics=true&env=http://datatables.org/alltables.env&callback=' %(stockCode)
    select_url = 'select * from yahoo.finance.quotes where symbol in ("%s")' %stockCode
    base_url = urllib.urlencode({'q': select_url, 'format': 'json', 'diagnostics': 'true', 'env': 'http://datatables.org/alltables.env', 'callback': ''})
    url = 'https://query.yahooapis.com/v1/public/yql?' + base_url
    
    preContent = urllib2.urlopen(url).read()
    jsonContent = json.loads(preContent)
    
    #jsonContent['query'] -
    #    count -
    #    lang -
    #    diagnotics -
    #    results -
    #	  quote -
    #		...
    #    created -
    
    infoDict = jsonContent['query']['results']['quote']
    
    symbol = str(infoDict['Symbol'])
    curPrice = str(infoDict['LastTradePriceOnly'])
    bidRealtime = str(infoDict['BidRealtime'])
    askRealtime = str(infoDict['AskRealtime'])
    changeRealtime = str(infoDict['ChangeRealtime'])
    changeinPercent = str(infoDict['ChangeinPercent'])
    changePercentChange = str(infoDict['Change_PercentChange'])
    
    openPrice = str(infoDict['Open'])
    previousClose = str(infoDict['PreviousClose'])
    daysRange = str(infoDict['DaysRange'])
    yearRange = str(infoDict['YearRange'])
    volume = str(infoDict['Volume'])
    avgVol = str(infoDict['AverageDailyVolume'])
    
    shortRatio = str(infoDict['ShortRatio'])
    marketcap = str(infoDict['MarketCapitalization'])
    compName = str(infoDict['Name'])
    twohma = str(infoDict['TwoHundreddayMovingAverage'])
    fiftyma = str(infoDict['FiftydayMovingAverage'])
    afterHoursChangeRealtime = str(infoDict['AfterHoursChangeRealtime'])
    
    title = "Stock INFO of %s" %compName
    desc = "Symbol:%s\n当前价格:%s\n买价:%s,卖价:%s\n涨跌:%s\n今开:%s,昨收:%s\n日内变动:%s\n年内变动:%s\n成交量:%s\n平均成交量:%s\n市值:%s,做空比率:%s\n200ma:%s,50ma:%s\n" %(symbol,curPrice,bidRealtime,askRealtime,changePercentChange,openPrice,previousClose,daysRange,yearRange,volume,avgVol,marketcap,shortRatio,twohma,fiftyma)
    
    picUrl = 'https://chart.finance.yahoo.com/t?s=%s&lang=en-US&region=US&width=300&height=180' %stockCode
    #gotoUrl = 'http://finance.yahoo.com/q?s=%s' %stockCode
    gotoUrl = 'http://xueqiu.com/S/%s' %stockCode
    
    echostr = pictextTpl %(
	msg['FromUserName'], msg['ToUserName'], str(int(time.time())), title, desc, picUrl, gotoUrl)
    return echostr
