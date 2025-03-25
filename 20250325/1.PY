import requests
from bs4 import BeautifulSoup

def get_arrival_time(station_name):
    # 目標 URL
    url = 'https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'

    # 發送 GET 請求
    response = requests.get(url)

    # 確認請求成功
    if response.status_code == 200:
        # 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到包含車站名稱和到達時間的表格
        table = soup.find('table', {'class': 'table table-striped'})
        
        if table:
            # 遍歷表格的每一行
            rows = table.find_all('tr')
            for row in rows:
                # 找到每一行中的所有單元格
                cells = row.find_all('td')
                if len(cells) > 1:
                    # 提取車站名稱和到達時間
                    current_station_name = cells[0].text.strip()
                    arrival_time = cells[1].text.strip()
                    if current_station_name == station_name:
                        return arrival_time
            return '找不到該車站名稱'
        else:
            return '找不到包含車站名稱和到達時間的表格'
    else:
        return f'無法取得網頁內容，狀態碼: {response.status_code}'

# 輸入車站名稱
station_name = input('請輸入車站名稱: ')
arrival_time = get_arrival_time(station_name)
print(f'車站名稱:
