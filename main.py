import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog

from lyric import get_lyrics as gl

now = str(datetime.now()).split(" ")[0]

try:
    haikei1 = "#EEFFFF"
    haikei2 = "#FFFFEE"
    haikei_kensaku = "#DDFFFF"
    button_color1 = "#FFBEDA"
    button_color2 = "#A4C6FF"
    button_color3 = "#FFBEDA"
    button_color4 = "#A4C6FF"
    button_color5 = "#FFBEDA"
    button_color6 = "#A4C6FF"    

    #大元
    root = tk.Tk()
    root.configure(bg=haikei1)
    root.title(u"歌詞を探してくれる川島海荷")
    root.geometry("780x450+400+50")
    iconfile = 'img/img.ico'
    root.iconbitmap(default=iconfile)
    df = None
    flag = None

    def out1(n):
        global df, get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag
        if n == "":
            left_3_c1.delete("all")
            left_3_c1.create_image(80, 100, image = img_morning, tag = "morning")

        else:
            #右側削除
            right_del()
            get_long_count = 0
            get_short_count = 0
            get_old_count = 0
            get_new_count = 0
            get_max_view_count = 0
            get_min_view_count = 0

            if gl.jugde_exist(n):   
                #検索中
                finding_show()  

                judge = messagebox.askyesno("確認だよ", "探してきていい？")
                if judge == True:
                    #検索結果を格納
                    df, song_num = gl.get_lyrics(n)
                    #検索終了
                    left_2_l1['text'] = f"{n}（{song_num}曲）"
                    left_3_c1.delete("all")
                    left_3_c1.create_image(60, 100, image = img_found, tag = "found")
                    get_long(df)
                    flag = "long"
                else:
                    df = None
                    left_2_l1['text'] = "アーティスト名"
                    left_3_c1.delete("all")
                    left_3_c1.create_image(80, 100, image = img_morning, tag = "morning")

            elif n == "川島海荷":
                df = None
                flag = None
                left_2_l1['text'] = "アーティスト名"
                left_3_c1.delete("all")
                left_3_c1.create_image(90, 100, image = img_yonda, tag = "yonda")

            else:
                df = None
                flag = None
                left_2_l1['text'] = "アーティスト名"
                left_3_c1.delete("all")
                left_3_c1.create_image(90, 120, image = img_daredayo, tag = "daredayo")

    def finding_show():
        left_3_c1.delete("all")
        left_3_c1.create_image(75, 100, image = img_finding, tag = "finding")

    def right_del():
        right_f1_1_t1.delete(0, tk.END)
        right_f1_2_t1.delete(0, tk.END)
        right_f1_3_t1.delete(0, tk.END)
        right_f1_4_t1.delete(0, tk.END)
        right_f1_5_t1.delete(0, tk.END)
        right_f2_e1.delete("1.0","end")
        right_f2_f1_l1["text"] = "歌詞"

    def refresh_dic():
        #検索中
        finding_show()

        judge = messagebox.askyesno("確認だよ", "辞書更新していい？")
        if judge == True:
            gl.refresh_dic()
            left_3_c1.delete("all")
            left_3_c1.create_image(74, 100, image = img_refresh, tag = "refresh")
        else:
            left_3_c1.delete("all")
            left_3_c1.create_image(80, 100, image = img_morning, tag = "morning")

    def right_insert(sl, s, l):
        global flag
        right_f1_1_t1.insert(tk.END,sl[0])
        right_f1_2_t1.insert(tk.END,sl[1])
        right_f1_3_t1.insert(tk.END,sl[2])
        right_f1_4_t1.insert(tk.END,sl[3])
        right_f1_5_t1.insert(tk.END,sl[4])
        right_f2_e1.insert(1.0, sl[-2])
        if flag == "long":
            insert_text = f"＜一番長い歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        elif flag == "short":
            insert_text = f"＜一番短い歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        elif flag == "old":
            insert_text = f"＜一番古い歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        elif flag == "new":
            insert_text = f"＜一番新しい歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        elif flag == "max":
            insert_text = f"＜一番見られてる歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        elif flag == "min":
            insert_text = f"＜一番見られてない歌詞（{sl[-1]}文字） {l}曲中{s+1}曲目＞"
        right_f2_f1_l1["text"] = insert_text

    def get_long(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_short_count = 0
        get_old_count = 0
        get_new_count = 0
        get_max_view_count = 0
        get_min_view_count = 0
        flag = "long"

        right_del()
        li = gl.get_long(df)
        song = get_long_count%len(li)
        right_insert(li[song], song, len(li))    
        get_long_count += 1

    def get_short(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count = 0
        get_old_count = 0
        get_new_count = 0
        get_max_view_count = 0
        get_min_view_count = 0
        flag = "short"

        right_del()
        li = gl.get_short(df)
        song = get_short_count%len(li)
        right_insert(li[song], song, len(li))  
        get_short_count += 1

    def get_old(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count = 0
        get_short_count = 0
        get_new_count = 0
        get_max_view_count = 0
        get_min_view_count = 0
        flag = "old"

        right_del()
        li = gl.get_old_date(df)
        song = get_old_count%len(li)
        right_insert(li[song], song, len(li))  
        get_old_count += 1

    def get_new(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count = 0
        get_short_count = 0
        get_old_count = 0
        get_max_view_count = 0
        get_min_view_count = 0
        flag = "new"

        right_del()
        li = gl.get_new_date(df)
        song = get_new_count%len(li)
        right_insert(li[song], song, len(li))  
        get_new_count += 1

    def get_max_view(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count = 0
        get_short_count = 0
        get_old_count = 0
        get_new_count = 0
        get_min_view_count = 0
        flag = "max"

        right_del()
        li = gl.get_max_view(df)
        song = get_max_view_count%len(li)
        right_insert(li[song], song, len(li))  
        get_max_view_count += 1

    def get_min_view(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count = 0
        get_short_count = 0
        get_old_count = 0
        get_new_count = 0
        get_max_view_count = 0
        flag = "min"

        right_del()
        li = gl.get_min_view(df)
        song = get_min_view_count%len(li)
        right_insert(li[song], song, len(li))  
        get_min_view_count += 1

    def lyric_up(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        right_del()
        if flag == "long":
            li = gl.get_long(df)
            song = get_long_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_long_count += 1
        elif flag == "short":
            li = gl.get_short(df)
            song = get_short_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_short_count += 1
        elif flag == "old":
            li = gl.get_old_date(df)
            song = get_old_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_old_count += 1
        elif flag == "new":
            li = gl.get_new_date(df)
            song = get_new_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_new_count += 1
        elif flag == "max":
            li = gl.get_max_view(df)
            song = get_max_view_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_max_view_count += 1
        elif flag == "min":
            li = gl.get_min_view(df)
            song = get_min_view_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_min_view_count += 1

    def lyric_down(df):
        global get_long_count, get_short_count, get_old_count, get_new_count, get_max_view_count, get_min_view_count, flag

        get_long_count -= 2
        get_short_count -= 2
        get_old_count -= 2
        get_new_count -= 2
        get_max_view_count -= 2
        get_min_view_count -= 2

        right_del()
        if flag == "long":
            li = gl.get_long(df)
            song = get_long_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_long_count += 1
        elif flag == "short":
            li = gl.get_short(df)
            song = get_short_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_short_count += 1
        elif flag == "old":
            li = gl.get_old_date(df)
            song = get_old_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_old_count += 1
        elif flag == "new":
            li = gl.get_new_date(df)
            song = get_new_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_new_count += 1
        elif flag == "max":
            li = gl.get_max_view(df)
            song = get_max_view_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_max_view_count += 1
        elif flag == "min":
            li = gl.get_min_view(df)
            song = get_min_view_count%len(li)
            right_insert(li[song], song, len(li)) 
            get_min_view_count += 1

    def out_csv(df, artist):
        global flag
        if flag in ["long", "short", "old", "new", "max", "min"]:
            target_dir = filedialog.askdirectory()
            if target_dir != "":
                path = f"{target_dir}/songs_{artist}_{now}.csv"
                gl.out_csv(df, path)
                messagebox.showinfo('確認してね', '書き出したよ！')

    style = ttk.Style()

    #左
    left = tk.Frame(root, background=haikei1)

    #検索窓
    left_1 = ttk.Frame(left, padding = 20, relief='sunken', style="kensaku.TFrame")
    t = tk.StringVar()
    left_1_l1 = ttk.Label(left_1, text = "＜アーティスト名＞", style="kensaku.TLabel", font=("Arial", 11, "bold"))
    left_1_e1 = ttk.Entry(left_1, textvariable = t, width=30)
    left_1_b1 = ttk.Button(left_1, text = "検索", width =7, padding = 2,  command = lambda: out1(t.get()))
    style.configure("kensaku.TFrame", background=haikei_kensaku)
    style.configure("kensaku.TLabel", background=haikei_kensaku)

    #ボタンスペース
    left_2 = ttk.Frame(left, padding = 20, style="left.TFrame")
    left_2_l1 = ttk.Label(left_2, text = "アーティスト名", style="left.TLabel")
    button_size = 18
    left_2_b1 = ttk.Button(left_2, text = "一番長い歌", style="button1.TButton", padding = 5, width = button_size , command = lambda: get_long(df))
    left_2_b2 = ttk.Button(left_2, text = "一番短い歌", style="button2.TButton", padding = 5,  width = button_size, command = lambda: get_short(df))
    left_2_b3 = ttk.Button(left_2, text = "一番新しい歌", style="button3.TButton", padding = 5,  width = button_size, command = lambda: get_new(df))
    left_2_b4 = ttk.Button(left_2, text = "一番古い歌", style="button4.TButton", padding = 5,  width = button_size, command = lambda: get_old(df))
    left_2_b5 = ttk.Button(left_2, text = "一番見られてる歌", style="button5.TButton", padding = 5,  width = button_size, command = lambda: get_max_view(df))
    left_2_b6 = ttk.Button(left_2, text = "一番見られてない歌", style="button6.TButton", padding = 5, width = button_size, command = lambda: get_min_view(df))
    left_2_l2 = ttk.Label(left_2, text = f"※{now}現在", style="left.TLabel")
    left_2_b7 = ttk.Button(left_2, text = "csv出力", padding = 3, width = 10, command = lambda: out_csv(df, t.get()))
    style.configure("button1.TButton", background=button_color1)
    style.configure("button2.TButton", background=button_color2)
    style.configure("button3.TButton", background=button_color3)
    style.configure("button4.TButton", background=button_color4)
    style.configure("button5.TButton", background=button_color5)
    style.configure("button6.TButton", background=button_color6)

    #川島海荷
    left_3 = ttk.Frame(left, padding = 20, style="left.TFrame")
    style.configure("left.TFrame", background=haikei1)
    style.configure("left.TLabel", background=haikei1)

    img_morning = tk.PhotoImage(file = "img/morning_1.png")
    img_daredayo = tk.PhotoImage(file = "img/daredayo.png")
    img_found = tk.PhotoImage(file = "img/umika_found.png")
    img_finding = tk.PhotoImage(file = "img/umika_finding.png")
    img_refresh = tk.PhotoImage(file = "img/umika_refresh.png")
    img_yonda = tk.PhotoImage(file = "img/umika_me.png")

    left_3_c1 = tk.Canvas(left_3, height = 200, width =170,bd=0, highlightthickness=0)
    left_3_c1.create_image(80, 100, image = img_morning, tag = "morning")
    left_3_b1 = ttk.Button(left_3, text = "※辞書更新", padding = 3, width = 10, command = lambda: refresh_dic())

    #右
    right = ttk.Frame(root, padding = 10, relief='ridge', style="right.TFrame")
    style.configure("right.TFrame", background=haikei2)
    style.configure("right.TLabel", background=haikei2)

    #情報
    right_f1_1 = ttk.Frame(right, padding = 5, height=20, width=100, style="right.TFrame")
    right_f1_1_l1 = ttk.Label(right_f1_1, text = "＜曲名＞　　 ", style="right.TLabel")
    right_f1_1_t1 = ttk.Entry(right_f1_1, width=30)
    right_f1_1_b1 = ttk.Button(right_f1_1, text = "<", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_1_b2 = ttk.Button(right_f1_1, text = ">", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_2 = ttk.Frame(right, padding = 5, height=20, width=100, style="right.TFrame")
    right_f1_2_l1 = ttk.Label(right_f1_2, text = "＜作詞＞　　 ", style="right.TLabel")
    right_f1_2_t1 = ttk.Entry(right_f1_2, width=30)
    right_f1_2_b1 = ttk.Button(right_f1_2, text = "<", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_2_b2 = ttk.Button(right_f1_2, text = ">", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_3 = ttk.Frame(right, padding = 5, height=20, width=100, style="right.TFrame")
    right_f1_3_l1 = ttk.Label(right_f1_3, text = "＜作曲＞　　 ", style="right.TLabel")
    right_f1_3_t1 = ttk.Entry(right_f1_3, width=30)
    right_f1_3_b1 = ttk.Button(right_f1_3, text = "<", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_3_b2 = ttk.Button(right_f1_3, text = ">", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_4 = ttk.Frame(right, padding = 5, height=20, width=100, style="right.TFrame")
    right_f1_4_l1 = ttk.Label(right_f1_4, text = "＜発売日＞　 ", style="right.TLabel")
    right_f1_4_t1 = ttk.Entry(right_f1_4, width=30)
    right_f1_4_b1 = ttk.Button(right_f1_4, text = "<", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_4_b2 = ttk.Button(right_f1_4, text = ">", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_5 = ttk.Frame(right, padding = 5, height=20, width=100, style="right.TFrame")
    right_f1_5_l1 = ttk.Label(right_f1_5, text = "＜表示回数＞ ", style="right.TLabel")
    right_f1_5_t1 = ttk.Entry(right_f1_5, width=30)
    right_f1_5_b1 = ttk.Button(right_f1_5, text = "<", padding = 0.5, width = 1 , command = lambda: get_long(df))
    right_f1_5_b2 = ttk.Button(right_f1_5, text = ">", padding = 0.5, width = 1 , command = lambda: get_long(df))

    #歌詞
    right_f2 = ttk.Frame(right, padding = 10, height=80, width=100, style="right.TFrame")
    right_f2_f1 = ttk.Frame(right_f2, padding = 4, height=80, width=100, style="right.TFrame")
    right_f2_f1_l1 = tk.Label(right_f2_f1, text = "＜歌詞＞", background=haikei2)
    right_f2_f1_b1 = ttk.Button(right_f2_f1, text = "<", padding = 0.5, width = 1 , command = lambda: lyric_down(df))
    right_f2_f1_b2 = ttk.Button(right_f2_f1, text = ">", padding = 0.5, width = 1 , command = lambda: lyric_up(df))
    right_f2_e1 = tk.Text(right_f2, height=60, width=50, font=("MS明朝", "10"))

    #配置
    left.pack(side = tk.LEFT, anchor = tk.N)

    left_1.pack(side = tk.TOP)
    left_1_l1.pack(side = tk.TOP)
    left_1_e1.pack(side = tk.LEFT)
    left_1_b1.pack(side = tk.LEFT)

    left_3.pack(side = tk.LEFT)
    left_3_c1.pack()
    left_3_b1.pack()

    left_2.pack(side = tk.LEFT, anchor=tk.CENTER)
    left_2_l1.pack(side = tk.TOP)
    left_2_b1.pack(side = tk.TOP, pady = 5)
    left_2_b2.pack(side = tk.TOP, pady = 5)
    left_2_b3.pack(side = tk.TOP, pady = 5)
    left_2_b4.pack(side = tk.TOP, pady = 5)
    left_2_b5.pack(side = tk.TOP, pady = 5)
    left_2_b6.pack(side = tk.TOP, pady = 5)
    left_2_l2.pack(side = tk.TOP)
    left_2_b7.pack(side = tk.TOP)

    right.pack(side = tk.LEFT, anchor = tk.N)

    right_f1_1.pack(side = tk.TOP)
    right_f1_1_l1.pack(side = tk.LEFT)
    right_f1_1_t1.pack(side = tk.LEFT)
    #right_f1_1_b1.pack(side = tk.LEFT)
    #right_f1_1_b2.pack(side = tk.LEFT)
    right_f1_2.pack(side = tk.TOP)
    right_f1_2_l1.pack(side = tk.LEFT)
    right_f1_2_t1.pack(side = tk.LEFT)
    #right_f1_2_b1.pack(side = tk.LEFT)
    #right_f1_2_b2.pack(side = tk.LEFT)
    right_f1_3.pack(side = tk.TOP)
    right_f1_3_l1.pack(side = tk.LEFT)
    right_f1_3_t1.pack(side = tk.LEFT)
    #right_f1_3_b1.pack(side = tk.LEFT)
    #right_f1_3_b2.pack(side = tk.LEFT)
    right_f1_4.pack(side = tk.TOP)
    right_f1_4_l1.pack(side = tk.LEFT)
    right_f1_4_t1.pack(side = tk.LEFT)
    #right_f1_4_b1.pack(side = tk.LEFT)
    #right_f1_4_b2.pack(side = tk.LEFT)
    right_f1_5.pack(side = tk.TOP)
    right_f1_5_l1.pack(side = tk.LEFT)
    right_f1_5_t1.pack(side = tk.LEFT)
    #right_f1_5_b1.pack(side = tk.LEFT)
    #right_f1_5_b2.pack(side = tk.LEFT)

    right_f2.pack(side = tk.TOP)
    right_f2_f1.pack(side = tk.TOP)
    right_f2_f1_l1.pack(side = tk.LEFT)
    right_f2_f1_b1.pack(side = tk.LEFT)
    right_f2_f1_b2.pack(side = tk.LEFT)
    right_f2_e1.pack(side = tk.TOP)

    #表示開始
    root.mainloop()

except Exception as e:
    print(e)

#pyinstaller --name 歌詞を探してくれる川島海荷.exe --onefile --noconsole --icon=img/img.ico main.py