import requests
from bs4 import BeautifulSoup
import pyamf
from pyamf import remoting
import re


def get_gateway_key():
    url = 'http://tdsheep.tdsheepvillage.com'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',
        "Cookie": ''#这里写你自己登录的cookie
    }
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.content)
    key = re.match(r'.*gateway_key=([0-9a-z]*)&.*', soup.find('embed')['flashvars']).group(1)
    print('获取gateway_key:', key)
    return key

# user.catch_slave 抓苦工
def catch_slave_params(id):
    return {'pf': "discuz", 'xc_publish': 'cn_cn', 'slave_type': 'friend', 'slave_id': id}
# 释放苦工
def release_slave_params(id):
    return {'pf': "discuz", 'xc_publish': 'cn_cn', 'slave_id': id}

class MyMessage:
    def __init__(self, method, params, key):
        self.json = 'false'
        self.gateway_key = key
        self.method = method
        self.params = params

    def send(self):
        # 按AMF协议编码数据
        req = remoting.Request('http_api', body=(self,))
        env = remoting.Envelope(amfVersion=pyamf.AMF3)
        env.bodies = [('/1', req)]
        data = bytes(remoting.encode(env).read())
        url = 'http://tdsheep.tdsheepvillage.com/gateway/?sessionid=6db08f5681c4f06a3bb2a667a02a7179&pf=discuz&xc_publish=cn_cn'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',
            "Cookie": '',#这里写你自己登录的cookie
            'Content-Type': 'application/x-amf'}
        req = requests.post(url, data, headers=header)
        return remoting.decode(req.content)['/1'].body['data']

key = get_gateway_key()
msg = MyMessage('user.get_friends', {'pf': "discuz", 'xc_publish': 'cn_cn'},key)
data = msg.send()
print('好友id\t好友力量\t打工地点')
for i in data:
    # print(i)
    print(i['uid'],i['power'],len(i['catch_by']))
    if len(i['catch_by']) != 2:
        msg = MyMessage('user.catch_slave', catch_slave_params(i['uid']), key)
        slave_data = msg.send()
        try:
            print(slave_data['msg'])
        except:
            print('抓获苦工：%s 苦工力量：'%(i['name']), i['power'])




