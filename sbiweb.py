#selenium起動

import selenium.webdriver.chrome.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import common as Co

#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options

#gmail
from gmail import sendGmail

# 指定時間待機
import time
import re

# マウスやキーボード操作に利用
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

# セレクトボックスの選択に利用
from selenium.webdriver.support.ui import Select

#-----------------------------
#SBI証券の口座でIPOのBB申込を行なう
#-----------------------------
def sbiIpoLogin(driver:selenium.webdriver.chrome.webdriver.WebDriver, in_data):
    # サイトを開く
    driver.get("https://www.sbisec.co.jp/ETGate")

    locator = (By.NAME, "ACT_login")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))

    # ユーザID、パスワードを入力
    driver.find_element(by=By.NAME, value="user_id").send_keys(in_data["g_username"])
    driver.find_element(by=By.NAME, value="user_password").send_keys(in_data["g_loginpass"])

    # ログインをクリック
    driver.find_element(by=By.NAME, value="ACT_login").click()

    time.sleep(3)

    # name属性で指定
    try:
        moneyTag = driver.find_element(by=By.XPATH,
                                       value="/html/body/table/tbody/tr[1]/td[1]/div[1]/div/div[2]/div[1]/div/div/div/span/p")
    except NoSuchElementException:
        tmp = driver.find_elements(by=By.XPATH, value="//b[contains(text(),'重要なお知らせ')]")
        if len(tmp) >= 1:
            ii = -1
        else:
            ii = -2
        return ii

    # 投資可能額が表示されるまで待機
    locator = (By.XPATH, "/html/body/table/tbody/tr[1]/td[1]/div[1]/div/div[2]/div[1]/div/div/div/span/p")
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))

    money = int(moneyTag.text.replace(",", "").replace("円", ""))
    print(money)

    return 0

#-----------------------------
#ログアウトする
#-----------------------------
def sbiLogOut(driver:selenium.webdriver.chrome.webdriver.WebDriver):
    try:
        driver.find_element(by=By.XPATH, value="//img[@title='ログアウト']").click()
    except NoSuchElementException:
        print("err")
        sendIpoMail(-3)
        return

#-----------------------------
#ログイン画面から「現物買い」ページにジャンプする
#-----------------------------
def sbiGotoSpotPurchase(driver:selenium.webdriver.chrome.webdriver.WebDriver, in_data):
    # 銘柄情報ページにジャンプ
    driver.find_element(by=By.NAME, value="i_stock_sec").send_keys(in_data["g_code"])
    driver.find_element(by=By.XPATH, value="//img[@title='株価検索']").click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)

    tmp = driver.find_elements(by=By.XPATH, value="//td[contains(text(),'対象銘柄はありません。または、表示できません。')]")
    if len(tmp) > 0:
        print("対象銘柄はありません")
        return 0

    locator = (By.XPATH, "//img[@title='自動更新稼動']")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))
    driver.find_element(by=By.XPATH, value="//img[@title='自動更新稼動']").click()

    # 現物買ページにジャンプ
    driver.find_element(by=By.XPATH, value="/html/body/div[4]/div/table/tbody/tr/td[1]/div/form[2]/div[4]/div[2]/div[1]/table/tbody/tr/td[1]/p/a").click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)

    return 1


# -----------------------------
# 現物買注文をおこなう。
# -----------------------------
def sbiOrderExecute(driver:selenium.webdriver.chrome.webdriver.WebDriver, in_data):

    # ボタンを設定する
    status = driver.find_element(by=By.NAME, value="sor_flg").is_selected()
    if status == True:  # SORにチェックが入っている場合には、チェックを外す
        driver.find_element(by=By.NAME, value="sor_flg").click()
    driver.find_element(by=By.NAME, value="input_market").send_keys(in_data["g_market"])  # 市場の入力
    driver.find_element(by=By.NAME, value="input_quantity").clear()  # 株数のクリア
    driver.find_element(by=By.NAME, value="input_quantity").send_keys(in_data["g_lot"])  # 株数の入力
    driver.find_element(by=By.ID, value="sashine").click()  # 「指値」ボタンをON
    driver.find_element(by=By.NAME, value="sasine_condition").send_keys("寄指")  # 指値種別の入力
    driver.find_element(by=By.NAME, value="input_price").send_keys(in_data["g_setorder"])
    print(f" Buy Order , {in_data['g_setorder']}")

    status = driver.find_element(by=By.NAME, value="skip_estimate").is_selected()
    if status == False:  # 注文確認画面を省略にチェックが入っていない場合には、チェックを付ける
        driver.find_element(by=By.NAME, value="skip_estimate").click()
    driver.find_element(by=By.NAME, value="trade_pwd").send_keys(in_data["g_ordpass"])  # 取引パスワード

    #driver.find_element(by=By.XPATH, value="//img[@title='注文発注']").click()

#-----------------------------
# 気配値を取得する
#-----------------------------
def sbiWatchKehai(driver:selenium.webdriver.chrome.webdriver.WebDriver, in_data):

    try:
        f_uri_kehai = Co.kehaiValue(driver.find_element(by=By.ID, value="MTB0_43").text)
        f_uri_kakaku = Co.toValue(driver.find_element(by=By.ID, value="MTB0_44").text)
        f_kai_kakaku = Co.toValue(driver.find_element(by=By.ID, value="MTB0_47").text)
        f_kai_kehai = Co.kehaiValue(driver.find_element(by=By.ID, value="MTB0_48").text)
    except Exception as e:
        f_uri_kehai = "", -1
        f_uri_kakaku = "", -1
        f_kai_kakaku = "", -1
        f_kai_kehai = "", -1

    return f_uri_kehai, f_uri_kakaku, f_kai_kehai, f_kai_kakaku
#    print(f"An error occurred: {e}")
#    print(f"{f_uri_kakaku}:{f_uri_hekai}  ===  {f_kai_hekai}:{f_kai_kakaku}")

#-----------------------------
#指定された銘柄コードの板情報を見に行く
#-----------------------------
def sbiWatchStock(driver:selenium.webdriver.chrome.webdriver.WebDriver, in_data):

    # ボタンを設定する
    status = driver.find_element(by=By.NAME, value="sor_flg").is_selected()
    if status == True:    #SORにチェックが入っている場合には、チェックを外す
        driver.find_element(by=By.NAME, value="sor_flg").click()
    driver.find_element(by=By.NAME, value="input_market").send_keys(in_data["g_market"])    #市場の入力
    driver.find_element(by=By.NAME, value="input_quantity").clear()    #株数のクリア
    driver.find_element(by=By.NAME, value="input_quantity").send_keys(in_data["g_lot"])    #株数の入力
    driver.find_element(by=By.ID, value="gyakusashine_gsn2").click()    #「逆指値」ボタンをON
    driver.find_element(by=By.ID, value="gyakusashine_sashine").click()    #「逆指値/成行」ボタンをON

#逆指値／指値／金額ボックス＝ id:gsn_input_price

    status = driver.find_element(by=By.NAME, value="skip_estimate").is_selected()
    if status == False:    #注文確認画面を省略にチェックが入っていない場合には、チェックを付ける
        driver.find_element(by=By.NAME, value="skip_estimate").click()
    driver.find_element(by=By.NAME, value="trade_pwd").send_keys(in_data["g_ordpass"])  #取引パスワード

    first = True

    # 始値がつくまで待機する
    for retry in range(100):
        kehai = sbiWatchKehai(driver, in_data)
        print(f"{retry}  売気配 {kehai[0][0]} {kehai[0][1]} : | {kehai[1]} || {kehai[3]} | : {kehai[2][0]} {kehai[2][1]} 買気配 ")

        try:
            #大引けになった場合の処理
            cTags = driver.find_elements(by=By.XPATH, value="//*[@id='MTB0_0']/span[3]")
            if len(cTags) > 0:
                if cTags[0].text == "C":
                    return 2

            #手動に戻った場合の処理
            shudo = driver.find_elements(by=By.XPATH, value="//img[@title='自動更新ON']")
            if len(shudo) > 0:
                driver.find_element(by=By.XPATH, value="//img[@title='自動更新ON']").click()

            moneyTag = driver.find_element(by=By.XPATH, value="//*[@id='MTB0_2']/span[1]")
            #print(f"{moneyTag.text} : {retry} : {(1+(int(in_data['g_setper'])/100))}")


            if moneyTag.text != "--":  # 数値が入っている場合

                if first == True:  # "--"の後に数値になった！
                    money = moneyTag.text.replace(",", "")
                    #ext1 = int(int(money) * (1+(int(in_data["g_setper"])/100)))
                    ext1 = int(int(money) * (1+(5/100)))
                    ext1 = round(ext1, -1)
                    driver.find_element(by=By.NAME, value="input_trigger_price").send_keys(str(ext1))
                    ext2 = int(int(money) * 1.1)
                    ext2 = round(ext2, -1)
                    print(f"{ext1} , {ext2}")
                    driver.find_element(by=By.NAME, value="gsn_input_price").send_keys(str(ext2))
                    driver.find_element(by=By.XPATH, value="//img[@title='注文発注']").click()

                    first = False
                    return 1
                else:
                    return -1   #すでに値が入っている。（注文済み？）

        except Exception as e:
            print(f"An error occurred: {e}")
            break

        #locator = (By.XPATH, "/html/body/div[4]/div/table/tbody/tr/td[1]/div/form[2]/div[4]/div[1]/div[3]/table/tbody/tr[1]/td[1]/p/span[1]")
        #WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))
        #moneyTag = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div/table/tbody/tr/td[1]/div/form[2]/div[4]/div[1]/div[3]/table/tbody/tr[1]/td[1]/p/span[1]")
        #money = int(moneyTag.text.replace(",", ""))

        time.sleep(3)

    return 0


    #time.sleep(5)
    #driver.find_element(by=By.XPATH, value="//img[@title='注文発注']").click()  #注文発注ボタン


