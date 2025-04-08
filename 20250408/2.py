from datetime import datetime

def calculate_julian_date(input_time_str):
    """
    計算輸入時間的星期幾以及距今的太陽日數。
    
    :param input_time_str: 時間字串，格式為 "YYYY-MM-DD HH:MM"
    :return: 該天是星期幾，與距今的太陽日數
    """
    # 將輸入的時間字串轉換為 datetime 物件
    input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")

    # 計算該天是星期幾
    weekday = input_time.strftime("%A")  # 星期幾 (英文)

    # 計算輸入時間的 Julian Date
    year = input_time.year
    month = input_time.month
    day = input_time.day + input_time.hour / 24 + input_time.minute / 1440

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)
    julian_date = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

    # 計算距今的太陽日數
    now = datetime.now()
    now_year = now.year
    now_month = now.month
    now_day = now.day + now.hour / 24 + now.minute / 1440

    if now_month <= 2:
        now_year -= 1
        now_month += 12

    A_now = now_year // 100
    B_now = 2 - A_now + (A_now // 4)
    now_julian_date = int(365.25 * (now_year + 4716)) + int(30.6001 * (now_month + 1)) + now_day + B_now - 1524.5

    days_since_input = now_julian_date - julian_date

    return weekday, julian_date, days_since_input

# 從終端機讀取輸入
input_time_str = input("請輸入日期 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30): ")

try:
    weekday, julian_date, days_since_input = calculate_julian_date(input_time_str)
    print(f"輸入時間 {input_time_str} 是星期 {weekday}")
    print(f"該時間的太陽日 (Julian Date) 為 {julian_date:.6f}")
except ValueError:
    print("輸入格式錯誤，請確認格式為 YYYY-MM-DD HH:MM")