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

if __name__ == '__main__':
    url = "https://reserve.tokyodisneyresort.jp/sp/hotel/search/"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=options)

    try:
        # トップページを表示
        driver.get(url)

        # 「ホテルから」をクリック
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='ホテルから']"))
        )
        link.click()

        # 「ホテル」をクリック
        link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(., '東京ディズニーランド')]"))
        )
        link.click()

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
        print("\n選択可能な部屋の種類:")
        for idx, room in enumerate(room_types):
            print(f"{idx+1}: {room}")
        room_choice = int(input("選択する部屋の種類の番号を入力してください: "))
        selected_room_type = room_types[room_choice - 1]
        print(f"\n選択された部屋の種類: {selected_room_type}")

        # XPath を動的に組み立てる（クラス属性内に選択した文字列が含まれるもの）
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

        ## 大人の人数を選択（2人）
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

        ## カレンダーのセレクトボックス（#boxCalendarSelect）を取得
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "boxCalendarSelect"))
        )
        select = Select(select_element)
        today = datetime.date.today()
        options_list = []
        for i in range(5):  # 現在の月～+4ヶ月
            new_date = today + datetime.timedelta(days=30 * i)
            year = new_date.year
            month = new_date.month
            option_value = f"{year},{month}"
            option_label = f"{year}/{month:02d}"
            options_list.append((option_value, option_label))
        print("選択可能な月:")
        for idx, (val, label) in enumerate(options_list):
            print(f"{idx+1}: {label}")
        choice = int(input("選択する番号を入力してください: "))
        selected_value = options_list[choice - 1][0]
        print(f"選択された値: {selected_value}")
        select.select_by_value(selected_value)

        # 更新待機
        time.sleep(3)

        # 空室セルを取得
        vacancy_cells = driver.find_elements(By.CSS_SELECTOR, "td.ok[data-date]")
        vacancy_dates = [cell.get_attribute("data-date") for cell in vacancy_cells]
        if len(vacancy_dates) == 0:
            print("空きなし")
        else:
            print("空室がある日:")
            for date in vacancy_dates:
                print(date)

    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        print('exit')
