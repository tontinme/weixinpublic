#--*-- coding: utf-8 --*--

"""
处理和KVDB的连接
"""

import sae.kvdb
import time
from datetime import datetime as DT
from datetime import timedelta

def onWork(ontime, userid):
    onTime = ontime
    idTime = time.strftime("%Y%m%d", time.localtime(onTime))
    #curTime = time.strftime("%Y-%m-%d:%H-%M-%S", time.localtime(onTime))
    curTime = DT.fromtimestamp(onTime).strftime('%Y-%m-%d:%H-%M-%S')
    echostr = "今天的上班时间是: %s\n" %curTime
    kv = sae.kvdb.KVClient()
    on_k = userid + ".." + idTime
    on_v = kv.get(on_k)
    if not on_v:
	on_v = [str(onTime)]
    	kv.set(on_k,on_v)
    else:
	on_v.append(str(onTime))
	kv.replace(on_k,on_v)
    kv.disconnect_all()
    return echostr

def afterWork(aftertime, userid):
    afterTime = aftertime
    idTime = time.strftime("%Y%m%d", time.localtime(afterTime))
    kv = sae.kvdb.KVClient()
    on_k = userid + ".." + idTime
    on_v = kv.get(on_k)
    after_k = userid + "__" + idTime
    after_v = kv.get(after_k)
    if not after_v:
	after_v = [str(afterTime)]
	kv.set(after_k, after_v)
    else:
	after_v.append(str(afterTime))
	kv.replace(after_k, after_v)
    if not on_v:
	echostr = "今天忘记打卡了吧"
	return echostr
    onTime = float(on_v[0])
    seconds = (DT.fromtimestamp(afterTime) - DT.fromtimestamp(onTime)).seconds
    totalTime = str(timedelta(seconds=seconds))
    echostr = "今天工作了%s, 回家咯" %totalTime
    kv.disconnect_all()
    return echostr

def traverseCard(traversetime, userid):
    traverseTime = traversetime
    idTime = time.strftime("%Y%m%d", time.localtime(traverseTime))
    kv = sae.kvdb.KVClient()
    on_k = userid + ".." + idTime
    on_v = kv.get(on_k)
    after_k = userid + "__" + idTime
    after_v = kv.get(after_k)
    if not on_v:
	onEchostr = "没有今天的上班记录"
    else:
	onFunc = lambda x: str(DT.fromtimestamp(float(x))).split(".")[0]
	onTmpList = [onFunc(v) for v in on_v]
	onEchostr = "今天的上班打卡时间: %s\n" %("\n".join(onTmpList))
    if not after_v:
	afterEchostr = "没有今天的下班记录"
    else:
	afterFunc = lambda x: str(DT.fromtimestamp(float(x))).split(".")[0]
	afterTmpList = [afterFunc(v) for v in after_v]
	afterEchostr = "今天的下班打开时间: %s\n" %("\n".join(afterTmpList))
    echostr = onEchostr + afterEchostr
    kv.disconnect_all()
    #echostr = "返回今天的所有打卡时间"
    return echostr

def setCard(idtime, userid, msg):
    setOpt = msg.split()
    if setOpt[0] == 'set':
	if setOpt[1] == 'work' and int(setOpt[2]):
	    echostr = setWorkCard(idtime, userid, int(setOpt[2]))
    else:
	echostr = msg

def setWorkCard(idtime, userid, worktime):
    idTime = time.strftime("%Y%m%d", time.localtime(idtime))
    kv = sae.kvdb.KVClient()
    set_k = userid + "##" + idTime
    set_v = [str(worktime), 'yes']
    if not kv.get(set_k):
	kv.add(set_k, set_v)
    else:
	kv.replace(set_k, set_v)
    kv.disconnect_all()
    #取上班时间，设置（覆盖）定时任务
    #需要在onWork()中增加逻辑，如果检测到有闹钟，那么添加今天的闹钟
    echostr = msg
    return echostr

def cancelCard(idtime, userid, msg):
    setOpt = msg.split()
    if setOpt == 'cancel':
	if setOpt[1] == 'work':
	    echostr = cancelWorkCard(idtime, userid)

def cancelWorkCard(idtime, userid, msg):
    idTime = time.strftime("%Y%m%d", time.localtime(idtime))
    kv = sae.kvdb.KVClient()
    cancel_k = userid + "##" + idTime
    cancel_v = kv.get(cancel_k)
    if cancel_v:
	cancel_v[1] = 'no'
	kv.replace(cancel_k, cancel_v)
    echostr = msg
    return echostr
