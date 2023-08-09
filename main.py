import tkinter as tk
import pickle
import time
import datetime

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import sbiweb as sbi
import test

DISP_MODE = "ON"   # "ON" or "OFF"

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Form")
        self.geometry("350x400")

        self.entries = {}
        self.submitted_data = None

        self.create_label_entry("ユーザーネーム", "g_username")
        self.create_label_entry("ログインパスワード", "g_loginpass")
        self.create_label_entry("発注パスワード", "g_ordpass")
        self.create_label_entry("メールアドレス", "g_mailaddr")
        self.create_label_entry("メールパスワード", "g_mailpass")
        self.create_label_entry("指値金額", "g_setorder")
        self.create_label_entry("購入単元数", "g_lot")
        self.create_label_entry("市場", "g_market")
        self.create_label_entry("銘柄コード", "g_code")

        self.load_previous_input()

        self.submit_button = tk.Button(self, text="　トレード開始　", command=self.submit, bg="red", fg="white")
        self.submit_button.pack(pady=10)

    def create_label_entry(self, label_text, key):
        frame = tk.Frame(self)
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, width=16, anchor='e')
        label.pack(side=tk.LEFT, padx=(0, 5))

        entry = tk.Entry(frame, width=30)
        entry.pack(side=tk.LEFT)

        self.entries[key] = entry

    def load_previous_input(self):
        try:
            with open("new_previous_input.pkl", "rb") as f:
                previous_input = pickle.load(f)
                for key, entry in previous_input.items():
                    entry_widget = self.entries[key]
                    entry_widget.insert(0, entry)
        except FileNotFoundError:
            pass

    def submit(self):
        submitted_data = {}
        for key in ["g_username", "g_loginpass", "g_ordpass", "g_mailaddr", "g_mailpass", "g_setorder", "g_lot",
                    "g_market", "g_code", ]:
            entry_widget = self.entries[key]
            input_text = entry_widget.get()
            submitted_data[key] = input_text
            # print(f"Submitted {key}: {input_text}")

        with open("new_previous_input.pkl", "wb") as f:
            pickle.dump(submitted_data, f)

        self.submitted_data = submitted_data
        self.destroy()


if __name__ == "__main__":
    #test.test1()
    #exit(0)

    app = Application()
    app.mainloop()
    user_input = app.submitted_data
    ret = 0

    if user_input is not None:
        if DISP_MODE == "OFF":
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        else:
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                # 自動でPCのChromeと同じバージョンのdriverをインストールする処理
                # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            except:
                # 例外発生時、配布されているもののうち最新のdriverをインストールする処理
                res = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
                options = Options()
                driver = webdriver.Chrome(service=Service(ChromeDriverManager(res.text).install()), options=options)

        #print(type(driver))

        ret = sbi.sbiIpoLogin(driver, user_input)   #ログイン
        if ret == 0:    #ログイン完了
            #注文可能になるまで待ち、注文可能になったら注文を入れる
            """
            for retry in range(2000):
                dt_now = datetime.datetime.now()
                orderEnable = sbi.sbiGotoSpotPurchase(driver,user_input)  #現物買いページにジャンプ
                if orderEnable == 1:
                    sbi.sbiOrderExecute(driver,user_input)
                    dt_now = datetime.datetime.now()
                    print('注文日時：' ,dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
                    break;
                else:
                    time.sleep(10)
            """
            orderEnable = sbi.sbiGotoSpotPurchase(driver, user_input)  # 現物買いページにジャンプ

            for retry in range(2000):
                ret1 = sbi.sbiWatchStock(driver, user_input)   #銘柄板情報に飛ぶ
                if ret1 == 0: #継続
                    driver.refresh()
                elif ret1 == 1: #注文完了
                    print(f"注文完了しましたよーー")
                    break
                elif ret1 == 2: #大引け
                    print(f"大引けーー")
                    break

            print(f"ret={ret}")
            time.sleep(1800) #このスリープ中（３０分）に注文内容を確認してねーー
            sbi.sbiLogOut(driver)                   #ログアウト

        driver.quit()

        print(f"ret={ret}")

    else:
        print("quit!")
