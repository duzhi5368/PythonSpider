import requests
from fake_useragent import UserAgent
import json
import os
import pandas as pd
import csv
ua = UserAgent()
# us = UserAgent(use_cache_server=False)
headers={
    'User-Agent':UserAgent(verify_ssl=False).random,
    'Host':'m.maoyan.com',
    'Referer':'http://m.maoyan.com/movie/1217236/comments?_v_=yes'
}

offset=0
pageNum=int(57675/15)
contentList=[]
for i in range(10):
    comment_api='http://m.maoyan.com/review/v2/comments.json?movieId=1217236&userId=-1&offset={0}&limit=15&ts=1544957345285&type=3'.format(offset)
    res_comment=requests.get(comment_api,headers=headers)
    json_comment=res_comment.text
    json_comment=json.loads(json_comment)
    data=json_comment['data']
    comments=data['comments']
    for item in comments:
        content=item['content']
        nickName=item['nick']
        contentList.append('nickName: '+nickName)
        contentList.append('content: '+content)
    offset=offset+15

# print(contentList)

from docx import Document
def file_do(list_info):
    document = Document()
    for value in list_info:
        document.add_paragraph(value)
    document.save("contentNPage.docx")

file_do(contentList)

