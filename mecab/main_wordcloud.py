import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from func import judge_exist, get_lyrics
from keitaiso import get_words, create_cloud

def create(text):
    if judge_exist(text):
        j1 = messagebox.askyesno("確認", f"{text}の歌詞でWordCloudを作成しますか？")
        if j1:
            df,length = get_lyrics(text)
            f2_l1['text'] = f"{text}（{length}曲）"

            lyric = ""
            for t in df["歌詞"]:
                lyric += f" {t}"

            #リスト化
            word_list = get_words(lyric)

            #作成
            create_cloud(word_list)
            img = tk.PhotoImage(file = "default_cloud.png", height = 337, width =600)
            #f2_c1.delete("all")
            f2_c1.create_image(320, 177, image = img, tag = "new")
            messagebox.showinfo('確認', '書き出し完了')
    else:
        messagebox.showerror("error", "だれ？？")

try:
    #大元
    root = tk.Tk()
    root.title(u"wordcloud")
    root.geometry("680x550+400+50")

    #検索窓
    f1 = ttk.Frame(root, padding = 10, relief='sunken')
    t = tk.StringVar()
    f1_l1 = ttk.Label(f1, text = "＜アーティスト名＞")
    f1_e1 = ttk.Entry(f1, textvariable = t, width=30)
    f1_b1 = ttk.Button(f1, text = "wordcloud作成", width =15, padding = 4,  command = lambda: create(t.get()))

    #WordCloud
    f2 = ttk.Frame(root, padding = 10, relief='sunken')
    f2_l1 = ttk.Label(f2, text = "アーティスト名")
    img = tk.PhotoImage(file = "default_cloud.png", height = 337, width =600)
    f2_c1 = tk.Canvas(f2, height = 350, width =630)
    f2_c1.place(x=0, y=0)
    f2_c1.create_image(320, 177, image = img, tag = "morning")

    f1.pack()
    f1_l1.pack(side = tk.LEFT)
    f1_e1.pack(side = tk.LEFT)
    f1_b1.pack(side = tk.LEFT)

    f2.pack()
    f2_l1.pack()
    f2_c1.pack()


    #表示開始
    root.mainloop()

except Exception as e:
    messagebox.showerror("error", e)