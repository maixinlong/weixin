# coding=utf-8
from django.http import HttpResponse
import hashlib, time, re, sys
from xml.etree import ElementTree as ET
from farm_lib.common.utils import cache
import weather
import wea
import baidu
reload(sys)
sys.setdefaultencoding('utf-8')
      
def weixin(request):
        print time.time()
        print '-come in--------'
        token = "maixinlong"
        params = request.GET
        args = [token, params['timestamp'], params['nonce']]
        args.sort()
        if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
            if params.has_key('echostr'):
                return HttpResponse(params['echostr'])
            else:
                reply = """<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName>
                            <CreateTime>%s</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[%s]]></Content>
                            <FuncFlag>0</FuncFlag></xml>"""
                if request.raw_post_data:
                    xml = ET.fromstring(request.raw_post_data)
                    content = xml.find("Content").text
                    fromUserName = xml.find("ToUserName").text
                    toUserName = xml.find("FromUserName").text
                    postTime = str(int(time.time()))
                    if not content:
                        return HttpResponse(reply % (toUserName, fromUserName, postTime, "输入点命令吧..."))
                    if content == "Hello2BizUser":
                        return HttpResponse(reply % (toUserName, fromUserName, postTime, "查询成绩绩点请到http://chajidian.sinaapp.com/ 本微信更多功能开发中..."))
                    elif content == "天气":
                        try:
                            city = 'beijing'
                            if cache.get('weather_msg'):
                                weather_msg = cache.get('weather_msg')
                                print 'cache get'
                            else:
                                weather_msg = wea.get_weather_by_city(city)
                                cache.set('weather_msg',weather_msg,60*60*3)
                                print 'cache set.......'
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, weather_msg))
                        except Exception,e:
                            print 'weixin err',e
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, '天气功能开发中...'))
                    elif content == "实时天气":
                        try:
                            temp_list = []
                            weather_msg = weather.main()
                            for k,v in weather_msg.items():
                                temp_list.append(k)
                                temp_list.append(v)
                            weather_msg = ''.join(temp_list)
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, weather_msg))
                        except:
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, '天气功能开发中....'))
                    else:
                        try:
                            rclist = baidu.baidu_search(content)
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, rclist))
                        except Exception,e:
                            return HttpResponse(reply % (toUserName, fromUserName, postTime, e))
                            #return HttpResponse(reply % (toUserName, fromUserName, postTime, "目前只支持查询天气哦（直接输入天气两字）,更多：功能开发中...i"))
                    
                else:
                    return HttpResponse("Invalid Request")
        else:
            return HttpResponse("Invalid Request")
