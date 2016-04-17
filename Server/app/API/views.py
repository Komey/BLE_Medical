# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from API.models import device_data as DD,user_info as UI
import json,datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def returnError(code):
    """
    返回错误信息
    :param code:错误码
    :return: JSON打包后消息体
    """
    val = {
        1001:'Unknow username',
        1002:'worng password',
        1003:'User name excepted',
        1004:'missing some part',
        1005:'Topic excepted',
        1006:'Unknow Topic',
        2000:'Success',
        2001:'Data saved.',
    }
    msg = {}
    msg['code'] = code
    msg['message'] = val[code]
    return json.dumps(msg)



@csrf_exempt
def login(request):
    UserName = request.REQUEST.get('username','')
    PassWord = request.REQUEST.get('password','')
    Location = request.REQUEST.get('location','')
    if UserName =='' or PassWord =='':
        return HttpResponse(returnError(1004))
    try:
        info = UI.objects.get(username = UserName)
        if info.password != PassWord:
            return HttpResponse(returnError(1002))
        else:
            info.location = Location
            info.save()
            val = {}
            val['code'] = 2000

            data = {
                'username':info.username,
                'sub_topic':json.loads(info.sub_topic),
            }
            val['message'] = data
            return  HttpResponse(json.dumps(val))
    except:
        return HttpResponse(returnError(1001))

@csrf_exempt
def logon(request):
    UserName = request.REQUEST.get('username','')
    PassWord = request.REQUEST.get('password','')
    if UserName =='' or PassWord =='':
        return HttpResponse(returnError(1004))
    try:
        user = UI.objects.get(username = UserName)
        return HttpResponse(returnError(1003))
    except:
        newuser = UI(username = UserName,password = PassWord,location = '',sub_topic = '[]')
        newuser.save()
        return HttpResponse(returnError(2000))

@csrf_exempt
def adddevice(request):
    UserName = request.REQUEST.get('username','')
    Topic = request.REQUEST.get('topic','')
    Qos = request.REQUEST.get('qos','0')
    Retain = request.REQUEST.get('retain','0')
    if UserName =='' or Topic =='':
        return HttpResponse(returnError(1004))
    try:
        user = UI.objects.get(username = UserName)
        val = {}
        val['code'] = 2000
        newdata = {
            'topic':Topic,
            'qos':Qos,
            'retain':Retain
        }
        strtopic = user.sub_topic
        listopic = json.loads(strtopic)
        if listopic.count(newdata) > 0:
            return HttpResponse(returnError(1005))
        listopic.append(newdata)
        user.sub_topic = json.dumps(listopic)
        user.save()
        val['message'] = listopic
        return HttpResponse(json.dumps(val))
    except:
        return HttpResponse(returnError(1001))

@csrf_exempt
def deldevice(request):
    UserName = request.REQUEST.get('username','')
    Topic = request.REQUEST.get('topic','')
    Qos = request.REQUEST.get('qos','0')
    Retain = request.REQUEST.get('retain','0')
    if UserName =='' or Topic =='':
        return HttpResponse(returnError(1004))
    try:
        user = UI.objects.get(username = UserName)
        val = {}
        val['code'] = 2000
        deldata = {
            'topic':Topic,
            'qos':Qos,
            'retain':Retain
        }
        strtopic = user.sub_topic
        listopic = json.loads(strtopic)
        if listopic.count(deldata) > 0:
            listopic.remove(deldata)
            user.sub_topic = json.dumps(listopic)
            user.save()
            val['message'] = listopic
            return HttpResponse(json.dumps(val))
        return HttpResponse(returnError(1006))
    except:
        return HttpResponse(returnError(1001))

@csrf_exempt
def adddata(request):
    DeviceID = request.REQUEST.get('deviceid','')
    HRM = request.REQUEST.get('hrm','')
    if HRM =='' or DeviceID =='':
        return HttpResponse(returnError(1004))
    data = DD(device_id = DeviceID,hrm = HRM)
    data.save()
    return HttpResponse(returnError(2001))

@csrf_exempt
def getdata(request):
    DeviceID = request.REQUEST.get('deviceid','')
    Count =int(request.REQUEST.get('count','10'))
    Date = request.REQUEST.get('date','')
    if DeviceID =='':
        return HttpResponse(returnError(1004))
    val = {}
    val['code'] = 2000

    if Date == '':
        data = DD.objects.filter(device_id = DeviceID).order_by('-date')[:Count]
    else:
        data = DD.objects.filter(device_id = DeviceID,date__contains = Date)[:Count]

    ldata = []
    for d in data:
        reda = {
            'hrm':d.hrm,
            'date':d.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        ldata.append(reda)
    val['message'] = ldata
    return HttpResponse(json.dumps(val))
