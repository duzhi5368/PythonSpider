import pandas as pd
import numpy as np
import re
import jieba
import wordcloud
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image

film_id="248906"

jieba.load_userdict("new.txt") #新定义词典
df=pd.read_excel('猫眼_' + film_id + '.xlsx')

comments=str()
for comment in df['评论内容']:
    comments=comments+comment

stopwords = {}.fromkeys([ line.rstrip() for line in open("stopwords.txt", "r", encoding='utf-8').readlines() ])
# segs = jieba.cut(comments,cut_all=False)
# segs = jieba.cut(comments)
segs = jieba.cut_for_search(comments)

cloud_text =[]
for seg in segs:
    if seg not in stopwords:
            cloud_text.append(seg)      

fre= Counter(cloud_text)

wc = wordcloud.WordCloud(
    font_path='C:\Windows\Fonts\simsun.ttc', # 设置字体格式
    max_words=150, # 最多显示词数
    max_font_size=150, # 字体最大值
    width=1000,
    height=1000,
    margin=1
)

wc.generate_from_frequencies(fre) # 从字典生成词云
plt.imshow(wc) # 显示词云
plt.axis('off') # 关闭坐标轴
plt.show() # 显示图像
wc.to_file('词云'+ film_id +'.png')