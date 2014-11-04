#--*--coding: utf-8 --*--

import sae
from bottle import Bottle, request, debug, template, static_file
import hashlib
import xml.etree.ElementTree as ET
from workcard import card
import time
from hubot import weather

app = Bottle()
debug(True)

@app.get('/wx')
def checkSignature():
    token = 'ilovevuurwerke'
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    tmpList = [timestamp, nonce, token]
    tmpList.sort()
    #tmpStr = "".join(tmpList)
    tmpStr = "%s%s%s" % tuple(tmpList)
    tmpHash = hashlib.sha1(tmpStr).hexdigest()
    if tmpHash == signature:
	return echostr
    else:
	return None

@app.get('/hubot/instance')
def hubot_get():
    weather_instance = weather.fetchWeather()
    return weather_instance

@app.get('/login')
def web_login():
    myList=["print me","no print me","print me"]
    return template("login", myList=myList)

@app.get("/images/:filename")
def file_images(filename):
    return static_file(filename,root='images')

def parse_msg():
    recvMsg = request.body.read()
    root = ET.fromstring(recvMsg)
    msg = {}
    for child in root:
	msg[child.tag] = child.text
    return msg

#########
#from sae.storage import Bucket
#import json
#########

@app.post('/wx')
def response_msg():
    msg = parse_msg()
    #
    #bucket = Bucket('log')
    #bucket.put_object("%s.txt" % int(time.time()), json.dumps(msg))
    #
    resp_msg = card.work_card(msg)
    #
    #bucket.put_object("%s.txt" % int(time.time()), json.dumps(resp_msg))
    #
    return resp_msg

application = sae.create_wsgi_app(app)
