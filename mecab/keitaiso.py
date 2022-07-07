#pip install mecab-python3
#pip install unidic
#pip install mecab-python3
#pip install unidic-lite

import MeCab
import re
import pandas as pd
from wordcloud import WordCloud

#記号除去            
p = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥♪％]')

#ひらがなorカタカナ1文字のやつ消す
h = re.compile(r"[\u3041-\u309F]+")
k = re.compile(r'[\u30A1-\u30F4]+')
e = re.compile(r'[a-z]+')

#ストップワード
#https://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/English.txt
#https://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt
with open("slothlib_e.txt", "r") as f:
    sloth_english = f.read()
    sloth_english = [t for t in sloth_english.split("\n") if t != ""]

with open("slothlib_j.txt", "r", encoding="utf-8") as f:
    sloth_japanese = f.read()
    sloth_japanese = [t for t in sloth_japanese.split("\n") if t != ""]

d_li = sloth_english + sloth_japanese
d_li += ["成る", "遣る", "為る",  "居る", "有る"]
d_li += ["無い", "良い", "行く"]


#形態素分解
def get_words(text):
    #ルビ部分の独立と記号除去
    text = text.replace("！", "!")
    text = text.replace("(", " ").replace(")", " ").replace("!", " ").replace("?", " ")
    text = p.sub('', text)
    
    m = MeCab.Tagger()
    m.parse('') 
    node = m.parseToNode(text)
    word_list = []
    while node:
        pos = node.feature.split(",")[0]
        if pos in ["名詞", "形状詞"]: 
            w = node.surface
            word_list.append(w)
        elif pos in ["動詞", "形容詞"]:
            w = node.feature.split(",")[7]
            if "-" in w:
                w = w.split("-")[0]
            word_list.append(w)
        node = node.next
    
    #小文字化
    word_list = [w.lower() for w in word_list]
    
    #数字消す
    word_list = [w for w in word_list if not w.isdecimal()]

    #英語消す
    #word_list = [w for w in word_list if not e.fullmatch(w)]
            
    #ひらがなカタカタの1文字消す
    word_list = [w for w in word_list if not (len(w) == 1 and (h.fullmatch(w) or k.fullmatch(w)))]
                
    #ストップワード消す
    word_list = [w for w in word_list if w not in d_li]

    return word_list

#WordCLoud
wordcloud = WordCloud(background_color="white", font_path='C:/Windows/Fonts/BIZ-UDMinchoM.ttc', width=1500,height=1000,min_font_size=7, collocations = False)
def create_cloud(li):
    words = " ".join(li)
    wordcloud.generate(words)
    wordcloud.to_file("wordcloud_samd.png")

#歌詞
with open("input_file_sand.txt", "r", encoding="utf-8") as f:
    text = f.read()
text = text.replace("\n", " ")

# df =pd.read_csv("C:\\Users\\Hakuta_Yuki\\Desktop\\csv\\songs_椎名林檎_2022-06-15.csv")
# #全部の歌詞
# text = ""
# for t in df["歌詞"]:
#     text += f" {t}"

#リスト化
word_list = get_words(text)

#WordCloud化
create_cloud(word_list)