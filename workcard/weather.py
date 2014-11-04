#--*--coding: utf-8 --*--

import json
import re
import time
import urllib

def fetchWeather(msg):

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
  weatherComUrl = 'http://www.weather.com.cn/data/sk/101010100.html'
  weatherComCon = urllib.urlopen(weatherComUrl).read()
  weatherCom_info = json.loads(weatherComCon)
  
  #with open('wea', 'rt') as f:
  #  con = f.read()
  curTime = repr(time.time()).replace('.','')[:13]
  #url = 'http://www.baidu.com/home/xman/data/superload?type=weather&_req_seqid=0x96d382e000004b20&asyn=1&t=%s' % curTime
  url = 'http://www.baidu.com/home/xman/data/superload?type=weather&t=%s' % curTime
  con = urllib.urlopen(url).read()
  #realtimeTemp = re.findall(r"u'实时：(\d+*?)℃'", con)[0]
  try:
    realtimePM25 = re.findall(r'pm25\&gt[^0-9]*(\d+)[^0-9]*pm25\&gt', con)[0]
  except IndexError:
    realtimePM25 = '-1'
  #c = re.sub(r'<alldata>.*<\\\/alldata>', 'TESTING', con)
  c = re.sub(r'\&lt.*\&gt', 'TESTING', con)
  w_info = json.loads(c)

  #w_info['data']['weather'].keys:
  #   content, packinfo, setting, id
  #w_info['data']['weather']['content'].keys:
  #   week(星期:周五), city, thirdday(后天详情), fourthday, ipprovince(北京), fifthday, cityname, source, isauto, ipcity, linkseven, weatherType, pslink, weatherType(aladdin), pslink, calendar(农历), tomorrow(明天详情), today, ##warning(可能没有该项)
  #	  calendar -
  #		festival - 非节日
  #		lunar - 九月廿四
  #	  warning -
  #		title - 北京市发布霾黄色预警
  #		url - 
  #		imgurl -
  #		...
  #w_info['data']['weather']['content']['today'].keys:
  #   pm25url(pm25链接:百度搜索页), temp(温度:21 ~ 11℃), img(代表天气的logo:url), pmdate(日期:2014-10-20), rtt, link(weather.com.cn天气页), condition(天气详情:霾转多云), pm25(数值:300), imgs(没看懂), wind(风力:微风), pollution(没看懂)
  
  temperature = (w_info['data']['weather']['content']['today']['temp']).encode('utf-8','ignore')
  pmdate = str(w_info['data']['weather']['content']['today']['pmdate'])
  condition = (w_info['data']['weather']['content']['today']['condition']).encode('utf-8','ignore')
  wind = (w_info['data']['weather']['content']['today']['wind']).encode('utf-8','ignore')
  conImg_url = (w_info['data']['weather']['content']['today']['img'][0]).encode('utf-8','ignore')
  pm25 = (w_info['data']['weather']['content']['today']['pm25']).encode('utf-8','ignore')
  try:
    warning = (w_info['data']['weather']['content']['warning']['title']).encode('utf-8','ignore')
  except ValueError:
    warning = ""
  if pm25 == '-1':
    pm25 = realtimePM25
  link = (w_info['data']['weather']['content']['today']['link']).encode('utf-8','ignore')
  lunar = (w_info['data']['weather']['content']['calendar']['lunar']).encode('utf-8','ignore')
  tomorrow_temp = (w_info['data']['weather']['content']['tomorrow']['temp']).encode('utf-8','ignore')
  tomorrow_cond = (w_info['data']['weather']['content']['tomorrow']['condition']).encode('utf-8','ignore')
  tomorrow_wind = (w_info['data']['weather']['content']['tomorrow']['wind']).encode('utf-8','ignore')
  afterTomorrow_temp = (w_info['data']['weather']['content']['thirdday']['temp']).encode('utf-8','ignore')
  afterTomorrow_cond = (w_info['data']['weather']['content']['thirdday']['condition']).encode('utf-8','ignore')
  afterTomorrow_wind = (w_info['data']['weather']['content']['thirdday']['wind']).encode('utf-8','ignore')
  #weatherCom_info['weatherinfo'].keys()
  #   city, WD(风向:东南风), WSE(2), temp(实时温度:16), njd(能见度), qy, isRadar(是否有雷达地图), cityid, Radar(雷达地图:JC_RADAR_AZ9010_JB), WS(风速:2级), time(发布时间), SD(相对湿度:83%)
  city = (weatherCom_info['weatherinfo']['city']).encode('utf-8', 'ignore')
  WD = (weatherCom_info['weatherinfo']['WD']).encode('utf-8', 'ignore')
  WS = (weatherCom_info['weatherinfo']['WS']).encode('utf-8', 'ignore')
  temp = (weatherCom_info['weatherinfo']['temp']).encode('utf-8', 'ignore')
  njd = (weatherCom_info['weatherinfo']['njd']).encode('utf-8', 'ignore')
  curDate = (weatherCom_info['weatherinfo']['time']).encode('utf-8', 'ignore')
  SD = (weatherCom_info['weatherinfo']['SD']).encode('utf-8', 'ignore')

  title = "%s今日天气:%s,%s,%s" % (city, temperature, condition, wind)
  if not warning:
 	 desc = "发布时间:%s\n实时温度:%s℃\n风向:%s,风力:%s\n能见度:%s,相对湿度:%s\npm25:%s\n农历:%s\n明天天气:%s,%s,%s\n后天天气:%s,%s,%s\n" %(curDate, temp, WD, WS, njd, SD, pm25, lunar, tomorrow_temp, tomorrow_cond, tomorrow_wind, afterTomorrow_temp, afterTomorrow_cond, afterTomorrow_wind, )
  else:
	desc = "发布时间:%s\n实时温度:%s℃\n风向:%s,风力:%s\n能见度:%s,相对湿度:%s\npm25:%s\n农历:%s\n预警:%s\n明天天气:%s,%s,%s\n后天天气:%s,%s,%s\n" %(curDate, temp, WD, WS, njd, SD, pm25, lunar, warning, tomorrow_temp, tomorrow_cond, tomorrow_wind, afterTomorrow_temp, afterTomorrow_cond, afterTomorrow_wind, )
	
  article_url = 'http://m.weather.com.cn/mweather/101010100.shtml' 
  echostr = pictextTpl % (
	msg['FromUserName'], msg['ToUserName'], str(int(time.time())), title, desc, conImg_url, article_url)
  return echostr
