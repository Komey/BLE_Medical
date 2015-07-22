from django.shortcuts import render
from django.http import HttpResponse
from API.models import device_data as DD,user_info as UI
import json,datetime
# Create your views here.
def login(request):
    UserName = request.REQUEST.get('username','')
    PassWord = request.REQUEST.get('password','')
    Location = request.REQUEST.get('location','')
    if UserName =='' or PassWord =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    try:
        info = UI.objects.get(username = UserName)
        if info.password != PassWord:
            return HttpResponse('{error:1002,maeeage:worng password}')
        else:
            info.location = Location
            info.save()
            val = {}
            val['error'] = 2000

            data = {
                'username':info.username,
                'sub_topic':json.loads(info.sub_topic),
            }
            val['message'] = data
            return  HttpResponse(json.dumps(val))
    except:
        return HttpResponse('{error:1001,maeeage:Unknow username}')

def logon(request):
    UserName = request.REQUEST.get('username','')
    PassWord = request.REQUEST.get('password','')
    if UserName =='' or PassWord =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    try:
        user = UI.objects.get(username = UserName)
        return HttpResponse('{error:1003,message:User name excepted}')
    except:
        newuser = UI(username = UserName,password = PassWord,location = '',sub_topic = '[]')
        newuser.save()
        return HttpResponse('{error:2000,message:Success!}')

def adddevice(request):
    UserName = request.REQUEST.get('username','')
    Topic = request.REQUEST.get('topic','')
    Qos = request.REQUEST.get('qos','0')
    Retain = request.REQUEST.get('retain','0')
    if UserName =='' or Topic =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    try:
        user = UI.objects.get(username = UserName)
        val = {}
        val['error'] = 2000
        newdata = {
            'topic':Topic,
            'qos':Qos,
            'retain':Retain
        }
        strtopic = user.sub_topic
        listopic = json.loads(strtopic)
        if listopic.count(newdata) > 0:
            return HttpResponse('{error:1005,maeeage:Topic excepted}')
        listopic.append(newdata)
        user.sub_topic = json.dumps(listopic)
        user.save()
        val['message'] = listopic
        return HttpResponse(json.dumps(val))
    except:
        return HttpResponse('{error:1001,maeeage:Unknow username}')

def deldevice(request):
    UserName = request.REQUEST.get('username','')
    Topic = request.REQUEST.get('topic','')
    Qos = request.REQUEST.get('qos','0')
    Retain = request.REQUEST.get('retain','0')
    if UserName =='' or Topic =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    try:
        user = UI.objects.get(username = UserName)
        val = {}
        val['error'] = 2000
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
        return HttpResponse('{error:1006,maeeage:Unknow Topic}')
    except:
        return HttpResponse('{error:1001,maeeage:Unknow username}')

def adddata(request):
    DeviceID = request.REQUEST.get('deviceid','')
    HRM = request.REQUEST.get('hrm','')
    if HRM =='' or DeviceID =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    data = DD(device_id = DeviceID,hrm = HRM)
    data.save()
    return HttpResponse('{error:2001,Data saved.}')

def getdata(request):
    DeviceID = request.REQUEST.get('deviceid','')
    Count =int(request.REQUEST.get('count','10'))
    Date = request.REQUEST.get('date','')
    if DeviceID =='':
        return HttpResponse('{error:1004,maeeage:missing some part}')
    val = {}
    val['error'] = 2000

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
