import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random

# 使用 requests 先抓取所有公車路線及參數
url = "https://ebus.gov.taipei/ebus"
response = requests.get(url)
response.raise_for_status()  # 如果請求失敗，拋出異常

response.encoding = 'utf-8'
html_content = response.text

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有包含 'javascript:go()' 的 <a> 標籤
links = soup.find_all('a', href=re.compile(r"javascript:go\('(.+)'\)"))

extracted_data = []
if links:
    for link in links:
        text_content = link.get_text().strip()  # 連結文字內容
        href_attr = link.get('href')  # href 屬性值

        # 使用正則表達式從 href 屬性中提取 go() 函式的參數
        match = re.search(r"go\('(.+)'\)", href_attr)

        if match:
            param = match.group(1)  # 提取第一個捕獲組的內容 (即參數)
            extracted_data.append({'路線名稱': text_content, 'go_參數': param})

# 初始化 Selenium，設定 headless 模式（加速）
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 開啟 CSV 檔案以儲存結果
with open("bus_data.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["公車名稱", "站牌名稱"])  # 標題列

    total_routes = len(extracted_data)
    for index, item in enumerate(extracted_data):
        bus_name = item["路線名稱"]
        param = item["go_參數"]
        detail_url = f"https://ebus.gov.taipei/EBus/VsSimpleMap?routeid={param}&gb=1"

        try:
            driver.get(detail_url)

            # 等待站牌資料渲染
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#plMapStops div.snz > span"))
            )
            time.sleep(random.uniform(2, 5))  # 隨機延遲 2 到 5 秒

            # 取出所有站牌名稱
            stops = driver.find_elements(By.CSS_SELECTOR, "#plMapStops div.snz > span")
            if stops:
                for stop in stops:
                    stop_name = stop.text.strip()
                    if stop_name:
                        writer.writerow([bus_name, stop_name])
            else:
                print(f"[警告] {bus_name} 找不到站牌資訊。")

            print(f"[{index + 1}/{total_routes}] 已成功處理路線: {bus_name}")

        except Exception as e:
            print(f"[錯誤] 無法處理路線 {bus_name}: {e}")
            with open("error_routes.txt", "a", encoding="utf-8") as error_file:
                error_file.write(f"{bus_name}, {detail_url}\n")
            continue

driver.quit()
print("✅ 資料擷取完成！")