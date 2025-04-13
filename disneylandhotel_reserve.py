import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

# 事前にユーザーから部屋選択を行う処理

# 部屋の種類リスト
room_types = [
    "スタンダード スーペリアルーム（１－３階）",
    "スタンダード スーペリアルーム（３－４階）",
    "スタンダード スーペリアルーム（４－９階）",
    "スタンダード スーペリアルーム（パークビュー）（３－６階）",
    "スタンダード スーペリアルーム（パークビュー）（７－８階）",
    "スタンダード スーペリアルーム（パークグランドビュー）（５－６階）",
    "スタンダード スーペリアルーム（パークグランドビュー）（７階）",
    "スタンダード スーペリアルーム（パークグランドビュー）（７－８階）",
    "スタンダード スーペリアアルコーヴルーム（１－３階）",
    "スタンダード スーペリアアルコーヴルーム（４－９階）",
    "スタンダード スーペリアアルコーヴルーム（パークビュー）（３－６階）",
    "スタンダード スーペリアアルコーヴルーム（パークビュー）（７－８階）",
    "スタンダード スーペリアアルコーヴルーム（パークグランドビュー）（５－６階）",
    "ディズニー美女と野獣ルーム（３－９階）",
    "ディズニー美女と野獣ルーム（１－２階）",
    "ディズニー美女と野獣ルーム（３－８階）",
    "ディズニー美女と野獣ルーム（５－９階）",
    "ディズニーティンカーベルルーム(５－９階）",
    "ディズニーティンカーベルルーム(３－９階）",
    "ディズニーふしぎの国のアリスルーム（３－９階）",
    "ディズニーふしぎの国のアリスルーム（３－８階）",
    "ディズニーシンデレラルーム（５－７階）",
    "コンシェルジュ・ディズニーシンデレラルーム（８－９階）",
    "スタンダード デラックスルーム（１－３階）",
    "スタンダード デラックスルーム（４－８階）",
    "スタンダード・デラックスルーム（４階）",
    "スタンダード デラックスルーム（３－４階）４名対応",
    "スタンダード デラックスルーム（４－８階）（アクセシブル）",
    "スタンダード・コーナールーム（３階）",
    "スタンダード・コーナールーム（パークビュー）（３－６階）",
    "スタンダード・コーナールーム（パークビュー）（７－８階）",
    "スタンダード ジュニアファミリールーム(１－３階）",
    "スタンダード ジュニアファミリールーム(パークビュー）（４－６階）",
    "スタンダード ジュニアファミリールーム(パークビュー）（７－８階）",
    "スタンダード・ファミリールーム（パークビュー）（５－６階）",
    "スタンダード・ファミリールーム（パークビュー）（７－９階）",
    "コンシェルジュ･スーペリアルーム（パークビュー）（３－６階）　４名対応",
    "コンシェルジュ･スーペリアルーム（パークビュー）（７－８階）　４名対応",
    "コンシェルジュ スーペリアルーム（パークグランドビュー）（８－９階）　４名対応",
    "コンシェルジュ スーペリアルアルコーヴルーム（パークグランドビュー）（７－９階）",
    "コンシェルジュ・バルコニールーム（パークグランドビュー）　（８階）　４名対応",
    "コンシェルジュ・バルコニーアルコーヴルーム（パークグランドビュー）　（８階）",
    "コンシェルジュ・タレットルーム（３－６階）",
    "コンシェルジュ・タレットルーム（４－６階）",
    "コンシェルジュ・タレットルーム（７階）",
    "コンシェルジュ･デラックスルーム（パークビュー）（３－６階）",
    "コンシェルジュ･デラックスルーム（パークビュー）（７－８階）",
    "ディズニー・マジックキングダム・スイート（８階）",
    "ウォルト･ディズニー･スイート（９階）"
]

print("選択可能な部屋の種類:")
for idx, room in enumerate(room_types):
    print(f"{idx+1}: {room}")
room_choice = int(input("選択する部屋の種類の番号を入力してください: "))
selected_room_type = room_types[room_choice - 1]
print(f"\n選択された部屋の種類: {selected_room_type}")

# ユーザーに予約希望日（YYYYMMDD形式）を入力してもらう
# ※この希望日から対象の月を自動算出します。
desired_date = input("予約希望日（例: 20250508）を入力してください: ").strip()
try:
    desired_datetime = datetime.datetime.strptime(desired_date, "%Y%m%d")
except Exception as e:
    print(f"日付形式が正しくありません: {str(e)}")
    sys.exit()

# 希望日から対象の月（例："2025,5"）を算出
selected_value = f"{desired_datetime.year},{desired_datetime.month}"
print(f"算出された対象月: {selected_value}")

# 以下、WebDriverを起動して自動操作を実施する

url = "https://reserve.tokyodisneyresort.jp/sp/hotel/search/"
chrome_options = Options()
# chrome_options.add_argument('--headless')  # ヘッドレスモードを有効にする場合はコメント解除
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

try:
    # トップページを表示
    driver.get(url)
    time.sleep(3)  # ページロード待機

    # 「ホテルから」をクリック
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='ホテルから']"))
    )
    link.click()

    # 「ホテル」をクリック（例として「東京ディズニーランド」を選択）
    link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(., '東京ディズニーランド')]"))
    )
    link.click()

    # XPath を動的に組み立てる（部屋の種類に合わせる）
    room_xpath = (
        f"//button[contains(@class, 'js-callVacancyStatusSearch') and "
        f"contains(@class, '{selected_room_type}')]"
    )
    print("使用する XPath:", room_xpath)
    room_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, room_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", room_button)
    try:
        room_button.click()
    except Exception:
        ActionChains(driver).move_to_element(room_button).click().perform()

    # 大人の人数を選択（例：2名）
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "adultNum"))
    )
    select_element.click()
    option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='adultNum']/option[@value='2']"))
    )
    option.click()

    # 「次へ」ボタンをクリック
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.next.js-conditionHide"))
    )
    next_button.click()

    # カレンダーのセレクトボックス（ID: boxCalendarSelect）から、算出された対象月をセット
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "boxCalendarSelect"))
    )
    select_box = Select(select_element)
    select_box.select_by_value(selected_value)
    time.sleep(3)  # カレンダー更新待機

    # 希望日のセルを取得してクリック（data-date属性が一致し、かつ"ok"クラス付き）
    date_cell_xpath = f"//td[contains(@class, 'ok') and @data-date='{desired_date}']"
    try:
        date_cell = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, date_cell_xpath))
        )
        print(f"{desired_date} は空室があるようです。セルをクリックして詳細画面へ移行します。")
        date_cell.click()
    except Exception as e:
        print(f"{desired_date} のセルが見つからないか、クリックできませんでした: {str(e)}")
        driver.quit()
        sys.exit()
    
    # 詳細画面（予約手続きボタンが含まれる部分）の表示状態を変更
    room_detail_id = f"room_{desired_date}"
    
    driver.execute_script("document.getElementById('priceInformationList').style.display = 'block';")
    room_detail = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, room_detail_id))
    )
    # 「予約手続きに進む」ボタンを取得しクリック（テキストに「予約手続きに進む」を含み、disableクラスがないもの）
    try:
        reserve_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, f"//li[starts-with(@id, 'room_{desired_date}')]" +
                "//p[@class='btnReserve']/button[contains(., '予約手続きに進む') and not(contains(@class, 'disable'))]"
            ))
        )
        print("予約手続きに進むボタンが見つかりました。クリックします。")
        reserve_button.click()
    except Exception as e:
        print(f"予約手続きに進むボタンが見つからない、またはクリックできませんでした: {str(e)}")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    print('exit')
