from bs4 import BeautifulSoup
import requests
import warnings
import re
from datetime import datetime
import json
import random
import time
import datetime
import pandas as pd


film_id="248906"
count=2000


headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Connection':'keep-alive'}
cookies={'cookie':'_lxsdk_cuid=168c325f322c8-0156d0257eb33d-10326653-13c680-168c325f323c8; uuid_n_v=v1; iuuid=30E9F9E02A1911E9947B6716B6E91453A6754AA9248F40F39FBA1FD0A2AD9B42; webp=true; ci=191%2C%E5%8F%B0%E5%B7%9E; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=49658649.1549462270794.1549465778684.1549548206227.3; _lxsdk=30E9F9E02A1911E9947B6716B6E91453A6754AA9248F40F39FBA1FD0A2AD9B42; _lxsdk_s=168c898414e-035-f0e-e6%7C%7C463'}

#url设置offset偏移量为0
url = 'http://m.maoyan.com/review/v2/comments.json?movieId='+ film_id + '&userId=-1&offset=0&limit=15&ts={}&type=3'

comment=[]
nick=[]
score=[]
comment_time=[]
gender=[]
userlevel=[]
userid=[]
upcount=[]
replycount=[]
ji=1


url_time=url_time=int(time.time())*1000#获取当前时间（单位是毫秒，所以要✖️1000）

for i in range(count):
    value=15*i
    url_range=url.format(url_time)
    res=requests.get(url_range,headers=headers,cookies=cookies,timeout=10)
    res.encoding='utf-8'
    print('正在爬取第'+str(ji)+'页')
    content=json.loads(res.text,encoding='utf-8')
    list_=content['data']['comments']
    count=0
    for item in list_:
        comment.append(item['content'])
        nick.append(item['nick'])
        score.append(item['score'])    
        comment_time.append(datetime.datetime.fromtimestamp(int(item['time']/1000)))
        gender.append(item['gender'])
        userlevel.append(item['userLevel'])
        userid.append(item['userId'])
        upcount.append(item['upCount'])
        replycount.append(item['replyCount'])
        count=count+1
        if count==15:
            url_time=item['time']
    ji+=1
    time.sleep(random.random())
print('爬取完成')
print(url_time)
result={'用户id':userid,'用户昵称':nick,'用户等级':userlevel,'性别':gender,'时间':comment_time,'评分':score,'评论内容':comment,'点赞':upcount,'评论':replycount}
results=pd.DataFrame(result)
results.info()
results.to_excel('猫眼_' + film_id + '.xlsx')