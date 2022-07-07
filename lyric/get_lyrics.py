import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime

dic = np.load('lyric/dic/artists_id.npy', allow_pickle=True)
dic = dic.item() #ndarrayを辞書型に変換

def jugde_exist(artist):
    global dic
    if artist in dic:
        return True
    else:
        return False

def get_lyrics(artist):
    num = dic[artist]
    res = requests.get(f"https://www.uta-net.com{num}")
    soup = BeautifulSoup(res.text, "html.parser")

    #ページ数を持ってくる
    j = soup.select_one(".col-7.col-lg-3.text-start.text-lg-end").get_text()
    j = j.split("ページ")[0]
    j = j.replace("全", "")
    page = int(j)  
    
    #曲のURL持ってくる(ページ数分の繰り返し)
    songs = []
    for p in range(page):
        res = requests.get(f"https://www.uta-net.com{num}/0/{p+1}/")
        soup = BeautifulSoup(res.text, "html.parser")
        for i in soup.select(".border-bottom"):
            for j in i.select(".sp-w-100.pt-2"):
                song = j.select_one("a").get_text()
                song_id = j.select_one("a").get("href")
                songs.append(song_id)
    #曲数分繰り返す
    titles = []
    lyricists = []
    composers = []
    dates = []
    views = []
    lyrics = []
    real_lyrics = []
    lyrics_len = []

    for s in songs:
        res = requests.get(f"https://www.uta-net.com{s}")
        soup = BeautifulSoup(res.text, "html.parser")
        
        title = soup.select_one(".ms-2.ms-md-3").get_text()

        info_l = []
        info = soup.select_one(".ms-2.ms-md-3.detail.mb-0")
        for i in info.children:
            ele = i.get_text()
            ele = ''.join(ele.split())
            if ele != "":
                info_l.append(ele)
        if len(info_l) == 6:
            lyricist = info_l[1] 
            composer = info_l[3]

            date = info_l[4].split("：")[1]
            date = date.split("/")
            date = datetime.date(int(date[0]),int(date[1]),int(date[2]))

            view = info_l[5].split("：")[1]
            view = view.replace(",", "")
            view = view.replace("回", "")
            view = int(view)
            
            real_lyric = soup.select_one("#kashi_area").get_text()
            lyric_length = len(soup.select_one("#kashi_area").get_text())

            lyric = soup.select_one("#kashi_area")
            lyric = str(lyric)
            lyric = lyric.replace('<div id="kashi_area" itemprop="text">', "")
            lyric = lyric.replace("</div>", "")
            lyric = lyric.replace("<br/>", "\n")
            lyric = lyric.replace("\u3000", " ")

            titles.append(title)
            lyricists.append(lyricist)
            composers.append(composer)
            dates.append(date)
            views.append(view)
            lyrics.append(lyric)
            real_lyrics.append(real_lyric)
            lyrics_len.append(lyric_length)

    df = pd.DataFrame(list(zip(titles, lyricists, composers, dates, views, lyrics, lyrics_len, real_lyrics)), 
        columns=["タイトル", "作詞", "作曲", "発売日", "表示回数", "改行入り歌詞", "文字数", "歌詞"])

    return df,len(songs)

def get_long(df):
    li = []
    length = 0
    for i in range(len(df)):
        l = df["文字数"][i]
        length = max(l,length)
    for i in range(len(df)):
        if df["文字数"][i] == length:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def get_short(df):
    li = []
    length = 1000000
    for i in range(len(df)):
        l = df["文字数"][i]
        length = min(l,length)
    for i in range(len(df)):
        if df["文字数"][i] == length:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def get_new_date(df):
    li = []
    new_date = datetime.date(1800, 1, 1)
    for i in range(len(df)):
        d = df["発売日"][i]
        new_date = max(d, new_date)
    for i in range(len(df)):
        if df["発売日"][i] == new_date:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def get_old_date(df):
    li = []
    old_date = datetime.date.today()
    for i in range(len(df)):
        d = df["発売日"][i]
        old_date = min(d, old_date)
    for i in range(len(df)):
        if df["発売日"][i] == old_date:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def get_max_view(df):
    li = []
    view = 0
    for i in range(len(df)):
        v = df["表示回数"][i]
        view = max(v, view)
    for i in range(len(df)):
        if df["表示回数"][i] == view:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def get_min_view(df):
    li = []
    view = 10000000000000
    for i in range(len(df)):
        v = df["表示回数"][i]
        view = min(v, view)
    for i in range(len(df)):
        if df["表示回数"][i] == view:
            li.append([df["タイトル"][i], df["作詞"][i], df["作曲"][i], df["発売日"][i], "{:,}".format(df["表示回数"][i]), df["改行入り歌詞"][i], df["文字数"][i]])
    return li

def refresh_dic():
    dic = {}
    names = []
    nums = []

    res = requests.get(f"https://www.uta-net.com/name_list/")
    soup = BeautifulSoup(res.text, "html.parser").select_one("#kana-navi1")

    for i in soup.select("a.hover"):
        try:
            kana = i.get("href")
            res = requests.get(f"https://www.uta-net.com{kana}")
            soup = BeautifulSoup(res.text, "html.parser")

            #各歌手
            for a in soup.select("p.flex-glow a"):
                name = a.get_text()
                num = a.get("href")
                names.append(name)
                nums.append(num)
                dic[name] = num

        except Exception as e:
            print(e)
            print(name,num)

    #歌手IDの辞書
    np.save(f'lyric/dic/artists_id.npy', dic)

def out_csv(df, path):
    df_out = df[df.columns[df.columns != '改行入り歌詞']]
    df_out.to_csv(path, index=False)