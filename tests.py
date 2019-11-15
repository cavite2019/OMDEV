#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 参数都不用管，只看graphid即可,去api接口处获得对应ip的

import urllib.request
import http.cookiejar
import urllib.parse
import urllib.request
import json
import requests
from prettytable import PrettyTable
import time
import sys

t = str(time.time()).replace('.', '')  #去掉.的时间戳 用于给图片命名
dict_graphid_name = {}

class ZabbixGraph:
    def __init__(self,ip,number= -1):#,number):#),graph):
        self.number = int(number)
        self.IP = ip          #

        #self.number = number
        # self.graph = graph     #
        self.header = {"Content-Type": "application/json-rpc"}
    def get_token(self): # 获得token 并返回
        data = {"jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": 'Admin',
                    "password": 'sherCock1407',
                },
                "id": 1,
                "auth": None
                }
        url_m6 = 'https://zabbix.omtools.me/'
        token = requests.post(url=url_m6, headers=self.header, data=json.dumps(data))
        json_dict_token = json.loads(token.text)
        return json_dict_token['result']
    def get_hostid(self):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output":"extend",# ["11609","fishdb1-132.1"],
                "filter": {
                    "host": self.IP
                }
            },
            "auth": self.get_token(),
            "id": 1
                        }
        url_m6 = 'https://zabbix.omtools.me/'
        hosts = requests.post(url=url_m6, headers=self.header, data=json.dumps(data))
        json_dict_hostid = json.loads(hosts.text)

        json_dict_hostid_result = json_dict_hostid['result'][0]['hostid']
        # print(json_dict_hostid_result)
        return json_dict_hostid_result

    def get_graphid_name(self):
        data ={
        "jsonrpc": "2.0",
        "method": "graph.get",
        "params": {
            "output": "extend",
            "hostids": self.get_hostid(),
            "sortfield": "name"
        },
        "auth": self.get_token(),
        "id": 1

                    }
        url_m6 = 'http://xxx/zabbix/api_jsonrpc.php'
        hosts = requests.post(url=url_m6, headers=self.header, data=json.dumps(data))
        json_dict_host = json.loads(hosts.text)
        json_dict_host_result = json_dict_host["result"]
        return json_dict_host_result
    def choose_object(self):

        counter = 0
        json_dict_host_result = self.get_graphid_name()
        # print(type(json_dict_host_result))
        tables = PrettyTable(['序号','监控项'])
        #tables = PrettyTable(['序号','监控项',' 序号',' 监控项','序号 ','监控项 ',])
        tables.align['序号','监控项','序号','监控项','序号','监控项',] = 'l'
        tables.horizontal_char = '-'
        tables.junction_char = "-"
        tables.left_padding_width = 3


        for i in json_dict_host_result:
            dict_graphid_name[counter]=i['graphid'],i['name']
            counter += 1
        self.dict_graphid_name1 = dict_graphid_name
        for i in dict_graphid_name:
            # print(i,dict_graphid_name[i][1])# 315338
            tables.add_row([i,dict_graphid_name[i][1]])

        if self.number == -1:
            print("请输入IP+项序号:")
            print(tables)
        # return object
        else:
            return dict_graphid_name

    def url_jpg(self):
        if self.number == -1:
            url_2hours = -1

        else:
            # print(dict_graphid_name[1])
            self.graph_id = self.choose_object()[self.number][0]

            url_2hours = 'http://xxx/zabbix/chart2.php?graphid=%s&period=7200' % self.graph_id
        # print(url_2hours)
        return url_2hours



    def get_jpg(self):
        # hosturl = 'http://xxx/zabbix/index.php'  # 自己填写
        # post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
        posturl = 'xxx/zabbix/index.php?request=charts.php%3Fddreset%3D1'  # 从数据包中分析出，处理post请求的url
         #Referer: http://xxx/zabbix/index.php?request=charts.php%3Fddreset%3D1


        # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        cj = http.cookiejar.LWPCookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        # 打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
       #h = urllib.request.urlopen(hosturl)


        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                  'Referer': 'http://xxx/zabbix/index.php'}

        # 构造Post数据，他也是从抓大的包里分析得出的。
        postData = {    'name': 'xxx',
                        'password': 'xxx',
                         'autologin':1,
                        'enter':'Sign in'
                     }


        # 需要给Post数据编码

        postData = urllib.parse.urlencode(postData).encode('utf-8')
        # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
        request = urllib.request.Request(posturl, postData, headers)
        response = urllib.request.urlopen(request)
        #text = response.read().decode()

        #下载图片
        jpg_link = self.url_jpg()  #图片链接
        if jpg_link == -1:
            pass
        else:
            path = '/Users/lee/PycharmProjects/pythonProjects/zabbix/ZabbixGraph/888.jpg' #%s_%s.jpg' % (self.graph_id,t)
            #request.urlretrieve(jpg_link, path)
            urllib.request.urlretrieve(jpg_link, path)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        item = ZabbixGraph(sys.argv[1])
        item.get_graphid_name()
        item.choose_object()
    elif len(sys.argv) != 2:
        item = ZabbixGraph(sys.argv[1],sys.argv[2])
        item.get_graphid_name()
        item.choose_object()
        # item.url_jpg()
        item.get_jpg()
    #