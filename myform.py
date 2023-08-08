from tkinter import *
from tkinter import ttk
import pickle

import  myform

global g_name
global g_pass
global g_code
global g_go

def runTrade():

    myform.g_go = 1

    myform.g_name = v_name.get()
    myform.g_pass = v_pass.get()
    myform.g_code = v_code.get()

    previous_input = {"name": myform.g_name, "pass": myform.g_pass, "code": myform.g_code}
    with open("previous_input.pkl", "wb") as f:
        pickle.dump(previous_input, f)

    # print(f"{},{v_pass.get()},{v_code.get()},zzzx")

    root.destroy()


#
#　最初のメニューを表示する
#
def init(f_v_name):
    global root
    global v_name
    global v_pass
    global v_code

    myform.g_go = 0
    myform.g_name = ""
    myform.g_pass = ""
    myform.g_code = ""

    # ウィンドウを作成
    root = Tk()

    # ウィンドウサイズを指定
    root.geometry("320x240")

    # ウィンドウタイトルを指定
    root.title(f_v_name)

    #グリッドの宣言
    frame1 = ttk.Frame(root, padding=(32))
    frame1.grid()

    # 会員ID
    label1 = ttk.Label(frame1, text='会員ID', padding=(5, 2))
    label1.grid(row=0, column=0, sticky=E)

    # パスワード
    label2 = ttk.Label(frame1, text='パスワード', padding=(5, 2))
    label2.grid(row=1, column=0, sticky=E)

    # 銘柄コード
    label3 = ttk.Label(frame1, text='銘柄コード', padding=(5, 2))
    label3.grid(row=2, column=0, sticky=E)



    # 会員ID
    v_name = StringVar()
    name_txt = ttk.Entry(
        frame1,
        textvariable=v_name,
        width=20)
    name_txt.grid(row=0, column=1)

    # パスワード
    v_pass = StringVar()
    pass_txt = ttk.Entry(
        frame1,
        textvariable=v_pass,
        width=20)
    pass_txt.grid(row=1, column=1)

    # 銘柄コード
    v_code = StringVar()
    code_txt = ttk.Entry(
        frame1,
        textvariable=v_code,
        width=20)
    code_txt.grid(row=2, column=1)

    #事前のデータがあれば読み込む。
    try:
        with open("previous_input.pkl", "rb") as f:
            previous_input = pickle.load(f)
            name_txt.insert(0, previous_input["name"])
            pass_txt.insert(0, previous_input["pass"])
            code_txt.insert(0, previous_input["code"])
    except FileNotFoundError:
        pass

    # Button
    button1 = ttk.Button(
        frame1, text='実行',
        command=runTrade)
    button1.grid(row=3, column=1)

    # ウィンドウ表示継続
    root.mainloop()

