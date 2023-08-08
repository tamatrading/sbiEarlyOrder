import tkinter as tk

def submit():
    global input_data
    input_data = input_var.get()
    print("入力内容:", input_data)
    root.destroy()

def create_form():
    # ウィンドウの作成
    global root

    root = tk.Tk()
    root.title("フォーム入力画面")

    # 入力欄と関連するStringVarの作成
    global input_var
    input_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=input_var)
    entry.pack()

    # ボタンの作成と配置
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    root.mainloop()

# グローバル変数の初期化
input_data = ""
